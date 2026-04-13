# HEROKU DEPLOYMENT QUICK START

## Prerequisites
- Heroku account (free at heroku.com)
- Heroku CLI installed
- Git repository initialized

## Step 1: Login to Heroku
```bash
heroku login
```

## Step 2: Create Heroku App
```bash
heroku create journal-desk-yourname
# Choose app name carefully - will be yourdomain.heroku.com
```

## Step 3: Add PostgreSQL Database
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

## Step 4: Set Environment Variables
```bash
heroku config:set SECRET_KEY="your-secret-key-here"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="journal-desk-yourname.herokuapp.com"
```

## Step 5: Deploy
```bash
git add .
git commit -m "Prepare for production deployment"
git push heroku main
```

## Step 6: Run Migrations
```bash
heroku run python manage.py migrate
```

## Step 7: Create Superuser
```bash
heroku run python manage.py createsuperuser
```

## Step 8: Open App
```bash
heroku open
```

## View Logs
```bash
heroku logs --tail
```

---

## QUICK DEPLOYMENT (Copy-Paste)

```bash
# 1. Initialize git (if not done)
cd /home/jayden/Desktop/now
git init
git add .
git commit -m "Initial commit - Journal Desk"

# 2. Create Heroku app
heroku create journal-desk-app
heroku addons:create heroku-postgresql:hobby-dev

# 3. Set config
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')

# 4. Deploy
git push heroku main

# 5. Run migrations
heroku run python manage.py migrate

# 6. Open app
heroku open
```

---

**Status:** Ready to deploy to https://journal-desk-yourname.herokuapp.com
