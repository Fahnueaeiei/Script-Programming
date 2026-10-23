# agentic-comm-automator/src/sms_tasks.py
from .utils import setup_logging
from .email_tasks import EmailTasks # Reuse EmailTasks for sending actual email
from .template_renderer import TemplateRenderer

logger = setup_logging(__name__)

class SMSTasks:
    """
    Provides a simplified interface to send SMS via email-to-SMS gateways.
    Relies on EmailTasks for the actual email transmission.
    """
    def __init__(self, email_tasks_instance):
        if not isinstance(email_tasks_instance, EmailTasks):
            raise TypeError("SMSTasks requires an instance of EmailTasks.")
        self.email_tasks = email_tasks_instance
        self.template_renderer = TemplateRenderer()
        
        # Common US carrier email-to-SMS gateways (add more as needed)
        self.carrier_gateways = {
            "att": "@txt.att.net",
            "verizon": "@vtext.com",
            "tmobile": "@tmomail.net",
            "sprint": "@messaging.sprintpcs.com",
            "boost": "@sms.boostmobile.com",
            "cricket": "@mms.cricketwireless.net",
            "us_cellular": "@email.uscc.net",
            # Add international carriers if known
        }
        logger.info("SMSTasks initialized.")

    def send_sms(self, phone_numbers, message, carrier_name=None):
        """
        Sends SMS messages via email-to-SMS gateway for multiple recipients.
        :param phone_numbers: List of recipient phone numbers (e.g., ['1234567890']).
        :param message: The text message content.
        :param carrier_name: Optional, specific carrier (e.g., 'att', 'verizon'). If None, requires phone_number to include gateway.
        :return: True if all messages were attempted (email-wise), False otherwise.
        """
        success_count = 0
        total_attempts = 0

        for phone_number in phone_numbers:
            total_attempts += 1
            sms_gateway_address = None

            if carrier_name and carrier_name.lower() in self.carrier_gateways:
                sms_gateway_address = f"{phone_number}{self.carrier_gateways[carrier_name.lower()]}"
            elif '@' in phone_number and '.' in phone_number: # Assume phone_number is already a full gateway address
                sms_gateway_address = phone_number
            else:
                logger.warning(f"No specific carrier provided for {phone_number} and it's not a gateway address. Cannot send SMS.")
                continue

            if sms_gateway_address:
                subject = "" # SMS emails usually don't show the subject or only a very short one
                logger.info(f"Attempting to send SMS to {phone_number} via gateway: {sms_gateway_address}")
                if self.email_tasks.send_email(
                    recipients={'to': [sms_gateway_address]},
                    subject=subject,
                    body=message
                ):
                    success_count += 1
            else:
                logger.error(f"Could not determine SMS gateway address for {phone_number}.")
        
        if total_attempts > 0:
            logger.info(f"Attempted to send {total_attempts} SMS messages, {success_count} succeeded (email-wise).")
            return success_count == total_attempts
        return False # No attempts made


