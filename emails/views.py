from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status

from emails.utils.file_parser import parse_uploaded_file
from emails.utils.message_formatter import personalize_message
from emails.utils.email_utils import send_bulk_emails
from emails.tasks.tasks import send_bulk_emails_task


from ai_core.services.deepseek_client import generate_ai_response
from ai_core.utils.email_utils import get_email_prompt_suggestions

import logging

logger = logging.getLogger(__name__)

class SendBulkEmailView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')
        subject = request.data.get('subject')
        message_template = request.data.get('message')

        if not file or not subject or not message_template:
            return Response({'error': 'Missing file, subject, or message.'}, status=400)

        try:
            recipients = parse_uploaded_file(file)
            task = send_bulk_emails_task.delay(subject, message_template, recipients)

            return Response({
                'message': 'Email sending task started.',
                'task_id': task.id
            }, status=202)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class GenerateEmailAIView(APIView):
    """
    Generates AI-powered email content from a given prompt using DeepSeek.
    Conversation history is kept temporarily during the request.
    """

    def post(self, request):
        prompt = request.data.get("prompt", "").strip()
        conversation_history = request.data.get("history", [])

        if not prompt:
            logger.warning("❌ Prompt is missing from request.")
            return Response({"error": "Prompt is required."}, status=400)

        try:
            logger.debug(f"📩 Prompt: '{prompt}' | History: {conversation_history}")

            ai_response = generate_ai_response(prompt, conversation_history)

            logger.debug(f"✅ AI response generated: {ai_response}")
            return Response({"response": ai_response}, status=200)

        except Exception as e:
            logger.exception("💥 AI generation failed:")
            return Response({"error": str(e)}, status=500)

class GetEmailPromptsView(APIView):
    """
    Returns a list of 6 random static AI prompt suggestions for email generation.
    """

    def get(self, request):
        try:
            prompts = get_email_prompt_suggestions()
            logger.debug(f"📋 Prompt suggestions returned: {prompts}")
            return Response({"prompts": prompts}, status=200)
        except Exception as e:
            logger.exception("💥 Failed to retrieve email prompt suggestions.")
            return Response({"error": str(e)}, status=500)