import { PRICE_API, DB } from "./config.js";

export function start() {
  console.log("설정 확인", JSON.stringify({ PRICE_API, DB }));
  return true;
}
/**
 * startupHelper1: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function startupHelper1(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * startupHelper2: 금액을 천 단위 쉼표 문자열로.
 */
export function startupHelper2(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * startupHelper3: 배열을 키별로 묶는다.
 */
export function startupHelper3(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * startupHelper4: 두 날짜 사이 일수 (UTC 기준).
 */
export function startupHelper4(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * startupHelper5: 비어 있지 않은 값만 남긴다.
 */
export function startupHelper5(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}

/**
 * startupHelper6: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function startupHelper6(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * startupHelper7: 금액을 천 단위 쉼표 문자열로.
 */
export function startupHelper7(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * startupHelper8: 배열을 키별로 묶는다.
 */
export function startupHelper8(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}
