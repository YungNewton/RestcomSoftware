from celery import shared_task
from emails.utils.email_utils import send_bulk_emails

@shared_task(bind=True)
def send_bulk_emails_task(self, subject, message_template, recipients):
    success, failure = send_bulk_emails(subject, message_template, recipients)
    return {"success": success, "failure": failure}
