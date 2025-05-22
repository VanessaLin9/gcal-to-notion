const { app, BrowserWindow, ipcMain, dialog} = require('electron');
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');

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

  //dialog.showSaveDialog({properties: ['openFile']});
  // 監聽選擇檔案的事件
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

  ipcMain.handle('select-credential', async () => {
    const result = await dialog.showOpenDialog({
      properties: ['openFile'],
      filters: [
        { name: 'JSON Files', extensions: ['json'] },
      ],
    });
    if(!result.canceled && result.filePaths.length > 0) {
        const sourcePath = result.filePaths[0];
        const destPath = path.join(__dirname, '..', 'credentials.json');
        fs.copyFileSync(sourcePath, destPath);
        return '✅ credentials.json 已匯入';
    }
    return '❌ 未選取任何檔案';
  });

  ipcMain.handle('select-token', async () => {
      const result = await dialog.showOpenDialog({
          properties: ['openFile'],
          filters: [{ name: 'JSON', extensions: ['json'] }]
      });

      if (!result.canceled && result.filePaths.length > 0) {
          const sourcePath = result.filePaths[0];
          const destPath = path.join(__dirname, '..', 'token.json');
          fs.copyFileSync(sourcePath, destPath);
          return '✅ token.json 已匯入';
      }
      return '❌ 未選取任何檔案';
  });

  app.on('activate', () => {
    // macOS 特有邏輯，沒有視窗就再開一個
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});


app.on('window-all-closed', () => {
  // macOS 通常不會自動退出 app
  if (process.platform !== 'darwin') app.quit();
});