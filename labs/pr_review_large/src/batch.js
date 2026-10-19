import { check } from "./settle.js";

// 같은 운송번호가 두 번 들어오면 한 번만 검증
export function checkAll(rows) {
  const out = [];
  for (const r of rows) {
    let dup = false;
    for (const o of out) if (o.id === r.id) dup = true;
    if (!dup) out.push({ id: r.id, ...check(r) });
  }
  return out;
}
/**
 * batchHelper1: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function batchHelper1(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * batchHelper2: 금액을 천 단위 쉼표 문자열로.
 */
export function batchHelper2(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * batchHelper3: 배열을 키별로 묶는다.
 */
export function batchHelper3(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * batchHelper4: 두 날짜 사이 일수 (UTC 기준).
 */
export function batchHelper4(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * batchHelper5: 비어 있지 않은 값만 남긴다.
 */
export function batchHelper5(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}

/**
 * batchHelper6: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function batchHelper6(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * batchHelper7: 금액을 천 단위 쉼표 문자열로.
 */
export function batchHelper7(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * batchHelper8: 배열을 키별로 묶는다.
 */
export function batchHelper8(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * batchHelper9: 두 날짜 사이 일수 (UTC 기준).
 */
export function batchHelper9(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * batchHelper10: 비어 있지 않은 값만 남긴다.
 */
export function batchHelper10(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}

/**
 * batchHelper11: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function batchHelper11(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * batchHelper12: 금액을 천 단위 쉼표 문자열로.
 */
export function batchHelper12(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}
