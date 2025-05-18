from django.urls import path
from .views import (
    SendBulkEmailView, GenerateEmailAIView, 
    GetEmailPromptsView,
)
urlpatterns = [
    path('send-bulk/', SendBulkEmailView.as_view(), name='send-bulk-email'),
    path('generate-ai-email/', GenerateEmailAIView.as_view(), name='generate-ai-email'),
    path('email-prompts/', GetEmailPromptsView.as_view(), name='get-email-prompts'),
]
