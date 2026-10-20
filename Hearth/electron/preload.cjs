const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("hearth", {
  load: () => ipcRenderer.invoke("data:load"),
  save: (data) => ipcRenderer.invoke("data:save", data),
  dataPath: () => ipcRenderer.invoke("data:path"),
  notify: (payload) => ipcRenderer.invoke("notify", payload),
});
