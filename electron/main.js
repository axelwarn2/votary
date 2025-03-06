const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let win;
let pythonProcess;

function createWindow() {
    win = new BrowserWindow({
        width: 1366,
        height: 768,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            enableRemoteModule: false
        }
    });

    win.loadURL('http://localhost:5173');
}

app.whenReady().then(() => {
    createWindow();

    pythonProcess = spawn('python', [path.join(__dirname, '../backend/main.py')]);

    pythonProcess.stdout.on('data', (data) => {
        win.webContents.send('from-python', data.toString().trim());
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python error: ${data}`);
    });
});

ipcMain.on('calculate-sum', (event, { num1, num2 }) => {
    pythonProcess.stdin.write(`sum:${num1},${num2}\n`);
    pythonProcess.stdin.flush;
});

ipcMain.on('calculate-subtraction', (event, { num1, num2 }) => {
    pythonProcess.stdin.write(`subtraction:${num1},${num2}\n`);
});

ipcMain.on('calculate-proizvedenie', (event, { num1, num2 }) => {
    pythonProcess.stdin.write(`proizvedenie:${num1}, ${num2}\n`);
    pythonProcess.stdin.flush;
});

ipcMain.on('calculate-division', (event, { num1, num2 }) => {
    pythonProcess.stdin.write(`division:${num1},${num2}\n`);
    pythonProcess.stdin.flush;
});

app.on('window-all-closed', () => {
    if (pythonProcess) pythonProcess.kill();
    if (process.platform !== 'darwin') app.quit();
});