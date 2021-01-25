# Electron Application Boilerplate

## Install required packages:
```text
npm init react-app .
npm i -D electron electron-builder concurrently wait-on
npm i cross-env electron-is-dev
```

<br>

## Setup Electron File:

Create a file called `electron.js` in `public/` folder and add the following code:

```javascript
const { app, BrowserWindow } = require('electron');
const path = require('path');
const isDev = require('electron-is-dev');

function createWindow() {
    const win = new BrowserWindow({
        width: 1800,
        height: 1000
    })

    win.loadURL(isDev ? 'http://localhost:3000' : `file://${path.join(__dirname, '../build/index.html')}`);
    
    // win.webContents.openDevTools()
}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow()
    }
})
```

<br>

## Update package.json File

Add the following to the top above the `dependencies` section:

```json
"main": "public/electron.js",
```

Replace the `"scripts"` section with this:

```json
"scripts": {
	"react-start": "react-scripts start",
	"react-build": "react-scripts build",
	"react-test": "react-scripts test",
	"react-eject": "react-scripts eject",
	"electron-build": "electron-builder",
	"build": "npm run react-build && npm run electron-build",
	"start": "concurrently \"cross-env BROWSER=none npm run react-start\" \"wait-on http://localhost:3000 && electron .\""
},
```

<br>

## Starting your App:
```text
npm start
```

<br>

## Building your App:
```text
npm build
```

