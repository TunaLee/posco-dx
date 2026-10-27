# 미니 깃 · 팀 코드 리뷰 (실습용 가상 자료)

미니 깃(`server.py` · http://127.0.0.1:8900)은 내 PC 안의 작은 GitHub. 리뷰용 팀 저장소 `shop` 에 팀원 PR 12개가 있다.
내가 만든 코드도 브랜치로 push 해서 PR 로 리뷰 · 병합한다.

## 저장소
- 리뷰용: `git clone http://127.0.0.1:8900/shop.git`
- 내 코드: `git remote add team http://127.0.0.1:8900/<이름>.git` → main 이 아닌 브랜치를 push 하면 PR
- 미니 깃 화면을 고칠 때는 `web/` 에 페이지를 더한다 · `server.py` 의 git 처리 부분은 건드리지 않는다

## 파일 위치
- 리뷰 결과 `data/reviews.json` · 그 밖의 기록 `data/`
- MCP 서버 `mcp/` · Hook `hooks/` · 테스트 `tests/` · 파이썬 표준 라이브러리만

## 리뷰 원칙
- 지적에는 근거 줄 · 고칠 방법 · 근거가 없으면 쓰지 않는다
- 승인 · 병합은 사람이 미니 깃 화면에서 한다
- `repos/` 는 저장소 원본 · 직접 고치지 않는다 (git push 로만)
