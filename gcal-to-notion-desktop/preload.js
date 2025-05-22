const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    runSync: () => ipcRenderer.invoke('run-sync'),
    selectCredentials: () => ipcRenderer.invoke('select-credential'),
    selectToken: () => ipcRenderer.invoke('select-token'),
    onFileSelected: (callback) => ipcRenderer.on('file-selected', (event, message) => callback(message)),
});

