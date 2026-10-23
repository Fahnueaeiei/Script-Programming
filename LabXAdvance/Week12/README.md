# Week 12 LabX ADV: Agentic Communication Workflows (Email & SMS)

A configuration-driven `CommunicationAgent` that runs the tasks listed in `configs/comm_pipeline_config.json`:
`send_email` (templates + attachments + CC), `send_sms` (email-to-SMS gateway), `process_inbox` (IMAP search, download
attachments, rule-based SMS alerts / auto-replies). A shared context (`report_date`, `sales_figure`, student info, ...) feeds the
`{placeholders}`; `${ENV_VAR}` values are filled from `.env`. Every run writes a JSON audit report to `reports/`.

## Setup
```bash
python3 -m venv venv && source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env     # fill in Gmail, App Password, recipient, STUDENT_NAME / STUDENT_SURNAME / STUDENT_ID
python3 main.py
```
Gmail needs 2-Step Verification + an App Password, and IMAP enabled. SMS vars may stay blank (SMS tasks are then skipped).

## Structure
```
src/ communication_agent.py email_tasks.py sms_tasks.py config_parser.py template_renderer.py utils.py
configs/comm_pipeline_config.json
data/ reports/(sales_report.pdf, summary_data.xlsx)  attachments/  incoming_attachments/
main.py  requirements.txt  .env.example
```
