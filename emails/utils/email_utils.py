#emails/utils/email_utils.py

from django.core.mail import EmailMessage, get_connection
from emails.utils.message_formatter import personalize_message
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_email_with_fallback(subject, body, from_email, to_list):
    """
    Attempts to send email using Gmail first. Falls back to Brevo SMTP if Gmail fails.
    """
    # Gmail SMTP (SSL - port 465)
    try:
        connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host='smtp.gmail.com',
            port=465,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_ssl=True
        )
        EmailMessage(subject, body, from_email, to_list, connection=connection).send()
        logger.info("✅ Email sent using Gmail SMTP.")
        return True
    except Exception as gmail_error:
        logger.warning(f"⚠️ Gmail SMTP failed: {gmail_error}. Trying Brevo...")

        # Brevo SMTP (TLS - port 587)
        try:
            connection = get_connection(
                backend='django.core.mail.backends.smtp.EmailBackend',
                host='smtp-relay.brevo.com',
                port=587,
                username=settings.BREVO_HOST_USER,
                password=settings.BREVO_HOST_PASSWORD,
                use_ssl=False
            )
            connection.use_tls = True
            EmailMessage(subject, body, from_email, to_list, connection=connection).send()
            logger.info("✅ Email sent using Brevo SMTP.")
            return True
        except Exception as brevo_error:
            logger.error(f"❌ Both Gmail and Brevo failed: {brevo_error}")
            return False

def send_bulk_emails(subject, message_template, recipients, batch_size=100):
    """
    Sends personalized emails in batches using fallback SMTP for each recipient.
    """
    success = 0
    failure = 0

    for i in range(0, len(recipients), batch_size):
        batch = recipients[i:i+batch_size]
        for recipient in batch:
            try:
                personalized_body = personalize_message(message_template, recipient)
                send_email_with_fallback(
                    subject=subject,
                    body=personalized_body,
                    from_email=recipient.get('from_email') or 'no-reply@example.com',
                    to_list=[recipient['email']]
                )
                success += 1
            except Exception as e:
                failure += 1

    return success, failure