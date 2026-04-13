from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Tag(models.Model):
    """Tags for better entry organization and filtering"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tags")
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default="#3498db")  # Hex color code
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "name")
        ordering = ("name",)

    def __str__(self):
        return f"{self.name} ({self.user})"


class Entry(models.Model):
    PRIORITY_LOW = "low"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_HIGH = "high"
    TASK_PRIORITY_CHOICES = (
        (PRIORITY_LOW, "Low"),
        (PRIORITY_MEDIUM, "Medium"),
        (PRIORITY_HIGH, "High"),
    )

    MOOD_CHOICES = (
        ("very_sad", "😢 Very Sad"),
        ("sad", "☹️ Sad"),
        ("neutral", "😐 Neutral"),
        ("happy", "🙂 Happy"),
        ("very_happy", "😄 Very Happy"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="entries")
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    tags = models.ManyToManyField(Tag, related_name="entries", blank=True)
    is_starred = models.BooleanField(default=False)
    task = models.CharField(max_length=100, blank=True)
    task_priority = models.CharField(
        max_length=10, choices=TASK_PRIORITY_CHOICES, blank=True
    )
    task_due_at = models.DateTimeField(null=True, blank=True)
    task_completed = models.BooleanField(default=False)
    task_completed_at = models.DateTimeField(null=True, blank=True)
    alert_phone_number = models.CharField(max_length=32, blank=True)
    alert_sent_at = models.DateTimeField(null=True, blank=True)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    is_private = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-date_created",)
        indexes = [
            models.Index(fields=["-date_created"]),
            models.Index(fields=["user", "-date_created"]),
            models.Index(fields=["user", "is_private"]),
        ]

    def __str__(self):
        return self.title

    @property
    def has_task(self):
        return bool(self.task and self.task.strip())

    @property
    def is_overdue(self):
        return (
            self.has_task
            and not self.task_completed
            and self.task_due_at is not None
            and self.task_due_at <= timezone.now()
        )

    @property
    def task_priority_label(self):
        if not self.task_priority:
            return "No priority"
        return self.get_task_priority_display()

    @property
    def days_old(self):
        return (timezone.now() - self.date_created).days

    def complete_task(self):
        """Mark task as completed"""
        if self.has_task:
            self.task_completed = True
            self.task_completed_at = timezone.now()
            self.save()


class Reminder(models.Model):
    """Reminders for tasks"""
    FREQUENCY_ONCE = "once"
    FREQUENCY_DAILY = "daily"
    FREQUENCY_WEEKLY = "weekly"
    FREQUENCY_MONTHLY = "monthly"
    
    FREQUENCY_CHOICES = (
        (FREQUENCY_ONCE, "One time"),
        (FREQUENCY_DAILY, "Daily"),
        (FREQUENCY_WEEKLY, "Weekly"),
        (FREQUENCY_MONTHLY, "Monthly"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reminders")
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="reminders")
    reminder_time = models.DateTimeField()
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default=FREQUENCY_ONCE)
    is_active = models.BooleanField(default=True)
    is_sent = models.BooleanField(default=False)
    last_sent = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("reminder_time",)

    def __str__(self):
        return f"Reminder for {self.entry.title}"


class DocumentUpload(models.Model):
    STATUS_STORED = "stored"
    STATUS_ANALYZED = "analyzed"
    STATUS_PENDING = "pending"

    STATUS_CHOICES = (
        (STATUS_STORED, "Stored"),
        (STATUS_PENDING, "Pending Review"),
        (STATUS_ANALYZED, "Analyzed"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="documents")
    entry = models.ForeignKey(Entry, on_delete=models.SET_NULL, null=True, blank=True, related_name="documents")
    title = models.CharField(max_length=200, blank=True)
    file = models.FileField(upload_to="uploads/%Y/%m/%d/")
    file_type = models.CharField(max_length=32, blank=True)
    analysis = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_STORED)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-uploaded_at",)

    def __str__(self):
        return self.title or self.file.name

    @property
    def file_name(self):
        return self.file.name.split("/")[-1]

    @property
    def file_extension(self):
        return self.file_name.split(".")[-1].lower() if "." in self.file_name else ""


class UserPreferences(models.Model):
    """User preferences and settings"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preferences")
    theme = models.CharField(max_length=10, choices=[("light", "Light"), ("dark", "Dark")], default="dark")
    notifications_enabled = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    language = models.CharField(max_length=5, default="en")
    items_per_page = models.IntegerField(default=10)
    show_analytics = models.BooleanField(default=True)
    auto_save_draft = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "User Preferences"

    def __str__(self):
        return f"{self.user.username}'s Preferences"


class EntryStats(models.Model):
    """Statistics for user entries"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="entry_stats")
    total_entries = models.IntegerField(default=0)
    total_words = models.IntegerField(default=0)
    completed_tasks = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_entry_date = models.DateField(null=True, blank=True)
    favorite_category = models.CharField(max_length=100, blank=True)
    favorite_mood = models.CharField(max_length=20, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Entry Stats"

    def __str__(self):
        return f"Stats for {self.user.username}"


class EntryShare(models.Model):
    """Share entries with other users or publicly"""
    SHARE_WITH_CHOICES = (
        ("user", "Specific User"),
        ("public", "Public"),
        ("link", "Shared Link"),
    )

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="shares")
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shared_entries")
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_shares", null=True, blank=True)
    share_type = models.CharField(max_length=20, choices=SHARE_WITH_CHOICES, default="user")
    share_key = models.CharField(max_length=50, unique=True, blank=True)
    can_edit = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("entry", "shared_with")

    def __str__(self):
        return f"{self.entry.title} shared with {self.shared_with}"


class VoiceEntry(models.Model):
    """Voice entry recordings"""
    entry = models.OneToOneField(Entry, on_delete=models.CASCADE, related_name="voice_entry", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="voice_entries")
    audio_file = models.FileField(upload_to="voice_entries/%Y/%m/%d/")
    duration = models.IntegerField(default=0)  # in seconds
    transcription = models.TextField(blank=True)
    transcription_status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("completed", "Completed"), ("failed", "Failed")],
        default="pending"
    )
    confidence_score = models.FloatField(default=0.0)
    language = models.CharField(max_length=10, default="en-US")
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Voice entry by {self.user.username}"


class BackupData(models.Model):
    """Cloud backup of user data"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="backups")
    backup_type = models.CharField(
        max_length=20,
        choices=[("manual", "Manual"), ("auto", "Automatic")],
        default="auto"
    )
    backup_provider = models.CharField(
        max_length=20,
        choices=[("local", "Local"), ("s3", "AWS S3"), ("gcs", "Google Cloud Storage")],
        default="local"
    )
    backup_location = models.CharField(max_length=500)
    entries_count = models.IntegerField(default=0)
    file_size = models.BigIntegerField(default=0)  # in bytes
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("in_progress", "In Progress"), ("completed", "Completed"), ("failed", "Failed")],
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    restored_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Backup for {self.user.username} - {self.created_at}"


class TeamEntry(models.Model):
    """Collaborative entries shared with team"""
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_team_entries")
    title = models.CharField(max_length=200)
    content = models.TextField()
    members = models.ManyToManyField(User, related_name="team_entries")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.title} by {self.creator.username}"


class CollaborationComment(models.Model):
    """Comments on collaborative entries"""
    team_entry = models.ForeignKey(TeamEntry, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.team_entry.title}"


class PushNotification(models.Model):
    """Push notifications for users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="push_notifications")
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=20,
        choices=[
            ("reminder", "Reminder"),
            ("share", "Share"),
            ("comment", "Comment"),
            ("mention", "Mention"),
            ("system", "System"),
        ],
        default="system"
    )
    related_entry = models.ForeignKey(Entry, on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class CalendarIntegration(models.Model):
    """Calendar integration settings"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="calendar_integration")
    provider = models.CharField(
        max_length=20,
        choices=[("google", "Google Calendar"), ("outlook", "Outlook"), ("ical", "iCalendar")],
        default="google"
    )
    is_enabled = models.BooleanField(default=False)
    sync_direction = models.CharField(
        max_length=20,
        choices=[("one_way", "One Way (J→Cal)"), ("two_way", "Two Way")],
        default="one_way"
    )
    calendar_id = models.CharField(max_length=255, blank=True)
    access_token = models.TextField(blank=True)
    refresh_token = models.TextField(blank=True)
    last_synced = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Calendar Integrations"

    def __str__(self):
        return f"{self.user.username}'s {self.provider} Calendar"


class AdvancedAnalytics(models.Model):
    """Advanced analytics and AI insights"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="advanced_analytics")
    
    # Mood trends
    mood_trend = models.CharField(max_length=50, blank=True)  # JSON data
    top_mood = models.CharField(max_length=20, blank=True)
    
    # Writing patterns
    average_words_per_entry = models.FloatField(default=0.0)
    peak_writing_hour = models.IntegerField(default=0)
    peak_writing_day = models.CharField(max_length=20, blank=True)
    
    # Productivity metrics
    task_completion_rate = models.FloatField(default=0.0)
    avg_days_to_complete = models.FloatField(default=0.0)
    
    # Category insights
    top_category = models.CharField(max_length=100, blank=True)
    category_breakdown = models.TextField(blank=True)  # JSON data
    
    # Time series data
    daily_entry_count = models.TextField(blank=True)  # JSON data
    weekly_stats = models.TextField(blank=True)  # JSON data
    
    # Generated insights
    ai_insights = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)  # JSON array
    
    last_calculated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Advanced Analytics"

    def __str__(self):
        return f"Analytics for {self.user.username}"


class EmailTemplate(models.Model):
    """Email templates for reminders and notifications"""
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    template_text = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class EmailLog(models.Model):
    """Log of all sent emails"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="email_logs")
    recipient = models.EmailField()
    subject = models.CharField(max_length=200)
    template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    related_entry = models.ForeignKey(Entry, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("sent", "Sent"), ("failed", "Failed")],
        default="pending"
    )
    sent_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Email to {self.recipient} - {self.status}"


class SocialShare(models.Model):
    """Social sharing history"""
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="social_shares")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(
        max_length=20,
        choices=[("twitter", "Twitter"), ("facebook", "Facebook"), ("linkedin", "LinkedIn"), ("instagram", "Instagram")],
        default="twitter"
    )
    shared_url = models.URLField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("shared", "Shared"), ("failed", "Failed")],
        default="pending"
    )
    engagement_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.entry.title} shared on {self.platform}"
