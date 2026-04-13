import logging

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

logger = logging.getLogger(__name__)


def _build_alert_message(entry):
    due_text = timezone.localtime(entry.task_due_at).strftime("%b %d, %Y %H:%M")
    return (
        f"Task reminder for '{entry.title}'\n\n"
        f"Task: {entry.task}\n"
        f"Due: {due_text}\n"
        f"Status: Not completed\n\n"
        "Please open your journal and complete or reschedule this task."
    )


def _send_email_alert(entry):
    if not getattr(settings, "TASK_ALERTS_EMAIL_ENABLED", True):
        return False

    if not entry.user.email:
        return False

    subject = f"Overdue task: {entry.task}"
    message = _build_alert_message(entry)

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@journal.local"),
            recipient_list=[entry.user.email],
            fail_silently=False,
        )
        return True
    except Exception:
        logger.exception("Failed sending email alert for entry_id=%s", entry.pk)
        return False


def _send_whatsapp_alert(entry):
    if not getattr(settings, "TASK_ALERTS_WHATSAPP_ENABLED", False):
        return False

    if (getattr(settings, "WHATSAPP_PROVIDER", "").lower() or "") != "twilio":
        return False

    number = (entry.alert_phone_number or "").strip()
    if not number:
        return False

    account_sid = getattr(settings, "TWILIO_ACCOUNT_SID", "").strip()
    auth_token = getattr(settings, "TWILIO_AUTH_TOKEN", "").strip()
    from_number = getattr(settings, "TWILIO_WHATSAPP_FROM", "").strip()

    if not account_sid or not auth_token or not from_number:
        logger.warning("Twilio WhatsApp settings are incomplete; skipping WhatsApp alert.")
        return False

    try:
        from twilio.rest import Client
    except ImportError:
        logger.warning(
            "twilio package is not installed. Install 'twilio' to send WhatsApp alerts."
        )
        return False

    to_number = number if number.startswith("whatsapp:") else f"whatsapp:{number}"
    twilio_from = (
        from_number if from_number.startswith("whatsapp:") else f"whatsapp:{from_number}"
    )

    message = _build_alert_message(entry)

    try:
        client = Client(account_sid, auth_token)
        client.messages.create(body=message, from_=twilio_from, to=to_number)
        return True
    except Exception:
        logger.exception("Failed sending WhatsApp alert for entry_id=%s", entry.pk)
        return False


def send_overdue_task_alert(entry):
    """Send overdue task alerts and return which channels succeeded."""
    email_sent = _send_email_alert(entry)
    whatsapp_sent = _send_whatsapp_alert(entry)
    return {"email": email_sent, "whatsapp": whatsapp_sent}
