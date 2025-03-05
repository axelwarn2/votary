const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    calculateSum: (num1, num2) => ipcRenderer.send('calculate-sum', { num1, num2 }),
    calculateSubtraction: (num1, num2) => ipcRenderer.send('calculate-subtraction', { num1, num2 }),
    calculateProizvedenie: (num1, num2) => ipcRenderer.send('calculate-proizvedenie', { num1, num2 }),
    calculateDivision: (num1, num2) => ipcRenderer.send('calculate-division', { num1, num2 }),
    onPythonData: (callback) => ipcRenderer.on('from-python', callback)
});