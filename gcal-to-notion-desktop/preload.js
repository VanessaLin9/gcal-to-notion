const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    runSync: () => ipcRenderer.send('open-gcal-to-notion'),
    onSyncResult: (callback) => ipcRenderer.on('sync-result', (event, message) => callback(message)),
});

