#ai_core/services/deepseek_client.py

import requests
import os
import logging
from dotenv import load_dotenv

# Load API key securely
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    "Content-Type": "application/json"
}

logger = logging.getLogger(__name__)

def generate_ai_response(prompt, conversation_history=[]):
    """
    Calls DeepSeek API to generate AI-based responses (email, chat, analytics).
    """
    try:
        messages = [{
            "role": "system",
            "content": (
                "You are a helpful AI assistant. You are called 'Restcom AI' if asked."
            )

        }] + [{"role": msg["role"], "content": msg["content"]} for msg in conversation_history]

        payload = {
            "model": "deepseek-chat",
            "messages": messages + [{"role": "user", "content": prompt}],
            "temperature": 0.85,
            "top_p": 0.9
        }

        logger.debug(f"📨 Sending to DeepSeek — Prompt: '{prompt}' | Messages: {messages}")

        response = requests.post(DEEPSEEK_URL, json=payload, headers=HEADERS)
        if response.status_code != 200:
            logger.warning(f"⚠️ DeepSeek API Error: {response.status_code} — {response.text}")
            return f"DeepSeek API Error: {response.status_code}, {response.text}"

        response_data = response.json()
        logger.debug(f"✅ DeepSeek response: {response_data}")

        return response_data["choices"][0]["message"]["content"].strip() if "choices" in response_data else "No response."

    except Exception as e:
        logger.exception("💥 Exception in generate_ai_response")
        return f"Error: {str(e)}"