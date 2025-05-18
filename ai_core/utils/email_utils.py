#ai_core/utils/email_utils.py

import random
import logging

logger = logging.getLogger(__name__)

def get_email_prompt_suggestions():
    """
    Returns 6 random static email prompt suggestions.
    """
    PRESET_PROMPTS = [
        "Write a professional promotional email for a new product launch.",
        "Generate a persuasive email to announce a limited-time discount offer.",
        "Create an informative email newsletter highlighting our recent updates.",
        "Write a follow-up email to re-engage inactive subscribers.",
        "Generate an email introducing our brand to potential new customers.",
        "Compose a holiday-themed promotional email for our entire customer base.",
        "Write a thank-you email to all users for their continued support.",
        "Create a reminder email about an upcoming webinar or live event.",
        "Generate a formal announcement about a change in our service or pricing.",
        "Write a reactivation email targeting users who haven’t engaged in a while.",
        "Create an email announcing a seasonal sale or clearance offer.",
        "Write a bulk message informing users about a new feature release.",
        "Generate a bulk email inviting users to follow us on social media.",
        "Compose an email encouraging users to refer others to our platform.",
        "Write a professional outreach email introducing our company to new leads.",
        "Generate a soft-sell email highlighting the value of upgrading to a premium plan.",
        "Compose a feedback request email asking users to share their opinions.",
        "Write a short and friendly email promoting our blog or resource hub.",
        "Create a formal notification email about upcoming maintenance or downtime.",
        "Generate an email announcing a company milestone or achievement."
    ]

    random_prompts = random.sample(PRESET_PROMPTS, 6)
    logger.debug(f"📋 Random prompt suggestions returned: {random_prompts}")
    return random_prompts

