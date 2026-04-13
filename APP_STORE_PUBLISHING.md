# App Store Publishing Guide

Complete guide to publish Journal Desk to all major app stores: Google Play Store, Apple App Store, Microsoft Store, and macOS App Store.

## Table of Contents

1. [Pre-Publishing Checklist](#pre-publishing-checklist)
2. [Google Play Store (Android)](#google-play-store-android)
3. [Apple App Store (iOS)](#apple-app-store-ios)
4. [Microsoft Store (Windows)](#microsoft-store-windows)
5. [macOS App Store](#macos-app-store)
6. [GitHub Releases (Desktop)](#github-releases-desktop)
7. [App Store Optimization](#app-store-optimization)
8. [Marketing & Launch](#marketing--launch)
9. [Post-Launch Maintenance](#post-launch-maintenance)

---

## Pre-Publishing Checklist

### Code Quality

- [ ] All tests pass
- [ ] No console errors
- [ ] Performance tested
- [ ] Works on minimum OS versions:
  - Android 8.0+
  - iOS 13.0+
  - Windows 10
  - macOS 10.13+

### App Store Compliance

- [ ] Privacy Policy created
- [ ] Terms of Service created
- [ ] GDPR compliance verified
- [ ] No restricted content
- [ ] Proper permissions declared
- [ ] Screenshots taken (at least 2, max 10)
- [ ] App description written (max 4000 chars)
- [ ] Keywords/tags identified (5-10)
- [ ] Support contact email set

### Assets

- [ ] High-res app icon (1024x1024px)
- [ ] Screenshots for each platform
- [ ] Feature graphic (1024x500px)
- [ ] App description
- [ ] Privacy policy
- [ ] Support info
- [ ] Company branding

### Accounts

- [ ] Google Play Developer account (~$25 lifetime)
- [ ] Apple Developer account (~$99/year)
- [ ] Microsoft Developer account (~$19/year)
- [ ] Company website/support URL

---

## Google Play Store (Android)

### Most Popular Android Store
**Market Share:** ~96% of Android users
**Fee:** $25 one-time registration
**Review Time:** ~2 hours
**Cost per App:** Free (commission on paid items)

### Step 1: Create Developer Account

```bash
1. Go to https://play.google.com/console
2. Click "Create account"
3. Enter Google account (or create new)
4. Accept terms
5. Pay $25 registration fee
6. Complete developer profile
```

### Step 2: Create Application

```bash
1. In Play Console, click "Create app"
2. Enter app name: "Journal Desk"
3. Select category: "Productivity"
4. Audience: Everyone (18+)
5. Click "Create app"
```

### Step 3: Prepare Signing Key

For React Native:

```bash
cd journal-mobile

# Generate keystore
keytool -genkey -v -keystore journal-release.keystore \
  -keyalg RSA -keysize 2048 \
  -validity 36500 -alias journal

# Store securely (backup this file!)
# Remember the password and key alias
```

Create `android/keystore.properties`:
```properties
MYAPP_RELEASE_STORE_FILE=journal-release.keystore
MYAPP_RELEASE_STORE_PASSWORD=your_password
MYAPP_RELEASE_KEY_ALIAS=journal
MYAPP_RELEASE_KEY_PASSWORD=your_password
```

### Step 4: Build Release APK

```bash
cd journal-mobile

# Build signed release APK
./gradlew assembleRelease

# Or build AAB (recommended for Play Store)
./gradlew bundleRelease

# Output: app/build/outputs/bundle/release/app-release.aab
```

### Step 5: Upload to Play Console

```bash
1. In Play Console, go to "Setup" > "App signing"
2. Choose Google Play App Signing (recommended)
3. Go to "Release management" > "Production"
4. Click "Create release"
5. Upload your AAB file
6. Review app info
7. Submit for review
```

### Step 6: Complete Store Listing

**Content Ratings:**

```bash
1. Go to "Setup" > "Content ratings"
2. Complete questionnaire:
   - Violence? No
   - Sexual content? No
   - Substance abuse? No
   - Profanity? No
   - Gambling? No
3. Get content rating
```

**Store Listing Details:**

```bash
1. Title: "Journal Desk - Daily Diary & Notes"
2. Short description (80 chars):
   "Private journal for thoughts, moods, tasks & voice entries"

3. Full description:
   "Journal Desk is your personal digital journal and diary 
    with advanced features:
    
    ✅ Daily entries with rich text and voice recording
    ✅ Mood tracking and analytics
    ✅ Task management and reminders
    ✅ Team collaboration
    ✅ Cloud backup and sync
    ✅ Dark mode
    ✅ Offline access
    ✅ End-to-end encryption
    
    Features:
    • Voice entries with transcription
    • Mood tracking dashboard
    • Task management system
    • Team collaboration
    • Cloud backup to Google Drive
    • Social media sharing
    • Calendar integration
    • Advanced analytics
    • Customizable themes
    • Privacy-first design
    
    Requirements:
    • Android 8.0+
    • 50MB storage"

4. Screenshots (5-8):
   - Dashboard
   - Create entry
   - Mood tracker
   - Voice entry
   - Analytics
   - Settings
   - Dark mode example

5. Feature graphic (1024x500px):
   - Show app name and main feature
   - Use branded colors
   - Include key feature

6. Icon (512x512px):
   - Must be square
   - No transparent areas
   - High contrast
```

### Step 7: Privacy Policy

```bash
1. Go to "Setup" > "Privacy policy"
2. Enter privacy policy URL
3. Example: https://yourdomain.com/privacy/
4. Must be accessible and in English
```

### Step 8: Submit for Review

```bash
1. Review all information
2. Check compliance:
   - [ ] No misleading content
   - [ ] Accurate descriptions
   - [ ] Rating appropriate
   - [ ] Screenshots match app
3. Click "Submit app for review"
4. Wait for approval (usually 2-4 hours)
5. Monitor email for status updates
```

---

## Apple App Store (iOS)

### Premium iOS Marketplace
**Market Share:** ~55% of mobile users
**Fee:** $99/year developer membership
**Review Time:** 24-48 hours
**Strictness:** More strict than Google

### Step 1: Apply for Developer Program

```bash
1. Go to https://developer.apple.com
2. Click "Enroll"
3. Sign in with Apple ID (create if needed)
4. Choose "Individual" or "Company"
5. Enter personal/company info
6. Agree to license agreement
7. Pay $99/year
8. Wait for approval (usually instant)
```

### Step 2: Create App ID

```bash
1. In Developer Account, go to "Identifiers"
2. Click "+"
3. Select "App IDs"
4. Explicit App ID
5. Name: "Journal Desk"
6. Bundle ID: "com.yourcompany.journal"
7. Capabilities: Push Notifications, CloudKit
8. Register
```

### Step 3: Create Certificates

```bash
# Generate Certificate Signing Request (CSR)
1. Open Keychain Access on Mac
2. Keychain Access > Certificate Assistant > Request a Certificate
3. Email: your-email@company.com
4. Common Name: Your Name/Company
5. Save to disk

# In Apple Developer Account:
1. Go to "Certificates"
2. Click "+"
3. Select "App Development"
4. Upload your CSR
5. Download certificate (.cer)
6. Open to install in Keychain
```

### Step 4: Create Provisioning Profile

```bash
1. In Developer Account, go to "Profiles"
2. Click "+"
3. Select "iOS App Development"  (or "App Store")
4. Select your App ID
5. Select your Certificate
6. Download profile
7. Open to install
```

### Step 5: Build for iOS

Using Xcode and React Native:

```bash
cd journal-mobile

# Install pods
cd ios && pod install && cd ..

# Build using Xcode
xcode-select --install  # If needed

# Build archive
xcodebuild -workspace ios/JournalDesk.xcworkspace \
  -scheme JournalDesk \
  -configuration Release \
  -archivePath build/JournalDesk.xcarchive \
  archive

# Export IPA
xcodebuild -exportArchive \
  -archivePath build/JournalDesk.xcarchive \
  -exportOptionsPlist ios/exportOptions.plist \
  -exportPath build/
```

Or use Fastlane (easier):

```bash
# Install fastlane
sudo gem install fastlane

# Initialize fastlane
cd ios
fastlane init

# Configure for App Store
fastlane match appstore --type appstore

# Build and upload
fastlane ios release
```

### Step 6: Create App Store Record

```bash
1. Go to App Store Connect: https://appstoreconnect.apple.com
2. Click "My Apps"
3. Click "+"
4. New App
5. Select platform: iOS
6. Name: "Journal Desk"
7. Primary language: English
8. Bundle ID: Select your App ID
9. SKU: journal-desk-ios (any unique ID)
```

### Step 7: Fill App Information

**General Information:**
```
Name: Journal Desk
Subtitle: Your Personal Digital Journal

Description:
Journal Desk is your private, secure digital journal for 
daily reflections, mood tracking, and personal growth.

Key Version Release Notes:
• Complete redesign with modern interface
• Voice entry with transcription
• Mood analytics and insights
• Team collaboration features
• Cloud backup and sync
• Dark mode support
• Performance improvements
```

**Privacy Policy:**
```bash
1. Go to "App Privacy"
2. Select category: "Health & Fitness"
3. List data collected:
   - User ID
   - Device ID
   - Entries and notes
   - Mood data
4. Data sharing: No third parties
5. Tracking: None
```

**Pricing & Availability:**
```bash
1. Tier: Free (0)
2. Territories: Select all or specific countries
3. Date: Immediate or future date
4. Effective price: Free
```

**Screenshots (2-5 per device):**

For iPhone 6.5":
1. Dashboard (showing key features)
2. Create entry (showing rich editor)
3. Mood tracker (showing analytics)
4. Voice entry (showing recording UI)
5. Settings (showing personalization)

Screenshots must:
- Be 1242x2688px (6.5" screenshots)
- Show actual app UI
- Include marketing text overlay
- Be in order of most important features
- Target your audience

**Preview Video (Optional):**
- 15-30 seconds
- Show key features
- Include voiceover or music
- 1242x2688px minimum

### Step 8: App Review Information

```bash
1. Contact Information:
   - First name: Your name
   - Email: support@yourdomain.com
   - Phone: +1-234-567-8900

2. Demo Account:
   - Username: demo@example.com
   - Password: DemoPassword123
   (Must be accessible during review)

3. Sign-In Required:
   - Yes - if login needed for core features

4. Notes for Reviewers:
   "Journal Desk is a personal journaling app with end-to-end 
    encryption. To test, use the provided demo account. 
    Voice entry requires microphone permission. Thanks!"

5. Content Rights:
   - Is the app content owned by you? Yes
   - Third-party content: None
   - Export/screening: None needed
```

### Step 9: Build Version

```bash
1. Build Information:
   - Build: 1.0 from Xcode
   - Testers: Internal and external

2. Testing Information:
   - Device to test on: iPhone/iPad
   - Include TestFlight reviewer notes

3. Review Notes:
   "This is our first release. To demonstrate features:
    1. Sign in with demo account
    2. Create an entry with text
    3. Try voice entry (tap microphone)
    4. Check mood tracker
    5. View analytics dashboard"
```

### Step 10: Submit for Review

```bash
1. Review all information
2. Check compliance:
   - Must run on iOS 13 or later
   - No ads for other apps
   - Works as described
   - Follows App Store Review Guidelines
3. Click "Submit for Review"
4. Wait for status updates
5. Monitor email for approval
```

---

## Microsoft Store (Windows)

### Windows Desktop Distribution
**Market Share:** ~78% of Windows users
**Fee:** $19 one-time (or free)
**Review Time:** ~24 hours
**For:** Electron desktop app

### Step 1: Create Developer Account

```bash
1. Go to https://partner.microsoft.com/dashboard
2. Sign in with Microsoft account
3. Select "Windows & Xbox" 
4. Register as app developer
5. Pay $19 fee (waived for some)
6. Complete profile
```

### Step 2: Reserve App Name

```bash
1. In Partner Center, click "Create a new app"
2. Click "Reserve a new name"
3. Enter: "Journal Desk"
4. Click "Reserve app name"
```

### Step 3: Add Product Information

**Basic Info:**
```
App name: Journal Desk
Description:
  Journal Desk is your personal digital journal with:
  ✓ Rich text entries
  ✓ Voice recording
  ✓ Mood tracking
  ✓ Task management
  ✓ Cloud sync
  ✓ Dark mode
  
Category: Productivity
Subcategory: Organizational

URL: https://journaldesk.com
Support email: support@journaldesk.com
```

### Step 4: Prepare MSIX Package

For Electron:

```bash
cd journal-desktop

# Install electron-builder
npm install --save-dev electron-builder

# In package.json:
{
  "build": {
    "appId": "com.journaldesk.app",
    "productName": "Journal Desk",
    "win": {
      "target": ["msix"],
      "certificateFile": "cert.pfx",
      "certificatePassword": "your_password"
    }
  }
}

# Build
npm run build

# Output: dist/Journal Desk Setup 1.0.0.msix
```

### Step 5: Upload Package

```bash
1. In Partner Center, go to "Packages"
2. Click "Upload package"
3. Drag/drop MSIX file
4. Wait for certification
5. Monitor processing
```

### Step 6: Store Listing

**Description:** (Shown in Store)
```
The Journal Desk application provides a personal journaling 
platform with end-to-end encryption, offline access, and 
synchronization across devices.
```

**Screenshots:** (3-9 required, 1920x1080px)
1. Dashboard overview
2. Creating entry
3. Mood tracker
4. Settings/preferences
5. Voice entry feature
6. Analytics
7. Theme customization

**Rated For:** (Content rating)
```
Age rating: 12+
Contains: None (or select applicable)
```

### Step 7: Submit for Review

```bash
1. Complete all sections:
   - [ ] Product info
   - [ ] Descriptions
   - [ ] Screenshots
   - [ ] Ratings
   - [ ] MSIX package
2. Click "Publish"
3. Wait for certification (24-48 hours)
4. Check email for status
```

---

## macOS App Store

### Apple's Mac Distribution
**Market Share:** ~15% of app users
**Fee:** Included in $99/year developer membership
**Review Time:** 24-48 hours
**For:** Mac-compatible Electron apps

### Step 1: Prepare for macOS

```bash
cd journal-desktop

# In package.json configure for Mac:
{
  "build": {
    "mac": {
      "target": ["dmg", "mas"],  // dmg for web, mas for App Store
      "category": "public.app-category.productivity",
      "signingIdentity": "Apple Development",
      "notarize": {
        "teamId": "ABCDEFG123"
      }
    }
  }
}
```

### Step 2: Code Signing

```bash
# Get Code Signing Certificate from Apple
1. In Xcode, go Preferences > Accounts
2. View Details for your Apple ID
3. Click "Download Manual Profiles" if needed
4. Get "Mac App Distribution" certificate

# Then in app build settings:
codesign --deep --force --verify --verbose \
  --sign "Apple Development: your@email.com" \
  dist/Journal\ Desk.app
```

### Step 3: Notarization (Build Verification)

```bash
# Apple requires app notarization for security
# Create App-specific password at https://appleid.apple.com

# In package.json:
{
  "notarize": {
    "appleId": "your@apple.com",
    "appleIdPassword": "@keychain:NOTARIZE_PASSWORD",
    "teamId": "your-team-id-from-apple"
  }
}

# Build (includes notarization)
npm run build
```

### Step 4: Create App Store App

```bash
1. Go to App Store Connect
2. "My Apps" > "+"
3. Select platform: macOS
4. Name: Journal Desk
5. Bundle ID: com.yourcompany.journal.macos
6. SKU: journal-desk-mac
```

### Step 5: Update App Information

Same as iOS process above for descriptions, screenshots, etc.

Note: macOS App Store requirements are same as iOS App Store.

### Step 6: Submit .pkg or .mas Build

```bash
# Build for App Store (mas target)
npm run build -- --mac  # Outputs .mas

# Or upload DMG for direct distribution
# (Some developers skip App Store and sell directly)
```

---

## GitHub Releases (Desktop)

### Direct Distribution
**Market Share:** Developers, early adopters
**Fee:** Free
**Review Time:** None (you control releases)
**For:** Electron or Tauri apps

### Step 1: Create GitHub Release

```bash
cd journal-desktop

# Tag version
git tag v1.0.0
git push origin v1.0.0

# Or in GitHub UI:
1. Go to Releases tab
2. Click "Draft a new release"
3. Tag version: v1.0.0
4. Release title: "Journal Desk v1.0"
5. Description: Release notes
```

### Step 2: Build Distributions

```bash
# Build all platforms
npm run build

# Creates:
# - dist/Journal Desk-1.0.0.dmg (macOS)
# - dist/Journal Desk Setup 1.0.0.exe (Windows)
# - dist/journal-desk-1.0.0.AppImage (Linux)
```

### Step 3: Upload Files

```bash
# Using GitHub CLI (easiest)
gh release create v1.0.0 \
  dist/Journal\ Desk-1.0.0.dmg \
  dist/Journal\ Desk\ Setup\ 1.0.0.exe \
  dist/journal-desk-1.0.0.AppImage \
  --title "Release v1.0.0" \
  --notes "Initial release with all features"

# Or upload manually in GitHub UI
1. Go to Release
2. Drag/drop files
3. Click "Publish release"
```

### Step 4: Setup Auto-Updates

In Electron app:

```javascript
const { autoUpdater } = require("electron-updater");

// In main process
autoUpdater.checkForUpdatesAndNotify();

// Users automatically get updates when you push to GitHub Releases
```

---

## App Store Optimization (ASO)

### Keywords & Discoverability

**Google Play Store:**
```
Keywords (5-10): journal, diary, notes, personal, mood, 
                 thoughts, private, entries, voice, task

Metadata Keywords field: journal, diary, mood tracker
```

**Apple App Store:**
```
Keywords field (up to 100 chars):
"journal, diary, notes, mood, task, personal"

Note: iOS uses keywords field, not metadata.keywords
```

### Rating & Reviews Management

```bash
# Respond to reviews
1. Check daily for 1-star reviews
2. Reply professionally:
   "We appreciate your feedback. We've fixed [issue]. 
    Please email support@journaldesk.com for help."

3. Encourage positive reviews:
   - Prompt after user creates 3rd entry
   - Ask for rating (not forced)
   - Make it easy to provide feedback
```

### Version Updates Strategy

```bash
# Timeline
v1.0 - Initial launch
v1.1 - Performance improvements, bug fixes
v1.2 - New features (collaboration, backup)
v2.0 - Major redesign, new features

# Each update should:
- Include new features or improvements
- Fix reported bugs
- Improve performance
- Not decrease functionality
- Maintain backward compatibility
```

---

## Marketing & Launch

### Pre-Launch (2 weeks before)

```bash
# 1. Create landing page
- Screenshots
- Feature list
- Links to app stores
- Email signup

# 2. Prepare social media
- Create Twitter account (@JournalDesk)
- Set up Instagram
- Create LinkedIn page
- Prepare launch posts

# 3. Reach out to influencers
- Tech bloggers
- Productivity YouTubers
- App review sites
- Send early access code

# 4. Create press release
- Distribution to tech press
- Product Hunt listing
- Hacker News submission
```

### Launch Day

```bash
# 1. Release across all platforms
- [ ] Google Play Store
- [ ] Apple App Store
- [ ] Microsoft Store
- [ ] macOS App Store
- [ ] GitHub Releases
- [ ] Website download page

# 2. Announce
- [ ] Tweet thread
- [ ] LinkedIn post
- [ ] Product Hunt
- [ ] Email newsletter
- [ ] Hacker News (https://news.ycombinator.com)
- [ ] Reddit (r/productivity, r/apps)

# 3. Monitor
- [ ] Track downloads
- [ ] Watch for reviews
- [ ] Respond to comments
- [ ] Fix any reported bugs immediately
```

### Post-Launch

```bash
Week 1:
- Monitor 1-star reviews closely
- Fix critical bugs same day
- Thank positive reviewers
- Engage with users

Week 2-4:
- Plan first content update
- Gather user feedback
- Improve based on reviews
- Market on social media

Month 2+:
- Regular update schedule
- Continuous improvement
- Community building
- User testimonials
```

---

## Post-Launch Maintenance

### Update Schedule

```bash
Recommended: Update every 1-2 weeks with:
- Security patches
- Performance improvements
- Bug fixes
- Small features

Major updates: Quarterly with new features
```

### Monitoring Metrics

Track for each platform:

```
- Downloads/installs
- DAU (Daily Active Users)
- Retention rate
- Average rating
- # of reviews
- Crash rate
- Session length
```

### Version Control

```bash
Each app store version = Git tag

git tag v1.0.0  # Initial release
git tag v1.1.0  # First update
git tag v1.2.0  # Second update
git tag v2.0.0  # Major revision

Keep changelog:
CHANGELOG.md containing all changes per version
```

---

## Resources

### Developer Accounts
- Google Play Console: https://play.google.com/console
- Apple App Store Connect: https://appstoreconnect.apple.com
- Microsoft Partner Center: https://partner.microsoft.com
- macOS App Store: (via App Store Connect)

### Tools
- App Store Optimization: Mobile Action, App Annie
- Screenshots: Figma, Sketch
- Privacy Policy Generator: Iubenda, GeniiusRx

### Guidelines
- Google Play Policies: https://policies.google.com/play/developer-content-policy
- Apple App Review Guidelines: https://developer.apple.com/app-store/review/guidelines
- Microsoft Store Policies: https://docs.microsoft.com/en-us/windows/uwp/publish/store-policies

---

**Last Updated:** April 11, 2026
**Version:** 2.0
**Status:** Ready for Publishing
