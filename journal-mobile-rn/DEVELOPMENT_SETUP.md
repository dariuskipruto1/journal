# React Native Mobile App - Development Setup

Complete setup guide to get Journal Desk mobile app running on your machine.

## 📋 Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Running the App](#running-the-app)
- [Backend Setup](#backend-setup)
- [Emulator Setup](#emulator-setup)
- [Troubleshooting](#troubleshooting)

## ✅ Requirements

### System Requirements

- **Node.js**: 16.0.0 or higher
- **npm**: 7.0.0 or higher (or Yarn 1.22+)
- **Git**: For cloning repository

### For Android Development

- **Android Studio**: Latest version
- **Android SDK**: API 31+ recommended
- **Java JDK**: 11+ (not OpenJDK 14+, which may have issues)
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 10GB free space

### For iOS Development (Mac Only)

- **Xcode**: 13.0+
- **CocoaPods**: `sudo gem install cocoapods`
- **RAM**: 8GB minimum
- **macOS**: 10.15+

## 🔧 Installation

### Step 1: Install Node.js & npm

**macOS (using Homebrew)**:
```bash
brew install node
```

**Windows (download installer)**:
- Visit https://nodejs.org
- Download LTS version
- Run installer

**Verify Installation**:
```bash
node --version  # Should be v16+
npm --version   # Should be v7+
```

### Step 2: Install Expo CLI

```bash
npm install -g expo-cli eas-cli
```

Verify:
```bash
expo --version
eas --version
```

### Step 3: Setup Android Development (Android Only)

**macOS**:
```bash
# Install Android Studio via Homebrew
brew install --cask android-studio

# Set ANDROID_HOME (add to ~/.zshrc or ~/.bash_profile)
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

**Windows**:
```bash
# Download from https://developer.android.com/studio
# Install using installer
# Set ANDROID_HOME environment variable:
# Settings → Environment Variables → New Variable
# ANDROID_HOME = C:\Users\<YourUsername>\AppData\Local\Android\sdk
```

**Ubuntu/Linux**:
```bash
# Install Java first
sudo apt-get install openjdk-11-jdk

# Then install Android SDK tools
# Download from https://developer.android.com/tools#command-tools
```

### Step 4: Setup iOS Development (Mac Only)

```bash
# Install Xcode command line tools
xcode-select --install

# Install CocoaPods
sudo gem install cocoapods

# Accept Xcode license
sudo xcode-select --reset
sudo xcodebuild -license accept
```

### Step 5: Clone Repository

```bash
cd ~/projects  # or your preferred location
git clone https://github.com/yourusername/journal-mobile-rn.git
cd journal-mobile-rn
```

### Step 6: Install Dependencies

```bash
npm install
```

If you encounter errors:
```bash
# Clear cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Step 7: Configure Backend URL

Edit `config/env.js`:

```javascript
export const ENV_CONFIG = {
  // For local development
  API_URL: __DEV__ ? 'http://192.168.1.X:8000/api' : 'https://api.journaldesk.io/api',
  // Replace X with your machine's local IP
};
```

**Find your local IP**:
- **Mac/Linux**: `ifconfig | grep inet`
- **Windows**: `ipconfig` (look for IPv4 Address)

## 🚀 Running the App

### Option 1: Expo Go (Quickest - Recommended for Beginners)

#### Setup

1. Download **Expo Go** app:
   - [iOS App Store](https://apps.apple.com/app/expo-go/id6824271732)
   - [Google Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent)

#### Run App

```bash
cd journal-mobile-rn
npm start
```

Follow the prompts:
- Press `a` for Android
- Press `i` for iOS (Mac only)
- Scan QR code with Expo Go app

### Option 2: Android Emulator

#### Setup Emulator

1. **Open Android Studio**
2. **Tools → Device Manager**
3. **Click "+ Create device"**
4. Select device (e.g., "Pixel 4a")
5. Select API level (33+)
6. Click "Finish"

#### Run App

```bash
# Start emulator first (via Android Studio or):
emulator -avd Pixel_4a_API_33

# Wait for emulator to fully load, then:
npm run android
```

#### Troubleshooting Android

If emulator won't start:
```bash
# Kill all adb processes
adb kill-server

# Restart
adb start-server

# Try again
npm run android
```

### Option 3: iOS Simulator (Mac Only)

#### Run App

```bash
# First time setup (installs dependencies)
npm run ios-setup

# Then just run:
npm run ios
```

#### Simulator Controls

- **Open app location**: Simulator → I/O → Location
- **Toggle dark mode**: Simulator → Features → Toggle Appearance
- **View console**: Simulator window → Debug → Console

### Option 4: Physical Device

#### Android Phone

1. Enable Developer Mode:
   - Settings → About phone → Tap "Build number" 7 times
   
2. Enable USB Debugging:
   - Settings → Developer Options → USB Debugging ✓

3. Connect via USB with file transfer enabled

4. Run:
```bash
npm run android
```

#### iPhone (via Mac)

1. Connect iPhone to Mac via USB

2. Trust computer when prompted on phone

3. Run:
```bash
npm run ios
```

## 🖥️ Backend Setup

### Using Existing Backend

If backend is already running:

```bash
# Make sure it's running
cd ~/projects/now  # Your Django project location
python manage.py runserver 0.0.0.0:8000

# Update config/env.js with your local IP
API_URL: 'http://192.168.X.X:8000/api'
```

### Starting Fresh Backend

If you have the Django backend:

```bash
# Navigate to backend
cd ~/projects/now

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver
```

## 📱 Emulator Setup

### Android Emulator

**List available emulators**:
```bash
emulator -list-avds
```

**Start emulator**:
```bash
emulator -avd Pixel_4a_API_33 -netdelay none -netspeed full
```

**Increase RAM (optional)**:
1. Open Android Studio
2. Device Manager → Select emulator → settings
3. Edit → Memory: 4096 (or higher)

### iOS Simulator

**List available simulators**:
```bash
xcrun simctl list devices
```

**Open specific simulator**:
```bash
open -a "Simulator" --args -CurrentDeviceUDID <device-id>
```

## 🔧 Common Setup Issues

### Issue: Node modules installation fails

```bash
# Clear npm cache
npm cache clean --force

# Try installing again
npm install

# If still fails, try with exact versions:
npm install --legacy-peer-deps
```

### Issue: Port 8081 already in use (Metro bundler)

```bash
# Find process on port 8081
lsof -i :8081

# Kill the process
kill -9 <PID>

# Or change port in package.json
npm start -- --port 8090
```

### Issue: Java version mismatch

```bash
# Check Java version
java -version

# Should be 11 or 12. If not:
# macOS
brew install openjdk@11
export JAVA_HOME=$(/usr/libexec/java_home -v 11)

# Windows - Set JAVA_HOME to JDK 11 installation
```

### Issue: Android SDK not found

```bash
# Make sure ANDROID_HOME is set
echo $ANDROID_HOME

# If empty, add to shell profile (.zshrc, .bash_profile, etc)
export ANDROID_HOME=$HOME/Library/Android/sdk
```

### Issue: Pod install fails (iOS)

```bash
cd ios
pod install --repo-update
cd ..
```

## 📊 Development Workflow

### 1. Start Development Server
```bash
npm start
```

### 2. Make Code Changes
Edit any file in `screens/`, `services/`, etc.

### 3. Hot Reload
Changes automatically reload (if --fast-refresh is enabled)

For full reload:
- Android: Reload via app menu or press `r`
- iOS: ⌘+R or device menu

### 4. View Logs
```bash
# In Expo terminal:
# Press 'l' for logs
# Press 'j' for debug
```

## 🐛 Debugging

### React DevTools

```bash
# Install
npm install -D @react-devtools/standalone

# Connect (during development session)
# Expo menu → Open Debugger
```

### Console Logging

```javascript
console.log('Message', data);
console.warn('Warning', data);
console.error('Error', data);
```

View in Expo terminal or Xcode/Android Studio console.

### Redux DevTools (if you add Redux)

```bash
npm install redux-devtools-extension
```

## ✨ Tips & Best Practices

✅ **Do**:
- Test on both iOS and Android
- Clear cache if seeing stale code
- Use Expo Go for quick iterations
- Keep config/env.js with correct API URL
- Commit frequently

❌ **Don't**:
- Hardcode API URLs in components
- Forget to clear cache when dependencies change
- Use localhost (use your local IP instead)
- Connect device without USB debugging enabled

## 🔗 Useful Commands

```bash
# Start development
npm start

# Run on Android
npm run android

# Run on iOS
npm run ios

# Build APK
npm run build-android

# Build IPA
npm run build-ios

# Clean cache
npm start -- --reset-cache

# Install dependencies fresh
rm -rf node_modules && npm install

# Check Expo status
expo whoami

# Log out from Expo
expo logout
```

## 📚 Additional Resources

- [Expo Documentation](https://docs.expo.dev)
- [React Native Getting Started](https://reactnative.dev/docs/getting-started)
- [React Navigation Guide](https://reactnavigation.org/docs/getting-started)
- [Android Studio Setup Guide](https://developer.android.com/studio/intro)
- [Xcode Setup Guide](https://developer.apple.com/xcode/)

## 🆘 Getting Help

1. Check [Troubleshooting](#troubleshooting) section
2. Search existing GitHub issues
3. Check Expo forums: https://forums.expo.dev
4. Report bugs with:
   - OS and version
   - Node/npm versions
   - Full error message
   - Steps to reproduce

## ✅ Verification Checklist

Mark off as you complete each step:

- [ ] Node.js 16+ installed
- [ ] npm 7+ installed
- [ ] Expo CLI installed
- [ ] Repository cloned
- [ ] Dependencies installed (`npm install`)
- [ ] Backend URL configured (`config/env.js`)
- [ ] Backend running (if needed)
- [ ] Emulator/device set up
- [ ] App starts successfully
- [ ] Can navigate through screens

---

**You're ready to develop!** 🎉

Start with:
```bash
npm start
```

Happy coding! 💻
