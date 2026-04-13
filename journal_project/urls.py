
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from journal.api import (
    EntryViewSet, TagViewSet, ReminderViewSet, 
    UserPreferencesViewSet, EntryStatsViewSet, DocumentUploadViewSet,
    VoiceEntryViewSet, BackupDataViewSet, TeamEntryViewSet,
    CollaborationCommentViewSet, PushNotificationViewSet,
    CalendarIntegrationViewSet, AdvancedAnalyticsViewSet,
    EmailLogViewSet, SocialShareViewSet
)

# API Router
router = DefaultRouter()

# Existing endpoints
router.register(r"api/entries", EntryViewSet, basename="api_entry")
router.register(r"api/tags", TagViewSet, basename="api_tag")
router.register(r"api/reminders", ReminderViewSet, basename="api_reminder")
router.register(r"api/preferences", UserPreferencesViewSet, basename="api_preferences")
router.register(r"api/stats", EntryStatsViewSet, basename="api_stats")
router.register(r"api/documents", DocumentUploadViewSet, basename="api_document")

# New feature endpoints
router.register(r"api/voice-entries", VoiceEntryViewSet, basename="api_voice_entry")
router.register(r"api/backups", BackupDataViewSet, basename="api_backup")
router.register(r"api/team-entries", TeamEntryViewSet, basename="api_team_entry")
router.register(r"api/comments", CollaborationCommentViewSet, basename="api_comment")
router.register(r"api/notifications", PushNotificationViewSet, basename="api_notification")
router.register(r"api/calendar", CalendarIntegrationViewSet, basename="api_calendar")
router.register(r"api/analytics", AdvancedAnalyticsViewSet, basename="api_analytics")
router.register(r"api/email-logs", EmailLogViewSet, basename="api_email_log")
router.register(r"api/social-shares", SocialShareViewSet, basename="api_social_share")

@require_http_methods(["GET"])
def health_check(request):
    """Health check endpoint for deployment monitoring"""
    return JsonResponse({
        "status": "healthy",
        "version": "1.0.0",
        "database": "connected"
    })

urlpatterns = [
    path("health/", health_check, name="health_check"),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("journal.urls")),
    path("", include(router.urls)),
    path("api/auth/", include("rest_framework.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = ["__debug__/", include(debug_toolbar.urls)] + urlpatterns
