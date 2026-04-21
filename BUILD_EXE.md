# AI联谊匹配系统 - 打包为EXE指南

## 方案一：使用PyInstaller打包后端

### 1. 安装PyInstaller

```bash
cd backend
pip install pyinstaller
```

### 2. 创建打包配置文件

创建 `backend/matchmaking.spec`:

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('matchmaking.db', '.')],
    hiddenimports=['uvicorn.logging', 'uvicorn.loops', 'uvicorn.loops.auto'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='联谊匹配系统-后端',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

### 3. 执行打包

```bash
cd backend
pyinstaller matchmaking.spec
```

打包后的可执行文件在 `backend/dist/联谊匹配系统-后端.exe`

## 方案二：使用electron-vite打包完整桌面应用

### 1. 安装electron

```bash
cd frontend
npm install electron electron-builder --save-dev
```

### 2. 创建electron主进程文件

创建 `frontend/electron/main.js`:

```javascript
const { app, BrowserWindow } = require('electron')
const { spawn } = require('child_process')
const path = require('path')

let mainWindow
let backendProcess

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  })

  // 加载前端页面
  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:3000')
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'))
  }
}

function startBackend() {
  // 启动Python后端
  const backendPath = path.join(__dirname, '../../backend/dist/联谊匹配系统-后端.exe')
  backendProcess = spawn(backendPath, [], {
    detached: false,
    windowsHide: true
  })
  
  backendProcess.stdout.on('data', (data) => {
    console.log(`后端: ${data}`)
  })
  
  backendProcess.stderr.on('data', (data) => {
    console.error(`后端错误: ${data}`)
  })
}

app.whenReady().then(() => {
  startBackend()
  
  // 等待后端启动
  setTimeout(() => {
    createWindow()
  }, 3000)
  
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', () => {
  if (backendProcess) {
    backendProcess.kill()
  }
  if (process.platform !== 'darwin') app.quit()
})
```

### 3. 修改package.json添加electron脚本

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "electron:dev": "NODE_ENV=development electron .",
    "electron:build": "npm run build && electron-builder"
  },
  "build": {
    "appId": "com.matchmaking.app",
    "productName": "AI联谊匹配系统",
    "directories": {
      "output": "release"
    },
    "files": [
      "dist/**/*",
      "electron/**/*"
    ],
    "extraResources": [
      {
        "from": "../backend/dist",
        "to": "backend"
      }
    ],
    "win": {
      "target": "nsis",
      "icon": "public/icon.ico"
    }
  },
  "main": "electron/main.js"
}
```

### 4. 执行打包

```bash
# 先打包后端
cd backend
pyinstaller matchmaking.spec

# 再打包前端+electron
cd ../frontend
npm run electron:build
```

打包后的安装程序在 `frontend/release/AI联谊匹配系统 Setup.exe`

## 方案三：使用Tauri打包（推荐，体积小）

### 1. 安装Tauri

```bash
cd frontend
npm install @tauri-apps/cli --save-dev
```

### 2. 初始化Tauri

```bash
npx tauri init
```

### 3. 配置tauri.conf.json

```json
{
  "build": {
    "beforeBuildCommand": "npm run build",
    "beforeDevCommand": "npm run dev",
    "devPath": "http://localhost:3000",
    "distDir": "../dist"
  },
  "tauri": {
    "allowlist": {
      "all": false,
      "shell": {
        "all": false,
        "open": true
      }
    },
    "bundle": {
      "active": true,
      "category": "DeveloperTool",
      "copyright": "",
      "deb": {
        "depends": []
      },
      "externalBin": [],
      "icon": [
        "icons/32x32.png",
        "icons/128x128.png",
        "icons/128x128@2x.png",
        "icons/icon.icns",
        "icons/icon.ico"
      ],
      "identifier": "com.matchmaking.app",
      "longDescription": "",
      "macOS": {
        "entitlements": null,
        "exceptionDomain": "",
        "frameworks": [],
        "providerShortName": null,
        "signingIdentity": null
      },
      "resources": [],
      "shortDescription": "",
      "targets": "all",
      "windows": {
        "certificateThumbprint": null,
        "digestAlgorithm": "sha256",
        "timestampUrl": ""
      }
    },
    "security": {
      "csp": null
    },
    "updater": {
      "active": false
    },
    "windows": [
      {
        "fullscreen": false,
        "height": 800,
        "resizable": true,
        "title": "AI联谊匹配系统",
        "width": 1200
      }
    ]
  }
}
```

### 4. 打包

```bash
npx tauri build
```

打包后的文件在 `frontend/src-tauri/target/release/`

## 推荐方案

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| PyInstaller | 简单快速 | 文件大(>100MB) | 纯后端部署 |
| Electron | 功能完整 | 文件大(>150MB) | 完整桌面应用 |
| Tauri | 体积小(~5MB) | 配置复杂 | 轻量级桌面应用 |

## 最终推荐

对于你的需求，建议使用 **方案一 + 分离部署**：

1. 后端用PyInstaller打包为exe
2. 前端用vite build生成静态文件
3. 使用一个简单的启动脚本同时启动前后端

这样用户只需要双击一个bat文件即可启动整个系统。
