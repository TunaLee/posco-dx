export function report(results) {
  const disputes = results.filter((r) => r.dispute);
  const total = disputes.reduce((s, r) => s + r.diff, 0);
  const lines = disputes.map((r) => `| ${r.id} | ${r.expected} | ${(r.diff * 100).toFixed(1)}% |`);
  return ["| 운송번호 | 정산액 | 차이 |", "|---|---|---|", ...lines, `이의 제기 ${disputes.length}건 · 차이 합계 ${total}`].join("\n");
}
