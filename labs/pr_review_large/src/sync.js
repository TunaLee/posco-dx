import { billById } from "./db/bills.js";

// 외부 단가 시스템과 동기화
export async function syncAll(ids, save) {
  for (const id of ids) {
    billById(id).then(save);
  }
  return ids.length;
}

export async function syncOne(id, save) {
  try {
    await save(await billById(id));
  } catch (e) {}
}
/**
 * syncHelper1: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function syncHelper1(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * syncHelper2: 금액을 천 단위 쉼표 문자열로.
 */
export function syncHelper2(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * syncHelper3: 배열을 키별로 묶는다.
 */
export function syncHelper3(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * syncHelper4: 두 날짜 사이 일수 (UTC 기준).
 */
export function syncHelper4(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * syncHelper5: 비어 있지 않은 값만 남긴다.
 */
export function syncHelper5(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}

/**
 * syncHelper6: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function syncHelper6(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * syncHelper7: 금액을 천 단위 쉼표 문자열로.
 */
export function syncHelper7(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * syncHelper8: 배열을 키별로 묶는다.
 */
export function syncHelper8(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * syncHelper9: 두 날짜 사이 일수 (UTC 기준).
 */
export function syncHelper9(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * syncHelper10: 비어 있지 않은 값만 남긴다.
 */
export function syncHelper10(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}
