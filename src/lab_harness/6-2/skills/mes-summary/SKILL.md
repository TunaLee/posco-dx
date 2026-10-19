---
name: mes-summary
description: MES 장애 로그를 코드별로 집계하거나 장애 코드의 처리 기준을 찾을 때.
---

# mes-summary

1. `python3 .claude/skills/mes-summary/summary.py data/mes_장애로그_1주.csv data/MES_장애대응_매뉴얼.md` 한 번 실행
2. 출력(코드별 건수 · 지속 시간 합계 · 최다 코드의 처리 기준)을 그대로 요약해 답한다
3. 스크립트가 실패할 때만 파일을 직접 본다
