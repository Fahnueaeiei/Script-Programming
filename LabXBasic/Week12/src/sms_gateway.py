# email-sms-automator/src/sms_gateway.py
from .utils import setup_logging
from .email_sender import EmailSender

logger = setup_logging(__name__)

class SMSGateway:
    """
    Provides a simplified interface to send SMS via email-to-SMS gateways.
    Relies on EmailSender for the actual email transmission.
    """
    def __init__(self, email_sender_instance):
        if not isinstance(email_sender_instance, EmailSender):
            raise TypeError("SMSGateway requires an instance of EmailSender.")
        self.email_sender = email_sender_instance
        
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
        logger.info("SMSGateway initialized.")

    def send_sms(self, phone_number, message, carrier_name=None):
        """
        Sends an SMS message via email-to-SMS gateway.
        :param phone_number: Recipient phone number (e.g., '1234567890').
        :param message: The text message content.
        :param carrier_name: Optional, specific carrier (e.g., 'att', 'verizon'). If None, tries common ones or assumes phone_number includes gateway.
        :return: True if message sent (email-wise), False otherwise.
        """
        sms_gateway_address = None

        if carrier_name and carrier_name.lower() in self.carrier_gateways:
            sms_gateway_address = f"{phone_number}{self.carrier_gateways[carrier_name.lower()]}"
        elif '@' in phone_number and '.' in phone_number: # Assume phone_number is already a full gateway address
            sms_gateway_address = phone_number
        else:
            logger.warning("No specific carrier provided and phone number is not a gateway address. Cannot send SMS.")
            return False

        if sms_gateway_address:
            subject = "" # SMS emails usually don't show the subject
            logger.info(f"Attempting to send SMS to {phone_number} via gateway: {sms_gateway_address}")
            return self.email_sender.send_email(sms_gateway_address, subject, message)
        else:
            logger.error("Could not determine SMS gateway address.")
            return False


