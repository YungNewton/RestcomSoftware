# accounts/utils.py

from emails.utils.email_utils import send_email_with_fallback
from django.conf import settings
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from decouple import config

# Backend base URL (from .env file)
BACKEND_URL = config("BACKEND_URL")

# Time-based signer for secure token generation
signer = TimestampSigner()

# -------------------------------------------------------------
# 🔐 EMAIL VERIFICATION UTILITIES
# -------------------------------------------------------------

# Generate signed token for email verification
def generate_verification_token(user):
    return signer.sign(user.email)

# Validate and unsign the email verification token (24hr expiry)
def verify_token(token):
    try:
        return signer.unsign(token, max_age=60*60*24)  # 24 hours
    except (SignatureExpired, BadSignature):
        return None

# Send verification email with secure tokenized link
def send_verification_email(user):
    token = generate_verification_token(user)
    url = f"{BACKEND_URL}/auth/verify-email/?token={token}"
    subject = "Verify Your Email"
    message = f"Click the link to verify your email:\n{url}"

    send_email_with_fallback(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

# -------------------------------------------------------------
# 🔁 PASSWORD RESET UTILITIES
# -------------------------------------------------------------

# Generate signed token for password reset
def generate_password_reset_token(user):
    return signer.sign(user.email)

# Validate password reset token (1-hour expiry)
def verify_password_reset_token(token):
    try:
        return signer.unsign(token, max_age=60*60)  # 1 hour
    except (SignatureExpired, BadSignature):
        return None

# Send password reset email with secure link
def send_password_reset_email(user):
    token = generate_password_reset_token(user)
    url = f"{BACKEND_URL}/auth/reset-password/?token={token}"
    subject = "Password Reset Request"
    message = f"Click this link to reset your password:\n{url}"

    send_email_with_fallback(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
