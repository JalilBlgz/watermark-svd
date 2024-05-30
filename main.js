const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');

const isDev = process.env.NODE_ENV !== 'production';
const isMac = process.platform === 'darwin';

let mainWindow;

// Main Window
function createMainWindow() {
  mainWindow = new BrowserWindow({
    height: 1000,
    icon: `${__dirname}/assets/icons/Icon_256x256.png`,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
    },
  });

  mainWindow.loadFile(path.join(__dirname, './renderer/index.html')); 

  mainWindow.on('closed', () => (mainWindow = null));
}


app.on('ready', () => {
  createMainWindow();

  const mainMenu = Menu.buildFromTemplate(menu);
  Menu.setApplicationMenu(mainMenu);
});

const menu = [
  ...(isMac
    ? [
        {
          label: app.name,
          submenu: [
            {
              label: 'Quit',
              click: () => app.quit(),
              accelerator: 'CmdOrCtrl+W',
            },
          ],
        },
      ]
    : []),
  ...(isDev
    ? [
        {
          label: 'Developer',
          submenu: [
            { role: 'reload' },
            { role: 'forcereload' },
            { type: 'separator' },
            { role: 'toggledevtools' },
          ],
        },
      ]
    : []),
];


app.on('window-all-closed', () => {
  if (!isMac) app.quit();
});


app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createMainWindow();
});
