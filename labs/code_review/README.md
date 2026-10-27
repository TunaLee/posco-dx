# 팀 코드 리뷰 — 하네스를 한 프로젝트에 쌓아 가기

> ※ 사람 · 코드 · PR 은 모두 실습용 가상 자료입니다.

준비된 것은 **팀 코드 저장소 서버(`repo/`)** 와 실습 3-1 용 **계산 도구(`tools/calc_server.py`)** 뿐이다. 작은 주문 · 정산 서비스(`shop/`)에 팀원 4명이 PR 12개를 올려 둔 상태다.
리뷰 콘솔 · MCP 서버 · Skill · Hook · 채점기는 모두 Claude Code 로 이 폴더에 만들어 간다. 실습 하나를 마칠 때마다 콘솔에 탭이 하나씩 생긴다.

> **`repo/` 는 저장소 원본이다 — 읽기만 하고 고치지 않는다.** 기록 · 결과는 `data/` 에 둔다.

## 처음 한 번 — 저장소 서버 켜기

```
python repo/server.py          # http://127.0.0.1:8900 · 끄려면 Ctrl+C
```

| 주소 | 내용 |
|---|---|
| `GET /api/prs` · `/api/prs/104` | PR 목록 · 한 건 |
| `GET /api/prs/104/diff` · `/files` | 변경 내용 · 바뀐 파일 전체 |
| `GET · POST /api/prs/104/comments` | 리뷰 코멘트 |
| `POST /api/prs/104/approve` · `/merge` | 승인 · 병합 (실습 4-2 에서 Hook 으로 막음) |
| `GET /api/answer` | 심어 둔 문제 목록 — **채점용 · 리뷰할 때 보지 않는다** |

## 실습마다 생기는 탭

| 실습 | Claude 에게 (짧게) | 콘솔 |
|---|---|---|
| 2-1 | Superpowers 로 「PR 을 보는 리뷰 콘솔을 만들고 싶어 · 탭 하나로 시작」 | 탭 ① PR 목록 |
| 3-1 | `claude mcp add calc -- python tools/calc_server.py` → 「calc 도구로 계산해 줘」 | 호출 표시 확인 |
| 3-2 | 「팀 코드 저장소 API 를 MCP 서버로 만들어 연결해 줘」 | 탭 ② 도구 호출 |
| 4-1 | 「코드 리뷰 절차를 Skill 로」 · 「보안 검토 Sub Agent」 | 탭 ③ 리뷰 |
| 4-2 | 「승인 · 병합은 Hook 으로 막고 막은 기록을 탭으로」 | 탭 ④ 막은 기록 |
| 5-1 | 「바뀐 함수만 돌려주는 도구를 추가해 줘」 | 탭 ② 응답 크기 비교 |
| 6-1 | 「보안 · 버그 · 테스트 리뷰어와 검증 Agent 팀으로」 | 탭 ⑤ 종합 리뷰 |
| 7-1 | 「같은 걸 찾는 검사 스크립트를 만들고 결과만 보고 판단해 줘」 | 토큰 비교 |
| 8-1 | 「리뷰 결과를 /api/answer 정답과 대조해 채점해 줘」 | 탭 ⑥ 채점 |
| 8-2 | 리뷰 초안 → 내가 고침 → 「고친 부분을 Skill 에 반영해 줘」 × 3 | 고친 양 감소 |
| 9-2 | 「기능을 하나씩 새 세션으로 구현해 탭으로 붙이는 루프」 | 탭 ⑦ ~ ⑪ |

## 막히면 — `solution/` (강사용 완성본)

| 파일 | 쓰는 실습 |
|---|---|
| `CLAUDE.md` · `app/` (콘솔 · 탭 ① ~ ⑥) | 2-1 · 탭이 막히면 그 탭 파일만 `app/tabs/` 로 |
| `mcp_server.py` | 3-2 · 5-1 · `claude mcp add repo -- python solution/mcp_server.py` |
| `dot_claude/` (Skill · Agent · settings) · `hooks/merge_guard.py` | 4-1 · 4-2 · 6-1 · `.claude/` 로 복사 |
| `checks.py` | 7-1 |
| `grade.py` · `tests/` | 8-1 |
| `features.json` · `PROMPT.md` · `progress.md` · `loop.py` | 9-2 · 이 폴더 맨 위로 복사 후 `python loop.py 5` |

- Windows 에서 `python` 이 없다고 나오면 `py` 로 실행한다.
- 저장소 서버가 꺼져 있으면 MCP 도구가 「연결 거부」 오류를 돌려준다 — 서버부터 켠다.
