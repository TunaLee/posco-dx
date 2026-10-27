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

## 실습 흐름

| 실습 | Claude 에게 (짧게) | 미니 깃에서 보이는 것 |
|---|---|---|
| 3-1 | Superpowers 로 「미니 깃에 PR 리뷰 현황 페이지를 추가하고 싶어」 | 새 페이지 · 내 PR |
| 4-1 | `claude mcp add calc -- python tools/calc_server.py` → 「calc 도구로 계산해 줘」 | 호출 표시 |
| 4-2 | 「Microsoft Learn MCP(https://learn.microsoft.com/api/mcp)를 연결해 줘」 → `/mcp` 로 도구 보기 | 호출 표시 · 출처 |
| 4-3 | 「GitHub MCP 와 같은 도구 이름으로 미니 깃 MCP 서버를 만들어 연결해 줘」 | MCP 서버 코드 PR |
| 4-4 | Ch2 의 `.claude/` 를 가져와 「코드 리뷰 절차를 Skill 로」 · 「shop PR 105 리뷰하고 코멘트 남겨 줘」 | PR 화면에 코멘트 |
| 4-5 | 「승인 · 병합은 Hook 으로 막아 줘」 | Claude 병합 0건 · 사람이 버튼으로 |
| 5-1 | 「바뀐 함수만 돌려주는 도구를 추가해 줘」 | 응답 크기 비교 |
| 6-1 | 「PR 을 나눠 Sub Agent 여러 개가 동시에 리뷰하고 합치는 Skill 을 만들어 줘」 | 순차 vs 병렬 시간 · PR 코멘트 |
| 7-1 | 「같은 걸 찾는 검사 스크립트를 만들고 결과만 보고 판단해 줘」 | 토큰 비교 |
| 8-1 | 「작성자별 PR 현황 페이지를 만들어 PR 로 올려 줘」 → 화면 보고 PR 에 수정 요청 → 반영 | PR 에 요청 · 반영 이력 |
| 8-2 | 「받은 수정 요청을 하네스에 반영해 줘」 → 다음 기능 PR | PR별 수정 요청 수 감소 |

## 막히면 — `solution/` (강사용 완성본)

| 파일 | 쓰는 실습 |
|---|---|
| `web/review.html` | 3-1 · `web/` 로 복사 → `/web/review.html` |
| `mcp_server.py` | 4-3 · 5-1 · `claude mcp add repo -- python solution/mcp_server.py` |
| `dot_claude/` (Skill · Agent · settings) · `hooks/merge_guard.py` | 4-4 · 4-5 · 6-1 · `.claude/` 로 복사 |
| `checks.py` | 7-1 |

- Windows 는 `python` 대신 `py` · Git for Windows 에 필요한 기능이 들어 있다
- 처음부터 다시: 서버를 끄고 `repos/` 폴더를 지운 뒤 다시 켠다
