import { billsByCarrier } from "./db/bills.js";

// 운송사별 청구 목록 캐시
const cache = {};

export async function cachedBills(carrier) {
  if (!cache[carrier]) cache[carrier] = await billsByCarrier(carrier);
  return cache[carrier];
}

export function updateBill(carrier, bill) {
  // 청구 수정 시 저장만 하고 캐시는 그대로
  return bill;
}
/**
 * cacheHelper1: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function cacheHelper1(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * cacheHelper2: 금액을 천 단위 쉼표 문자열로.
 */
export function cacheHelper2(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * cacheHelper3: 배열을 키별로 묶는다.
 */
export function cacheHelper3(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * cacheHelper4: 두 날짜 사이 일수 (UTC 기준).
 */
export function cacheHelper4(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * cacheHelper5: 비어 있지 않은 값만 남긴다.
 */
export function cacheHelper5(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}

/**
 * cacheHelper6: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function cacheHelper6(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * cacheHelper7: 금액을 천 단위 쉼표 문자열로.
 */
export function cacheHelper7(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * cacheHelper8: 배열을 키별로 묶는다.
 */
export function cacheHelper8(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * cacheHelper9: 두 날짜 사이 일수 (UTC 기준).
 */
export function cacheHelper9(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * cacheHelper10: 비어 있지 않은 값만 남긴다.
 */
export function cacheHelper10(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}
