# 팀 코드 리뷰 (실습용 가상 자료)

팀 코드 저장소(`repo/` · http://127.0.0.1:8900)의 PR 을 리뷰하는 프로젝트. 실습마다 리뷰 콘솔에 탭을 하나씩 붙인다.

## 콘솔
- `python app/server.py` → http://127.0.0.1:8810
- 탭 하나 = `app/tabs/` 의 HTML 파일 하나 · 이름은 `번호_이름.html` (다음 번호로) · `<title>` 이 탭 이름
- 탭은 `/repo/...`(저장소 API) · `/files/data/...` 만 읽는다 · `app/server.py` · `app/index.html` 은 고치지 않는다

## 파일 위치
- 기록(JSON · JSONL): `data/` · 리뷰 결과 `data/reviews.json`
- MCP 서버 `mcp_server.py` · Hook `hooks/` · 기능 `reports/` · 테스트 `tests/`
- 파이썬 표준 라이브러리만

## 리뷰 원칙
- 지적에는 근거 줄 · 고칠 방법 · 근거가 없으면 쓰지 않는다
- 승인 · 병합은 사람이 한다
- `repo/` 는 저장소 원본 · 고치지 않는다 · `/api/answer` 는 채점용 · 리뷰할 때 보지 않는다
