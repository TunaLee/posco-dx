// 회의실 예약 — PRD F1~F5. 예약은 이 브라우저(localStorage)에만 저장된다.
const ROOMS = ["대회의실", "소회의실 A", "소회의실 B"];
const SLOTS = [];
for (let h = 9; h < 18; h++) SLOTS.push(`${String(h).padStart(2, "0")}:00`, `${String(h).padStart(2, "0")}:30`);
const KEY = "room-bookings";

const $ = (id) => document.getElementById(id);
const load = () => { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch { return []; } };
const save = (list) => localStorage.setItem(KEY, JSON.stringify(list));
const today = () => new Date().toISOString().slice(0, 10);
const endOf = (t) => { const i = SLOTS.indexOf(t); return i + 1 < SLOTS.length ? SLOTS[i + 1] : "18:00"; };

let day = today();
let picked = null; // { room, start }
let opened = null; // 상세 창의 예약

// F2 시간표
function render() {
  $("day").value = day;
  const list = load().filter((b) => b.date === day);
  const grid = $("grid");
  grid.innerHTML = '<div class="head"></div>' + ROOMS.map((r) => `<div class="head">${r}</div>`).join("");
  for (const t of SLOTS) {
    grid.insertAdjacentHTML("beforeend", `<div class="time">${t.endsWith(":00") ? t : ""}</div>`);
    for (const room of ROOMS) {
      const b = list.find((x) => x.room === room && x.start <= t && t < x.end);
      const cell = document.createElement("div");
      cell.className = "cell" + (b ? " busy" : "") + (b && b.start === t ? " first" : "");
      if (b && b.start === t) cell.innerHTML = `<span class="tag">${b.title} · ${b.who}</span>`;
      cell.onclick = () => (b ? openDetail(b) : openForm(room, t));
      grid.appendChild(cell);
    }
  }
}

// F3 예약 창
function openForm(room, start) {
  picked = { room, start };
  const f = $("bookForm");
  f.reset();
  $("formTitle").textContent = `${room} · ${day}`;
  f.start.innerHTML = SLOTS.map((t) => `<option ${t === start ? "selected" : ""}>${t}</option>`).join("");
  f.end.innerHTML = [...SLOTS.slice(1), "18:00"].map((t) => `<option ${t === endOf(start) ? "selected" : ""}>${t}</option>`).join("");
  $("err").textContent = "";
  $("form").showModal();
}

$("bookForm").addEventListener("submit", (e) => {
  const f = e.target;
  const b = { id: Date.now(), room: picked.room, date: day, start: f.start.value, end: f.end.value, who: f.who.value.trim(), title: f.title.value.trim() };
  if (b.end <= b.start) { e.preventDefault(); $("err").textContent = "끝 시간이 시작보다 늦어야 한다"; return; }
  // F4 겹침 막기
  const clash = load().some((x) => x.room === b.room && x.date === b.date && x.start < b.end && b.start < x.end);
  if (clash) { e.preventDefault(); $("err").textContent = "이미 예약된 시간"; return; }
  save([...load(), b]);
  render();
});
$("close").onclick = () => $("form").close();

// F5 상세 · 취소
function openDetail(b) {
  opened = b;
  $("dTitle").textContent = b.title;
  $("dInfo").textContent = `${b.room} · ${b.date} ${b.start}~${b.end} · ${b.who}`;
  $("detail").showModal();
}
$("dCancel").onclick = () => { save(load().filter((x) => x.id !== opened.id)); $("detail").close(); render(); };
$("dClose").onclick = () => $("detail").close();

// F1 날짜 선택
const shift = (n) => { const d = new Date(day); d.setDate(d.getDate() + n); day = d.toISOString().slice(0, 10); render(); };
$("prev").onclick = () => shift(-1);
$("next").onclick = () => shift(1);
$("day").onchange = (e) => { day = e.target.value || today(); render(); };

render();
