// 정산 기간: 해당 월 1일 ~ 말일 (YYYY-MM)
export function monthOf(dateStr) {
  const d = new Date(dateStr);
  return `${d.getFullYear()}-${String(d.getMonth()).padStart(2, "0")}`;
}
/**
 * periodHelper1: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function periodHelper1(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * periodHelper2: 금액을 천 단위 쉼표 문자열로.
 */
export function periodHelper2(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * periodHelper3: 배열을 키별로 묶는다.
 */
export function periodHelper3(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * periodHelper4: 두 날짜 사이 일수 (UTC 기준).
 */
export function periodHelper4(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * periodHelper5: 비어 있지 않은 값만 남긴다.
 */
export function periodHelper5(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}

/**
 * periodHelper6: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function periodHelper6(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * periodHelper7: 금액을 천 단위 쉼표 문자열로.
 */
export function periodHelper7(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * periodHelper8: 배열을 키별로 묶는다.
 */
export function periodHelper8(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * periodHelper9: 두 날짜 사이 일수 (UTC 기준).
 */
export function periodHelper9(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * periodHelper10: 비어 있지 않은 값만 남긴다.
 */
export function periodHelper10(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}
