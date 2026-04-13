import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from journal.alerts import send_overdue_task_alert
from journal.models import Entry

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Send overdue task reminders via configured alert channels."

    def handle(self, *args, **options):
        logger.info("Starting send_task_alerts command")
        
        overdue_entries = Entry.objects.select_related("user").filter(
            task__gt="",
            task_completed=False,
            task_due_at__isnull=False,
            task_due_at__lte=timezone.now(),
            alert_sent_at__isnull=True,
        )

        total = overdue_entries.count()
        if total == 0:
            self.stdout.write(self.style.SUCCESS("No overdue tasks pending alerts."))
            logger.info("No overdue tasks pending alerts")
            return

        email_count = 0
        whatsapp_count = 0
        alerted_count = 0
        failed_count = 0

        for entry in overdue_entries:
            try:
                results = send_overdue_task_alert(entry)

                if results.get("email"):
                    email_count += 1
                if results.get("whatsapp"):
                    whatsapp_count += 1

                if results.get("email") or results.get("whatsapp"):
                    entry.alert_sent_at = timezone.now()
                    entry.save()
                    alerted_count += 1
                else:
                    failed_count += 1
                    logger.warning("No alerts sent for entry %s (user: %s)", entry.pk, entry.user.username)
            except Exception as e:
                failed_count += 1
                logger.error("Failed to send alerts for entry %s: %s", entry.pk, str(e), exc_info=True)

        success_message = (
            "Processed overdue tasks: "
            f"{total} checked, "
            f"{alerted_count} alerted, "
            f"{email_count} email, "
            f"{whatsapp_count} WhatsApp"
        )
        if failed_count > 0:
            success_message += f", {failed_count} failed."
        else:
            success_message += "."
        
        self.stdout.write(self.style.SUCCESS(success_message))
        logger.info(success_message)
