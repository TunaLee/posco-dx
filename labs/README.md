# 하네스 엔지니어링 실습

> ※ 사람 · 코드 · PR 은 모두 실습용 가상 자료입니다.

준비된 것은 **팀 코드 저장소 서버뿐**이다. 앱은 Claude Code 와 함께 처음부터 만들고, 실습마다 탭이 하나씩 늘어난다.

## 준비 (한 번만)

1. **Claude Code 설치 · 로그인** — 회사 Business(Team) 계정. 확인: `claude --version` · `claude auth status`
2. **Python 3.10 이상** — 표준 라이브러리만 쓴다. 설치할 패키지 없음.
3. VS Code 로 `code_review/` 를 열고 저장소 서버를 켠다: `python repo/server.py` (Windows 는 `py`)

- 터미널에 `ANTHROPIC_API_KEY` 가 있으면 API 요금으로 돈다. 회사 계정으로 돌리려면 비워 둔다.

## 실습마다 생기는 탭

`code_review/README.md` 참고. 막히면 `code_review/solution/` (강사용 완성본).

## 폴더

| 폴더 | 내용 |
|---|---|
| `code_review/` | 팀 코드 저장소(`repo/`) · 완성본(`solution/`) · 실습 내내 이 폴더 하나 |
| `agent_watch/` | Ch6 · Ch7 · 에이전트 실행 타임라인 · 토큰 대시보드 |
| `meta_harness/` · `samples/` | Ch9 실습 9-1 · 내 업무 하네스 |
