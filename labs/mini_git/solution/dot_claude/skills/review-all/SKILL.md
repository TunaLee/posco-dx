---
name: review-all
description: PR 여러 개를 한꺼번에 리뷰할 때. 「열린 PR 전부 리뷰」 「PR 101~112 리뷰」 같은 요청에 쓴다. Sub Agent 여러 개로 동시에 돌린다.
---

# 병렬 리뷰 (오케스트레이터)

메인은 나누고 합치기만 한다. 코드를 직접 읽지 않는다.

1. `mcp__repo__list_pull_requests` 로 리뷰할 PR 목록을 받는다.
2. PR 을 3~4개씩 묶는다 (Sub Agent 하나당 한 묶음).
3. 묶음마다 `code-reviewer` Agent 를 **한 메시지에서 동시에** 띄운다. 위임문에 넣을 것:
   - 목표: 맡은 PR 들을 code-review Skill 절차대로 리뷰하고 PR 마다 코멘트
   - 범위: 맡은 PR 번호만
   - 반환 형식: PR 마다 한 줄 — `#번호 · 🔴N 🟡N ⚪N · 가장 큰 문제 한 줄`
4. 모두 끝나면 결과를 합쳐 `out/review_all.md` 에 PR 별 표 + 맨 위 요약 한 줄로 저장한다.
5. 승인 · 병합은 하지 않는다.
