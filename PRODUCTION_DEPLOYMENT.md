# Production Deployment Guide

Complete step-by-step guide to deploy Journal Desk to production on major cloud platforms.

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Setup](#environment-setup)
3. [Heroku Deployment](#heroku-deployment)
4. [AWS EC2 Deployment](#aws-ec2-deployment)
5. [DigitalOcean Deployment](#digitalocean-deployment)
6. [Azure Deployment](#azure-deployment)
7. [PostgreSQL Setup](#postgresql-setup)
8. [SSL/HTTPS Configuration](#ssltls-configuration)
9. [Monitoring & Scaling](#monitoring--scaling)
10. [Maintenance & Updates](#maintenance--updates)

---

## Pre-Deployment Checklist

### Code & Security

- [ ] All tests pass: `python manage.py test`
- [ ] No debug mode: `DEBUG = False` in settings.py
- [ ] Secret key secure and not in repository
- [ ] ALLOWED_HOSTS configured properly
- [ ] CSRF_TRUSTED_ORIGINS set correctly
- [ ] All dependencies in requirements.txt
- [ ] No hardcoded credentials in code
- [ ] Static files collected: `python manage.py collectstatic`

### Features

- [ ] All 10 features tested in staging
- [ ] Email configuration working
- [ ] Cloud storage (S3/GCS) configured
- [ ] Backup system tested
- [ ] API endpoints verified

### Performance

- [ ] Database optimized with indexes
- [ ] Cache system (Redis) configured
- [ ] CDN setup for static assets
- [ ] Cron jobs for background tasks
- [ ] Rate limiting configured

### Monitoring

- [ ] Error tracking (Sentry) configured
- [ ] Analytics setup (Google Analytics)
- [ ] Logging configured
- [ ] Health check endpoint ready
- [ ] Backup strategy defined

---

## Environment Setup

### Local Testing Before Production

```bash
# Create production settings file
cp journal_project/settings.py journal_project/settings_local.py

# Create production requirements
pip freeze > requirements.txt

# Update requirements.txt for production
# Add: gunicorn, whitenoise, psycopg2-binary, sentry-sdk
echo "gunicorn==22.0.0" >> requirements.txt
echo "psycopg2-binary==2.9.9" >> requirements.txt
echo "sentry-sdk==1.45.0" >> requirements.txt
echo "django-storages[s3]==1.14.0" >> requirements.txt
```

### Environment Variables

Create `.env.production`:

```env
# Security
DEBUG=False
SECRET_KEY=your_production_secret_key_here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@db-host:5432/journal_prod
DB_ENGINE=django.db.backends.postgresql
DB_NAME=journal_production
DB_USER=journal_user
DB_PASSWORD=secure_password_here
DB_HOST=db.yourdomain.com
DB_PORT=5432

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your_app_specific_password

# Cloud Storage (AWS S3)
USE_S3=True
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_STORAGE_BUCKET_NAME=journal-prod-bucket
AWS_S3_REGION_NAME=us-east-1

# Redis (Cache & Sessions)
REDIS_URL=redis://user:password@cache.yourdomain.com:6379/0

# Celery (Background Tasks)
CELERY_BROKER_URL=redis://user:password@celery.yourdomain.com:6379/0

# Sentry (Error Tracking)
SENTRY_DSN=https://your_sentry_key@o0000000.ingest.sentry.io/0000000

# Site Settings
SITE_URL=https://yourdomain.com
SITE_NAME=Journal Desk
```

### Production Django Settings

Create `journal_project/settings_production.py`:

```python
from .settings import *
import os
from decouple import config

# Security
DEBUG = False
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default=5432),
        'CONN_MAX_AGE': 600,
    }
}

# Static & Media Files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# AWS S3 Storage
if config('USE_S3', default=False, cast=bool):
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@yourdomain.com')

# Security Headers
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Celery
CELERY_BROKER_URL = config('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = config('CELERY_BROKER_URL')

# Sentry Error Tracking
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=config('SENTRY_DSN', default=''),
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=False,
    environment='production'
)

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {module} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/journal/django.log',
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'sentry_sdk.integrations.logging.EventHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'sentry'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

---

## Heroku Deployment

### Fastest & Easiest Option

**Time to Deploy:** ~10 minutes
**Cost:** Free tier available, then $7-50/month
**Best for:** Rapid deployment, low maintenance

### Step 1: Setup Heroku CLI

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Add Redis addon (optional)
heroku addons:create heroku-redis:premium-0
```

### Step 2: Create Procfile

Create `Procfile`:
```
web: gunicorn journal_project.wsgi
release: python manage.py migrate
```

### Step 3: Create Runtime Specification

Create `runtime.txt`:
```
python-3.11.8
```

### Step 4: Update requirements.txt

```bash
pip install gunicorn whitenoise django-heroku
pip freeze > requirements.txt
```

### Step 5: Update Django Settings

Add to `journal_project/settings.py`:

```python
import django_heroku
import dj_database_url

# Heroku database
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
    }

# Heroku settings
django_heroku.settings(locals())
```

### Step 6: Configure Environment Variables

```bash
# Set production settings
heroku config:set SETTINGS_MODULE=journal_project.settings_production

# Set secret key
heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')

# Set email configuration
heroku config:set EMAIL_HOST=smtp.gmail.com
heroku config:set EMAIL_HOST_USER=your-email@gmail.com
heroku config:set EMAIL_HOST_PASSWORD=your_app_password
```

### Step 7: Deploy

```bash
# Commit changes
git add .
git commit -m "Prepare for production"

# Push to Heroku
git push heroku main

# View logs
heroku logs --tail

# Open app
heroku open
```

---

## AWS EC2 Deployment

### More Control & Power

**Time to Deploy:** ~30 minutes
**Cost:** $5-100+ per month (depending on instance size)
**Best for:** Scalability, custom requirements, advanced configuration

### Step 1: Launch EC2 Instance

```bash
# Using AWS CLI
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --count 1 \
  --instance-type t3.small \
  --key-name my-key-pair \
  --security-groups allow-http-https
```

Or use AWS Console:
1. Go to EC2 Dashboard
2. Click "Launch Instance"
3. Select Ubuntu 22.04 LTS
4. Choose t3.small instance
5. Configure security groups (allow ports 22, 80, 443)
6. Launch

### Step 2: Connect to Server

```bash
# SSH into instance
ssh -i my-key-pair.pem ubuntu@your-ec2-instance-dns

# Update system
sudo apt update && sudo apt upgrade -y
```

### Step 3: Install Dependencies

```bash
# System packages
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git redis-server supervisor

# Create app user
sudo useradd -m -s /bin/bash journal
sudo su - journal

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
pip install gunicorn
```

### Step 4: Setup PostgreSQL

```bash
sudo -u postgres psql

# Inside PostgreSQL shell
CREATE DATABASE journal_prod;
CREATE USER journal_user WITH PASSWORD 'secure_password';
ALTER ROLE journal_user SET client_encoding TO 'utf8';
GRANT ALL PRIVILEGES ON DATABASE journal_prod TO journal_user;
\q
```

### Step 5: Configure Application

```bash
# Clone repository
cd /home/journal
git clone https://github.com/yourusername/journal.git
cd journal

# Setup environment
cp .env.example .env.production
nano .env.production  # Edit with your values

# Collect static files
python manage.py collectstatic --settings=journal_project.settings_production --noinput

# Run migrations
python manage.py migrate --settings=journal_project.settings_production
```

### Step 6: Create Systemd Service

Create `/etc/systemd/system/journal.service`:

```ini
[Unit]
Description=Journal Desk Django Application
After=network.target

[Service]
User=journal
Group=www-data
WorkingDirectory=/home/journal/journal
Environment="PATH=/home/journal/journal/venv/bin"
ExecStart=/home/journal/journal/venv/bin/gunicorn \
    --workers 3 \
    --worker-class sync \
    --bind 127.0.0.1:8000 \
    --timeout 120 \
    --access-logfile - \
    journal_project.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable journal
sudo systemctl start journal
sudo systemctl status journal
```

### Step 7: Configure Nginx

Create `/etc/nginx/sites-available/journal`:

```nginx
upstream journal_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    client_max_body_size 50M;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    client_max_body_size 50M;

    # SSL certificates (see SSL section below)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    # Static files
    location /static/ {
        alias /home/journal/journal/static/;
        expires 30d;
    }

    location /media/ {
        alias /home/journal/journal/media/;
    }

    # Application
    location / {
        proxy_pass http://journal_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/journal /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 8: Setup SSL/HTTPS (Let's Encrypt)

See SSL section below.

---

## DigitalOcean Deployment

### Best of Both Worlds

**Time to Deploy:** ~20 minutes
**Cost:** $5-40+ per month
**Best for:** Simplicity + control

### Step 1: Create Droplet

1. Go to DigitalOcean Dashboard
2. Click "Create" → "Droplets"
3. Choose image: Ubuntu 22.04 x64
4. Choose plan: Basic ($5/month - 1 CPU, 1GB RAM)
5. Add SSH key
6. Create

### Step 2: Setup (Same as AWS)

Follow AWS EC2 steps 2-8, they're identical for Ubuntu servers.

### Step 3: Add DigitalOcean Spaces (Optional)

For cloud storage:

```python
# settings_production.py
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "access_key": config('DO_SPACE_KEY'),
            "secret_key": config('DO_SPACE_SECRET'),
            "endpoint_url": config('DO_SPACE_ENDPOINT'),
            "location": "media",
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
        "OPTIONS": {
            "access_key": config('DO_SPACE_KEY'),
            "secret_key": config('DO_SPACE_SECRET'),
            "endpoint_url": config('DO_SPACE_ENDPOINT'),
            "location": "static",
        },
    },
}
```

---

## Azure Deployment

### Enterprise Solutions

**Time to Deploy:** ~25 minutes
**Cost:** $5-100+ per month
**Best for:** Enterprise features, advanced security

### Step 1: Create App Service

```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login
az login

# Create resource group
az group create --name journal-rg --location eastus

# Create App Service Plan
az appservice plan create --name journal-plan --resource-group journal-rg --sku B1 --is-linux

# Create Web App
az webapp create --resource-group journal-rg --plan journal-plan --name my-journal-app --runtime "PYTHON:3.11"
```

### Step 2: Configure Deployment

```bash
# Setup git deployment
az webapp deployment user set --user-name your-username --password your-password
az webapp deployment source config-local-git --name my-journal-app --resource-group journal-rg

# Deploy using git
git remote add azure https://your-username@my-journal-app.scm.azurewebsites.net:443/my-journal-app.git
git push azure main
```

### Step 3: Configure Database

```bash
# Create PostgreSQL server
az postgres server create \
  --resource-group journal-rg \
  --name journal-db-server \
  --location eastus \
  --admin-user dbadmin \
  --admin-password Admin@12345
```

---

## PostgreSQL Setup

### Initialize Production Database

```bash
# Connect to database
psql -h db.yourdomain.com -U journal_user -d journal_prod

# Verify tables
\dt

# Check indexes
\d entry

# Backup database (before production switch)
pg_dump -h db.yourdomain.com -U journal_user journal_prod > backup.sql

# Restore from backup
psql -h db.yourdomain.com -U journal_user journal_prod < backup.sql
```

### Performance Tuning

```sql
-- Add indexes for faster queries
CREATE INDEX idx_entry_date ON journal_entry(created_at);
CREATE INDEX idx_entry_user ON journal_entry(user_id);
CREATE INDEX idx_task_status ON journal_entry_task(status);
CREATE INDEX idx_mood_date ON journal_entry(mood_rating, created_at);

-- Analyze table statistics
ANALYZE;

-- Check slow queries
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;
```

---

## SSL/HTTPS Configuration

### Using Let's Encrypt (Free)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# For Nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
sudo systemctl enable certbot.timer
```

### Using AWS Certificate Manager

```bash
aws acm request-certificate \
  --domain-name yourdomain.com \
  --subject-alternative-names www.yourdomain.com \
  --region us-east-1
```

---

## Monitoring & Scaling

### Monitoring Setup

#### 1. Sentry (Error Tracking)

Already configured in settings_production.py above.

#### 2. Prometheus + Grafana (Metrics)

```bash
# Install Prometheus (on separate server)
sudo apt install -y prometheus

# Configure /etc/prometheus/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'django'
    static_configs:
      - targets: ['localhost:8000']
```

#### 3. CloudWatch (AWS Monitoring)

```python
# settings_production.py
LOGGING = {
    'handlers': {
        'watchtower': {
            'level': 'ERROR',
            'class': 'watchtower.CloudWatchLogHandler',
            'log_group': '/journal/django',
            'stream_name': 'production',
        },
    },
}
```

### Scaling Database

```bash
# Upgrade PostgreSQL
aws rds modify-db-instance \
  --db-instance-identifier journal-db \
  --allocated-storage 200 \
  --apply-immediately
```

### Scaling Application

Add more Gunicorn workers:
```bash
# In systemd service
ExecStart=/usr/local/bin/gunicorn --workers 8 --worker-class sync
```

---

## Maintenance & Updates

### Regular Tasks

**Daily:**
- Check error logs
- Monitor database size

**Weekly:**
- Verify backups
- Check disk space
- Review slow queries

**Monthly:**
- Update dependencies: `pip install --upgrade -r requirements.txt`
- Database maintenance
- Security patches

### Database Backups

```bash
# Automated daily backup
(crontab -l 2>/dev/null; echo "0 2 * * * pg_dump -h localhost -U journal_user journal_prod > /backups/journal-$(date +\%Y\%m\%d).sql") | crontab -

# Verify backups
ls -lah /backups/
```

### Zero-Downtime Deployment

```bash
# 1. Test locally
python manage.py test

# 2. Deploy to staging
git checkout staging && git pull origin staging

# 3. Blue-green deployment
# Keep current version as "blue" (active)
# Deploy new version to "green" (standby)
# Switch load balancer to "green"
# Keep "blue" available for rollback

# 4. Database migrations
python manage.py migrate --plan
python manage.py migrate

# 5. Restart services
sudo systemctl restart journal
```

### Rollback Procedure

```bash
# If something goes wrong
git revert <commit-hash>
git push production main

# Restart services
sudo systemctl restart journal

# Verify
curl https://yourdomain.com/health/
```

---

## Deployment Checklist

Before going live:

**Infrastructure:**
- [ ] Database configured and tested
- [ ] Redis cache ready
- [ ] SSL certificate installed
- [ ] Monitoring tools active
- [ ] Backup system working

**Application:**
- [ ] All tests pass
- [ ] Static files collected
- [ ] Database migrations applied
- [ ] Media files configuration
- [ ] Email service working

**Security:**
- [ ] DEBUG = False
- [ ] SECRET_KEY configured
- [ ] ALLOWED_HOSTS set
- [ ] Security headers enabled
- [ ] HTTPS redirects working

**Monitoring:**
- [ ] Error tracking active
- [ ] Logs configured
- [ ] Health checks working
- [ ] Alerts configured
- [ ] Performance baselines set

---

**Last Updated:** April 11, 2026
**Version:** 2.0
**Status:** Production Ready

For support: support@yourdomain.com
Documentation: https://docs.yourdomain.com
