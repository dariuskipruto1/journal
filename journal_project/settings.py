"""Django settings for journal_project."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass  # python-dotenv not installed, use system environment variables


def _env_int(name, default):
    raw_value = os.getenv(name, str(default))
    try:
        return int(raw_value)
    except (TypeError, ValueError):
        return default


def _env_csv(name, default):
    raw_value = os.getenv(name, default)
    return [item.strip() for item in raw_value.split(",") if item.strip()]

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY", "django-insecure-journal-desk-production-key-2026"
)

DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() in {"1", "true", "yes", "on"}

# === APP BRANDING CONFIGURATION ===
APP_NAME = "Journal Desk"
APP_TAGLINE = "Your Personal Digital Journal & Diary"
COMPANY_NAME = "Journal Desk Inc."
COMPANY_WEBSITE = "https://journaldesk.io"
COMPANY_EMAIL = "support@journaldesk.io"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost,testserver").split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "drf_spectacular",
    "django_filters",
    "push_notifications",
    "django_apscheduler",
    "journal",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "journal_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "journal_project.wsgi.application"

# Database configuration - use PostgreSQL in production, SQLite in development
DATABASES = {}

if os.getenv("DATABASE_URL"):
    try:
        import dj_database_url
        DATABASES = {
            "default": dj_database_url.config(
                default=os.getenv("DATABASE_URL"),
                conn_max_age=600,
                conn_health_checks=True,
            )
        }
    except ImportError:
        # Fallback if dj_database_url not installed
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": os.getenv("DB_NAME", "journal"),
                "USER": os.getenv("DB_USER", "postgres"),
                "PASSWORD": os.getenv("DB_PASSWORD", ""),
                "HOST": os.getenv("DB_HOST", "localhost"),
                "PORT": os.getenv("DB_PORT", "5432"),
            }
        }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "entry_list"
LOGOUT_REDIRECT_URL = "login"

EMAIL_BACKEND = os.getenv(
    "DJANGO_EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
DEFAULT_FROM_EMAIL = os.getenv("DJANGO_DEFAULT_FROM_EMAIL", "noreply@journal.local")
EMAIL_HOST = os.getenv("DJANGO_EMAIL_HOST", "")
EMAIL_PORT = int(os.getenv("DJANGO_EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.getenv("DJANGO_EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("DJANGO_EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.getenv("DJANGO_EMAIL_USE_TLS", "True").lower() in {
    "1",
    "true",
    "yes",
    "on",
}

TASK_ALERTS_EMAIL_ENABLED = os.getenv("TASK_ALERTS_EMAIL_ENABLED", "True").lower() in {
    "1",
    "true",
    "yes",
    "on",
}
TASK_ALERTS_WHATSAPP_ENABLED = os.getenv(
    "TASK_ALERTS_WHATSAPP_ENABLED", "False"
).lower() in {"1", "true", "yes", "on"}
WHATSAPP_PROVIDER = os.getenv("WHATSAPP_PROVIDER", "")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
OLLAMA_TIMEOUT_SECONDS = _env_int("OLLAMA_TIMEOUT_SECONDS", 30)
OLLAMA_FALLBACK_MODELS = _env_csv(
    "OLLAMA_FALLBACK_MODELS",
    "llama2,llama3.2,mistral,qwen2.5",
)
WEATHER_DEFAULT_LOCATION = os.getenv("WEATHER_DEFAULT_LOCATION", "Nairobi")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Caching configuration
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "journal-cache",
    }
}

# Session configuration
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_SAMESITE = "Lax"

# CSRF configuration
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_FAILURE_VIEW = "django.views.csrf.csrf_failure"

# Security headers
SECURE_HSTS_SECONDS = 0 if DEBUG else 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
SECURE_SSL_REDIRECT = not DEBUG
X_FRAME_OPTIONS = "DENY"
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG" if DEBUG else "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose" if DEBUG else "simple",
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs" / "journal.log",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "journal": {
            "handlers": ["console", "file"],
            "level": "DEBUG" if DEBUG else "INFO",
            "propagate": False,
        },
    },
}

# REST Framework configuration
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S",
}

# CORS configuration
CORS_ALLOWED_ORIGINS = os.getenv(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:8000,http://127.0.0.1:3000,http://127.0.0.1:8000"
).split(",")
CORS_ALLOW_CREDENTIALS = True

# Static files optimization
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ============ NEW FEATURE CONFIGURATIONS ============

# Push Notifications Configuration
PUSH_NOTIFICATIONS_SETTINGS = {
    "FCM_API_KEY": os.getenv("FCM_API_KEY", ""),
    "APNS_CERTIFICATE": os.getenv("APNS_CERTIFICATE", ""),
}

# Voice Entry Configuration
VOICE_ENTRY_CONFIG = {
    "MAX_UPLOAD_SIZE": 50 * 1024 * 1024,  # 50MB
    "ALLOWED_FORMATS": ["audio/mpeg", "audio/wav", "audio/ogg", "audio/m4a"],
    "TRANSCRIPTION_SERVICE": os.getenv("TRANSCRIPTION_SERVICE", "google"),  # google, azure, aws
}

# Cloud Backup Configuration
BACKUP_CONFIG = {
    "ENABLED": True,
    "AUTO_BACKUP_ENABLED": os.getenv("AUTO_BACKUP_ENABLED", "True").lower() in {"1", "true", "yes", "on"},
    "BACKUP_INTERVAL_HOURS": _env_int("BACKUP_INTERVAL_HOURS", 24),
    "BACKUP_PROVIDERS": {
        "s3": {
            "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID", ""),
            "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY", ""),
            "aws_storage_bucket_name": os.getenv("AWS_STORAGE_BUCKET_NAME", ""),
            "aws_s3_region_name": os.getenv("AWS_S3_REGION_NAME", "us-east-1"),
        },
        "gcs": {
            "project_id": os.getenv("GCP_PROJECT_ID", ""),
            "credentials_file": os.getenv("GCP_CREDENTIALS_FILE", ""),
            "bucket_name": os.getenv("GCP_BUCKET_NAME", ""),
        },
    },
}

# Social Sharing Configuration
SOCIAL_SHARE_CONFIG = {
    "TWITTER_API_KEY": os.getenv("TWITTER_API_KEY", ""),
    "TWITTER_API_SECRET": os.getenv("TWITTER_API_SECRET", ""),
    "FACEBOOK_APP_ID": os.getenv("FACEBOOK_APP_ID", ""),
    "FACEBOOK_APP_SECRET": os.getenv("FACEBOOK_APP_SECRET", ""),
    "LINKEDIN_API_KEY": os.getenv("LINKEDIN_API_KEY", ""),
    "LINKEDIN_API_SECRET": os.getenv("LINKEDIN_API_SECRET", ""),
}

# Calendar Integration Configuration
CALENDAR_CONFIG = {
    "GOOGLE_CALENDAR": {
        "client_id": os.getenv("GOOGLE_CALENDAR_CLIENT_ID", ""),
        "client_secret": os.getenv("GOOGLE_CALENDAR_CLIENT_SECRET", ""),
        "redirect_uri": os.getenv("GOOGLE_CALENDAR_REDIRECT_URI", "http://localhost:8000/api/calendar/callback/"),
    },
    "OUTLOOK": {
        "client_id": os.getenv("OUTLOOK_CLIENT_ID", ""),
        "client_secret": os.getenv("OUTLOOK_CLIENT_SECRET", ""),
        "redirect_uri": os.getenv("OUTLOOK_REDIRECT_URI", "http://localhost:8000/api/calendar/callback/"),
    },
}

# Email Reminder Configuration
EMAIL_REMINDER_CONFIG = {
    "ENABLED": True,
    "USE_CELERY": os.getenv("USE_CELERY", "False").lower() in {"1", "true", "yes", "on"},
    "CHECK_INTERVAL_MINUTES": _env_int("EMAIL_CHECK_INTERVAL", 15),
    "RETRY_FAILED_EMAILS": True,
    "RETRY_ATTEMPTS": 3,
}

# Celery Configuration (for async tasks)
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes

# WebSocket Configuration (for real-time features)
ASGI_APPLICATION = "journal_project.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.getenv("REDIS_URL", "redis://localhost:6379")],
        },
    },
}

# Dark Mode / Theme Configuration
THEME_CONFIG = {
    "DEFAULT_THEME": "dark",
    "AVAILABLE_THEMES": ["light", "dark", "auto"],
    "COLORS": {
        "primary_blue": "#57c1ff",
        "dark_background": "#0a1830",
        "text_light": "#f8fbff",
        "text_soft": "#d5dce7",
        "accent_strong": "#258dff",
        "success": "#10b981",
        "warning": "#fbbf24",
        "danger": "#ef4444",
    },
}

# Advanced Analytics Configuration
ANALYTICS_CONFIG = {
    "ENABLED": True,
    "CALCULATE_DAILY": True,
    "CALCULATE_WEEKLY": True,
    "CALCULATE_MONTHLY": True,
    "RETENTION_DAYS": 90,
}

# Rate Limiting
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = "default"

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'", "https:"),
    "script-src": ("'self'", "'unsafe-inline'", "https:"),
    "style-src": ("'self'", "'unsafe-inline'", "https:"),
    "img-src": ("'self'", "data:", "https:"),
    "font-src": ("'self'", "https:"),
    "connect-src": ("'self'", "https:"),
}

# Sentry Configuration (Error Tracking)
if os.getenv("SENTRY_DSN"):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False,
    )

# API Documentation
SPECTACULAR_SETTINGS = {
    "TITLE": "Journal Pro API",
    "DESCRIPTION": "Professional Journal Application API",
    "VERSION": "1.0.0",
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAuthenticated"],
    "SCHEMA_PATH_PREFIX": "/api/",
}

# Mobile App Configuration
MOBILE_APP_CONFIG = {
    "IOS_APP_ID": os.getenv("IOS_APP_ID", ""),
    "ANDROID_APP_ID": os.getenv("ANDROID_APP_ID", ""),
    "API_BASE_URL": os.getenv("API_BASE_URL", "http://localhost:8000/api/"),
}
