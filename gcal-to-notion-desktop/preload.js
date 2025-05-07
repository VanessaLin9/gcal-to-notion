const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    runSync: () => ipcRenderer.invoke('run-sync')
});

