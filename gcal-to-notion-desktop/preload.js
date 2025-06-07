const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
    runSync: () => ipcRenderer.invoke('run-sync'),
    selectCredential: () => ipcRenderer.invoke('select-credential'),
    selectToken: () => ipcRenderer.invoke('select-token'),
    loginGoogle: () => ipcRenderer.invoke('login-google'),
    deleteToken: () => ipcRenderer.invoke('delete-token')
});

