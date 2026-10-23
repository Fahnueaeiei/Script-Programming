# Week 12 LabX BASIC: Automating Communications (Email & SMS)

Python scripts that send email (plain text + attachment), send SMS through an email-to-SMS gateway,
and receive/process email over IMAP (download attachments, mark as read).

## Setup
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then edit .env
```
Fill `.env` with your Gmail address, a Gmail **App Password** (Google Account -> Security -> 2-Step Verification -> App passwords),
a recipient address, and your `STUDENT_NAME`, `STUDENT_SURNAME`, `STUDENT_ID` (they appear in the email subject/body).
`TEST_SMS_PHONE_NUMBER` / `TEST_SMS_CARRIER` are optional; leave blank to skip Task 3.
Also enable IMAP in Gmail settings (Forwarding and POP/IMAP).

## Run
```bash
python3 main.py
```
Tasks: 1) plain text email, 2) email with `data/dummy_report.pdf`, 3) SMS via gateway (optional),
4) send email to self, then search UNSEEN, print details, download attachments to `data/attachments/`, mark as read.

## Structure
```
src/  utils.py  email_sender.py  email_receiver.py  sms_gateway.py
data/ dummy_report.pdf  attachments/
main.py  requirements.txt  .env.example
```
`.env` is git-ignored: never commit credentials.
