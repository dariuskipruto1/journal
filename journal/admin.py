from django.contrib import admin
from .models import (
    Entry, Tag, Reminder, DocumentUpload, UserPreferences, EntryStats, EntryShare,
    VoiceEntry, BackupData, TeamEntry, CollaborationComment, PushNotification,
    CalendarIntegration, AdvancedAnalytics, EmailTemplate, EmailLog, SocialShare
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("name",)
    ordering = ("-created_at",)


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "mood", "task_completed", "is_starred", "date_created")
    list_filter = ("date_created", "task_completed", "is_starred", "category", "mood")
    search_fields = ("title", "content")
    filter_horizontal = ("tags",)
    readonly_fields = ("date_created", "date_updated", "task_completed_at")
    fieldsets = (
        ("Entry Info", {"fields": ("user", "title", "content", "category", "tags")}),
        ("Mood & Location", {"fields": ("mood", "location")}),
        ("Task", {
            "fields": ("task", "task_priority", "task_due_at", "task_completed", "task_completed_at"),
            "classes": ("collapse",),
        }),
        ("Notifications", {
            "fields": ("alert_phone_number", "alert_sent_at"),
            "classes": ("collapse",),
        }),
        ("Status", {
            "fields": ("is_starred", "is_private", "featured", "view_count"),
        }),
        ("Timestamps", {
            "fields": ("date_created", "date_updated"),
            "classes": ("collapse",),
        }),
    )
    ordering = ("-date_created",)


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ("entry", "user", "reminder_time", "frequency", "is_active", "is_sent")
    list_filter = ("frequency", "is_active", "is_sent", "created_at")
    search_fields = ("entry__title", "user__username")
    ordering = ("reminder_time",)


@admin.register(DocumentUpload)
class DocumentUploadAdmin(admin.ModelAdmin):
    list_display = ("file_name", "user", "file_type", "status", "uploaded_at")
    list_filter = ("status", "file_type", "uploaded_at")
    search_fields = ("title", "file")
    readonly_fields = ("file_type", "uploaded_at", "processed_at")
    ordering = ("-uploaded_at",)


@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ("user", "theme", "notifications_enabled", "email_notifications", "updated_at")
    list_filter = ("theme", "notifications_enabled", "updated_at")
    search_fields = ("user__username",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(EntryStats)
class EntryStatsAdmin(admin.ModelAdmin):
    list_display = ("user", "total_entries", "completed_tasks", "current_streak", "longest_streak")
    list_filter = ("updated_at",)
    search_fields = ("user__username",)
    readonly_fields = ("updated_at",)


@admin.register(EntryShare)
class EntryShareAdmin(admin.ModelAdmin):
    list_display = ("entry", "shared_by", "shared_with", "share_type", "can_edit", "created_at")
    list_filter = ("share_type", "can_edit", "created_at")
    search_fields = ("entry__title", "shared_by__username", "shared_with__username")
    readonly_fields = ("share_key", "created_at")


# ============ NEW FEATURE ADMIN CLASSES ============

@admin.register(VoiceEntry)
class VoiceEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "duration", "transcription_status", "confidence_score", "created_at")
    list_filter = ("transcription_status", "created_at")
    search_fields = ("transcription", "user__username")
    readonly_fields = ("created_at", "processed_at", "confidence_score")
    ordering = ("-created_at",)


@admin.register(BackupData)
class BackupDataAdmin(admin.ModelAdmin):
    list_display = ("user", "backup_type", "backup_provider", "status", "entries_count", "created_at")
    list_filter = ("backup_type", "backup_provider", "status", "created_at")
    search_fields = ("user__username", "backup_location")
    readonly_fields = ("created_at", "completed_at", "restored_at")
    ordering = ("-created_at",)


@admin.register(TeamEntry)
class TeamEntryAdmin(admin.ModelAdmin):
    list_display = ("title", "creator", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "content", "creator__username")
    filter_horizontal = ("members",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(CollaborationComment)
class CollaborationCommentAdmin(admin.ModelAdmin):
    list_display = ("team_entry", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("content", "user__username", "team_entry__title")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(PushNotification)
class PushNotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "notification_type", "is_read", "is_sent", "created_at")
    list_filter = ("notification_type", "is_read", "is_sent", "created_at")
    search_fields = ("title", "message", "user__username")
    readonly_fields = ("created_at", "sent_at")
    ordering = ("-created_at",)


@admin.register(CalendarIntegration)
class CalendarIntegrationAdmin(admin.ModelAdmin):
    list_display = ("user", "provider", "is_enabled", "sync_direction", "last_synced")
    list_filter = ("provider", "is_enabled", "sync_direction")
    search_fields = ("user__username", "calendar_id")
    readonly_fields = ("created_at", "updated_at", "last_synced")


@admin.register(AdvancedAnalytics)
class AdvancedAnalyticsAdmin(admin.ModelAdmin):
    list_display = ("user", "task_completion_rate", "top_mood", "top_category", "last_calculated")
    list_filter = ("last_calculated",)
    search_fields = ("user__username", "top_category")
    readonly_fields = ("last_calculated",)


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "subject", "template_text")
    readonly_fields = ("created_at", "updated_at")


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ("recipient", "subject", "status", "sent_at", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("recipient", "subject", "user__username")
    readonly_fields = ("created_at", "sent_at")
    ordering = ("-created_at",)


@admin.register(SocialShare)
class SocialShareAdmin(admin.ModelAdmin):
    list_display = ("entry", "platform", "status", "engagement_count", "created_at")
    list_filter = ("platform", "status", "created_at")
    search_fields = ("entry__title", "user__username", "shared_url")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
