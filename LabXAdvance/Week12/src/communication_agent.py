# agentic-comm-automator/src/communication_agent.py
import os
import json
import datetime
import time # For sleep
from email.utils import parseaddr
from .utils import setup_logging, log_audit_entry, ensure_directory_exists, get_env_variable
from .email_tasks import EmailTasks
from .sms_tasks import SMSTasks
from .template_renderer import TemplateRenderer

logger = setup_logging(__name__)

class CommunicationAgent:
    """
    An agent that orchestrates communication tasks (email, SMS) based on a
    structured configuration file, managing an internal context for dynamic values.
    """
    def __init__(self, config, base_dir):
        self.config = config
        self.audit_log = []
        self.context = {} # Stores dynamic values for templating and task chaining
        self.start_time = datetime.datetime.now()
        self.base_dir = base_dir

        # Initialize communication task handlers
        try:
            sender_email = get_env_variable("SENDER_EMAIL")
            sender_app_password = get_env_variable("SENDER_APP_PASSWORD")
            smtp_server = get_env_variable("SMTP_SERVER")
            smtp_port = int(get_env_variable("SMTP_PORT"))
            imap_server = get_env_variable("IMAP_SERVER")
            
            self.email_tasks = EmailTasks(smtp_server, smtp_port, imap_server, sender_email, sender_app_password)
            self.sms_tasks = SMSTasks(self.email_tasks) # SMS tasks uses EmailTasks for underlying send
            self.template_renderer = TemplateRenderer()
            logger.info("CommunicationAgent initialized with task handlers.")
        except ValueError as e:
            logger.critical(f"Agent initialization failed: Missing environment variables. {e}")
            raise

    def _update_context(self, key, value):
        """Updates a value in the agent's context."""
        self.context[key] = value
        logger.debug(f"Context updated: '{key}' = {value}")

    def _get_context_value(self, key, default=None):
        """Retrieves a value from the agent's context."""
        return self.context.get(key, default)

    def _render_template(self, template_string):
        """Renders a template string using the current agent context."""
        try:
            return self.template_renderer.render(template_string, self.context)
        except Exception as e:
            log_audit_entry(self.audit_log, "ERROR", f"Template rendering failed: {e}", "template_render", {"template": template_string, "context": self.context})
            raise

    def _process_task(self, task):
        """Dispatches a task to the appropriate handler and manages context."""
        task_type = task.get("type")
        task_name = task.get("name", task_type)
        task_params = task.get("parameters", {})
        output_context_key = task.get("output_context_key")

        logger.info(f"Executing task: '{task_name}' (Type: {task_type})")
        log_audit_entry(self.audit_log, "INFO", f"Starting task '{task_name}'", task_type, task)

        try:
            success = False
            task_output_data = None # Data produced by the task to be stored in context

            if task_type == "send_email":
                recipients = {k: [self._render_template(r) for r in v] for k, v in task_params.get('recipients', {}).items()}
                subject = self._render_template(task_params.get("subject_template"))
                body = self._render_template(task_params.get("body_template"))
                
                attachments = []
                for att_path in task_params.get("attachments", []):
                    rendered_path = os.path.join(self.base_dir, self._render_template(att_path))
                    attachments.append(rendered_path)

                is_html = task_params.get("is_html", False)
                success = self.email_tasks.send_email(recipients, subject, body, attachments, is_html)
                if success:
                    task_output_data = {"recipients": recipients, "subject": subject, "attachments": attachments}

            elif task_type == "send_sms":
                phone_numbers = [self._render_template(p) for p in task_params.get("phone_numbers", [])]
                phone_numbers = [p for p in phone_numbers if p.strip() and not p.startswith("${")]
                if not phone_numbers:
                    logger.warning(f"Task '{task_name}': no phone number configured. Skipping SMS (optional).")
                    log_audit_entry(self.audit_log, "WARNING", f"Task '{task_name}' skipped: no phone number configured.", task_type)
                    return
                message = self._render_template(task_params.get("message_template"))
                carrier_name = task_params.get("carrier_name")
                if carrier_name and carrier_name.startswith("${"):
                    carrier_name = None
                success = self.sms_tasks.send_sms(phone_numbers, message, carrier_name)
                if success:
                    task_output_data = {"phone_numbers": phone_numbers, "message": message}

            elif task_type == "process_inbox":
                mailbox = task_params.get("mailbox", "INBOX")
                search_criteria = task_params.get("search_criteria", {})
                rules = task_params.get("rules", [])
                download_attachments_base_dir = os.path.join(self.base_dir, task_params.get("download_attachments_base_dir", "data/incoming_attachments"))
                
                rendered_sender = self._render_template(search_criteria.get("from_sender", "")) if search_criteria.get("from_sender") else None
                rendered_subject_contains = self._render_template(search_criteria.get("subject_contains", "")) if search_criteria.get("subject_contains") else None

                wait_seconds = task_params.get("wait_seconds", 0)
                if wait_seconds:
                    logger.info(f"Waiting {wait_seconds}s for the mail server to deliver messages...")
                    time.sleep(wait_seconds)

                uids = self.email_tasks.search_emails(
                    mailbox=mailbox,
                    criteria=search_criteria.get("status", "UNSEEN"),
                    from_sender=rendered_sender,
                    subject_contains=rendered_subject_contains
                )
                
                processed_emails_summary = []
                if uids:
                    for uid in uids:
                        email_info = self.email_tasks.fetch_email_content(
                            uid=uid,
                            mark_as_read=True, # Always mark as read for processing
                            download_attachments_dir=download_attachments_base_dir
                        )
                        if email_info:
                            processed_emails_summary.append(email_info)
                            # Apply rules to the fetched email
                            for rule in rules:
                                if_conditions = rule.get("if", {})
                                then_actions = rule.get("then", {})

                                condition_met = True
                                if "subject_contains" in if_conditions and \
                                   self._render_template(if_conditions["subject_contains"]) not in email_info['subject']:
                                    condition_met = False
                                if "body_contains" in if_conditions and \
                                   self._render_template(if_conditions["body_contains"]) not in email_info['text_body']:
                                    condition_met = False
                                if "has_attachments" in if_conditions and \
                                   if_conditions["has_attachments"] != email_info['has_attachments']:
                                    condition_met = False
                                
                                # Add more conditions as needed (e.g., from_sender_is, size_greater_than)

                                if condition_met:
                                    logger.info(f"Rule matched for email UID {email_info['uid']}. Applying actions...")
                                    if "send_sms_alert" in then_actions and then_actions["send_sms_alert"]:
                                        alert_msg_template = then_actions.get("alert_message_template", "Urgent email received: {subject} from {sender}")
                                        alert_message = self.template_renderer.render(alert_msg_template, {**self.context, **email_info})
                                        alert_phone_numbers = [self._render_template(p) for p in then_actions.get("alert_phone_numbers", [])]
                                        alert_phone_numbers = [p for p in alert_phone_numbers if p.strip() and not p.startswith("${")]
                                        alert_carrier = then_actions.get("alert_carrier")
                                        if alert_carrier and alert_carrier.startswith("${"):
                                            alert_carrier = None
                                        if alert_phone_numbers:
                                            self.sms_tasks.send_sms(alert_phone_numbers, alert_message, alert_carrier)
                                        else:
                                            logger.warning("SMS alert rule matched but no phone number configured. Skipping SMS.")
                                    
                                    if "reply_with_template" in then_actions:
                                        reply_body_template = then_actions["reply_with_template"]
                                        reply_subject_template = then_actions.get("reply_subject_template", "Re: {subject}")
                                        reply_body = self.template_renderer.render(reply_body_template, {**self.context, **email_info})
                                        reply_subject = self.template_renderer.render(reply_subject_template, {**self.context, **email_info})
                                        self.email_tasks.send_email(
                                            recipients={'to': [parseaddr(email_info['sender'])[1] or email_info['sender']]},
                                            subject=reply_subject,
                                            body=reply_body
                                        )
                                    
                                    # Add more actions (e.g., move_to_folder, delete_email, trigger_external_script)
                                else:
                                    logger.info(f"No rule matched for email UID {email_info['uid']}.")
                        else:
                            logger.error(f"Failed to fetch content for email UID {uid.decode('utf-8')}.")
                    success = True # Even if some emails failed, the task itself ran
                    task_output_data = {"processed_emails": processed_emails_summary}
                else:
                    logger.info("No emails found matching search criteria for inbox processing.")
                    success = True # No emails found is not a failure of the task itself

            else:
                log_audit_entry(self.audit_log, "WARNING", f"Unsupported task type: {task_type}", task_type, task)
                logger.warning(f"Unsupported task type: {task_type}")
                return # Do not log as success/failure for unknown task

            # Store the output data if the task was successful and produced data
            if success and task_output_data is not None and output_context_key:
                self._update_context(output_context_key, task_output_data)
            
            if success:
                log_audit_entry(self.audit_log, "SUCCESS", f"Task '{task_name}' completed successfully.", task_type, task)
            else:
                log_audit_entry(self.audit_log, "ERROR", f"Task '{task_name}' failed.", task_type, task)

        except Exception as e:
            log_audit_entry(self.audit_log, "ERROR", f"An error occurred during task '{task_name}': {e}", task_type, {"error": str(e), "task_details": task})
            logger.error(f"Error during task '{task_name}': {e}", exc_info=True)

    def _generate_audit_report(self, output_dir="reports"):
        """Generates a JSON audit report."""
        ensure_directory_exists(output_dir)
        report_filename = f"audit_report_comm_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = os.path.join(output_dir, report_filename)
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(self.audit_log, f, indent=4, ensure_ascii=False, default=str)
            logger.info(f"Audit report saved to: {report_path}")
            log_audit_entry(self.audit_log, "INFO", f"Audit report generated at {report_path}", "audit_report")
        except Exception as e:
            logger.error(f"Failed to save audit report: {e}")
            log_audit_entry(self.audit_log, "CRITICAL", f"Failed to save audit report: {e}", "audit_report")

    def run(self):
        """Executes all tasks defined in the configuration."""
        logger.info("Starting Communication Agent run...")
        log_audit_entry(self.audit_log, "INFO", "Communication Agent started.", "agent_run")

        # Simulate some data that might come from previous agent runs (e.g., Week 20)
        self._update_context("student_name", os.getenv("STUDENT_NAME", ""))
        self._update_context("student_surname", os.getenv("STUDENT_SURNAME", ""))
        self._update_context("student_id", os.getenv("STUDENT_ID", ""))
        self._update_context("report_name", "DailySalesSummary")
        self._update_context("report_date", datetime.date.today().strftime("%Y-%m-%d"))
        self._update_context("sales_figure", 12345.67)
        self._update_context("total_customers", 500)
        self._update_context("attachment_path_1", "data/reports/sales_report.pdf")
        self._update_context("attachment_path_2", "data/reports/summary_data.xlsx")


        for task in self.config.get("tasks", []):
            self._process_task(task)
        
        end_time = datetime.datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        log_audit_entry(self.audit_log, "INFO", f"Communication Agent finished in {duration:.2f} seconds.", "agent_run_summary")
        logger.info(f"Communication Agent finished. Total time: {duration:.2f} seconds.")
        
        # Save audit report in a dedicated 'reports' subfolder within the base directory
        audit_report_dir = os.path.join(self.base_dir, 'reports')
        self._generate_audit_report(audit_report_dir)


