---
name: build
description: 승인된 design.md대로 하네스 파일을 만들 때.
---

# build

1. docs/<이름>/APPROVED 가 있는지 확인 — 없으면 멈춘다
2. 대상 폴더(사용자가 정한 곳, 없으면 out/<이름>/)에 design.md 그대로:
   CLAUDE.md · .claude/skills/ · .claude/agents/ · .claude/hooks/ + .claude/settings.json · eval/cases.jsonl
3. 설계에 없는 규칙은 넣지 않는다 · 모르는 값은 TODO
4. 만든 파일 목록과 각 파일이 design.md 어느 줄에서 왔는지 표로
