# React Native Mobile App Setup

This guide will help you build the React Native mobile app for the Journal application.

## Prerequisites

- Node.js (v16+) and npm
- Expo CLI: `npm install -g expo-cli`
- Android Studio (for Android) or Xcode (for iOS)
- Expo go app on your phone for testing

## Quick Start

### 1. Create React Native Project

```bash
expo init journal-mobile --template

# Choose: bare workflow or managed workflow
# Recommended: managed workflow (easiest)
```

### 2. Install Dependencies

```bash
cd journal-mobile
npm install
npm install @react-navigation/native @react-navigation/bottom-tabs
npm install react-native-screens react-native-safe-area-context
npm install axios
npm install react-native-voice
npm install react-native-camera
npm install react-native-calendar-events
npm install react-native-share
npm install @react-native-community/async-storage
npm install jwt-decode
```

### 3. Project Structure

```
journal-mobile/
├── src/
│   ├── components/
│   │   ├── EntryCard.js
│   │   ├── TaskItem.js
│   │   ├── MoodTracker.js
│   │   └── ...
│   ├── screens/
│   │   ├── HomeScreen.js
│   │   ├── EntriesScreen.js
│   │   ├── CreateEntryScreen.js
│   │   ├── TasksScreen.js
│   │   ├── MoodTrackerScreen.js
│   │   ├── SettingsScreen.js
│   │   └── ...
│   ├── services/
│   │   ├── api.js
│   │   ├── voice.js
│   │   ├── storage.js
│   │   └── ...
│   ├── navigation/
│   │   └── MainNavigator.js
│   ├── styles/
│   │   └── theme.js
│   └── App.js
├── app.json
├── .expo/
└── package.json
```

## API Connection

Update `src/services/api.js`:

```javascript
import axios from 'axios';
import AsyncStorage from '@react-native-community/async-storage';

const API_BASE_URL = 'http://your-server-ip:8000/api/';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Add token to requests
api.interceptors.request.use(async (config) => {
  const token = await AsyncStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

## Key Features to Implement

### 1. Authentication
- Login screen
- Sign up screen
- Token-based auth with JWT

### 2. Journal Entries
- List entries with infinite scroll
- Create/edit/delete entries
- Search and filter
- View entry details

### 3. Task Management
- Add tasks to entries
- Mark tasks complete
- Priority levels
- Due date reminders

### 4. Voice Recording
- Record and transcribe voice entries
- Save to cloud
- Playback

### 5. Mood Tracking
- Daily mood check-in
- Emoji selection
- Mood history and trends

### 6. Notifications
- Push notifications
- Local notifications for reminders
- In-app notification center

### 7. Sync & Offline
- Offline support with AsyncStorage
- Auto-sync when online
- Background sync

## Building & Deployment

### Android Build

```bash
# Generate APK
eas build --platform android --type apk

# Generate AAB (for Play Store)
eas build --platform android --type app-bundle
```

### iOS Build

```bash
# Requires macOS with Xcode
eas build --platform ios
```

### Testing

```bash
# Web testing
npm run web

# Device testing
expo start
# Scan QR code with Expo Go app
```

## Environment Setup

Create `.env.local`:

```
REACT_APP_API_URL=http://your-backend-url:8000
REACT_APP_DEBUG=true
```

## Performance Tips

1. Use React.memo for components
2. Implement lazy loading for lists
3. Optimize images
4. Use AsyncStorage for caching
5. Implement proper error handling
6. Use background tasks for syncing

## Security

1. Store auth tokens securely
2. Use HTTPS for API calls
3. Implement certificate pinning
4. Validate input
5. Sanitize sensitive data

## Next Steps

1. Create the project structure
2. Build authentication screens
3. Create main navigation flow
4. Implement entry management
5. Add voice recording features
6. Implement sync/offline support
7. Add push notifications
8. Test thoroughly
9. Build and deploy to app stores

## Resources

- [React Native Docs](https://reactnative.dev/)
- [Expo Docs](https://docs.expo.dev/)
- [React Navigation](https://reactnavigation.org/)
- [React Native Community Libraries](https://react-native-community.github.io/)
