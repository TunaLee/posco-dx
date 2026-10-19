/**
 * formatHelper1: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function formatHelper1(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * formatHelper2: 금액을 천 단위 쉼표 문자열로.
 */
export function formatHelper2(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * formatHelper3: 배열을 키별로 묶는다.
 */
export function formatHelper3(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * formatHelper4: 두 날짜 사이 일수 (UTC 기준).
 */
export function formatHelper4(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * formatHelper5: 비어 있지 않은 값만 남긴다.
 */
export function formatHelper5(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}

/**
 * formatHelper6: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function formatHelper6(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * formatHelper7: 금액을 천 단위 쉼표 문자열로.
 */
export function formatHelper7(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * formatHelper8: 배열을 키별로 묶는다.
 */
export function formatHelper8(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * formatHelper9: 두 날짜 사이 일수 (UTC 기준).
 */
export function formatHelper9(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * formatHelper10: 비어 있지 않은 값만 남긴다.
 */
export function formatHelper10(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}

/**
 * formatHelper11: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function formatHelper11(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * formatHelper12: 금액을 천 단위 쉼표 문자열로.
 */
export function formatHelper12(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * formatHelper13: 배열을 키별로 묶는다.
 */
export function formatHelper13(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * formatHelper14: 두 날짜 사이 일수 (UTC 기준).
 */
export function formatHelper14(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * formatHelper15: 비어 있지 않은 값만 남긴다.
 */
export function formatHelper15(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}

/**
 * formatHelper16: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function formatHelper16(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}
