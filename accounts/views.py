# accounts/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.hashers import make_password

from .serializers import RegisterSerializer
from .models import User
from .utils import (
    send_verification_email,
    verify_token,
    send_password_reset_email,
    verify_password_reset_token
)

# -------------------------------------------------------------
# 🔐 REGISTER & EMAIL VERIFICATION VIEWS
# -------------------------------------------------------------

class RegisterView(APIView):
    """
    Handles user registration.
    - Saves user with is_active=False
    - Sends verification email
    """
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False  # Prevent login until email is verified
            user.save()

            send_verification_email(user)
            return Response({'detail': 'Verification email sent.'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ResendVerificationView(APIView):
    """
    Re-sends email verification if user exists and is not yet active.
    """
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required.'}, status=400)

        try:
            user = User.objects.get(email=email)
            if user.is_active:
                return Response({'detail': 'Account already verified.'}, status=400)
            
            send_verification_email(user)
            return Response({'detail': 'Verification email re-sent.'})
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=404)

class VerifyEmailView(APIView):
    """
    Verifies user email using the token sent to their inbox.
    """
    def get(self, request):
        token = request.GET.get('token')
        email = verify_token(token)

        if not email:
            return Response({'detail': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            user.is_active = True
            user.save()
            return Response({'detail': 'Email verified successfully.'})
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

# -------------------------------------------------------------
# 🔁 PASSWORD RESET VIEWS
# -------------------------------------------------------------

class RequestPasswordResetView(APIView):
    """
    Accepts an email and sends a password reset link if user exists.
    """
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required.'}, status=400)

        try:
            user = User.objects.get(email=email)
            send_password_reset_email(user)
            return Response({'detail': 'Password reset link sent.'})
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=404)

class ConfirmPasswordResetView(APIView):
    """
    Resets user's password if token is valid.
    """
    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        if not token or not new_password:
            return Response({'error': 'Token and new password are required.'}, status=400)

        email = verify_password_reset_token(token)
        if not email:
            return Response({'error': 'Invalid or expired token.'}, status=400)

        try:
            user = User.objects.get(email=email)
            user.password = make_password(new_password)
            user.save()
            return Response({'detail': 'Password reset successful.'})
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)


# -------------------------------------------------------------
# 🗑️ ACCOUNT DELETION VIEWS
# -------------------------------------------------------------
        
class DeleteAccountView(APIView):
    """
    Allows the currently authenticated user to delete their own account.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        email = user.email
        user.delete()
        return Response({'detail': f'User {email} deleted successfully.'}, status=200)
