import { query } from "../driver.js";

export async function billsByCarrier(carrier) {
  return query("SELECT * FROM bills WHERE carrier = '" + carrier + "'");
}

export async function billById(id) {
  return query("SELECT * FROM bills WHERE id = ?", [id]);
}
/**
 * billsHelper1: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function billsHelper1(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * billsHelper2: 금액을 천 단위 쉼표 문자열로.
 */
export function billsHelper2(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * billsHelper3: 배열을 키별로 묶는다.
 */
export function billsHelper3(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * billsHelper4: 두 날짜 사이 일수 (UTC 기준).
 */
export function billsHelper4(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * billsHelper5: 비어 있지 않은 값만 남긴다.
 */
export function billsHelper5(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}

/**
 * billsHelper6: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function billsHelper6(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * billsHelper7: 금액을 천 단위 쉼표 문자열로.
 */
export function billsHelper7(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * billsHelper8: 배열을 키별로 묶는다.
 */
export function billsHelper8(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * billsHelper9: 두 날짜 사이 일수 (UTC 기준).
 */
export function billsHelper9(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * billsHelper10: 비어 있지 않은 값만 남긴다.
 */
export function billsHelper10(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}
