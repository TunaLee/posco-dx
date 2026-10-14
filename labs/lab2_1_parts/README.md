# 실습 2-1 · 하네스 부품 (Skill · Sub Agent · Hook)

처음에는 `.claude/` 가 없다 (하네스 미적용). 장표 「실습 2-1 하네스」의 파일 네 개를 같은 경로로 만든 뒤 같은 요청을 다시 한다.

| 부품 | 경로 |
|---|---|
| Skill | `.claude/skills/incident-report/SKILL.md` |
| Sub Agent | `.claude/agents/reviewer.md` |
| Hook 등록 | `.claude/settings.json` |
| Hook 코드 | `.claude/hooks/guard.py` |

Windows 에서 `python3` 가 안 잡히면 `settings.json` 의 `python3` 을 `python` 으로.
