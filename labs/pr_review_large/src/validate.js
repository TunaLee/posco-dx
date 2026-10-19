/**
 * validateHelper1: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function validateHelper1(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * validateHelper2: 금액을 천 단위 쉼표 문자열로.
 */
export function validateHelper2(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * validateHelper3: 배열을 키별로 묶는다.
 */
export function validateHelper3(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * validateHelper4: 두 날짜 사이 일수 (UTC 기준).
 */
export function validateHelper4(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * validateHelper5: 비어 있지 않은 값만 남긴다.
 */
export function validateHelper5(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}

/**
 * validateHelper6: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function validateHelper6(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * validateHelper7: 금액을 천 단위 쉼표 문자열로.
 */
export function validateHelper7(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * validateHelper8: 배열을 키별로 묶는다.
 */
export function validateHelper8(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * validateHelper9: 두 날짜 사이 일수 (UTC 기준).
 */
export function validateHelper9(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * validateHelper10: 비어 있지 않은 값만 남긴다.
 */
export function validateHelper10(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}

/**
 * validateHelper11: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function validateHelper11(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * validateHelper12: 금액을 천 단위 쉼표 문자열로.
 */
export function validateHelper12(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * validateHelper13: 배열을 키별로 묶는다.
 */
export function validateHelper13(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * validateHelper14: 두 날짜 사이 일수 (UTC 기준).
 */
export function validateHelper14(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * validateHelper15: 비어 있지 않은 값만 남긴다.
 */
export function validateHelper15(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}

/**
 * validateHelper16: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function validateHelper16(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}
