---
name: code-review
description: 팀 코드 저장소의 PR 을 리뷰할 때. 「PR 105 리뷰해 줘」 「안 본 PR 리뷰」 같은 요청에 쓴다.
---

# 코드 리뷰 절차

1. `mcp__repo__get_pr` 로 설명을 읽고, `mcp__repo__changed_functions` 로 바뀐 함수만 본다. 전체 diff 는 꼭 필요할 때만.
2. 네 가지 관점으로 본다 — 보안(비밀 키 · SQL 조립 · 권한) · 버그(경계값 · 예외 · 상태) · 성능(반복 쿼리) · 테스트(빠진 경우).
3. 보안이 의심되면 `security-reviewer` Agent 에게 맡기고 결과만 받는다.
4. 지적마다 근거 줄을 붙인다. 근거가 없으면 쓰지 않는다. 문제가 없으면 「지적 없음」.
5. `data/reviews.json` 에 아래 형식으로 덧붙이고, `mcp__repo__add_comment` 로 PR 에 요약 한 줄을 남긴다.
6. 승인 · 병합은 하지 않는다 (사람이 한다).

## 형식 (data/reviews.json 의 한 항목)
{"pr": 105, "kind": "보안|버그|성능|테스트", "file": "shop/payment.py", "title": "API 키 하드코딩", "detail": "근거 줄 · 고칠 방법"}

## 코멘트 예시 (사람이 고른 좋은 예 · 실습 8-2 에서 늘어남)
- 「`offset = page * size` — page 가 1부터라 첫 페이지를 건너뜁니다. `(page - 1) * size` 로 바꾸고 1 · 2페이지 테스트를 추가해 주세요.」
