# 운송비 정산 검증 CLI · 루프 하네스

Node.js · 외부 패키지 없음 · ES 모듈 · 테스트는 `node --test` (test/*.test.js)
자료: data/운송비청구.csv · data/정산기준.md

## 한 번 실행할 때마다
1. progress.md 와 git log 로 지금까지 한 일을 확인한다
2. features.json 에서 passes 가 false 인 첫 기능 하나만 고른다 (두 개 이상 하지 않는다)
3. 테스트를 먼저 쓰고 실패를 확인 → 구현 → npm test 전체 통과
4. 통과했을 때만 그 기능의 passes 를 true 로 · progress.md 에 한 줄 · git commit
5. 막히면 passes 는 그대로 두고 progress.md 에 막힌 이유를 남긴다

## 금지
- features.json 의 설명 · 확인 항목을 고치거나 지우지 않는다 (passes 만 바꾼다)
- 테스트를 지우거나 건너뛰게 바꾸지 않는다
- data/ 원본을 고치지 않는다
