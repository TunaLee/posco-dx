# 코드 리뷰 하네스 — `.claude/` 를 Claude 와 함께 만들기

> ※ 코드는 실습용 더미다. 일부러 문제를 심어 두었다 · 실제로 돌리지 않는다.

이 폴더를 VS Code 로 열고 Claude Code 에게 리뷰를 맡긴다. 하네스(`.claude/`)는 처음엔 없다 — Claude 와 함께 하나씩 만든다.

| 실습 | Claude 에게 (짧게) | 생기는 것 |
|---|---|---|
| 2-1 ① | 「shop 코드 리뷰해 줘」 (하네스 없이) | 매번 다른 형식의 리뷰 |
| 2-1 ② | 「코드 리뷰 절차를 Skill 로 만들어 줘」 | `.claude/skills/code-review/SKILL.md` |
| 2-1 ③ | 「보안 검토 Sub Agent 를 만들어 줘」 | `.claude/agents/security-reviewer.md` |
| 2-1 ④ | 새 대화: 「shop 코드 리뷰해 줘」 | 같은 형식 · `out/review.md` |
| 2-2 ① | 「리뷰하고 바로 고쳐 줘」 | 코드가 고쳐짐 (리뷰어가 고쳐 버림) |
| 2-2 ② | 「리뷰 중에는 shop/ · tests/ 를 못 고치게 Hook 으로 막아 줘」 | `.claude/settings.json` · `.claude/hooks/` |
| 2-2 ③ | 새 대화: 「리뷰하고 바로 고쳐 줘」 | 막힘 · 이유 한 줄 · 리뷰만 |

- `.claude/` 쓰기는 Claude Code 가 승인을 묻는다 → 내용을 읽고 승인
- 2-2 ① 에서 고쳐진 코드는 `git checkout -- shop` 으로 되돌린다 (처음에 `git init` · 첫 커밋 해 두기)
- 막히면 `solution/` → `dot_claude/` 를 `.claude/` 로 복사
- 여기서 만든 `.claude/` 는 Ch4 미니 깃 실습에 그대로 가져간다
