# Branding & Customization Guide

Complete guide to customize the Journal Desk application with your own branding.

## Quick Customization Checklist

- [ ] Change app name
- [ ] Update logo and favicon
- [ ] Customize colors
- [ ] Update descriptions
- [ ] Configure email templates
- [ ] Set up social links
- [ ] Customize fonts
- [ ] Update footer information

## 1. App Name & Descriptions

### Change App Name

Edit `journal/templates/base.html`:
```html
<!-- Find line ~15 -->
<a class="navbar-brand" href="{% url 'entry_list' %}">
    <i class="fas fa-journal-whills"></i> Journal Desk
    <!-- Change to: -->
    <i class="fas fa-journal-whills"></i> Your App Name
</a>
```

Edit `journal/templates/journal/dashboard.html`:
```html
<h1>Welcome to Your App Name</h1>
```

Edit `journal_project/settings.py`:
```python
# Find and update
PROJECT_NAME = "Your App Name"
PROJECT_DESCRIPTION = "Your description here"
PROJECT_VERSION = "2.0"
```

Edit Browser Title in `journal/templates/base.html`:
```html
<title>{% block title %}Your App Name | Your Tagline{% endblock %}</title>
```

### Update Meta Descriptions

Edit `journal/templates/base.html`:
```html
<meta name="description" content="Your description goes here">
<meta name="keywords" content="journaling, diary, notes, personal">
<meta name="theme-color" content="#57c1ff">
```

## 2. Logo & Favicon

### Replace Favicon

```bash
# Option 1: Use existing favicon
# Place your favicon.ico in:
# journal/static/journal/images/favicon.ico

# Option 2: Generate favicon with icon
# Using Font Awesome icon in settings.py
```

Update favicon in `journal/templates/base.html`:
```html
<link rel="icon" type="image/svg+xml" href="{% static 'journal/images/favicon.svg' %}">
<!-- or -->
<link rel="icon" type="image/ico" href="{% static 'journal/images/favicon.ico' %}">
```

### Add Logo to Navbar

Create `journal/static/journal/images/logo.png`

Edit `journal/templates/base.html`:
```html
<a class="navbar-brand" href="{% url 'entry_list' %}">
    <img src="{% static 'journal/images/logo.png' %}" alt="Logo" height="40">
    Your App Name
</a>
```

Or use Font Awesome:
```html
<i class="fas fa-book-open"></i>  <!-- Change icon -->
<i class="fas fa-pen-fancy"></i>
<i class="fas fa-feather-alt"></i>
<i class="fas fa-star"></i>
```

## 3. Color Customization

### Primary Colors

Edit `journal/static/journal/css/style.css`:

```css
:root {
  /* Main brand colors */
  --primary-blue: #57c1ff;      /* Change this to your primary color */
  --accent-blue: #258dff;       /* Darker shade for hover */
  --dark-bg: #0a1830;           /* Dark mode background */
  --light-bg: #f8fbff;          /* Light mode background */
  
  /* Semantic colors */
  --success: #10b981;           /* Green - success, online */
  --warning: #fbbf24;           /* Orange - warnings, alerts */
  --danger: #ef4444;            /* Red - errors, overdue */
  --info: #3b82f6;              /* Blue - information */
  
  /* Typography */
  --text-light: #f8fbff;        /* Light text on dark */
  --text-dark: #0a1830;         /* Dark text on light */
  --text-soft: #d5dce7;         /* Secondary text */
  --text-muted: #8892aa;        /* Tertiary text */
}

[data-theme="light"] {
  --text-light: #0a1830;
  --text-dark: #f8fbff;
  --bg-primary: #f8fbff;
  --bg-secondary: #e8eef6;
}

[data-theme="dark"] {
  --text-light: #f8fbff;
  --text-dark: #0a1830;
  --bg-primary: #0a1830;
  --bg-secondary: #0f172a;
}
```

### Quick Color Changes

Find these in `style.css` and customize:

```css
/* Replace primary color throughout */
find: #57c1ff
replace-with: your_primary_color

/* Replace accent color */
find: #258dff
replace-with: your_accent_color

/* Replace dark background */
find: #0a1830
replace-with: your_dark_color

/* Replace light background */
find: #f8fbff
replace-with: your_light_color
```

### Example: Blue → Purple Theme

```bash
# Original
--primary-blue: #57c1ff;      (Cyan)
--accent-blue: #258dff;       (Darker cyan)
--success: #10b981;           (Green)

# Change to Purple
--primary-blue: #a855f7;      (Purple)
--accent-blue: #9333ea;       (Darker purple)
--success: #8b5cf6;           (Lighter purple)
```

## 4. Fonts & Typography

### Change Font Family

Edit `journal/static/journal/css/style.css`:

```css
:root {
  /* Current font */
  --font-primary: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  
  /* Change to your preference */
  --font-primary: 'Inter', 'Helvetica Neue', sans-serif;
  /* or */
  --font-primary: 'Poppins', sans-serif;
  /* or */
  --font-primary: 'Raleway', sans-serif;
}

body {
  font-family: var(--font-primary);
}
```

### Add Google Fonts

Edit `journal/templates/base.html`:

```html
<head>
  <!-- Add Google Fonts link -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
  
  <!-- Your CSS -->
  <link rel="stylesheet" href="{% static 'journal/css/style.css' %}">
</head>
```

### Customize Font Sizes

```css
/* Headings */
h1 { font-size: 2.5rem; }      /* Change size */
h2 { font-size: 2rem; }
h3 { font-size: 1.5rem; }
h4 { font-size: 1.25rem; }

/* Body text */
p { font-size: 1rem; }
small { font-size: 0.875rem; }
```

## 5. Footer Customization

### Update Footer Links

Edit `journal/templates/base.html`, find footer section:

```html
<footer class="footer mt-5">
    <div class="container">
        <div class="row mb-4">
            <div class="col-md-4">
                <h6>Your Company Name</h6>
                <p class="text-muted">Your tagline or mission statement</p>
            </div>
            <div class="col-md-4">
                <h6>Quick Links</h6>
                <ul class="list-unstyled">
                    <li><a href="{% url 'help_page' %}">Help & FAQ</a></li>
                    <li><a href="/privacy/">Privacy Policy</a></li>
                    <li><a href="/terms/">Terms of Service</a></li>
                    <li><a href="/contact/">Contact Us</a></li>
                </ul>
            </div>
            <div class="col-md-4">
                <h6>Connect</h6>
                <div class="gap-2 d-flex">
                    <a href="https://twitter.com/yourhandle" title="Twitter">
                        <i class="fab fa-twitter"></i>
                    </a>
                    <a href="https://github.com/yourusername" title="GitHub">
                        <i class="fab fa-github"></i>
                    </a>
                    <a href="mailto:contact@example.com" title="Email">
                        <i class="fas fa-envelope"></i>
                    </a>
                </div>
            </div>
        </div>
        <hr>
        <div class="text-center text-muted">
            <p>&copy; 2026 Your Company. All rights reserved. Made with 
                <i class="fas fa-heart text-danger"></i> for thoughtful journaling.
            </p>
        </div>
    </div>
</footer>
```

## 6. Email Templates

### Create Email Templates

Create directory:
```bash
mkdir -p journal/templates/emails
```

### Email Reminder Template

Create `journal/templates/emails/reminder.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .container { max-width: 600px; margin: 0 auto; }
        .header { background-color: #57c1ff; color: white; padding: 20px; }
        .content { padding: 20px; background-color: #f9f9f9; }
        .footer { text-align: center; padding: 10px; color: #999; font-size: 12px; }
        .btn { display: inline-block; background-color: #57c1ff; color: white; 
               padding: 10px 20px; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📝 Journal Reminder</h1>
        </div>
        <div class="content">
            <p>Hi {{ user.first_name|default:user.username }},</p>
            <p>You have an upcoming task reminder:</p>
            <div style="background-color: white; padding: 15px; border-left: 4px solid #57c1ff;">
                <h3>{{ task_title }}</h3>
                <p><strong>Due:</strong> {{ due_date }}</p>
                <p><strong>Entry:</strong> {{ entry_title }}</p>
            </div>
            <p style="text-align: center; margin-top: 20px;">
                <a href="{{APP_URL}}/entries/" class="btn">View Entries</a>
            </p>
        </div>
        <div class="footer">
            <p>This is a reminder from Journal Desk. 
               <a href="{{APP_URL}}/preferences/">Update preferences</a></p>
        </div>
    </div>
</body>
</html>
```

### Override Email in Views

Edit `journal/views.py`:

```python
from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_reminder_email(reminder):
    subject = f"Reminder: {reminder.entry.task}"
    
    # Render HTML template
    from django.conf import settings
    html_message = render_to_string('emails/reminder.html', {
        'user': reminder.user,
        'task_title': reminder.entry.task,
        'due_date': reminder.reminder_time.strftime("%B %d, %Y at %I:%M %p"),
        'entry_title': reminder.entry.title,
        'APP_URL': settings.SITE_URL,
    })
    
    send_mail(
        subject,
        'You have a reminder pending',  # Plain text fallback
        'noreply@journaldesk.com',
        [reminder.user.email],
        html_message=html_message,
    )
```

## 7. Navigation Menu

### Customize Menu Items

Edit `journal/templates/base.html`:

```html
<div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav ms-auto">
        <!-- Add or remove menu items here -->
        <li class="nav-item">
            <a class="nav-link" href="{% url 'entry_list' %}">
                <i class="fas fa-book"></i> My Entries
            </a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="{% url 'analytics' %}">
                <i class="fas fa-chart-bar"></i> Analytics
            </a>
        </li>
        <!-- Add custom menu items -->
        <li class="nav-item">
            <a class="nav-link" href="/blog/">
                <i class="fas fa-blog"></i> Blog
            </a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="/community/">
                <i class="fas fa-users"></i> Community
            </a>
        </li>
    </ul>
</div>
```

## 8. Dashboard Customization

### Update Dashboard Message

Edit `journal/templates/journal/dashboard.html`:

```html
<!-- Welcome section -->
<div class="welcome-section">
    <h1>Welcome back, {{ user.first_name|default:user.username }}! 👋</h1>
    <p>You're doing amazing! Check your progress below.</p>
    <!-- Customize these stats -->
    <div class="stats-grid">
        <div class="stat-card">
            <h3>{{ total_entries }}</h3>
            <p>Entries Written</p>
        </div>
        <div class="stat-card">
            <h3>{{ this_week_entries }}</h3>
            <p>This Week</p>
        </div>
        <div class="stat-card">
            <h3>{{ pending_tasks }}</h3>
            <p>Pending Tasks</p>
        </div>
    </div>
</div>
```

## 9. Settings Configuration

### Update Django Settings

Edit `journal_project/settings.py`:

```python
# Company/App Information
APP_NAME = "Your Journal App Name"
APP_DESCRIPTION = "Your description"
COMPANY_NAME = "Your Company"
COMPANY_EMAIL = "support@yourcompany.com"
COMPANY_WEBSITE = "https://yourcompany.com"
COMPANY_PHONE = "+1-234-567-8900"

# Contact Information
CONTACT_EMAIL = "contact@example.com"
SUPPORT_URL = "https://support.example.com"

# Social Links
TWITTER_URL = "https://twitter.com/yourhandle"
GITHUB_URL = "https://github.com/yourhandle"
FACEBOOK_URL = "https://facebook.com/yourpage"
LINKEDIN_URL = "https://linkedin.com/company/yourcompany"

# Features
FEATURES = {
    'voice_entry': True,
    'collaboration': True,
    'cloud_backup': True,
    'social_sharing': True,
    'calendar_sync': True,
    'advanced_analytics': True,
}

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # or your email provider
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'noreply@yourcompany.com'

# Site Information
SITE_ID = 1
SITE_NAME = "Your App Name"
SITE_URL = "https://yourapp.com"
```

## 10. Create Custom Pages

### Add About Page

1. Create `journal/templates/journal/about_custom.html`
2. Add view in `journal/views.py`
3. Add URL in `journal/urls.py`

Example:

```python
# views.py
@login_required
def about_page(request):
    context = {
        'title': 'About Us',
        'description': 'Your custom about page content',
    }
    return render(request, 'journal/about_custom.html', context)

# urls.py
path('about-us/', views.about_page, name='about_custom'),
```

## 11. Deployment Branding

### Update Settings for Production

```python
# settings.py

# SECURITY
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
DEBUG = False
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Static Files CDN
STATIC_URL = 'https://cdn.yourdomain.com/static/'
MEDIA_URL = 'https://cdn.yourdomain.com/media/'

# Email
DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com'
```

## 12. Testing Branding Changes

### Preview Changes Locally

1. Update files as above
2. Run server: `python manage.py runserver`
3. Visit: `http://localhost:8000`
4. Check:
   - [ ] Logo displays
   - [ ] Colors correct
   - [ ] Footer updated
   - [ ] Menu items correct
   - [ ] Emails formatted properly

### Mobile Preview

Browser DevTools (F12):
- Click device toggle (mobile icon)
- Select device (iPhone, Android, etc.)
- Preview responsive design with branding

## Deployment Checklist

Before deploying with custom branding:

- [ ] All color hex codes match brand guidelines
- [ ] Logo files optimized for web
- [ ] Favicon displays correctly
- [ ] Footer links work
- [ ] Email templates formatted
- [ ] Social links correct
- [ ] Performance tested
- [ ] Cross-browser tested
- [ ] Mobile responsive verified
- [ ] Accessibility checked

## Resources

- **Color Picker**: https://colorpicker.com
- **Google Fonts**: https://fonts.google.com
- **Icon Library**: https://fontawesome.com
- **Logo Generator**: https://looka.com
- **Email Template**: https://mjml.io

---

**Last Updated:** April 11, 2026
**Status:** Ready for Customization
