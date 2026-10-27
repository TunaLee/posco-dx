# 하네스 엔지니어링 실습

> ※ 사람 · 코드 · PR 은 모두 실습용 가상 자료입니다.

준비된 것은 **리뷰용 더미 코드**(`review_lab/`)와 **미니 깃 뼈대**(`mini_git/` · 내 PC 안의 작은 GitHub)다.
Ch2 에서 더미 코드로 `.claude/`(Skill · Agent · Hook)를 Claude 와 함께 만들고, Ch3 부터 미니 깃 위에서 기능 · MCP 서버를 만들어 push 하고 팀원 PR 을 리뷰한다.

## 준비 (한 번만)

1. **Claude Code 설치 · 로그인** — 회사 Business(Team) 계정. 확인: `claude --version` · `claude auth status`
2. **Python 3.10 이상** — 표준 라이브러리만 쓴다. 설치할 패키지 없음.
3. VS Code 로 `mini_git/` 을 열고 켠다: `python server.py` (Windows 는 `py`) → http://127.0.0.1:8900

- 터미널에 `ANTHROPIC_API_KEY` 가 있으면 API 요금으로 돈다. 회사 계정으로 돌리려면 비워 둔다.

## 실습 흐름

- Ch2 실습 2-1 · 2-2: `review_lab/README.md`
- Ch3 ~ Ch9: `mini_git/README.md`
- 막히면 각 폴더의 `solution/` (강사용 완성본)

## 폴더

| 폴더 | 내용 |
|---|---|
| `review_lab/` | Ch2 · 리뷰용 더미 코드 · 완성본(`solution/dot_claude/`) |
| `mini_git/` | 미니 깃 뼈대 · 리뷰용 팀 PR(`seed/`) · 계산 도구(`tools/`) · 완성본(`solution/`) |
| `agent_watch/` | Ch6 · Ch7 · 에이전트 실행 타임라인 · 토큰 대시보드 |
| `meta_harness/` · `samples/` | Ch9 실습 9-1 · 내 업무 하네스 |
