# Journal Desk - React Native Mobile App

A feature-rich journaling application built with React Native and Expo, supporting iOS and Android platforms.

## 🚀 Features

- **📝 Journal Entries**: Write, edit, and manage daily journal entries with rich formatting
- **😊 Mood Tracking**: Log your mood throughout the day with visual analytics
- **🎤 Voice Entries**: Record voice memos that get automatically transcribed
- **📊 Analytics**: Get insights into your mood trends, productivity, and writing patterns
- **✅ Task Management**: Create and manage tasks with priority levels
- **🔔 Notifications**: Smart reminders to keep you journaling consistently
- **⚙️ Customization**: Dark mode, notification preferences, and user settings
- **☁️ Cloud Sync**: Sync your entries across all your devices
- **🔐 Secure**: Token-based authentication with encrypted data storage

## 📱 Platforms

- **iOS**: 13.0+ (iPhone & iPad)
- **Android**: 5.0+ (phones and tablets)

## 🛠️ Tech Stack

- **Framework**: React Native 0.73.0
- **Build System**: Expo (SDK 50.0.0)
- **Navigation**: React Navigation with Bottom Tabs & Stack
- **UI Components**: React Native Paper
- **HTTP Client**: Axios
- **Local Storage**: AsyncStorage
- **Charts**: React Native Chart Kit
- **Calendar**: React Native Calendars
- **Audio**: Expo Audio & Camera
- **State Management**: React Hooks (Context + useReducer)

## 📋 Requirements

Before you begin, ensure you have:

- **Node.js** 16+ (https://nodejs.org)
- **npm** 7+ or **yarn** 1.22+
- **Expo CLI**: Install with `npm install -g eas-cli`
- **Git**: For version control

For building:
- **Android**: Android Studio + Android SDK
- **iOS**: Mac with Xcode 13+

## 🚀 Quick Start

### 1. Clone Repository

```bash
cd journal-mobile-rn
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure API

Edit `config/env.js` and set your backend API URL:

```javascript
// Development (local machine)
API_URL: 'http://192.168.1.X:8000/api'  // Replace X with your IP

// Production
API_URL: 'https://yourdomain.com/api'
```

### 4. Start Development Server

```bash
npm start
```

Then:
- **Android Emulator**: Press `a`
- **iOS Simulator**: Press `i` (Mac only)
- **Scan QR Code**: Use Expo Go app (download from app stores)

## 📖 Project Structure

```
journal-mobile-rn/
├── App.js                 # Main navigation & app entry point
├── screens/               # Screen components
│   ├── LoginScreen.js     # Authentication
│   ├── SignupScreen.js    # Registration
│   ├── DashboardScreen.js # Home page
│   ├── EntriesScreen.js   # Entry list
│   ├── CreateEntryScreen.js     # Create entry
│   ├── MoodTrackerScreen.js     # Mood tracking
│   ├── AnalyticsScreen.js       # Statistics
│   ├── TasksScreen.js           # Task management
│   ├── VoiceEntryScreen.js      # Voice recording
│   ├── NotificationsScreen.js   # Notifications
│   └── SettingsScreen.js        # User settings
├── services/              # API & external services
│   └── api.js             # API client with interceptors
├── config/                # Configuration
│   └── env.js             # Environment variables
├── app.json               # Expo configuration
├── eas.json               # Expo build configuration
├── package.json           # Dependencies
├── BUILD_AND_PUBLISH.md   # Build guide
└── README.md              # This file
```

## 🔑 Key Screens

### Authentication Flow
- **LoginScreen**: Enter credentials to access app
- **SignupScreen**: Create new account with email verification

### Main Navigation (4 Tabs)
1. **Dashboard**: Stats, quick actions, insights
2. **Entries**: List, search, create new entries
3. **Mood**: Mood tracking, trends, correlations
4. **More**: Settings, notifications, analytics, tasks, voice entries

## 🧪 Testing Features

### Login Credentials (Development)
```
Username: testuser
Password: testpass123
```

### Test Data
- Dashboard shows mock statistics
- Sample entries provided for list view
- Mood tracker has sample trend data
- Task list has example tasks

## 🔐 Security Features

- **Token-based Authentication**: JWT tokens with secure storage
- **AsyncStorage**: Encrypted local persistence
- **API Interceptors**: Automatic token refresh on 401
- **Data Validation**: Input validation on all forms
- **HTTPS**: Enforced for production environments

## 🎯 API Integration

All API calls go through centralized service in `services/api.js`:

```javascript
import { entriesAPI, statsAPI, authAPI } from './services/api';

// Create entry
const entry = await entriesAPI.create('Title', 'Content', 3);

// Get statistics
const stats = await statsAPI.getDashboard();

// Login
const auth = await authAPI.login('username', 'password');
```

## 🎨 Styling & Branding

- **Primary Color**: #57b8d9 (Teal)
- **Secondary Color**: #7c5dcd (Purple)
- **Success**: #10b981 (Green)
- **Warning**: #f59e0b (Orange)
- **Error**: #ef4444 (Red)

Update colors in `config/env.js` under `COLORS` object.

## 🏗️ Building for Production

### Android

```bash
# Build optimized APK (testing)
eas build --platform android --profile preview

# Build AAB (Google Play) - RECOMMENDED
eas build --platform android --profile production
```

### iOS

```bash
# Build IPA (TestFlight/App Store)
eas build --platform ios --profile production
```

See [BUILD_AND_PUBLISH.md](./BUILD_AND_PUBLISH.md) for complete instructions.

## 📤 Publishing

### Google Play Store
1. Build AAB file
2. Create app listing in Play Console
3. Upload build and complete store information
4. Submit for review (2-4 hours)

### Apple App Store
1. Build IPA file
2. Create app in App Store Connect
3. Upload build and complete store form
4. Submit for review (24-48 hours)

Complete guide: [BUILD_AND_PUBLISH.md](./BUILD_AND_PUBLISH.md)

## 🔄 API Endpoints Expected

The backend (Django) should provide these endpoints with token authentication:

```
POST   /api/auth/login/              # Login
POST   /api/auth/register/           # Register
POST   /api/auth/logout/             # Logout

GET    /api/entries/                 # List entries
POST   /api/entries/                 # Create entry
GET    /api/entries/{id}/            # Get entry
PATCH  /api/entries/{id}/            # Update entry
DELETE /api/entries/{id}/            # Delete entry

GET    /api/stats/                   # Dashboard stats
GET    /api/stats/mood-trends/       # Mood analytics
GET    /api/stats/productivity/      # Productivity score
GET    /api/stats/streak/            # Current streak

GET    /api/tasks/                   # List tasks
POST   /api/tasks/                   # Create task
POST   /api/tasks/{id}/toggle/       # Toggle task
DELETE /api/tasks/{id}/              # Delete task

POST   /api/voice-entries/           # Upload voice entry
GET    /api/voice-entries/           # List voice entries

GET    /api/notifications/           # List notifications
POST   /api/notifications/{id}/mark-read/  # Mark read

GET    /api/user/profile/            # User profile
PATCH  /api/user/profile/            # Update profile
PATCH  /api/user/preferences/        # Update preferences
```

## 🐛 Troubleshooting

### App Won't Load
```bash
# Clear cache and reinstall
npm run web -- --reset-cache

# Or restart Expo
npm start -- --clear
```

### Can't Connect to Backend
- Verify backend API URL in `config/env.js`
- Ensure backend is running
- Check network connectivity
- Use local IP for same-network testing (not 127.0.0.1)

### Build Fails
```bash
# Clear dependencies
rm -rf node_modules package-lock.json

# Reinstall
npm install

# Try again
npm start
```

### Videos/Screenshots Not Loading
- Check image paths are correct
- Ensure images are in correct format
- Verify file permissions

## 📚 Documentation

- [Build & Publish Guide](./BUILD_AND_PUBLISH.md)
- [React Native Docs](https://reactnative.dev)
- [Expo Documentation](https://docs.expo.dev)
- [React Navigation Guide](https://reactnavigation.org)

## 🤝 Contributing

To contribute to the project:

1. Create feature branch: `git checkout -b feature/amazing-feature`
2. Commit changes: `git commit -m 'Add amazing feature'`
3. Push to branch: `git push origin feature/amazing-feature`
4. Submit pull request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🆘 Support

For issues and questions:
- Check existing issues on GitHub
- Create detailed bug reports with screenshots
- Include device/OS information
- Contact: support@journaldesk.io

## 🎯 Roadmap (Future Features)

- [ ] AI-powered mood prediction
- [ ] Collaborative journaling
- [ ] Integration with calendar apps
- [ ] Advanced search with NLP
- [ ] Social sharing capabilities
- [ ] Community features
- [ ] Meditation & mindfulness content
- [ ] Web app synchronization

## 🙏 Acknowledgments

Built with:
- React Native & Expo teams
- React Navigation community
- Open source contributors

---

**Version**: 1.0.0  
**Last Updated**: January 2024  
**Platform**: iOS 13+ / Android 5.0+
