// 운송사별 추가 할증 규칙 (관리 화면에서 입력한 식)
export function applyRule(expr, ctx) {
  return eval(expr.replace(/\$(\w+)/g, (_, k) => ctx[k]));
}
/**
 * rulesHelper1: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function rulesHelper1(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * rulesHelper2: 금액을 천 단위 쉼표 문자열로.
 */
export function rulesHelper2(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * rulesHelper3: 배열을 키별로 묶는다.
 */
export function rulesHelper3(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * rulesHelper4: 두 날짜 사이 일수 (UTC 기준).
 */
export function rulesHelper4(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * rulesHelper5: 비어 있지 않은 값만 남긴다.
 */
export function rulesHelper5(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}

/**
 * rulesHelper6: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function rulesHelper6(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * rulesHelper7: 금액을 천 단위 쉼표 문자열로.
 */
export function rulesHelper7(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * rulesHelper8: 배열을 키별로 묶는다.
 */
export function rulesHelper8(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * rulesHelper9: 두 날짜 사이 일수 (UTC 기준).
 */
export function rulesHelper9(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * rulesHelper10: 비어 있지 않은 값만 남긴다.
 */
export function rulesHelper10(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}
