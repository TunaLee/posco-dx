# 메타 하네스 · 상황에 맞는 하네스를 만드는 하네스

결과물: 사용자가 말한 업무 하나에 맞춘 하네스 폴더

## 순서 (건너뛰지 않는다 · 하네스마다 docs/<하네스 이름>/ 하나)
1. 인터뷰 — interview Skill → docs/<이름>/interview.md
2. 설계 — design Skill → docs/<이름>/design.md
3. 사용자 승인 — 설계 요약을 보여 주고 멈춘다. docs/<이름>/APPROVED 는 사람만 만든다
4. 생성 — build Skill → 사용자가 정한 대상 폴더 (없으면 out/<이름>/)
5. 검토 — harness-reviewer 에게 맡기고 지적 반영
6. 시험 — try Skill → 하네스 미적용 vs 적용 비교표
7. 판정은 사람 — 비교표를 보여 주고 고칠 점을 묻는다

## 원칙
- 범용 규칙을 늘어놓지 않는다. 인터뷰에 나온 것만 넣고, 모르는 값은 TODO
- 부품은 필요한 것만: 매번 지킬 원칙 → CLAUDE.md · 절차 → Skill · 어기면 사고 → Hook · 확인 → 검증 Agent · 큰 일 나누기 → Sub Agent
- 유형별 예시는 templates/README.md
