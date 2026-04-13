# Electron Desktop App Setup

Build a cross-platform desktop app for Windows, macOS, and Linux.

## Prerequisites

- Node.js (v16+) and npm
- Python (for native modules)
- Git

## Quick Start

### 1. Create Electron Project

```bash
mkdir journal-desktop
cd journal-desktop
npm init -y
npm install --save-dev electron electron-builder
npm install axios
npm install sqlite3 --save-optional
npm install dotenv
```

### 2. Project Structure

```
journal-desktop/
├── public/
│   ├── electron.js
│   ├── preload.js
│   └── icon.png
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── assets/
│   ├── styles/
│   ├── App.js
│   └── index.js
├── dist/
├── package.json
├── electron-builder.yml
└── README.md
```

## Setup Files

### public/electron.js

```javascript
const { app, BrowserWindow, Menu, ipcMain } = require('electron');
const path = require('path');
const isDev = require('electron-is-dev');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  const startUrl = isDev
    ? 'http://localhost:3000'
    : `file://${path.join(__dirname, '../build/index.html')}`;

  mainWindow.loadURL(startUrl);

  if (isDev) {
    mainWindow.webContents.openDevTools();
  }
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

// IPC handlers
ipcMain.handle('api-request', async (event, method, endpoint, data) => {
  // Handle API calls here
});
```

### public/preload.js

```javascript
const { contextBridge, ipcMain } = require('electron');

contextBridge.exposeInMainWorld('electron', {
  apiRequest: (method, endpoint, data) =>
    ipcIpcRenderer.invoke('api-request', method, endpoint, data),
  // Add other IPC calls here
});
```

### package.json Scripts

```json
{
  "scripts": {
    "dev": "concurrently \"npm run react-start\" \"wait-on http://127.0.0.1:3000 && electron .\"",
    "react-start": "react-scripts start",
    "react-build": "react-scripts build",
    "electron-dev": "electron .",
    "electron-build": "npm run react-build && electron-builder",
    "build": "npm run react-build && electron-builder",
    "dist": "npm run build"
  },
  "homepage": "./",
  "main": "public/electron.js"
}
```

### electron-builder.yml

```yaml
appId: com.journaldesk.app
productName: Journal Desk

directories:
  buildResources: assets
  output: dist

files:
  - from: build
    to: ./
  - from: public/electron.js
  - from: public/preload.js

win:
  target:
    - nsis
    - portable
  certificateFile: null

mac:
  target:
    - dmg
    - zip
  identity: null

linux:
  target:
    - AppImage
    - deb
  icon: assets/icon.png

nsis:
  oneClick: false
  allowToChangeInstallationDirectory: true
  createDesktopShortcut: true
  createStartMenuShortcut: true

```

## Features to Implement

### 1. Local Database
- SQLite for offline data
- Sync with backend when online

### 2. System Integration
- Native notifications
- System tray icon
- Auto-launch on startup
- File system integration

### 3. Offline Support
- Full offline functionality
- Auto-sync queue
- Conflict resolution

### 4. Performance
- App caching
- Lazy loading
- Memory optimization

### 5. Security
- Secure credential storage
- API token management
- Data encryption

## Development

### Run in Development Mode

```bash
npm run dev
```

This starts:
1. React dev server on http://localhost:3000
2. Electron app that loads the React app

### Build for Production

```bash
npm run build
```

This creates installers for:
- Windows (.exe, .msi)
- macOS (.dmg)
- Linux (.AppImage, .deb)

## Architecture

### Render Process (React)
- UI components
- State management
- Styling

### Main Process (Electron)
- Window management
- File system access
- Native integrations
- Background tasks

### IPC Communication
- Secure message passing
- Data serialization
- Error handling

## Database Integration

### SQLite Setup

```javascript
const sqlite3 = require('sqlite3');
const db = new sqlite3.Database('./journal.db');

// Create tables
db.serialize(() => {
  db.run(`CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT,
    date DATETIME,
    mood TEXT,
    synced BOOLEAN
  )`);
});
```

## Distribution

### GitHub Releases

```bash
# Create release and upload installers
npm run dist
```

### Microsoft Store

1. Create developer account
2. Reserve app name
3. Submit build
4. Wait for review

### Mac App Store

1. Sign app with certificate
2. Submit for notarization
3. Upload to Mac App Store

## Security Best Practices

1. Use context isolation
2. Validate all IPC messages
3. Never expose node integration
4. Use preload scripts for safe APIs
5. Sign and notarize releases
6. Keep Electron updated

## Performance Tips

1. Code splitting with React
2. Lazy load heavy modules
3. Use Web Workers for heavy tasks
4. Optimize bundle size
5. Use V8 code caching

## Troubleshooting

### App won't start
```bash
# Clear cache
rm -rf node_modules
npm install
```

### Build fails
```bash
# Rebuild native modules
npm rebuild
npm run build
```

### Notarization fails
- Check certificate
- Verify bundle identifier
- Check entitlements file

## Resources

- [Electron Docs](https://www.electronjs.org/docs)
- [Electron Builder](https://www.electron.build/)
- [React Integration](https://github.com/electron-react-boilerplate/electron-react-boilerplate)
- [IPC Security](https://www.electronjs.org/docs/api/ipc-main)
