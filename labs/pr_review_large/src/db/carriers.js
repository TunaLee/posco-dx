import { query } from "../driver.js";

export async function carrierByName(name) {
  return query(`SELECT * FROM carriers WHERE name LIKE '%${name}%'`);
}
/**
 * carriersHelper1: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function carriersHelper1(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * carriersHelper2: 금액을 천 단위 쉼표 문자열로.
 */
export function carriersHelper2(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * carriersHelper3: 배열을 키별로 묶는다.
 */
export function carriersHelper3(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * carriersHelper4: 두 날짜 사이 일수 (UTC 기준).
 */
export function carriersHelper4(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * carriersHelper5: 비어 있지 않은 값만 남긴다.
 */
export function carriersHelper5(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}

/**
 * carriersHelper6: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function carriersHelper6(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * carriersHelper7: 금액을 천 단위 쉼표 문자열로.
 */
export function carriersHelper7(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * carriersHelper8: 배열을 키별로 묶는다.
 */
export function carriersHelper8(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * carriersHelper9: 두 날짜 사이 일수 (UTC 기준).
 */
export function carriersHelper9(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * carriersHelper10: 비어 있지 않은 값만 남긴다.
 */
export function carriersHelper10(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}
