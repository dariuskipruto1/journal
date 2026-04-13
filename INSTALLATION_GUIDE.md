# Journal Pro - Complete Setup Guide

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy `.env.example` to `.env` and update with your values:

```bash
cp .env.example .env
```

### 3. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create a superuser account
python manage.py createsuperuser

# Load initial data (optional)
python manage.py loaddata initial_data.json
```

### 4. Static Files

```bash
# Collect static files
python manage.py collectstatic --noinput
```

### 5. Run Development Server

```bash
# Start the application
python manage.py runserver

# Start in production-like mode
gunicorn journal_project.wsgi:application
```

The app will be available at: `http://localhost:8000`

---

## 📋 Feature Configuration

### Email Reminders

Set in your `.env`:
```
DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
DJANGO_EMAIL_HOST=smtp.gmail.com
DJANGO_EMAIL_PORT=587
DJANGO_EMAIL_HOST_USER=your-email@gmail.com
DJANGO_EMAIL_HOST_PASSWORD=your-app-password
DJANGO_EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=noreply@journaldesk.app
```

### Push Notifications (Firebase Cloud Messaging)

```
FCM_API_KEY=your-fcm-server-key
```

### Voice Entry Transcription

Choose your service:

**Google Cloud Speech-to-Text:**
```
TRANSCRIPTION_SERVICE=google
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

**Azure Cognitive Services:**
```
TRANSCRIPTION_SERVICE=azure
AZURE_SPEECH_KEY=your-key
AZURE_SPEECH_REGION=eastus
```

**AWS Transcribe:**
```
TRANSCRIPTION_SERVICE=aws
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_DEFAULT_REGION=us-east-1
```

### Cloud Backup

**AWS S3:**
```
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=my-journal-backups
AWS_S3_REGION_NAME=us-east-1
```

**Google Cloud Storage:**
```
GCP_PROJECT_ID=your-project
GCP_CREDENTIALS_FILE=/path/to/credentials.json
GCP_BUCKET_NAME=my-journal-backups
```

### Calendar Integration

**Google Calendar:**
```
GOOGLE_CALENDAR_CLIENT_ID=your-client-id
GOOGLE_CALENDAR_CLIENT_SECRET=your-secret
GOOGLE_CALENDAR_REDIRECT_URI=http://localhost:8000/api/calendar/callback/
```

**Outlook Calendar:**
```
OUTLOOK_CLIENT_ID=your-client-id
OUTLOOK_CLIENT_SECRET=your-secret
OUTLOOK_REDIRECT_URI=http://localhost:8000/api/calendar/callback/
```

### Redis (for Celery & WebSockets)

```
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
```

---

## 🎨 Features Overview

### Dashboard
- Real-time stats and activity feed
- Weather updates and time display
- Quick action buttons
- Analytics overview

### Journal Entries
- Rich text editing
- Mood tracking
- Category organization
- Star/favorite marking
- Search & filtering

### Tasks & Reminders
- Create tasks with priorities
- Set due dates
- Email reminders
- Task completion tracking
- Overdue alerts

### Voice Entries
- Record audio notes directly
- Automatic transcription
- Search within transcriptions
- Convert voice to text entry

### Collaboration
- Share entries with specific users
- Team entries for group journaling
- Comments and discussions
- Real-time notifications

### Cloud Backup
- Automatic daily backups
- Manual backup creation
- Multi-provider support (S3, GCS)
- One-click restore

### Social Sharing
- Share entries on Twitter, Facebook, LinkedIn
- Generate shareable links
- Track engagement metrics
- Comment integration

### Calendar Integration
- Sync entries with Google/Outlook Calendar
- Two-way synchronization
- Task deadlines in calendar
- Reminder notifications

### Advanced Analytics
- Mood trend analysis
- Writing pattern insights
- Productivity metrics
- Task completion rates
- Category breakdown
- AI-powered recommendations

---

## 🔧 API Documentation

Access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/schema/`

### Available Endpoints

**Entries API:**
- `GET /api/entries/` - List all entries
- `POST /api/entries/` - Create new entry
- `GET /api/entries/{id}/` - Get entry details
- `PUT /api/entries/{id}/` - Update entry
- `DELETE /api/entries/{id}/` - Delete entry
- `POST /api/entries/{id}/complete_task/` - Mark task complete
- `POST /api/entries/{id}/toggle_star/` - Toggle favorite
- `GET /api/entries/starred/` - Get starred entries
- `GET /api/entries/overdue_tasks/` - Get overdue tasks
- `GET /api/entries/search/` - Search entries

**Voice Entries API:**
- `GET /api/voice-entries/` - List voice entries
- `POST /api/voice-entries/` - Upload voice entry
- `GET /api/voice-entries/{id}/transcription/` - Get transcription

**Backup API:**
- `GET /api/backups/` - List backups
- `POST /api/backups/create_backup/` - Create new backup
- `POST /api/backups/{id}/restore/` - Restore backup

**Notifications API:**
- `GET /api/notifications/` - Get notifications
- `POST /api/notifications/{id}/mark_read/` - Mark as read
- `POST /api/notifications/mark_all_read/` - Mark all as read
- `GET /api/notifications/unread_count/` - Unread count

**Team Entries API:**
- `GET /api/team-entries/` - List team entries
- `POST /api/team-entries/` - Create team entry
- `POST /api/team-entries/{id}/add_member/` - Add member
- `POST /api/team-entries/{id}/remove_member/` - Remove member

---

## 📱 Mobile App Setup

The mobile app can connect to this API. Configure in `.env`:

```
API_BASE_URL=http://your-domain.com/api/
IOS_APP_ID=com.yourcompany.journaldesk
ANDROID_APP_ID=com.yourcompany.journaldesk
```

---

## 🔐 Security

- All user data is encrypted
- HTTPS required in production
- CSRF protection enabled
- SQL injection prevention
- XSS protection via CSP headers
- Rate limiting on API endpoints
- JWT token support for mobile apps

---

## 🚀 Deployment

### Production Checklist

```bash
# Set production environment
export DJANGO_DEBUG=False
export DJANGO_SECRET_KEY=your-long-random-secret-key
export ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start with Gunicorn
gunicorn journal_project.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --worker-class sync \
  --timeout 30
```

### Docker Deployment

```bash
# Build image
docker build -t journal-pro .

# Run container
docker run -p 8000:8000 \
  -e DJANGO_DEBUG=False \
  -e DATABASE_URL=postgresql://user:pass@db:5432/journal \
  journal-pro
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Database Migration Errors
```bash
# Reset database (development only)
python manage.py shell
>>> from django.core.management import call_command
>>> call_command('migrate', database='default', verbosity=0)
```

### Missing Static Files
```bash
# Recollect static files
python manage.py collectstatic --clear --noinput
```

### Email Not Sending
```bash
# Test email configuration
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'This is a test', 'from@example.com', ['to@example.com'])
```

---

## 📧 Support

For issues, bugs, or feature requests, please visit:
- GitHub Issues: https://github.com/yourrepo/issues
- Documentation: https://docs.journaldesk.app
- Community Forum: https://community.journaldesk.app

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

**Happy Journaling! ✨**
