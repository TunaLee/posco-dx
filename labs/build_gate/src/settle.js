// 운송비 정산 · 청구 검증
export function settle(row) {
  return Math.round(row.distance * row.weight * row.unitPrice);
}

export function check(row) {
  const expected = settle(row);
  const diff = Math.abs(row.billed - expected) / expected;
  return { expected, diff, dispute: diff >= 0.01 };
}

export function checkAll(rows) {
  const out = [];
  for (const r of rows) {
    // 같은 운송번호가 두 번 들어오면 한 번만
    let dup = false;
    for (const o of out) if (o.id === r.id) dup = true;
    if (!dup) out.push({ id: r.id, ...check(r) });
  }
  return out;
}
