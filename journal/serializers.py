from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Entry, Tag, Reminder, DocumentUpload, UserPreferences, EntryStats, EntryShare,
    VoiceEntry, BackupData, TeamEntry, CollaborationComment, PushNotification,
    CalendarIntegration, AdvancedAnalytics, EmailTemplate, EmailLog, SocialShare
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "color", "created_at")


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ("id", "entry", "reminder_time", "frequency", "is_active", "is_sent", "last_sent", "created_at")


class DocumentUploadSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = DocumentUpload
        fields = ("id", "title", "file", "file_url", "file_type", "status", "analysis", "uploaded_at", "processed_at")

    def get_file_url(self, obj):
        request = self.context.get("request")
        if obj.file:
            return request.build_absolute_uri(obj.file.url) if request else obj.file.url
        return None


class EntrySerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), write_only=True, many=True, required=False
    )
    reminders = ReminderSerializer(many=True, read_only=True)
    days_old = serializers.ReadOnlyField()
    has_task = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    task_priority_label = serializers.ReadOnlyField()

    class Meta:
        model = Entry
        fields = (
            "id", "title", "content", "category", "tags", "tag_ids", "is_starred",
            "task", "task_priority", "task_priority_label", "task_due_at", "task_completed",
            "task_completed_at", "alert_phone_number", "mood", "location", "is_private",
            "featured", "view_count", "days_old", "has_task", "is_overdue", "reminders",
            "date_created", "date_updated"
        )
        read_only_fields = ("id", "date_created", "date_updated", "task_completed_at", "view_count")

    def create(self, validated_data):
        tag_ids = validated_data.pop("tag_ids", [])
        entry = Entry.objects.create(**validated_data)
        if tag_ids:
            entry.tags.set(tag_ids)
        return entry

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop("tag_ids", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tag_ids is not None:
            instance.tags.set(tag_ids)
        return instance


class EntryListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    tags = TagSerializer(many=True, read_only=True)
    task_priority_label = serializers.ReadOnlyField()

    class Meta:
        model = Entry
        fields = (
            "id", "title", "category", "tags", "is_starred", "task", "task_priority",
            "task_priority_label", "task_due_at", "task_completed", "mood", "is_private",
            "featured", "days_old", "date_created"
        )


class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = (
            "theme", "notifications_enabled", "email_notifications", "sms_notifications",
            "language", "items_per_page", "show_analytics", "auto_save_draft"
        )


class EntryStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryStats
        fields = (
            "total_entries", "total_words", "completed_tasks", "current_streak",
            "longest_streak", "last_entry_date", "favorite_category", "favorite_mood"
        )


class EntryShareSerializer(serializers.ModelSerializer):
    entry = EntryListSerializer(read_only=True)
    shared_by = UserSerializer(read_only=True)
    shared_with = UserSerializer(read_only=True)

    class Meta:
        model = EntryShare
        fields = ("id", "entry", "shared_by", "shared_with", "share_type", "can_edit", "created_at", "expires_at")


# ============ NEW FEATURE SERIALIZERS ============

class VoiceEntrySerializer(serializers.ModelSerializer):
    audio_url = serializers.SerializerMethodField()
    duration_formatted = serializers.SerializerMethodField()

    class Meta:
        model = VoiceEntry
        fields = (
            "id", "entry", "audio_file", "audio_url", "duration", "duration_formatted",
            "transcription", "transcription_status", "confidence_score", "language",
            "created_at", "processed_at"
        )
        read_only_fields = ("id", "transcription", "confidence_score", "created_at", "processed_at")

    def get_audio_url(self, obj):
        request = self.context.get("request")
        if obj.audio_file:
            return request.build_absolute_uri(obj.audio_file.url) if request else obj.audio_file.url
        return None

    def get_duration_formatted(self, obj):
        minutes = obj.duration // 60
        seconds = obj.duration % 60
        return f"{minutes}:{seconds:02d}"


class BackupDataSerializer(serializers.ModelSerializer):
    size_formatted = serializers.SerializerMethodField()

    class Meta:
        model = BackupData
        fields = (
            "id", "backup_type", "backup_provider", "backup_location", "entries_count",
            "file_size", "size_formatted", "status", "created_at", "completed_at",
            "restored_at", "error_message"
        )
        read_only_fields = ("id", "created_at", "completed_at", "restored_at")

    def get_size_formatted(self, obj):
        size = obj.file_size
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"


class CollaborationCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CollaborationComment
        fields = ("id", "team_entry", "user", "content", "created_at", "updated_at")
        read_only_fields = ("id", "user", "created_at", "updated_at")


class TeamEntrySerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    members = UserSerializer(read_only=True, many=True)
    comments = CollaborationCommentSerializer(read_only=True, many=True)
    member_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, many=True, required=False
    )

    class Meta:
        model = TeamEntry
        fields = (
            "id", "creator", "title", "content", "members", "member_ids", "comments",
            "is_active", "created_at", "updated_at"
        )
        read_only_fields = ("id", "creator", "created_at", "updated_at")

    def create(self, validated_data):
        member_ids = validated_data.pop("member_ids", [])
        team_entry = TeamEntry.objects.create(**validated_data)
        if member_ids:
            team_entry.members.add(validated_data.get("creator"), *member_ids)
        else:
            team_entry.members.add(validated_data.get("creator"))
        return team_entry


class PushNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushNotification
        fields = (
            "id", "title", "message", "notification_type", "related_entry",
            "is_read", "is_sent", "sent_at", "created_at"
        )
        read_only_fields = ("id", "is_sent", "sent_at", "created_at")


class CalendarIntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarIntegration
        fields = (
            "id", "provider", "is_enabled", "sync_direction", "calendar_id",
            "last_synced", "created_at", "updated_at"
        )
        read_only_fields = ("id", "access_token", "refresh_token", "last_synced", "created_at", "updated_at")

    def validate_access_token(self, value):
        if not value and self.instance and self.instance.is_enabled:
            raise serializers.ValidationError("Access token is required to enable calendar integration")
        return value


class AdvancedAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvancedAnalytics
        fields = (
            "mood_trend", "top_mood", "average_words_per_entry", "peak_writing_hour",
            "peak_writing_day", "task_completion_rate", "avg_days_to_complete",
            "top_category", "category_breakdown", "daily_entry_count", "weekly_stats",
            "ai_insights", "recommendations", "last_calculated"
        )
        read_only_fields = ("id", "last_calculated")


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = ("id", "name", "subject", "template_text", "is_active", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class EmailLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailLog
        fields = (
            "id", "recipient", "subject", "template", "related_entry", "status",
            "sent_at", "error_message", "created_at"
        )
        read_only_fields = ("id", "sent_at", "created_at")


class SocialShareSerializer(serializers.ModelSerializer):
    entry = EntryListSerializer(read_only=True)

    class Meta:
        model = SocialShare
        fields = (
            "id", "entry", "platform", "shared_url", "status", "engagement_count", "created_at"
        )
        read_only_fields = ("id", "shared_url", "status", "engagement_count", "created_at")
