const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    getMeetingData: (meetingId) => ipcRenderer.invoke('get-meeting-data', meetingId),
    getTaskData: (taskId) => ipcRenderer.invoke('get-task-data', taskId),
    getStatisticData: (employee) => ipcRenderer.invoke('get-statistic-data', employee),
    onPythonData: (callback) => ipcRenderer.on('from-python', callback),
});