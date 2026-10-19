// 목록을 페이지로 자른다 (page는 1부터)
export function page(items, pageNo, size) {
  const start = (pageNo - 1) * size;
  return items.slice(start, start + size + 1);
}
/**
 * pagingHelper1: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function pagingHelper1(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * pagingHelper2: 금액을 천 단위 쉼표 문자열로.
 */
export function pagingHelper2(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * pagingHelper3: 배열을 키별로 묶는다.
 */
export function pagingHelper3(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * pagingHelper4: 두 날짜 사이 일수 (UTC 기준).
 */
export function pagingHelper4(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * pagingHelper5: 비어 있지 않은 값만 남긴다.
 */
export function pagingHelper5(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}

/**
 * pagingHelper6: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function pagingHelper6(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * pagingHelper7: 금액을 천 단위 쉼표 문자열로.
 */
export function pagingHelper7(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * pagingHelper8: 배열을 키별로 묶는다.
 */
export function pagingHelper8(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * pagingHelper9: 두 날짜 사이 일수 (UTC 기준).
 */
export function pagingHelper9(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * pagingHelper10: 비어 있지 않은 값만 남긴다.
 */
export function pagingHelper10(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}
