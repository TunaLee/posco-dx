---
name: try
description: 만든 하네스를 예시 입력으로 시험할 때.
---

# try

1. 대상 폴더의 eval/cases.jsonl 입력마다
   - 하네스 미적용: 빈 임시 폴더에서 claude -p --setting-sources ""
   - 하네스 적용: 대상 폴더에서 claude -p --setting-sources project
2. 결과를 runs/<이름>/ 에 저장하고 표로: 입력 · 기대 결과 · 미적용 · 적용
3. 합격 판정은 하지 않는다 — 사람이 표를 보고 판정한다
