# accounts/urls.py
from django.urls import path
from .views import (
    RegisterView, VerifyEmailView,
    RequestPasswordResetView, ConfirmPasswordResetView,
    ResendVerificationView, LoginView,
)

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verification/', ResendVerificationView.as_view(), name='resend-verification'),
    path('request-password-reset/', RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('reset-password/confirm/', ConfirmPasswordResetView.as_view(), name='confirm-password-reset'),
]
