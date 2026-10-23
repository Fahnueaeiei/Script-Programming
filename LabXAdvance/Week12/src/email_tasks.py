# agentic-comm-automator/src/email_tasks.py
import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import decode_header
import os
from .utils import setup_logging, ensure_directory_exists
from .template_renderer import TemplateRenderer

logger = setup_logging(__name__)

class EmailTasks:
    """
    Handles sending and receiving emails via SMTP and IMAP protocols.
    """
    def __init__(self, smtp_server, smtp_port, imap_server, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.imap_server = imap_server
        self.sender_email = sender_email
        self.sender_password = sender_password
        self._smtp_server = None # Internal SMTP server object
        self._imap_mail = None # Internal IMAP mail object
        self.template_renderer = TemplateRenderer()
        logger.info(f"EmailTasks initialized for {sender_email}.")

    # --- SMTP (Sending) Methods ---
    def _connect_smtp(self):
        """Establishes and logs into the SMTP server."""
        if self._smtp_server: # Already connected
            return True
        try:
            self._smtp_server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self._smtp_server.starttls()  # Secure the connection
            self._smtp_server.login(self.sender_email, self.sender_password)
            logger.info("Successfully connected and logged into SMTP server.")
            return True
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP authentication failed. Check email and app password. Error: {e}")
            self._smtp_server = None
            return False
        except smtplib.SMTPConnectError as e:
            logger.error(f"SMTP connection failed. Check server address and port. Error: {e}")
            self._smtp_server = None
            return False
        except Exception as e:
            logger.error(f"An unexpected error occurred during SMTP connect/login: {e}")
            self._smtp_server = None
            return False

    def _disconnect_smtp(self):
        """Disconnects from the SMTP server."""
        if self._smtp_server:
            try:
                self._smtp_server.quit()
                logger.info("Disconnected from SMTP server.")
            except Exception as e:
                logger.warning(f"Error during SMTP disconnection: {e}")
            finally:
                self._smtp_server = None

    def send_email(self, recipients, subject, body, attachments=None, is_html=False):
        """
        Sends an email with dynamic content and multiple attachments.
        :param recipients: Dictionary with lists for 'to', 'cc', 'bcc'.
        :param subject: The subject line of the email.
        :param body: The content of the email.
        :param attachments: List of file paths to attach.
        :param is_html: Set to True if the body is HTML, False for plain text.
        :return: True if email sent successfully, False otherwise.
        """
        if not self._connect_smtp():
            return False

        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['Subject'] = subject

        to_recipients = recipients.get('to', [])
        cc_recipients = recipients.get('cc', [])
        bcc_recipients = recipients.get('bcc', []) # BCC is handled separately, not in header

        msg['To'] = ", ".join(to_recipients)
        if cc_recipients:
            msg['Cc'] = ", ".join(cc_recipients)

        msg.attach(MIMEText(body, 'html' if is_html else 'plain'))

        # Attach files
        if attachments:
            for attachment_path in attachments:
                if not os.path.exists(attachment_path):
                    logger.warning(f"Attachment file not found: {attachment_path}. Skipping.")
                    continue
                try:
                    with open(attachment_path, "rb") as f:
                        part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
                    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
                    msg.attach(part)
                    logger.info(f"Attached file: {attachment_path}")
                except Exception as e:
                    logger.error(f"Error attaching file {attachment_path}: {e}")

        all_recipients = to_recipients + cc_recipients + bcc_recipients
        if not all_recipients:
            logger.error("No recipients specified for email.")
            self._disconnect_smtp()
            return False

        try:
            self._smtp_server.send_message(msg, from_addr=self.sender_email, to_addrs=all_recipients)
            logger.info(f"Email sent successfully to {', '.join(to_recipients)} (CC: {', '.join(cc_recipients)}). Subject: '{subject}'.")
            return True
        except Exception as e:
            logger.error(f"Failed to send email. Error: {e}")
            return False
        finally:
            self._disconnect_smtp()

    # --- IMAP (Receiving) Methods ---
    def _connect_imap(self):
        """Establishes and logs into the IMAP server."""
        if self._imap_mail: # Already connected
            return True
        try:
            self._imap_mail = imaplib.IMAP4_SSL(self.imap_server)
            self._imap_mail.login(self.sender_email, self.sender_password)
            logger.info("Successfully connected and logged into IMAP server.")
            return True
        except imaplib.IMAP4.error as e:
            logger.error(f"IMAP authentication failed. Check email and app password. Error: {e}")
            self._imap_mail = None
            return False
        except Exception as e:
            logger.error(f"An unexpected error occurred during IMAP connect/login: {e}")
            self._imap_mail = None
            return False

    def _disconnect_imap(self):
        """Disconnects from the IMAP server."""
        if self._imap_mail:
            try:
                self._imap_mail.logout()
                logger.info("Disconnected from IMAP server.")
            except Exception as e:
                logger.warning(f"Error during IMAP disconnection: {e}")
            finally:
                self._imap_mail = None

    def search_emails(self, mailbox='INBOX', criteria='UNSEEN', from_sender=None, subject_contains=None):
        """
        Searches for emails based on criteria.
        :param mailbox: Mailbox to search (e.g., 'INBOX').
        :param criteria: IMAP search criteria (e.g., 'UNSEEN', 'ALL', 'SEEN').
        :param from_sender: Filter by sender email address.
        :param subject_contains: Filter by subject line containing this string.
        :return: A list of email UIDs (unique identifiers).
        """
        if not self._connect_imap():
            return []
        
        try:
            self._imap_mail.select(mailbox)
            search_query = [criteria]
            if from_sender:
                search_query.extend(['FROM', f'"{from_sender}"'])
            if subject_contains:
                search_query.extend(['SUBJECT', f'"{subject_contains}"'])

            status, email_ids = self._imap_mail.search(None, *search_query)
            if status != 'OK':
                logger.error(f"IMAP search failed. Status: {status}")
                return []
            
            uids = email_ids[0].split()
            logger.info(f"Found {len(uids)} emails matching criteria in '{mailbox}'.")
            return uids
        except Exception as e:
            logger.error(f"Error searching emails: {e}")
            return []
        finally:
            self._disconnect_imap()

    def fetch_email_content(self, uid, mark_as_read=True, download_attachments_dir=None):
        """
        Fetches the content of a specific email by UID.
        Optionally marks as read and downloads attachments.
        :param uid: The unique ID of the email (bytes).
        :param mark_as_read: If True, marks the email as SEEN.
        :param download_attachments_dir: Directory to save attachments, or None to skip.
        :return: A dictionary containing email details or None.
        """
        if not self._connect_imap():
            return None
        
        try:
            self._imap_mail.select('INBOX')
            
            status, msg_data = self._imap_mail.fetch(uid, '(RFC822)')
            if status != 'OK':
                logger.error(f"Failed to fetch email UID {uid}. Status: {status}")
                return None
            
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            sender = self._decode_header_part(msg['From'])
            subject = self._decode_header_part(msg['Subject'])
            
            email_text_body = ""
            email_html_body = ""
            attachments_meta = [] # List of dicts: {'filename': 'name', 'filepath': 'path'}
            
            # Flag to check if email has attachments
            has_attachments = msg.get_content_maintype() == 'multipart' and any(part.get_filename() for part in msg.walk())


            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                filename = part.get_filename()

                if "attachment" in content_disposition or (filename and part.get_content_maintype() != 'multipart'):
                    if filename and download_attachments_dir:
                        ensure_directory_exists(download_attachments_dir)
                        filepath = os.path.join(download_attachments_dir, filename)
                        try:
                            with open(filepath, "wb") as f:
                                f.write(part.get_payload(decode=True))
                            attachments_meta.append({'filename': filename, 'filepath': filepath})
                            logger.info(f"Downloaded attachment: {filepath}")
                        except Exception as e:
                            logger.error(f"Error downloading attachment {filename}: {e}")
                    elif filename: # If not downloading, just log its presence
                        attachments_meta.append({'filename': filename, 'filepath': None})
                        logger.debug(f"Found attachment: {filename} (not downloaded)")
                elif "text/plain" in content_type and not "attachment" in content_disposition:
                    try:
                        email_text_body += part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='replace')
                    except Exception as e:
                        logger.warning(f"Could not decode plain text part from email UID {uid}. Error: {e}")
                elif "text/html" in content_type and not "attachment" in content_disposition:
                    try:
                        email_html_body += part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='replace')
                    except Exception as e:
                        logger.warning(f"Could not decode HTML text part from email UID {uid}. Error: {e}")

            if mark_as_read:
                self._imap_mail.store(uid, '+FLAGS', '\\Seen')
                logger.info(f"Marked email UID {uid.decode('utf-8')} as read.")

            return {
                "uid": uid.decode('utf-8'),
                "sender": sender,
                "subject": subject,
                "text_body": email_text_body,
                "html_body": email_html_body,
                "has_attachments": bool(attachments_meta),
                "attachments_meta": attachments_meta
            }
        except Exception as e:
            logger.error(f"Error fetching/parsing email UID {uid.decode('utf-8')}: {e}")
            return None
        finally:
            self._disconnect_imap()

    def _decode_header_part(self, header_value):
        """Decodes header parts that might be encoded (e.g., '=?UTF-8?B?U3ViamVjdA==?=')."""
        if header_value is None:
            return ""
        decoded_parts = decode_header(header_value)
        decoded_string = ""
        for part, charset in decoded_parts:
            if isinstance(part, bytes):
                try:
                    decoded_string += part.decode(charset if charset else 'utf-8')
                except:
                    decoded_string += part.decode('latin-1', errors='replace') # Fallback for decoding
            else:
                decoded_string += part
        return decoded_string.strip()


