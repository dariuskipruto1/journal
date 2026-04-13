# Testing Guide - Journal Desk Application

Comprehensive testing guide for all features of the Journal Desk application.

## Quick Test Setup

### 1. Start the Server
```bash
cd /home/jayden/Desktop/now
python manage.py runserver 0.0.0.0:8000
```

### 2. Access the App
- Navigate to: `http://localhost:8000`
- You should see login page

### 3. Create Test Account
```bash
python manage.py createsuperuser
# OR access /admin and create account manually
```

Or use quick create:
```bash
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> User.objects.create_user('testuser', 'test@example.com', 'password123')
```

## Feature Testing Checklist

### ✅ Core Features (Foundation)

#### Entry Management (`/entries/`)
- [ ] Create new entry
  - [ ] Add title
  - [ ] Add content
  - [ ] Select category
  - [ ] Add tags
  - [ ] Save entry
- [ ] View all entries
  - [ ] Entries display in list
  - [ ] Sorting works (newest/oldest)
  - [ ] Filter by category
  - [ ] Filter by status
- [ ] Edit entry
  - [ ] Open entry
  - [ ] Modify content
  - [ ] Save changes
  - [ ] Verify update
- [ ] Delete entry
  - [ ] Confirm deletion dialog
  - [ ] Entry removed from list
- [ ] Star/favorite
  - [ ] Click star icon
  - [ ] Entry marked as favorite
  - [ ] Filter by starred works

#### Task Management (`/tasks/`)
- [ ] Create task in entry
  - [ ] Set task title
  - [ ] Set priority (Low/Medium/High)
  - [ ] Set due date/time
  - [ ] Save task
- [ ] View tasks
  - [ ] Tasks display
  - [ ] Sort by due date
  - [ ] Filter by status
- [ ] Mark task complete
  - [ ] Toggle completion
  - [ ] Status updates
- [ ] Overdue indication
  - [ ] Red color for overdue
  - [ ] Correct date shown

#### Analytics (`/analytics/`)
- [ ] View dashboard
  - [ ] Charts render
  - [ ] Statistics display
  - [ ] Data is correct
- [ ] Entry statistics
  - [ ] Total count
  - [ ] Date range stats
  - [ ] Category breakdown
- [ ] Task statistics
  - [ ] Completion rate
  - [ ] Priority breakdown

#### Mood Tracker (`/mood/`)
- [ ] Record mood
  - [ ] Select emoji
  - [ ] Choose mood level
  - [ ] Save mood
- [ ] View mood history
  - [ ] Past moods display
  - [ ] Dates show correctly
- [ ] Mood trends
  - [ ] Chart renders
  - [ ] Shows trend over time

### 🚀 New Features (v2.0)

#### Dark/Light Mode (`/preferences/`)
- [ ] Access preferences
  - [ ] Click Settings menu
  - [ ] Go to Preferences
- [ ] Toggle theme
  - [ ] Click Light Mode button
  - [ ] All pages change to light
  - [ ] Click Dark Mode button
  - [ ] All pages change to dark
- [ ] Persistence
  - [ ] Refresh page
  - [ ] Theme remains selected
  - [ ] Open in new tab
  - [ ] Theme persists
- [ ] Smooth transitions
  - [ ] No jarring changes
  - [ ] Colors transition smoothly

#### Email Reminders (`/email-reminders/`)
- [ ] Access feature
  - [ ] Click Features menu
  - [ ] Select Email Reminders
- [ ] Create reminder
  - [ ] Select entry/task
  - [ ] Choose frequency (Once/Daily/Weekly/Monthly)
  - [ ] Set time
  - [ ] Save reminder
- [ ] View reminders
  - [ ] List displays
  - [ ] All reminders shown
- [ ] Manage reminders
  - [ ] Enable/disable toggle works
  - [ ] Delete reminder works
  - [ ] Status updates instantly

#### Notifications (`/notifications/`)
- [ ] Access notifications
  - [ ] Click Features menu
  - [ ] Select Notifications
- [ ] View notifications
  - [ ] List displays
  - [ ] Icons show correct type
  - [ ] Timestamps display
- [ ] Mark as read
  - [ ] Click notification
  - [ ] Mark as read toggles
  - [ ] Styling updates
- [ ] Clear notifications
  - [ ] Click "Mark All Read"
  - [ ] All marked as read
  - [ ] Click "Clear All"
  - [ ] All notifications removed

#### Voice Entry (`/voice-entry/`)
- [ ] Access voice entry
  - [ ] Click Features menu
  - [ ] Select Voice Entry
- [ ] Record voice
  - [ ] Click "Start Recording"
  - [ ] Browser requests microphone
  - [ ] Grant permission
  - [ ] Recording indicator shows
  - [ ] Timer counts
- [ ] Waveform visualization
  - [ ] Waveform appears
  - [ ] Updates as you speak
- [ ] Stop recording
  - [ ] Click "Stop Recording"
  - [ ] Waveform stops updating
  - [ ] Save button appears
- [ ] Transcription
  - [ ] Processing message shows
  - [ ] Transcribed text appears
  - [ ] Confidence score shows
- [ ] Playback
  - [ ] Click play button
  - [ ] Audio plays
  - [ ] Waveform progresses
- [ ] Language support
  - [ ] Change language dropdown
  - [ ] Record again
  - [ ] Different language transcribes

#### Collaboration (`/collaboration/`)
- [ ] Access collaboration
  - [ ] Click Features menu
  - [ ] Select Collaboration
- [ ] Create team entry
  - [ ] Click "Create Collaborative Entry"
  - [ ] Add title
  - [ ] Add content
  - [ ] Save entry
- [ ] View team entries
  - [ ] List displays
  - [ ] Creator shown
  - [ ] Member count shows
- [ ] Add comment
  - [ ] Click entry
  - [ ] Add comment
  - [ ] Comment appears
  - [ ] Timestamp shows
- [ ] Real-time updates
  - [ ] Member joins
  - [ ] Updates appear (if multi-user test)

#### Cloud Backup (`/cloud-backup/`)
- [ ] Access backup
  - [ ] Click Features menu
  - [ ] Select Cloud Backup
- [ ] Create backup
  - [ ] Click "Create Backup Now"
  - [ ] Backup starts
  - [ ] Status updates
  - [ ] Completion message
- [ ] View backups
  - [ ] List displays
  - [ ] Status shows
  - [ ] Size shows
  - [ ] Date shows
- [ ] Backup settings
  - [ ] Select provider (S3/GCS/Local)
  - [ ] Enable auto-backup
  - [ ] Set schedule
- [ ] Restore backup
  - [ ] Select completed backup
  - [ ] Click "Restore"
  - [ ] Confirm dialog
  - [ ] Process completes

#### Social Sharing (`/social-sharing/`)
- [ ] Access social sharing
  - [ ] Click Features menu
  - [ ] Select Social Sharing
- [ ] Connect platforms
  - [ ] Click Twitter Connect
  - [ ] Authorize (or show auth flow)
  - [ ] Repeat for LinkedIn, Facebook
- [ ] Share entry
  - [ ] Select entry
  - [ ] Choose platform
  - [ ] Click Share
  - [ ] Success message
- [ ] View shared entries
  - [ ] List displays
  - [ ] Platform shows
  - [ ] Share date shows
- [ ] Manage shares
  - [ ] Click Share URL icon
  - [ ] Copy link button works
  - [ ] Click Unshare
  - [ ] Share removed

#### Calendar Integration (`/calendar-integration/`)
- [ ] Access calendar
  - [ ] Click Features menu
  - [ ] Select Calendar Integration
- [ ] Connect calendar
  - [ ] Choose provider (Google/Outlook/iCalendar)
  - [ ] Click Connect
  - [ ] Authorization flow
  - [ ] Connected message
- [ ] Sync settings
  - [ ] Toggle one-way/two-way
  - [ ] Enable/disable sync
  - [ ] Settings save
- [ ] Sync now
  - [ ] Click "Sync Now"
  - [ ] Status updates
  - [ ] Completion message
- [ ] Verify sync
  - [ ] Open Google Calendar
  - [ ] Entries with due dates appear as events
  - [ ] Titles match

#### Advanced Analytics (`/advanced-analytics/`)
- [ ] Access analytics
  - [ ] Click Features menu
  - [ ] Select Advanced Analytics
- [ ] View stats
  - [ ] Total entries displays
  - [ ] Total words displays
  - [ ] Average shown
  - [ ] Longest streak shown
- [ ] Mood distribution
  - [ ] Chart renders
  - [ ] Correct moods shown
  - [ ] Percentages calculate
- [ ] Writing insights
  - [ ] Peak hour shows
  - [ ] Peak day shows
  - [ ] Avg words/entry shows
- [ ] Productivity metrics
  - [ ] Task completion rate shows
  - [ ] Average days to complete
  - [ ] Current streak shown

### 🎨 UI/UX Features

#### Responsive Design
- [ ] Desktop view
  - [ ] Sidebar shows
  - [ ] Content displays properly
  - [ ] All elements visible
- [ ] Tablet view
  - [ ] Resize to tablet size
  - [ ] Layout adapts
  - [ ] Navigation accessible
  - [ ] Content readable
- [ ] Mobile view
  - [ ] Resize to mobile size
  - [ ] Hamburger menu appears
  - [ ] Touch friendly buttons
  - [ ] No horizontal scroll

#### Navigation
- [ ] Main menu
  - [ ] Entries link works
  - [ ] Tasks link works
  - [ ] Analytics link works
  - [ ] All links navigate
- [ ] Features dropdown
  - [ ] Dropdown opens
  - [ ] All items show
  - [ ] Items clickable
  - [ ] Correct pages load
- [ ] Breadcrumb navigation
  - [ ] Shows current path
  - [ ] Links work

#### Loading States
- [ ] Loading spinners
  - [ ] Show during load
  - [ ] Disappear when done
- [ ] Optimistic updates
  - [ ] Changes appear immediately
  - [ ] Confirmed after save
- [ ] Error messages
  - [ ] Display on error
  - [ ] Clear messaging
  - [ ] Dismiss button works

#### Animations
- [ ] Page transitions
  - [ ] Smooth fade in
  - [ ] No jarring changes
- [ ] Button hover
  - [ ] Color change
  - [ ] Scale effect
  - [ ] Shadow effect
- [ ] Card animations
  - [ ] Hover lift
  - [ ] Smooth glow

### 🔒 Security Testing

#### Authentication
- [ ] Login required
  - [ ] Redirect to login when not authenticated
  - [ ] Can't access /entries without login
  - [ ] Can't access /tasks without login
- [ ] Session management
  - [ ] Logout works
  - [ ] Session cleared
  - [ ] Login required again
- [ ] Password
  - [ ] Hashed in database
  - [ ] Can login with correct password
  - [ ] Can't login with wrong password

#### Authorization
- [ ] User isolation
  - [ ] User A can't see User B's entries
  - [ ] User B can't edit User A's entries
- [ ] CSRF protection
  - [ ] Forms have CSRF token
  - [ ] POST without token fails

#### Input Validation
- [ ] Entry creation
  - [ ] Empty title rejected
  - [ ] Empty content rejected
  - [ ] Special characters escaped
- [ ] Task creation
  - [ ] Invalid dates rejected
  - [ ] Priority validated
- [ ] Form sanitization
  - [ ] XSS attempts prevented
  - [ ] HTML injection prevented

### ⚡ Performance Testing

#### Page Load
- [ ] Dashboard
  - [ ] Loads in < 1 second
  - [ ] All data displays
- [ ] Entries list
  - [ ] Loads in < 1 second
  - [ ] Infinite scroll works
- [ ] Analytics
  - [ ] Charts render < 2 seconds
  - [ ] No page freeze

#### API Response
- [ ] Create entry
  - [ ] Response in < 100ms
- [ ] List entries
  - [ ] Response in < 100ms
- [ ] Update entry
  - [ ] Response in < 100ms

#### Animation Performance
- [ ] 60fps target
  - [ ] Smooth page transitions
  - [ ] Fluid button hovers
  - [ ] No jank on scroll

### 📱 Cross-Browser Testing

- [ ] Chrome 90+
  - [ ] All features work
  - [ ] Responsive works
  - [ ] Animations smooth
- [ ] Firefox 88+
  - [ ] All features work
  - [ ] Responsive works
  - [ ] Animations smooth
- [ ] Safari 14+
  - [ ] All features work
  - [ ] Responsive works
  - [ ] Animations smooth
- [ ] Edge 90+
  - [ ] All features work
  - [ ] Responsive works
  - [ ] Animations smooth

## Automated Testing

### Run Tests

```bash
# All tests
python manage.py test

# Specific app
python manage.py test journal

# Specific test class
python manage.py test journal.tests.EntryViewTests

# With verbosity
python manage.py test -v 2

# With coverage
coverage run --source='journal' manage.py test
coverage report
coverage html  # Creates htmlcov/index.html
```

### Write Tests

Create `journal/tests.py`:

```python
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Entry

User = get_user_model()

class EntryTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'testuser',
            'test@example.com',
            'password123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='password123')

    def test_create_entry(self):
        response = self.client.post('/entries/', {
            'title': 'Test Entry',
            'content': 'Test content',
            'category': 'test'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(Entry.objects.filter(title='Test Entry').exists())

    def test_entry_isolation(self):
        # Create another user
        other_user = User.objects.create_user(
            'otheruser',
            'other@example.com',
            'password123'
        )
        # Create entry for first user
        entry = Entry.objects.create(
            user=self.user,
            title='Private Entry',
            content='Only for testuser'
        )
        # Login as other user
        self.client.logout()
        self.client.login(username='otheruser', password='password123')
        
        # Should not see other user's entry
        response = self.client.get(f'/entries/{entry.id}/')
        self.assertEqual(response.status_code, 403)
```

## Troubleshooting Tests

### Common Issues

**Tests fail with "ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

**Database locked during tests**
```bash
python manage.py testdb --create-db
```

**Tests hang**
```bash
# Increase timeout
python manage.py test --keepdb  # Reuse database
```

## Test Results Documentation

### Template Test Report

```
Test Run Date: April 11, 2026
Python Version: 3.14.3
Django Version: 6.0.3

RESULTS:
✅ Entry Management: 8/8 tests passed
✅ Task Management: 6/6 tests passed
✅ Analytics: 5/5 tests passed
✅ Mood Tracker: 4/4 tests passed
✅ Email Reminders: 5/5 tests passed
✅ Notifications: 5/5 tests passed
✅ Voice Entry: 6/6 tests passed
✅ Collaboration: 5/5 tests passed
✅ Cloud Backup: 5/5 tests passed
✅ Social Sharing: 5/5 tests passed
✅ Calendar Integration: 5/5 tests passed
✅ Advanced Analytics: 6/6 tests passed
✅ Theme Toggle: 3/3 tests passed

COVERAGE: 95.2%
PERFORMANCE: 100% (all < 100ms)
SECURITY: Passed all checks

NOTES:
- All features working as expected
- No errors or warnings
- Performance targets met
- Security measures verified
```

## Sign Off

Once all tests pass and features are verified:

```bash
# Generate test report
python manage.py test journal -v 2 > test_results.txt

# Coverage report
coverage report > coverage_results.txt
```

**Tested By:** _________________
**Date:** _________________
**Status:** ✅ Ready for Production / ❌ Issues Found
