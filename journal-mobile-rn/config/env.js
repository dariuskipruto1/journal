// Environment Configuration
// Update these values based on your deployment

export const ENV_CONFIG = {
  // API Configuration
  // For development: 'http://192.168.1.X:8000/api' (replace X with your machine's local IP)
  // For staging: 'https://staging-api.journaldesk.io/api'
  // For production: 'https://api.journaldesk.io/api'
  API_URL: __DEV__ ? 'http://localhost:8000/api' : 'https://api.journaldesk.io/api',

  // App Name & Branding
  APP_NAME: 'Journal Desk',
  APP_VERSION: '1.0.0',
  COMPANY_NAME: 'Journal Desk Inc.',
  COMPANY_WEBSITE: 'https://journaldesk.io',
  COMPANY_EMAIL: 'support@journaldesk.io',

  // Colors
  COLORS: {
    PRIMARY: '#57b8d9',
    PRIMARY_DARK: '#3a8fa8',
    PRIMARY_LIGHT: '#7fd4f0',
    SECONDARY: '#7c5dcd',
    SUCCESS: '#10b981',
    WARNING: '#f59e0b',
    ERROR: '#ef4444',
    GRAY: '#999',
    LIGHT_GRAY: '#f0f0f0',
    DARK_GRAY: '#333',
  },

  // Feature Flags
  FEATURES: {
    CLOUD_BACKUP: true,
    EMAIL_REMINDERS: true,
    VOICE_ENTRY: true,
    COLLABORATION: true,
    ADVANCED_ANALYTICS: true,
    DARK_MODE: true,
    SOCIAL_SHARING: true,
  },

  // Social Links (optional)
  SOCIAL: {
    TWITTER: 'https://twitter.com/journaldesk',
    FACEBOOK: 'https://facebook.com/journaldesk',
    INSTAGRAM: 'https://instagram.com/journaldesk',
  },

  // App Stores (for app-store links)
  STORES: {
    GOOGLE_PLAY: 'https://play.google.com/store/apps/details?id=com.journaldesk.app',
    APP_STORE: 'https://apps.apple.com/app/journal-desk/id123456789',
  },

  // Third-party API Keys (if needed)
  // IMPORTANT: Never commit real API keys. Use environment variables instead
  SENTRY_DSN: process.env.SENTRY_DSN || '',
  FIREBASE_CONFIG: {
    apiKey: process.env.FIREBASE_API_KEY || '',
    authDomain: process.env.FIREBASE_AUTH_DOMAIN || '',
    projectId: process.env.FIREBASE_PROJECT_ID || '',
  },
};

// Helper function to get the correct API URL for different environments
export const getAPIUrl = () => {
  if (__DEV__) {
    // Development: Use localhost for iOS/Android simulator, or local IP for physical device
    // Change this to your machine's local IP if testing on physical device
    // Example: 'http://192.168.1.10:8000/api'
    return ENV_CONFIG.API_URL;
  }
  return ENV_CONFIG.API_URL;
};

// Helper to check if feature is enabled
export const isFeatureEnabled = (feature) => {
  return ENV_CONFIG.FEATURES[feature] === true;
};
