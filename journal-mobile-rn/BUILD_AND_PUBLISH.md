# Mobile App Build & Distribution Guide

## Overview
This guide covers building the Journal Desk React Native mobile app for both Android and iOS, and publishing to app stores.

## Prerequisites

### Required Software
- **Node.js & npm**: v16+ (download from https://nodejs.org)
- **Expo CLI**: `npm install -g eas-cli`
- **Android Development**:
  - Android Studio (for emulator/debugging)
  - Java Development Kit (JDK) 11+
  - Android SDK (API 31+)
- **iOS Development** (Mac only):
  - Xcode 13+
  - CocoaPods

### Accounts Required
- **Expo Account**: https://expo.dev (free)
- **Google Play Developer Account**: $25 one-time (https://play.google.com/apps/publish)
- **Apple Developer Account**: $99/year (https://developer.apple.com/programs)

## Setup Instructions

### 1. Install Dependencies

```bash
cd journal-mobile-rn
npm install
```

### 2. Configure Environment

Edit `config/env.js` and set your backend API URL:

```javascript
// For development (local Django server)
API_URL: 'http://192.168.1.X:8000/api'  // Replace X with your machine's IP

// For production (deployed backend)
API_URL: 'https://yourdomain.com/api'
```

To find your local IP on different OS:
- **Mac/Linux**: `ifconfig | grep inet`
- **Windows**: `ipconfig` (look for IPv4 Address)

### 3. Test in Expo Go (Optional)

```bash
# Start development server
npm start

# Scan QR code with Expo Go app on your phone
# Or press 'a' for Android emulator or 'i' for iOS simulator
```

## Building for Android

### Build APK (Testing)

APK files are used for testing on physical devices or emulators.

```bash
# Using Expo Application Services (Recommended)
eas build --platform android --local

# Or build locally (requires Android SDK installed)
npm run build-android
```

### Build AAB (Google Play Store)

Android App Bundle (AAB) is required for publishing to Google Play Store.

```bash
# Using Expo
eas build --platform android --local

# Select "production" when prompted
```

**Output**: `journal-desk.aab` (ready for Google Play)

### Local Android Build

If you want to build locally without Expo:

```bash
# Install Android dependencies
npm install

# Build APK
cd android
./gradlew assembleRelease

# Build AAB
./gradlew bundleRelease

# Output locations:
# APK: app/build/outputs/apk/release/
# AAB: app/build/outputs/bundle/release/
```

## Building for iOS

### Prerequisites
- Mac with Xcode installed
- Apple Developer Account (paid)

### Build IPA (TestFlight/App Store)

```bash
# Using Expo (Recommended)
eas build --platform ios --local

# Or build locally
npm run build-ios
```

**Output**: `journal-desk.ipa` (ready for TestFlight/App Store)

### Local iOS Build

```bash
cd iOS/
pod install
cd ..
npm run build-ios
open journal-mobile-rn.xcworkspace
```

## Publishing to App Stores

### Google Play Store Publishing

#### Step 1: Create App Listing

1. Go to https://play.google.com/apps/publish
2. Click "Create app"
3. Fill app details:
   - App name: "Journal Desk"
   - Default language: English
   - App category: Productivity

#### Step 2: Fill App Information

In left sidebar, complete:
- **Store listing**: 
  - Screenshot (at least 2)
  - Short description (80 chars max)
  - Full description (4000 chars max)
  - App icon (512x512 PNG)
  - Feature graphic (1024x500 PNG)
- **Graphics**: Upload screenshots
- **Content rating**: Complete questionnaire
- **Pricing & distribution**:
  - Set as Free
  - Select countries for distribution

#### Step 3: Upload Build

1. Go to "Releases" → "Production"
2. Create new release
3. Upload the AAB file (journal-desk.aab)
4. Set version name: 1.0.0
5. Add release notes

#### Step 4: Review & Submit

1. Complete pricing & distribution
2. Accept policies
3. Click "Submit for Review"

**Review Timeline**: 2-4 hours typically

### Apple App Store Publishing

#### Step 1: Create App ID

1. Go to https://appstoreconnect.apple.com
2. Apps → New App
3. Platform: iOS
4. Fill app details:
   - Name: "Journal Desk"
   - Bundle ID: `com.journaldesk.app` (must match app.json)
   - SKU: `journal-desk-001`
   - User Access: Full Access

#### Step 2: Configure App Information

- App Category: Productivity
- Subtitle: "Your Personal Digital Diary"
- Description: 4000 character limit
- Keywords: journal, diary, mood tracking, mindfulness
- Support URL: https://journaldesk.io/support
- Privacy Policy: https://journaldesk.io/privacy

#### Step 3: Add App Screenshots

Required resolution (at least 2):
- **iPhone 6.7"**: 1290 x 2796 px
- **iPad 12.9"**: 2048 x 2732 px

Add 2-4 localized screenshots for each device

#### Step 4: Add App Icon

1. High-Res Icon (1024x1024 PNG)
2. App Preview (30-second video showing app features)

#### Step 5: Upload Build via Xcode

```bash
# Create archive
xcode-select --install
npm run build-ios

# Open archived app in Xcode
open journal-mobile-rn.xcworkspace

# In Xcode: Product → Archive
# Then: Distribute App → App Store Connect
```

Or use Transporter:

```bash
# Download from App Store Connect
# Or use: transporter -f journal-desk.ipa -u your-apple-id -p your-password
```

#### Step 6: Review Build

1. In App Store Connect, go to "Builds"
2. Select your build
3. Check "Comply with Export Regulations"
4. Add build to "1.0 Prepare for Submission"

#### Step 7: Submit for Review

1. Go to version 1.0
2. In "Submission" section:
   - Sign export compliance
   - Review rating
   - Select build
3. Click "Submit for Review"

**Review Timeline**: 24-48 hours typically

## Version Updates

### Increment Version

```bash
# Edit app.json
{
  "expo": {
    "version": "1.1.0",  // Update this
    "ios": {
      "buildNumber": "2"  // Increment for each iOS build
    },
    "android": {
      "versionCode": 2    // Increment for each Android build
    }
  }
}

# Rebuild and resubmit to stores
```

## Building Multiple Variants

### Development Build

```bash
# This skips code optimization
eas build --platform android --profile development
```

### Release Build

```bash
# Fully optimized for production
eas build --platform android --profile production
```

## Troubleshooting

### Android Build Issues

**Issue**: `Java version mismatch`
```bash
# Install Java 11
brew install openjdk@11
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
```

**Issue**: `Build fails with dependency error`
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build-android
```

### iOS Build Issues

**Issue**: `CocoaPods dependency conflict`
```bash
cd ios
rm -rf Pods Podfile.lock
pod install
cd ..
```

**Issue**: `Signing certificate not found`
```bash
# Create new signing certificate in Xcode:
# Xcode → Preferences → Accounts → View Details → '+' button
```

### Store Submission Issues

**Issue**: `App rejected for privacy policy`
- Ensure privacy policy URL is accessible
- Must explicitly mention data collection practices

**Issue**: `Build rejected: Compliance issue`
- For encryption: Complete export compliance questionnaire
- Include in submission: "This app does not use encryption"

## Monitoring After Release

### Track Analytics

**Google Play Console**:
- Statistics → Installs and downloads
- User acquisition → Traffic source
- Crashes & ANRs → Monitor stability

**App Store Connect**:
- Analytics → Overview
- App Store → Sales and Trends
- TestFlight → Crash logs

### Collect Feedback

- Monitor app store reviews
- Set up in-app feedback mechanism
- Use Sentry for crash reporting (optional)

## Best Practices

✅ **Do**:
- Test on multiple devices before release
- Always use AAB/IPA format for stores
- Implement analytics from day 1
- Monitor crash reports
- Keep app version in sync across platforms
- Update app.json version before building
- Use TestFlight for iOS beta testing
- Use Play Console internal testing for Android

❌ **Don't**:
- Skip testing before submission
- Hardcode API URLs (use env config)
- Submit with debugging code
- Ignore store review guidelines
- Release with known bugs
- Use deprecated APIs

## Useful Links

- Expo Documentation: https://docs.expo.dev
- Google Play Console: https://play.google.com/apps/publish
- App Store Connect: https://appstoreconnect.apple.com
- React Native Docs: https://reactnative.dev/docs
- App Privacy Policy Template: https://www.privacypolicygenerator.info

## Support

For issues with:
- **Expo builds**: https://github.com/expo/expo/issues
- **Google Play**: https://support.google.com/googleplay
- **App Store**: https://developer.apple.com/support
- **App**: Report to support@journaldesk.io
