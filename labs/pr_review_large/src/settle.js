// 운송비 정산 · 청구 검증
export function settle(row) {
  return Math.round(row.distance * row.weight * row.unitPrice);
}

export function check(row) {
  const expected = settle(row);
  const diff = Math.abs(row.billed - expected) / expected;
  return { expected, diff, dispute: diff >= 0.01 };
}
/**
 * settleHelper1: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function settleHelper1(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * settleHelper2: 금액을 천 단위 쉼표 문자열로.
 */
export function settleHelper2(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * settleHelper3: 배열을 키별로 묶는다.
 */
export function settleHelper3(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * settleHelper4: 두 날짜 사이 일수 (UTC 기준).
 */
export function settleHelper4(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * settleHelper5: 비어 있지 않은 값만 남긴다.
 */
export function settleHelper5(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}

/**
 * settleHelper6: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function settleHelper6(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * settleHelper7: 금액을 천 단위 쉼표 문자열로.
 */
export function settleHelper7(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * settleHelper8: 배열을 키별로 묶는다.
 */
export function settleHelper8(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * settleHelper9: 두 날짜 사이 일수 (UTC 기준).
 */
export function settleHelper9(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * settleHelper10: 비어 있지 않은 값만 남긴다.
 */
export function settleHelper10(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}

/**
 * settleHelper11: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function settleHelper11(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * settleHelper12: 금액을 천 단위 쉼표 문자열로.
 */
export function settleHelper12(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}
