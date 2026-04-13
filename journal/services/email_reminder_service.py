"""
Email Reminder Service
Handles sending email reminders for tasks and entries
"""

import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from journal.models import Reminder, EmailLog, EmailTemplate, PushNotification
from datetime import timedelta

logger = logging.getLogger(__name__)


class EmailReminderService:
    """Service for sending email reminders"""
    
    @staticmethod
    def send_pending_reminders():
        """
        Check for pending reminders and send emails
        Called by scheduled task
        """
        now = timezone.now()
        pending_reminders = Reminder.objects.filter(
            is_active=True,
            is_sent=False,
            reminder_time__lte=now
        ).select_related('entry__user')
        
        sent_count = 0
        for reminder in pending_reminders:
            try:
                EmailReminderService.send_reminder_email(reminder)
                sent_count += 1
            except Exception as e:
                logger.error(f"Failed to send reminder {reminder.id}: {str(e)}")  # type: ignore
        
        return sent_count

    @staticmethod
    def send_reminder_email(reminder: Reminder):
        """Send email for a specific reminder"""
        user = reminder.entry.user
        
        # Get template
        try:
            template = EmailTemplate.objects.get(name="reminder_notification")
        except EmailTemplate.DoesNotExist:
            template = None
        
        subject = f"Reminder: {reminder.entry.title}"
        
        context = {
            'user': user,
            'entry': reminder.entry,
            'reminder': reminder,
            'site_url': settings.MOBILE_APP_CONFIG.get("API_BASE_URL", "http://localhost:8000"),
        }
        
        # Render email body
        if template:
            body = template.template_text.format(**context)
        else:
            body = f"""
            Hi {user.first_name or user.username},
            
            You have a reminder for your entry: {reminder.entry.title}
            
            Task: {reminder.entry.task or 'No task'}
            Due: {reminder.entry.task_due_at.strftime('%Y-%m-%d %H:%M') if reminder.entry.task_due_at else 'Not set'}
            
            Visit your journal to view and update.
            
            Best regards,
            Journal Desk Team
            """
        
        # Send email
        try:
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            
            # Log email
            EmailLog.objects.create(
                user=user,
                recipient=user.email,
                subject=subject,
                template=template,
                related_entry=reminder.entry,
                status='sent',
                sent_at=timezone.now()
            )
            
            # Mark reminder as sent
            reminder.is_sent = True
            reminder.last_sent = timezone.now()
            reminder.save()
            
            logger.info(f"Reminder email sent to {user.email} for entry {reminder.entry.id}")  # type: ignore
            
        except Exception as e:
            logger.error(f"Failed to send reminder email: {str(e)}")
            EmailLog.objects.create(
                user=user,
                recipient=user.email,
                subject=subject,
                template=template,
                related_entry=reminder.entry,
                status='failed',
                error_message=str(e)
            )
            raise

    @staticmethod
    def schedule_reminder(entry, reminder_time, frequency='once'):
        """
        Schedule a reminder for an entry
        """
        reminder, created = Reminder.objects.get_or_create(
            user=entry.user,
            entry=entry,
            reminder_time=reminder_time,
            frequency=frequency
        )
        return reminder, created

    @staticmethod
    def get_upcoming_reminders(user, days_ahead=7):
        """
        Get reminders for the next N days
        """
        now = timezone.now()
        future = now + timedelta(days=days_ahead)
        
        return Reminder.objects.filter(
            user=user,
            is_active=True,
            reminder_time__range=[now, future]
        ).order_by('reminder_time').select_related('entry')

    @staticmethod
    def create_email_template(name, subject, template_text):
        """
        Create or update email template
        """
        template, created = EmailTemplate.objects.get_or_create(
            name=name,
            defaults={'subject': subject, 'template_text': template_text}
        )
        if not created:
            template.subject = subject
            template.template_text = template_text
            template.save()
        return template

    @staticmethod
    def get_email_history(user, days=30):
        """
        Get email history for a user
        """
        since = timezone.now() - timedelta(days=days)
        return EmailLog.objects.filter(
            user=user,
            created_at__gte=since
        ).order_by('-created_at')
