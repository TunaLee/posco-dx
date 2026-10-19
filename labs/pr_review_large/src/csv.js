// 청구 CSV 한 줄 → 객체 (거리 · 중량 · 단가 · 청구액은 숫자)
export function parseLine(line) {
  const [id, carrier, distance, weight, unitPrice, billed] = line.split(",");
  return {
    id, carrier,
    distance: parseInt(distance),
    weight: parseFloat(weight),
    unitPrice: parseInt(unitPrice),
    billed: parseInt(billed),
  };
}
/**
 * csvHelper1: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function csvHelper1(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * csvHelper2: 금액을 천 단위 쉼표 문자열로.
 */
export function csvHelper2(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * csvHelper3: 배열을 키별로 묶는다.
 */
export function csvHelper3(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * csvHelper4: 두 날짜 사이 일수 (UTC 기준).
 */
export function csvHelper4(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * csvHelper5: 비어 있지 않은 값만 남긴다.
 */
export function csvHelper5(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}

/**
 * csvHelper6: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function csvHelper6(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * csvHelper7: 금액을 천 단위 쉼표 문자열로.
 */
export function csvHelper7(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * csvHelper8: 배열을 키별로 묶는다.
 */
export function csvHelper8(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * csvHelper9: 두 날짜 사이 일수 (UTC 기준).
 */
export function csvHelper9(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * csvHelper10: 비어 있지 않은 값만 남긴다.
 */
export function csvHelper10(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}

/**
 * csvHelper11: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function csvHelper11(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * csvHelper12: 금액을 천 단위 쉼표 문자열로.
 */
export function csvHelper12(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}
