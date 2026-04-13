from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("entries/", views.entry_list, name="entry_list"),
    path("entries/search/", views.entry_search, name="entry_search"),
    path("documents/", views.document_upload, name="document_upload"),
    path("tasks/", views.task_list, name="task_list"),
    path("analytics/", views.analytics, name="analytics"),
    path("profile/", views.profile, name="profile"),
    path("help/", views.help_page, name="help_page"),
    path("calendar/", views.calendar_view, name="calendar"),
    path("settings/", views.settings_view, name="settings"),
    path("about/", views.about_view, name="about"),
    path("categories/", views.categories_view, name="categories"),
    path("export/", views.export_view, name="export"),
    path("reminders/", views.reminders_view, name="reminders"),
    path("mood/", views.mood_tracker_view, name="mood_tracker"),
    path("notes/", views.quick_notes_view, name="quick_notes"),
    path("insights/", views.insights_view, name="insights"),
    path("chatbot/", views.ollama_chat, name="ollama_chat"),
    path("chatbot/live/", views.assistant_realtime, name="assistant_realtime"),
    path("chatbot/health/", views.chatbot_health, name="chatbot_health"),
    path("entries/export/", views.entry_export_csv, name="entry_export_csv"),
    path("entry/<int:pk>/", views.entry_detail, name="entry_detail"),
    path("entry/<int:pk>/edit/", views.entry_edit, name="entry_edit"),
    path("entry/<int:pk>/delete/", views.entry_delete, name="entry_delete"),
    path("entry/<int:pk>/toggle-task/", views.entry_toggle_task, name="entry_toggle_task"),
    path("entry/<int:pk>/toggle-star/", views.entry_toggle_star, name="entry_toggle_star"),
    
    # New feature routes
    path("email-reminders/", views.email_reminders_view, name="email_reminders"),
    path("notifications/", views.notifications_view, name="notifications"),
    path("collaboration/", views.collaboration_view, name="collaboration"),
    path("cloud-backup/", views.cloud_backup_view, name="cloud_backup"),
    path("social-sharing/", views.social_sharing_view, name="social_sharing"),
    path("calendar-integration/", views.calendar_integration_view, name="calendar_integration"),
    path("advanced-analytics/", views.advanced_analytics_view, name="advanced_analytics"),
    path("voice-entry/", views.voice_entry_view, name="voice_entry"),
    path("theme-toggle/", views.theme_toggle, name="theme_toggle"),
    path("preferences/", views.user_preferences, name="user_preferences"),
    
    path("signup/", views.signup, name="signup"),
]
