const { app, BrowserWindow, ipcMain, Notification, shell } = require("electron");
const path = require("path");
const fs = require("fs");

const DATA_FILE = "hearth-data.json";

function dataPath() {
  return path.join(app.getPath("userData"), DATA_FILE);
}

function defaultData() {
  return {
    tasks: [],
    habits: [],
    journal: {},
    sessions: [],
    settings: {
      theme: "light",
      displayName: "",
      focusMinutes: 25,
      breakMinutes: 5,
      seeded: false,
    },
  };
}

function readData() {
  try {
    const raw = fs.readFileSync(dataPath(), "utf8");
    const parsed = JSON.parse(raw);
    return {
      ...defaultData(),
      ...parsed,
      settings: { ...defaultData().settings, ...(parsed.settings || {}) },
    };
  } catch {
    return defaultData();
  }
}

function writeData(data) {
  fs.mkdirSync(path.dirname(dataPath()), { recursive: true });
  fs.writeFileSync(dataPath(), JSON.stringify(data, null, 2), "utf8");
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1180,
    height: 760,
    minWidth: 900,
    minHeight: 620,
    backgroundColor: "#f3eee4",
    title: "Hearth",
    autoHideMenuBar: true,
    webPreferences: {
      preload: path.join(__dirname, "preload.cjs"),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
    },
  });

  win.loadFile(path.join(__dirname, "..", "renderer", "index.html"));

  win.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: "deny" };
  });
}

app.whenReady().then(() => {
  ipcMain.handle("data:load", () => readData());
  ipcMain.handle("data:save", (_event, data) => {
    writeData(data);
    return true;
  });
  ipcMain.handle("data:path", () => dataPath());
  ipcMain.handle("notify", (_event, { title, body }) => {
    if (Notification.isSupported()) {
      new Notification({ title, body }).show();
    }
  });

  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
