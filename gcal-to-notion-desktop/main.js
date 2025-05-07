const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { exec } = require('child_process');


function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
    },
  });

  win.loadFile('index.html');
  win.webContents.openDevTools();
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    // macOS 特有邏輯，沒有視窗就再開一個
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  // macOS 通常不會自動退出 app
  if (process.platform !== 'darwin') app.quit();
});

ipcMain.handle('run-sync', async () => {
    console.log("Get event!");
    return new Promise((resolve) => {
      exec('../.venv/bin/python ../sync_gcal_to_notion.py', (error, stdout, stderr) => {
        if (error) {
          console.error('Exec Error:', error.message);
          resolve(`❌ Error: ${stderr || error.message}`);
          return;
        }
        resolve(`✅ Python Script Output:\n${stdout}`);
      });
    });
  });
  