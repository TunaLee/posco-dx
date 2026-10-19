"""MES 장애 로그 코드별 집계 + 최다 코드의 처리 기준 (매뉴얼 부록 A)."""
import csv
import sys
from collections import Counter, defaultdict

log, manual = sys.argv[1], sys.argv[2]
cnt, dur = Counter(), defaultdict(int)
with open(log, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        cnt[r["코드"]] += 1
        dur[r["코드"]] += int(r["지속(분)"] or 0)
print("코드 | 건수 | 지속(분)")
for code, n in cnt.most_common():
    print(f"{code} | {n} | {dur[code]}")
top = cnt.most_common(1)[0][0]
rule = next((l.strip() for l in open(manual, encoding="utf-8") if l.strip().startswith(f"- {top}:")), "매뉴얼에 없음")
print(f"최다: {top} · 처리 기준 {rule[2:]}")
