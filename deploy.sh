#!/bin/bash
# Heroku Deployment Script for Journal Desk
# This script automates the deployment process to Heroku

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Journal Desk Heroku Deployment ===${NC}"

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo -e "${RED}Heroku CLI not found. Please install it from https://devcenter.heroku.com/articles/heroku-cli${NC}"
    exit 1
fi

# Check if git is initialized
if [ ! -d .git ]; then
    echo -e "${YELLOW}Initializing git repository...${NC}"
    git init
    git config user.email "dev@journaldesk.io"
    git config user.name "Journal Desk"
fi

# Create app name
APP_NAME="${1:-journal-desk-$(date +%s)}"

echo -e "${YELLOW}Creating Heroku app: $APP_NAME${NC}"
heroku create $APP_NAME

echo -e "${YELLOW}Adding PostgreSQL database...${NC}"
heroku addons:create heroku-postgresql:hobby-dev -a $APP_NAME

echo -e "${YELLOW}Setting environment variables...${NC}"
heroku config:set DJANGO_DEBUG=False -a $APP_NAME
heroku config:set DJANGO_SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())') -a $APP_NAME
heroku config:set DJANGO_ALLOWED_HOSTS="$APP_NAME.herokuapp.com" -a $APP_NAME
heroku config:set TASK_ALERTS_EMAIL_ENABLED=False -a $APP_NAME

echo -e "${YELLOW}Deploying application...${NC}"
git push heroku master

echo -e "${YELLOW}Running migrations...${NC}"
heroku run python manage.py migrate -a $APP_NAME

echo -e "${YELLOW}Collecting static files...${NC}"
heroku run python manage.py collectstatic --noinput -a $APP_NAME

echo -e "${GREEN}✓ Deployment complete!${NC}"
echo -e "${GREEN}Your app is live at: https://$APP_NAME.herokuapp.com${NC}"
echo -e "${YELLOW}Create a superuser with: heroku run python manage.py createsuperuser -a $APP_NAME${NC}"
