# 하네스 엔지니어링 · 평가와 검증

POSCO DX 강의 슬라이드와 실습 저장소.

- 슬라이드: https://tunalee.github.io/posco-dx/ (← → 이동 · PDF 버튼)
- 다시 만들기: `python3 src/build.py` → `docs/index.html`
- 구성: `src/hx.py` (본문) · 도해 `src/viz_hx.py` · 장면 `src/scenes_*.py` · 그림 부품 `src/art.py`
- 배포: main에 push하면 GitHub Actions(`.github/workflows/pages.yml`)가 Pages로 올린다.

## 실습 (`labs/`)

엔진은 Claude Code 헤드리스(`claude -p`). Business 계정 로그인으로 돌고 API 키는 필요 없다. 모든 스크립트에 `--dry-run`(호출 없이 저장된 출력) · `--show-cmd`(실제 명령 보기)가 있다.

| 실습 | 폴더 |
|---|---|
| 1-1 맨몸 vs 하네스 | `labs/lab1_harness_vs_bare` |
| 2-1 Skill · 명령 · Sub Agent · Hook | `labs/lab2_claude_code_parts` |
| 3-1 컨텍스트 실험 | `labs/lab3_context` |
| 4-1 공개 하네스 비교 (Superpowers · gstack) | `labs/lab4_public_harness` |
| 5-1 멀티에이전트 + 타임라인 | `labs/lab5_multiagent` |
| 6-1 토큰 절감 (caveman · ponytail · rtk) | `labs/lab6_tokens` |
| 7-1 평가셋 · 회귀 테스트 | `labs/lab7_eval_regression` |
| 8-1 내 하네스 플러그인 | `labs/lab8_final_plugin` |
| 심화: Agent SDK (API 키 필요) | `labs/sdk_optional` |

설치와 실행은 `labs/README.md`.

모든 사람 · 회사 · 데이터 예시는 교육용 가상 자료다.
