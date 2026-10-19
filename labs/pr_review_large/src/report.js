// 이의 제기 목록 보고서 · 차이 큰 순
export function report(results) {
  const disputes = results.filter((r) => r.dispute);
  disputes.sort((a, b) => String(b.diff).localeCompare(String(a.diff)));
  const total = disputes.reduce((s, r) => s + r.diff, 0);
  const lines = disputes.map((r) => `| ${r.id} | ${r.expected} | ${(r.diff * 100).toFixed(1)}% |`);
  return ["| 운송번호 | 정산액 | 차이 |", "|---|---|---|", ...lines, `이의 제기 ${disputes.length}건 · 차이 합계 ${total}`].join("\n");
}
/**
 * reportHelper1: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function reportHelper1(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * reportHelper2: 금액을 천 단위 쉼표 문자열로.
 */
export function reportHelper2(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * reportHelper3: 배열을 키별로 묶는다.
 */
export function reportHelper3(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * reportHelper4: 두 날짜 사이 일수 (UTC 기준).
 */
export function reportHelper4(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * reportHelper5: 비어 있지 않은 값만 남긴다.
 */
export function reportHelper5(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}

/**
 * reportHelper6: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function reportHelper6(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * reportHelper7: 금액을 천 단위 쉼표 문자열로.
 */
export function reportHelper7(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * reportHelper8: 배열을 키별로 묶는다.
 */
export function reportHelper8(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * reportHelper9: 두 날짜 사이 일수 (UTC 기준).
 */
export function reportHelper9(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * reportHelper10: 비어 있지 않은 값만 남긴다.
 */
export function reportHelper10(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}
