const PAGES = [
  { id: "today", label: "Bugün" },
  { id: "tasks", label: "Görevler" },
  { id: "habits", label: "Alışkanlıklar" },
  { id: "journal", label: "Günlük" },
  { id: "focus", label: "Odak" },
  { id: "settings", label: "Ayarlar" },
];

const DAYS_TR = ["Paz", "Pzt", "Sal", "Çar", "Per", "Cum", "Cmt"];
const MONTHS_TR = [
  "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
  "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık",
];

const state = {
  page: "today",
  data: null,
  journalDate: todayKey(),
  timer: {
    running: false,
    mode: "focus",
    remaining: 25 * 60,
    handle: null,
  },
};

function uid() {
  return crypto.randomUUID();
}

function todayKey(date = new Date()) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

function parseKey(key) {
  const [y, m, d] = key.split("-").map(Number);
  return new Date(y, m - 1, d);
}

function formatLong(date = new Date()) {
  return `${date.getDate()} ${MONTHS_TR[date.getMonth()]} ${date.getFullYear()}`;
}

function weekdayIndex(date) {
  return date.getDay();
}

function lastNDates(n) {
  const dates = [];
  const now = new Date();
  for (let i = n - 1; i >= 0; i -= 1) {
    const d = new Date(now);
    d.setDate(now.getDate() - i);
    dates.push(todayKey(d));
  }
  return dates;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

async function persist() {
  await window.hearth.save(state.data);
}

function seedIfNeeded() {
  if (state.data.settings.seeded) return;
  const today = todayKey();
  state.data.tasks = [
    { id: uid(), title: "Hearth projesini GitHub'a yükle", done: false, priority: "high", dueDate: today, createdAt: Date.now() },
    { id: uid(), title: "README ekran görüntüsünü ekle", done: false, priority: "medium", dueDate: today, createdAt: Date.now() },
    { id: uid(), title: "İlk odak seansını tamamla", done: false, priority: "low", dueDate: today, createdAt: Date.now() },
  ];
  state.data.habits = [
    { id: uid(), name: "Kitap oku", checks: { [today]: false } },
    { id: uid(), name: "Yürüyüş", checks: { [today]: false } },
    { id: uid(), name: "Su iç", checks: { [today]: true } },
  ];
  state.data.journal[today] = {
    content: "Hearth ile ilk gün. Bugün küçük bir görev listesi ve bir odak seansı yeterli.",
    updatedAt: Date.now(),
  };
  state.data.settings.seeded = true;
}

function applyTheme() {
  document.documentElement.dataset.theme = state.data.settings.theme;
}

function greeting() {
  const hour = new Date().getHours();
  const name = state.data.settings.displayName.trim();
  const who = name || "orada";
  if (hour < 12) return `Günaydın, ${who}`;
  if (hour < 18) return `İyi günler, ${who}`;
  return `İyi akşamlar, ${who}`;
}

function priorityLabel(priority) {
  return { high: "Yüksek", medium: "Orta", low: "Düşük" }[priority] || "Orta";
}

function openTasks() {
  return state.data.tasks.filter((task) => !task.done);
}

function doneThisWeek() {
  const start = new Date();
  start.setDate(start.getDate() - 6);
  start.setHours(0, 0, 0, 0);
  return state.data.tasks.filter((task) => task.done && task.completedAt && task.completedAt >= start.getTime()).length;
}

function focusMinutesThisWeek() {
  const start = new Date();
  start.setDate(start.getDate() - 6);
  start.setHours(0, 0, 0, 0);
  return Math.round(
    state.data.sessions
      .filter((session) => session.endedAt >= start.getTime() && session.mode === "focus")
      .reduce((sum, session) => sum + session.durationSec, 0) / 60
  );
}

function habitStreak(habit) {
  let streak = 0;
  const cursor = new Date();
  while (habit.checks[todayKey(cursor)]) {
    streak += 1;
    cursor.setDate(cursor.getDate() - 1);
  }
  return streak;
}

function renderNav() {
  const nav = document.getElementById("nav");
  nav.innerHTML = PAGES.map(
    (page) => `<button type="button" data-page="${page.id}" class="${state.page === page.id ? "active" : ""}">${page.label}</button>`
  ).join("");
  nav.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => {
      state.page = button.dataset.page;
      render();
    });
  });
}

function setHeader(eyebrow, title, actionsHtml = "") {
  document.getElementById("page-eyebrow").textContent = eyebrow;
  document.getElementById("page-title").textContent = title;
  document.getElementById("topbar-actions").innerHTML = actionsHtml;
  document.getElementById("sidebar-date").textContent = formatLong();
}

function renderToday() {
  const today = todayKey();
  const todaysTasks = state.data.tasks.filter((task) => !task.done && (!task.dueDate || task.dueDate === today));
  const note = state.data.journal[today]?.content || "";
  setHeader("Bugün", greeting());
  document.getElementById("content").innerHTML = `
    <div class="grid two">
      <article class="card">
        <h2>Bugünün işleri</h2>
        <div>${todaysTasks.length ? todaysTasks.map(taskRow).join("") : `<p class="empty">Bugün için açık görev yok.</p>`}</div>
      </article>
      <div class="stack">
        <article class="card">
          <h2>Haftalık özet</h2>
          <div class="grid three">
            <div class="stat"><b>${doneThisWeek()}</b><span class="muted">biten görev</span></div>
            <div class="stat"><b>${focusMinutesThisWeek()}</b><span class="muted">odak dk</span></div>
            <div class="stat"><b>${state.data.habits.filter((habit) => habit.checks[today]).length}</b><span class="muted">alışkanlık</span></div>
          </div>
        </article>
        <article class="card">
          <h2>Günün notu</h2>
          <p>${note ? escapeHtml(note).slice(0, 220) : `<span class="muted">Henüz bir günlük yazılmamış.</span>`}</p>
        </article>
      </div>
    </div>
  `;
  bindTaskToggles();
}

function taskRow(task) {
  return `
    <div class="task ${task.done ? "done" : ""}" data-id="${task.id}">
      <input type="checkbox" ${task.done ? "checked" : ""} data-toggle="${task.id}" />
      <div style="flex:1">
        <div class="task-title">${escapeHtml(task.title)}</div>
        <small class="muted">${task.dueDate ? task.dueDate : "Tarihsiz"}</small>
      </div>
      <span class="prio ${task.priority}">${priorityLabel(task.priority)}</span>
      <button class="danger" data-delete="${task.id}" type="button">Sil</button>
    </div>
  `;
}

function bindTaskToggles() {
  document.querySelectorAll("[data-toggle]").forEach((input) => {
    input.addEventListener("change", async () => {
      const task = state.data.tasks.find((item) => item.id === input.dataset.toggle);
      task.done = input.checked;
      task.completedAt = input.checked ? Date.now() : null;
      await persist();
      render();
    });
  });
  document.querySelectorAll("[data-delete]").forEach((button) => {
    button.addEventListener("click", async () => {
      state.data.tasks = state.data.tasks.filter((item) => item.id !== button.dataset.delete);
      await persist();
      render();
    });
  });
}

function renderTasks() {
  setHeader("Görevler", "Ne üzerine çalışıyorsun?", `<button class="primary" id="add-task" type="button">Görev ekle</button>`);
  document.getElementById("content").innerHTML = `
    <article class="card stack">
      <form class="form-grid" id="task-form">
        <input type="text" name="title" placeholder="Görev başlığı" required />
        <select name="priority">
          <option value="low">Düşük</option>
          <option value="medium" selected>Orta</option>
          <option value="high">Yüksek</option>
        </select>
        <input type="date" name="dueDate" value="${todayKey()}" />
        <button class="primary" type="submit">Kaydet</button>
      </form>
      <div>
        <div class="row"><h2>Açık</h2><span class="muted">${openTasks().length}</span></div>
        ${openTasks().length ? openTasks().map(taskRow).join("") : `<p class="empty">Açık görev yok.</p>`}
      </div>
      <div>
        <div class="row"><h2>Tamamlanan</h2></div>
        ${state.data.tasks.filter((task) => task.done).map(taskRow).join("") || `<p class="empty">Henüz tamamlanan görev yok.</p>`}
      </div>
    </article>
  `;
  document.getElementById("task-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = new FormData(event.target);
    state.data.tasks.unshift({
      id: uid(),
      title: String(form.get("title")).trim(),
      priority: String(form.get("priority")),
      dueDate: String(form.get("dueDate") || ""),
      done: false,
      createdAt: Date.now(),
    });
    await persist();
    render();
  });
  document.getElementById("add-task")?.addEventListener("click", () => {
    document.querySelector("[name=title]").focus();
  });
  bindTaskToggles();
}

function renderHabits() {
  const week = lastNDates(7);
  setHeader("Alışkanlıklar", "Küçük tekrarlar");
  document.getElementById("content").innerHTML = `
    <article class="card stack">
      <form class="form-grid" id="habit-form">
        <input type="text" name="name" placeholder="Yeni alışkanlık" required />
        <button class="primary" type="submit">Ekle</button>
      </form>
      <div class="row muted">${week.map((day) => `<span>${DAYS_TR[weekdayIndex(parseKey(day))]}</span>`).join("")}</div>
      ${state.data.habits.map((habit) => `
        <div class="habit">
          <div style="flex:1">
            <strong>${escapeHtml(habit.name)}</strong>
            <div class="muted">${habitStreak(habit)} gün seri</div>
          </div>
          <div class="checks">
            ${week.map((day) => `<button class="check ${habit.checks[day] ? "on" : ""}" data-habit="${habit.id}" data-day="${day}" type="button"></button>`).join("")}
          </div>
          <button class="danger" data-habit-delete="${habit.id}" type="button">Sil</button>
        </div>
      `).join("") || `<p class="empty">İlk alışkanlığını ekle.</p>`}
    </article>
  `;
  document.getElementById("habit-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const name = new FormData(event.target).get("name");
    state.data.habits.push({ id: uid(), name: String(name).trim(), checks: {} });
    await persist();
    render();
  });
  document.querySelectorAll("[data-habit]").forEach((button) => {
    button.addEventListener("click", async () => {
      const habit = state.data.habits.find((item) => item.id === button.dataset.habit);
      habit.checks[button.dataset.day] = !habit.checks[button.dataset.day];
      await persist();
      render();
    });
  });
  document.querySelectorAll("[data-habit-delete]").forEach((button) => {
    button.addEventListener("click", async () => {
      state.data.habits = state.data.habits.filter((item) => item.id !== button.dataset.habitDelete);
      await persist();
      render();
    });
  });
}

function monthDays(key) {
  const date = parseKey(key);
  const year = date.getFullYear();
  const month = date.getMonth();
  const first = new Date(year, month, 1);
  const last = new Date(year, month + 1, 0);
  const blanks = first.getDay();
  const days = [];
  for (let i = 0; i < blanks; i += 1) days.push(null);
  for (let day = 1; day <= last.getDate(); day += 1) {
    days.push(todayKey(new Date(year, month, day)));
  }
  return days;
}

function renderJournal() {
  const entry = state.data.journal[state.journalDate] || { content: "" };
  setHeader("Günlük", formatLong(parseKey(state.journalDate)));
  document.getElementById("content").innerHTML = `
    <div class="grid two">
      <article class="card">
        <div class="calendar">
          ${DAYS_TR.map((day) => `<span class="muted" style="text-align:center">${day}</span>`).join("")}
          ${monthDays(state.journalDate).map((day) => {
            if (!day) return "<span></span>";
            const active = day === state.journalDate ? "active" : "";
            const has = state.data.journal[day]?.content ? "has" : "";
            return `<button class="${active} ${has}" data-day="${day}" type="button">${Number(day.slice(-2))}</button>`;
          }).join("")}
        </div>
      </article>
      <article class="card stack">
        <textarea id="journal-text" placeholder="Bugün aklında ne kaldı?">${escapeHtml(entry.content)}</textarea>
        <div class="row">
          <span class="muted">Yalnızca bu bilgisayarda saklanır.</span>
          <button class="primary" id="save-journal" type="button">Kaydet</button>
        </div>
      </article>
    </div>
  `;
  document.querySelectorAll("[data-day]").forEach((button) => {
    button.addEventListener("click", () => {
      state.journalDate = button.dataset.day;
      render();
    });
  });
  document.getElementById("save-journal").addEventListener("click", async () => {
    state.data.journal[state.journalDate] = {
      content: document.getElementById("journal-text").value,
      updatedAt: Date.now(),
    };
    await persist();
    render();
  });
}

function formatClock(total) {
  const minutes = String(Math.floor(total / 60)).padStart(2, "0");
  const seconds = String(total % 60).padStart(2, "0");
  return `${minutes}:${seconds}`;
}

function configuredSeconds(mode = state.timer.mode) {
  const minutes = mode === "focus" ? state.data.settings.focusMinutes : state.data.settings.breakMinutes;
  return minutes * 60;
}

function stopTimer(reset = false) {
  clearInterval(state.timer.handle);
  state.timer.handle = null;
  state.timer.running = false;
  if (reset) state.timer.remaining = configuredSeconds();
}

async function completeTimer() {
  const duration = configuredSeconds();
  state.data.sessions.unshift({
    id: uid(),
    mode: state.timer.mode,
    durationSec: duration,
    endedAt: Date.now(),
  });
  await persist();
  await window.hearth.notify({
    title: state.timer.mode === "focus" ? "Odak bitti" : "Mola bitti",
    body: state.timer.mode === "focus" ? "Kısa bir mola zamanı." : "Yeni bir odak turuna hazır mısın?",
  });
  state.timer.mode = state.timer.mode === "focus" ? "break" : "focus";
  stopTimer(true);
  render();
}

function startTimer() {
  if (state.timer.running) return;
  state.timer.running = true;
  state.timer.handle = setInterval(async () => {
    state.timer.remaining -= 1;
    const face = document.getElementById("timer-face");
    if (face) face.textContent = formatClock(state.timer.remaining);
    if (state.timer.remaining <= 0) {
      await completeTimer();
    }
  }, 1000);
}

function renderFocus() {
  setHeader("Odak", state.timer.mode === "focus" ? "Derin iş" : "Mola");
  const recent = state.data.sessions.slice(0, 6);
  document.getElementById("content").innerHTML = `
    <div class="grid two">
      <article class="card timer">
        <p class="muted">${state.timer.mode === "focus" ? "Odak seansı" : "Kısa mola"}</p>
        <div class="timer-face" id="timer-face">${formatClock(state.timer.remaining)}</div>
        <div class="actions" style="justify-content:center">
          <button class="primary" id="timer-start" type="button">${state.timer.running ? "Çalışıyor" : "Başlat"}</button>
          <button class="ghost" id="timer-pause" type="button">Duraklat</button>
          <button class="ghost" id="timer-reset" type="button">Sıfırla</button>
        </div>
      </article>
      <article class="card">
        <h2>Son seanslar</h2>
        ${recent.map((session) => `
          <div class="session">
            <div>
              <strong>${session.mode === "focus" ? "Odak" : "Mola"}</strong>
              <div class="muted">${new Date(session.endedAt).toLocaleString("tr-TR")}</div>
            </div>
            <span>${Math.round(session.durationSec / 60)} dk</span>
          </div>
        `).join("") || `<p class="empty">İlk seansını başlat.</p>`}
      </article>
    </div>
  `;
  document.getElementById("timer-start").addEventListener("click", () => {
    startTimer();
    render();
  });
  document.getElementById("timer-pause").addEventListener("click", () => {
    stopTimer(false);
    render();
  });
  document.getElementById("timer-reset").addEventListener("click", () => {
    stopTimer(true);
    render();
  });
}

async function renderSettings() {
  const dataPath = await window.hearth.dataPath();
  setHeader("Ayarlar", "Çalışma alanın");
  document.getElementById("content").innerHTML = `
    <article class="card stack">
      <label class="stack">
        <span>Görünen ad</span>
        <input type="text" id="display-name" value="${escapeHtml(state.data.settings.displayName)}" placeholder="Adın" />
      </label>
      <div class="grid two">
        <label class="stack">
          <span>Odak (dk)</span>
          <input type="number" id="focus-min" min="1" max="90" value="${state.data.settings.focusMinutes}" />
        </label>
        <label class="stack">
          <span>Mola (dk)</span>
          <input type="number" id="break-min" min="1" max="30" value="${state.data.settings.breakMinutes}" />
        </label>
      </div>
      <div class="actions">
        <button class="primary" id="save-settings" type="button">Kaydet</button>
        <button class="ghost" id="export-data" type="button">Veriyi dışa aktar</button>
        <button class="danger" id="reset-data" type="button">Örnek veriyi sıfırla</button>
      </div>
      <p class="muted">Yerel veri dosyası: ${escapeHtml(dataPath)}</p>
    </article>
  `;
  document.getElementById("save-settings").addEventListener("click", async () => {
    state.data.settings.displayName = document.getElementById("display-name").value.trim();
    state.data.settings.focusMinutes = Number(document.getElementById("focus-min").value);
    state.data.settings.breakMinutes = Number(document.getElementById("break-min").value);
    if (!state.timer.running) state.timer.remaining = configuredSeconds();
    await persist();
    render();
  });
  document.getElementById("export-data").addEventListener("click", () => {
    const blob = new Blob([JSON.stringify(state.data, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "hearth-backup.json";
    link.click();
    URL.revokeObjectURL(url);
  });
  document.getElementById("reset-data").addEventListener("click", async () => {
    state.data.settings.seeded = false;
    state.data.tasks = [];
    state.data.habits = [];
    state.data.journal = {};
    state.data.sessions = [];
    seedIfNeeded();
    await persist();
    render();
  });
}

function render() {
  applyTheme();
  renderNav();
  const pages = { today: renderToday, tasks: renderTasks, habits: renderHabits, journal: renderJournal, focus: renderFocus, settings: renderSettings };
  pages[state.page]();
}

async function boot() {
  state.data = await window.hearth.load();
  seedIfNeeded();
  await persist();
  state.timer.remaining = configuredSeconds("focus");
  applyTheme();
  document.getElementById("theme-toggle").addEventListener("click", async () => {
    state.data.settings.theme = state.data.settings.theme === "dark" ? "light" : "dark";
    await persist();
    render();
  });
  render();
}

boot();
