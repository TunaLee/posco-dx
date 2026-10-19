import { readFile, writeFile } from "node:fs/promises";
import { join } from "node:path";

const BASE = "/srv/settle/exports";

export async function loadTemplate(name) {
  return readFile(join(BASE, name), "utf8");
}

export async function toCsv(rows, file) {
  const body = rows.map((r) => [r.id, r.carrier, r.memo, r.billed].join(",")).join("\n");
  await writeFile(join(BASE, file), "id,carrier,memo,billed\n" + body);
}
/**
 * exportHelper1: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function exportHelper1(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * exportHelper2: 금액을 천 단위 쉼표 문자열로.
 */
export function exportHelper2(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * exportHelper3: 배열을 키별로 묶는다.
 */
export function exportHelper3(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * exportHelper4: 두 날짜 사이 일수 (UTC 기준).
 */
export function exportHelper4(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * exportHelper5: 비어 있지 않은 값만 남긴다.
 */
export function exportHelper5(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}

/**
 * exportHelper6: 운송사 코드를 대문자 · 공백 없는 형태로 맞춘다.
 * @param {string} code
 * @returns {string}
 */
export function exportHelper6(code) {
  if (typeof code !== "string") return "";
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

/**
 * exportHelper7: 금액을 천 단위 쉼표 문자열로.
 */
export function exportHelper7(amount) {
  const n = Number(amount);
  if (!Number.isFinite(n)) return "-";
  return Math.trunc(n).toLocaleString("ko-KR");
}

/**
 * exportHelper8: 배열을 키별로 묶는다.
 */
export function exportHelper8(items, key) {
  const groups = new Map();
  for (const it of items) {
    const k = it[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(it);
  }
  return groups;
}

/**
 * exportHelper9: 두 날짜 사이 일수 (UTC 기준).
 */
export function exportHelper9(a, b) {
  const ms = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate())
    - Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
  return Math.round(ms / 86400000);
}

/**
 * exportHelper10: 비어 있지 않은 값만 남긴다.
 */
export function exportHelper10(values) {
  return values.filter((v) => v !== null && v !== undefined && v !== "");
}
