# Journal Desk - Complete Deployment Guide

This guide provides step-by-step instructions for deploying Journal Desk to production using different platforms.

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Local Docker Deployment](#local-docker-deployment)
3. [Heroku Deployment](#heroku-deployment)
4. [AWS Deployment](#aws-deployment)
5. [DigitalOcean Deployment](#digitalocean-deployment)
6. [Post-Deployment](#post-deployment)

---

## Pre-Deployment Checklist

Before deploying to production, ensure:

- [ ] All Python errors are fixed (`python manage.py check` passes)
- [ ] Database migrations are up to date
- [ ] Static files are collected (`python manage.py collectstatic`)
- [ ] Environment variables are configured
- [ ] Secret key is changed from default
- [ ] DEBUG is set to False
- [ ] Allowed hosts are properly configured
- [ ] Git repository is initialized
- [ ] Tests pass (if applicable)

**Verification:**
```bash
cd /home/jayden/Desktop/now
python manage.py check        # Should show: System check identified no issues
python manage.py migrate      # Should show: No migrations to apply
python manage.py collectstatic --noinput
```

---

## Local Docker Deployment

Deploy locally using Docker for testing before production deployment.

### Prerequisites
- Docker installed (https://docs.docker.com/get-docker/)
- Docker Compose installed (https://docs.docker.com/compose/install/)

### Steps

1. **Update environment variables in docker-compose.yml**
   ```bash
   # Edit docker-compose.yml and set:
   # - DJANGO_SECRET_KEY: Generate a secure key
   # - DJANGO_ALLOWED_HOSTS: localhost,127.0.0.1
   ```

2. **Build and start services**
   ```bash
   docker-compose up -d
   ```

3. **Check services are running**
   ```bash
   docker-compose ps
   # All services should show "Up"
   ```

4. **Access the application**
   - Web: http://localhost
   - API: http://localhost/api/
   - Admin: http://localhost/admin/

5. **Create superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **View logs**
   ```bash
   docker-compose logs -f web
   ```

7. **Stop services**
   ```bash
   docker-compose down
   ```

---

## Heroku Deployment

Deploy to Heroku for free or paid hosting.

### Prerequisites
- Heroku account (free at https://heroku.com)
- Heroku CLI installed (https://devcenter.heroku.com/articles/heroku-cli)
- Git initialized

### Automatic Deployment Script

Run the automated deployment script:
```bash
chmod +x deploy.sh
./deploy.sh journal-desk-yourname
```

Replace `journal-desk-yourname` with your desired app name.

### Manual Deployment

1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Create Heroku app**
   ```bash
   heroku create journal-desk-yourname
   ```

3. **Add PostgreSQL database**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. **Set environment variables**
   ```bash
   heroku config:set DJANGO_DEBUG=False
   heroku config:set DJANGO_SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
   heroku config:set DJANGO_ALLOWED_HOSTS="journal-desk-yourname.herokuapp.com"
   heroku config:set TASK_ALERTS_EMAIL_ENABLED=False
   ```

5. **Deploy**
   ```bash
   git push heroku master
   ```

6. **Run migrations**
   ```bash
   heroku run python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   heroku run python manage.py createsuperuser
   ```

8. **Open application**
   ```bash
   heroku open
   ```

### View Logs
```bash
heroku logs --tail
```

### Update Application
```bash
git add .
git commit -m "Update: your changes"
git push heroku master
```

---

## AWS Deployment

Deploy to AWS EC2 with RDS database.

### Prerequisites
- AWS account
- EC2 instance (Ubuntu 22.04)
- RDS PostgreSQL database

### Steps

1. **Connect to EC2 instance**
   ```bash
   ssh -i your-key.pem ec2-user@your-instance-ip
   ```

2. **Install dependencies**
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3.11 python3-pip python3-venv
   sudo apt-get install -y postgresql-client-common postgresql-client
   sudo apt-get install -y nginx supervisor
   ```

3. **Clone repository**
   ```bash
   git clone https://github.com/yourusername/journal-desk.git
   cd journal-desk
   ```

4. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

5. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Configure environment**
   ```bash
   nano .env.production
   # Set all required environment variables
   cp .env.production .env
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run migrations**
   ```bash
   python manage.py migrate
   ```

9. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

10. **Configure Supervisor for Gunicorn**
    ```bash
    sudo tee /etc/supervisor/conf.d/journal.conf > /dev/null <<EOF
    [program:journal]
    directory=/home/ec2-user/journal-desk
    command=/home/ec2-user/journal-desk/venv/bin/gunicorn \\
            journal_project.wsgi:application \\
            --bind 127.0.0.1:8000 \\
            --workers 4
    autostart=true
    autorestart=true
    redirect_stderr=true
    stdout_logfile=/var/log/journal.log
    EOF
    ```

11. **Configure Nginx**
    ```bash
    sudo cp nginx.conf /etc/nginx/sites-available/journal
    sudo ln -s /etc/nginx/sites-available/journal /etc/nginx/sites-enabled/
    sudo rm /etc/nginx/sites-enabled/default
    sudo nginx -t
    sudo systemctl restart nginx
    ```

12. **Start Supervisor**
    ```bash
    sudo supervisorctl reread
    sudo supervisorctl update
    sudo supervisorctl start journal
    ```

---

## DigitalOcean Deployment

Deploy to DigitalOcean App Platform or Droplet.

### App Platform (Easiest)

1. **Connect GitHub repository**
   - Go to App Platform dashboard
   - Click "Create App"
   - Select your GitHub repository

2. **Configure**
   - Set Python buildpack
   - Set run command: `gunicorn journal_project.wsgi:application`
   - Add PostgreSQL database
   - Set environment variables

3. **Deploy**
   - Click "Deploy"
   - Monitor logs

### Droplet (Traditional)

Similar to AWS deployment above. Follow the same steps for EC2 but use `root` user for DigitalOcean Droplets.

---

## Post-Deployment

### Verify Deployment

```bash
# Check health endpoint
curl https://your-domain.com/health/

# Check admin panel
https://your-domain.com/admin/
```

### Configure Domain

1. Update your domain's DNS records to point to your server
2. Update ALLOWED_HOSTS in environment variables
3. Set up SSL/HTTPS (automated with Heroku, use Let's Encrypt for others)

### Setup Monitoring

1. **Enable Sentry for error tracking**
   ```bash
   heroku config:set SENTRY_DSN=https://your-sentry-key@sentry.io/project
   ```

2. **Enable logging**
   - Check application logs: `docker-compose logs` or `heroku logs`

3. **Setup backups**
   - Heroku: Automatic daily backups
   - AWS/DigitalOcean: Configure automated snapshots

### Schedule Tasks

For background tasks like email reminders:

```bash
# Heroku
heroku ps:type worker=free
heroku run:detached celery -A journal_project worker

# Docker
# Services are configured in docker-compose.yml
```

### Performance Optimization

1. **Enable caching**
   - Redis: Set REDIS_URL environment variable
   - Update CACHES setting in settings.py

2. **Optimize database**
   - Create indexes on frequently queried fields
   - Use `select_related()` and `prefetch_related()`

3. **CDN for static files**
   - AWS CloudFront
   - Cloudflare

---

## Troubleshooting

### Database Connection Error
```bash
# Check DATABASE_URL is set correctly
heroku config:get DATABASE_URL
# or
docker-compose exec db psql -U journal_user -d journal_prod
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
# Ensure STATIC_ROOT and STATIC_URL are configured
```

### 502 Bad Gateway
```bash
# Check application logs
heroku logs --tail
docker-compose logs web

# Restart services
heroku restart
docker-compose restart web
```

### Permission Denied
```bash
# Make sure files have correct permissions
chmod -R 755 /path/to/project
```

---

## Support

For issues, check:
- Django documentation: https://docs.djangoproject.com
- Heroku documentation: https://devcenter.heroku.com
- Docker documentation: https://docs.docker.com
- Project issues: Check PRODUCTION_DEPLOYMENT.md

---

**Status: Ready for Production ✅**
