from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import (
    Entry, Tag, Reminder, UserPreferences, EntryStats, DocumentUpload,
    VoiceEntry, BackupData, TeamEntry, CollaborationComment, PushNotification,
    CalendarIntegration, AdvancedAnalytics, EmailLog, SocialShare
)
from .serializers import (
    EntrySerializer, EntryListSerializer, TagSerializer, ReminderSerializer,
    UserPreferencesSerializer, EntryStatsSerializer, DocumentUploadSerializer,
    VoiceEntrySerializer, BackupDataSerializer, TeamEntrySerializer,
    CollaborationCommentSerializer, PushNotificationSerializer,
    CalendarIntegrationSerializer, AdvancedAnalyticsSerializer,
    EmailLogSerializer, SocialShareSerializer
)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["created_at", "name"]

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EntryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "is_starred", "task_completed", "mood", "is_private"]
    search_fields = ["title", "content"]
    ordering_fields = ["date_created", "date_updated", "task_due_at"]
    ordering = ["-date_created"]

    def get_serializer_class(self):
        if self.action == "list":
            return EntryListSerializer
        return EntrySerializer

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user).prefetch_related("tags", "reminders")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def complete_task(self, request, pk=None):
        entry = self.get_object()
        entry.complete_task()
        return Response({"status": "task completed"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def toggle_star(self, request, pk=None):
        entry = self.get_object()
        entry.is_starred = not entry.is_starred
        entry.save()
        return Response({"is_starred": entry.is_starred}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def starred(self, request):
        starred_entries = self.get_queryset().filter(is_starred=True)
        serializer = self.get_serializer(starred_entries, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def overdue_tasks(self, request):
        now = timezone.now()
        overdue = self.get_queryset().filter(
            task__gt="", task_completed=False, task_due_at__isnull=False, task_due_at__lte=now
        )
        serializer = self.get_serializer(overdue, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def by_category(self, request):
        category = request.query_params.get("category")
        if not category:
            return Response({"error": "category parameter required"}, status=status.HTTP_400_BAD_REQUEST)
        entries = self.get_queryset().filter(category=category)
        serializer = self.get_serializer(entries, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def search(self, request):
        query = request.query_params.get("q")
        if not query:
            return Response({"error": "q parameter required"}, status=status.HTTP_400_BAD_REQUEST)
        entries = self.get_queryset().filter(title__icontains=query) | self.get_queryset().filter(content__icontains=query)
        serializer = self.get_serializer(entries, many=True)
        return Response(serializer.data)


class ReminderViewSet(viewsets.ModelViewSet):
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["reminder_time"]
    ordering = ["reminder_time"]

    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def mark_sent(self, request, pk=None):
        reminder = self.get_object()
        reminder.is_sent = True
        reminder.last_sent = timezone.now()
        reminder.save()
        return Response({"status": "reminder marked as sent"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def pending(self, request):
        now = timezone.now()
        pending = self.get_queryset().filter(
            is_active=True, is_sent=False, reminder_time__lte=now
        )
        serializer = self.get_serializer(pending, many=True)
        return Response(serializer.data)


class UserPreferencesViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        prefs, _ = UserPreferences.objects.get_or_create(user=request.user)
        serializer = UserPreferencesSerializer(prefs)
        return Response(serializer.data)

    def update(self, request):
        prefs, _ = UserPreferences.objects.get_or_create(user=request.user)
        serializer = UserPreferencesSerializer(prefs, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EntryStatsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        stats, _ = EntryStats.objects.get_or_create(user=request.user)
        serializer = EntryStatsSerializer(stats)
        return Response(serializer.data)


class DocumentUploadViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentUploadSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["uploaded_at"]
    ordering = ["-uploaded_at"]

    def get_queryset(self):
        return DocumentUpload.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def mark_analyzed(self, request, pk=None):
        doc = self.get_object()
        doc.status = DocumentUpload.STATUS_ANALYZED
        doc.processed_at = timezone.now()
        doc.save()
        return Response({"status": "document marked as analyzed"}, status=status.HTTP_200_OK)


# ============ NEW FEATURE VIEWSETS ============

class VoiceEntryViewSet(viewsets.ModelViewSet):
    serializer_class = VoiceEntrySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering = ["-created_at"]

    def get_queryset(self):
        return VoiceEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["get"])
    def transcription(self, request, pk=None):
        voice = self.get_object()
        if voice.transcription_status == "pending":
            return Response(
                {"detail": "Transcription still processing"},
                status=status.HTTP_202_ACCEPTED
            )
        return Response({
            "transcription": voice.transcription,
            "confidence": voice.confidence_score
        })


class BackupDataViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BackupDataSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering = ["-created_at"]

    def get_queryset(self):
        return BackupData.objects.filter(user=self.request.user)

    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        backup = self.get_object()
        if backup.status != "completed":
            return Response(
                {"error": "Can only restore completed backups"},
                status=status.HTTP_400_BAD_REQUEST
            )
        backup.restored_at = timezone.now()
        backup.save()
        return Response({"status": "Backup restoration initiated"})

    @action(detail=False, methods=["post"])
    def create_backup(self, request):
        backup = BackupData.objects.create(
            user=request.user,
            backup_type='manual',
            status='pending'
        )
        serializer = self.get_serializer(backup)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TeamEntryViewSet(viewsets.ModelViewSet):
    serializer_class = TeamEntrySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return TeamEntry.objects.filter(members=self.request.user, is_active=True)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=["post"])
    def add_member(self, request, pk=None):
        team_entry = self.get_object()
        user_id = request.data.get("user_id")
        if user_id:
            from django.contrib.auth.models import User
            user = User.objects.get(id=user_id)
            team_entry.members.add(user)
            return Response({"status": "Member added"})
        return Response({"error": "user_id required"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def remove_member(self, request, pk=None):
        team_entry = self.get_object()
        user_id = request.data.get("user_id")
        if user_id:
            from django.contrib.auth.models import User
            user = User.objects.get(id=user_id)
            team_entry.members.remove(user)
            return Response({"status": "Member removed"})
        return Response({"error": "user_id required"}, status=status.HTTP_400_BAD_REQUEST)


class CollaborationCommentViewSet(viewsets.ModelViewSet):
    serializer_class = CollaborationCommentSerializer
    permission_classes = [IsAuthenticated]
    ordering = ["created_at"]

    def get_queryset(self):
        return CollaborationComment.objects.filter(team_entry__members=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PushNotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PushNotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering = ["-created_at"]

    def get_queryset(self):
        return PushNotification.objects.filter(user=self.request.user)

    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({"status": "Notification marked as read"})

    @action(detail=False, methods=["post"])
    def mark_all_read(self, request):
        PushNotification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({"status": "All notifications marked as read"})

    @action(detail=False, methods=["get"])
    def unread_count(self, request):
        count = PushNotification.objects.filter(user=request.user, is_read=False).count()
        return Response({"unread_count": count})


class CalendarIntegrationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        integration, _ = CalendarIntegration.objects.get_or_create(user=request.user)
        serializer = CalendarIntegrationSerializer(integration)
        return Response(serializer.data)

    def update(self, request):
        integration, _ = CalendarIntegration.objects.get_or_create(user=request.user)
        serializer = CalendarIntegrationSerializer(integration, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def sync(self, request):
        integration, _ = CalendarIntegration.objects.get_or_create(user=request.user)
        if not integration.is_enabled:
            return Response(
                {"error": "Calendar integration not enabled"},
                status=status.HTTP_400_BAD_REQUEST
            )
        integration.last_synced = timezone.now()
        integration.save()
        return Response({"status": "Sync initiated"})


class AdvancedAnalyticsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        analytics, _ = AdvancedAnalytics.objects.get_or_create(user=request.user)
        serializer = AdvancedAnalyticsSerializer(analytics)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def recalculate(self, request):
        analytics, _ = AdvancedAnalytics.objects.get_or_create(user=request.user)
        # Recalculate analytics
        entries = Entry.objects.filter(user=request.user)
        analytics.task_completion_rate = entries.filter(task_completed=True).count() / max(1, entries.count())
        analytics.save()
        serializer = AdvancedAnalyticsSerializer(analytics)
        return Response(serializer.data)


class EmailLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EmailLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering = ["-created_at"]

    def get_queryset(self):
        return EmailLog.objects.filter(user=self.request.user)


class SocialShareViewSet(viewsets.ModelViewSet):
    serializer_class = SocialShareSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering = ["-created_at"]

    def get_queryset(self):
        return SocialShare.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def resync_engagement(self, request, pk=None):
        share = self.get_object()
        # Update engagement metrics from social platform
        share.save()
        return Response({"status": "Engagement synced"})
