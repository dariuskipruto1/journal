"""
Push Notification Service
Handles push notifications for users across web and mobile
"""

import logging
from django.utils import timezone
from django.conf import settings
from journal.models import PushNotification, Entry
import requests

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for sending push notifications"""
    
    @staticmethod
    def notify_reminder(user, entry: Entry):
        """Create notification for entry reminder"""
        notification = PushNotification.objects.create(
            user=user,
            title=f"Reminder: {entry.title}",
            message=entry.task or entry.content[:100],
            notification_type='reminder',
            related_entry=entry
        )
        
        # Try to send via Firebase Cloud Messaging
        NotificationService._send_fcm(notification)
        
        return notification

    @staticmethod
    def notify_shared_entry(user, entry: Entry, shared_by_user):
        """Notification when someone shares an entry"""
        notification = PushNotification.objects.create(
            user=user,
            title=f"{shared_by_user.first_name or shared_by_user.username} shared an entry",
            message=entry.title,
            notification_type='share',
            related_entry=entry
        )
        
        NotificationService._send_fcm(notification)
        return notification

    @staticmethod
    def notify_collaboration(user, team_entry, message: str = ""):
        """Notification for collaboration updates"""
        notification = PushNotification.objects.create(
            user=user,
            title=f"New in: {team_entry.title}",
            message=message or "Someone commented on a collaborative entry",
            notification_type='comment'
        )
        
        NotificationService._send_fcm(notification)
        return notification

    @staticmethod
    def notify_mention(user, team_entry, mentioned_by, message: str = ""):
        """Notification when user is mentioned"""
        notification = PushNotification.objects.create(
            user=user,
            title=f"{mentioned_by.first_name or mentioned_by.username} mentioned you",
            message=message or f"in '{team_entry.title}'",
            notification_type='mention'
        )
        
        NotificationService._send_fcm(notification)
        return notification

    @staticmethod
    def notify_system(user, title: str, message: str):
        """Send system notification"""
        notification = PushNotification.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type='system'
        )
        
        NotificationService._send_fcm(notification)
        return notification

    @staticmethod
    def _send_fcm(notification: PushNotification):
        """
        Send via Firebase Cloud Messaging
        """
        fcm_api_key = settings.PUSH_NOTIFICATIONS_SETTINGS.get("FCM_API_KEY")
        if not fcm_api_key:
            logger.warning("FCM API key not configured")
            return False
        
        # TODO: Implement FCM token management and sending logic
        # This would require storing FCM tokens for each user device
        notification.is_sent = True
        notification.sent_at = timezone.now()
        notification.save()
        
        return True

    @staticmethod
    def _send_apns(notification: PushNotification):
        """
        Send via Apple Push Notification Service
        """
        apns_cert = settings.PUSH_NOTIFICATIONS_SETTINGS.get("APNS_CERTIFICATE")
        if not apns_cert:
            logger.warning("APNS certificate not configured")
            return False
        
        # TODO: Implement APNS sending logic
        notification.is_sent = True
        notification.sent_at = timezone.now()
        notification.save()
        
        return True

    @staticmethod
    def get_unread_notifications(user, limit=20):
        """Get unread notifications for user"""
        return PushNotification.objects.filter(
            user=user,
            is_read=False
        ).order_by('-created_at')[:limit]

    @staticmethod
    def mark_as_read(notification: PushNotification):
        """Mark notification as read"""
        notification.is_read = True
        notification.save()

    @staticmethod
    def mark_all_as_read(user):
        """Mark all notifications as read for user"""
        PushNotification.objects.filter(
            user=user,
            is_read=False
        ).update(is_read=True)
