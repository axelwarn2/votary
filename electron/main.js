const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const events = require("node:events");

let win;
let pythonProcess;

function createWindow() {
    win = new BrowserWindow({
        width: 1200,
        height: 800,
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

ipcMain.handle('get-meeting-data', async (event, meetingId) => {
    return new Promise((resolve) => {
        pythonProcess.stdin.write(`get_meeting:${meetingId}\n`);

        pythonProcess.stdout.once('data', (data) => {
            resolve(data.toString().trim());
        });
    });
});

ipcMain.handle('get-task-data', async (event, taskId) => {
    return new Promise((resolve) => {
        pythonProcess.stdin.write(`get_task:${taskId}\n`);

        pythonProcess.stdout.once('data', (data) => {
            resolve(data.toString().trim());
        });
    });
});

ipcMain.handle('get-statistic-data', async (event, employee) => {
    return new Promise((resolve) => {
        pythonProcess.stdin.write(`get_statistic:${employee}\n`);

        pythonProcess.stdout.once('data', (data) => {
            resolve(data.toString().trim());
        });
    });
});

app.on('window-all-closed', () => {
    if (pythonProcess) pythonProcess.kill();
    if (process.platform !== 'darwin') app.quit();
});