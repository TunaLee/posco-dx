---
name: code-review
description: 변경 사항(PR · CHANGES.md)을 코드 리뷰할 때.
---

# code-review

1. CHANGES.md 와 변경 파일 목록을 읽는다
2. reviewer · qa · security Sub Agent에게 **동시에** 맡긴다 (파일 목록 · 기준 · 반환 형식 전달)
   - 변경 파일이 10개를 넘으면 reviewer는 파일 6개 안팎씩 묶어 여러 개를 동시에 띄운다
3. 돌아온 결과를 모아 중복을 합치고 심각도순(높음 · 중간 · 낮음)으로 정리한다
4. review/리뷰결과.md: | 파일:줄 | 심각도 | 분류 | 문제 | 고칠 방향 | 찾은 담당 |
