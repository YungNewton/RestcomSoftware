#emails/utils/message_formatter.py

def personalize_message(template, context):
    message = template
    for key, value in context.items():
        placeholder = f"{{{{{key}}}}}"
        message = message.replace(placeholder, value)
    return message
