# 미니 깃 — 내 PC 안의 작은 GitHub

> ※ 사람 · 코드 · PR 은 모두 실습용 가상 자료입니다.

실습 뼈대다. 켜면 git 원격 저장소 · PR 화면 · API 가 한 번에 뜬다.
그 위에 Claude Code 로 기능을 더하고, MCP 서버를 만들고, 내 코드를 push 하고, 팀원 PR 을 리뷰한다.

```
python server.py               # http://127.0.0.1:8900 · 처음 켜면 shop.git(팀원 PR 12개)을 만든다
```

## git 으로 쓰기

```
git clone http://127.0.0.1:8900/shop.git                      # 리뷰용 팀 저장소
git remote add team http://127.0.0.1:8900/my-tools.git        # 내 코드 · 처음 push 하면 저장소가 생김
git push team main
git checkout -b feature/calc && git push team feature/calc    # main 이 아닌 브랜치 = PR
```

- 화면: `/` 저장소 · `/r/shop` PR 목록 · `/r/shop/pr/104` 변경 내용 · 코멘트 · 승인 · 병합 버튼
- 병합은 서버가 실제로 `git merge` → `git pull team main` 으로 받는다
- 로그인 없음 · `127.0.0.1` 이라 내 PC 에서만 접속

## API (MCP 서버가 쓰는 곳)

| 주소 | 내용 |
|---|---|
| `GET /api/repos` | 저장소 목록 |
| `GET /api/repos/shop/prs` · `/prs/104` | PR 목록 · 한 건 |
| `GET /api/repos/shop/prs/104/diff` · `/files` | 변경 내용 · 바뀐 파일 전체 |
| `GET · POST /api/repos/shop/prs/104/comments` | 리뷰 코멘트 |
| `POST /api/repos/shop/prs/104/approve` · `/merge` | 승인 · 병합 (실습 4-2 에서 Claude 는 Hook 으로 막음) |
| `GET /api/answer` | shop 에 심어 둔 문제 — **채점용 · 리뷰할 때 보지 않는다** |

## 실습 흐름

| 실습 | Claude 에게 (짧게) | 미니 깃에서 보이는 것 |
|---|---|---|
| 2-1 | Superpowers 로 「미니 깃에 PR 리뷰 현황 페이지를 추가하고 싶어」 | 새 페이지 · 내 PR |
| 3-1 | `claude mcp add calc -- python tools/calc_server.py` → 「calc 도구로 계산해 줘」 | 호출 표시 |
| 3-2 | 「미니 깃 API 를 MCP 서버로 만들어 연결해 줘」 | MCP 서버 코드 PR |
| 4-1 | 「코드 리뷰 절차를 Skill 로」 · 「shop PR 105 리뷰하고 코멘트 남겨 줘」 | PR 화면에 코멘트 |
| 4-2 | 「승인 · 병합은 Hook 으로 막아 줘」 | Claude 병합 0건 · 사람이 버튼으로 |
| 5-1 | 「바뀐 함수만 돌려주는 도구를 추가해 줘」 | 응답 크기 비교 |
| 6-1 | 「보안 · 버그 · 테스트 리뷰어와 검증 Agent 팀으로」 | PR마다 종합 코멘트 |
| 7-1 | 「같은 걸 찾는 검사 스크립트를 만들고 결과만 보고 판단해 줘」 | 토큰 비교 |
| 8-1 | 「리뷰 결과를 /api/answer 정답과 대조해 채점해 줘」 | 채점 페이지 |
| 8-2 | 리뷰 초안 → 내가 고침 → 「고친 부분을 Skill 에 반영해 줘」 × 3 | 고친 양 감소 |
| 9-2 | 「기능을 하나씩 새 세션으로 구현해 브랜치로 push 하는 루프」 | PR 다섯 개 · 사람이 병합 |

## 막히면 — `solution/` (강사용 완성본)

| 파일 | 쓰는 실습 |
|---|---|
| `web/review.html` | 2-1 · `web/` 로 복사 → `/web/review.html` |
| `mcp_server.py` | 3-2 · 5-1 · `claude mcp add repo -- python solution/mcp_server.py` |
| `dot_claude/` (Skill · Agent · settings) · `hooks/merge_guard.py` | 4-1 · 4-2 · 6-1 · `.claude/` 로 복사 |
| `checks.py` | 7-1 |
| `grade.py` · `tests/` | 8-1 |
| `CLAUDE.md` · `features.json` · `PROMPT.md` · `progress.md` · `loop.py` | 9-2 · 이 폴더 맨 위로 복사 후 `python loop.py 5` |

- Windows 는 `python` 대신 `py` · Git for Windows 에 필요한 기능이 들어 있다
- 처음부터 다시: 서버를 끄고 `repos/` 폴더를 지운 뒤 다시 켠다
