from celery import shared_task
from emails.utils.email_utils import send_bulk_emails
from django.core.files.base import ContentFile

@shared_task(bind=True)
def send_bulk_emails_task(self, subject, message_template, recipients, attachment_data=None):
    attachment = None
    if attachment_data:
        attachment = ContentFile(attachment_data["content"])
        attachment.name = attachment_data["name"]
        attachment.content_type = attachment_data["content_type"]

    success, failure = send_bulk_emails(subject, message_template, recipients, attachment)
    return {"success": success, "failure": failure}
