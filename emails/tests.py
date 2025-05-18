from django.test import TestCase

# Create your tests here.

import io
import csv
from django.core.files.uploadedfile import SimpleUploadedFile
from emails.utils.file_parser import parse_uploaded_file
from emails.utils.email_utils import send_bulk_emails

# Generate test data
def generate_test_csv(num=200, corrupt_every=20):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['email', 'first_name', 'last_name'])  # headers

    for i in range(num):
        if i % corrupt_every == 0:
            # Introduce a corrupted row
            writer.writerow(['', 'BadUser', ''])  # missing email
        else:
            writer.writerow([f'user{i}@example.com', f'First{i}', f'Last{i}'])

    return output.getvalue().encode()

# Create an in-memory uploaded file
csv_bytes = generate_test_csv()
test_file = SimpleUploadedFile("test_bulk.csv", csv_bytes, content_type="text/csv")

try:
    recipients = parse_uploaded_file(test_file)
    print(f"✅ Parsed {len(recipients)} valid recipients from file.")
except Exception as e:
    print(f"❌ File parsing failed: {str(e)}")
    recipients = []

if recipients:
    print("\n🧪 Sending bulk emails to test recipients...")
    subject = "Test Email - {{first_name}}"
    message_template = "Hello {{full_name}}, this is a test email."
    success, failure = send_bulk_emails(subject, message_template, recipients, batch_size=50)

    print("\n📊 Test Result Summary:")
    print(f"✅ Success: {success}")
    print(f"❌ Failed:  {failure}")
else:
    print("⚠️ No valid recipients to test with.")
