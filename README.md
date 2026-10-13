# 하네스 엔지니어링 · 평가와 검증

AX 심화 과정 강의 슬라이드와 실습 저장소. 판교 · 포항 두 판본을 같은 소스에서 만든다.

- 슬라이드: `docs/pangyo/`, `docs/pohang/` (브라우저로 열기 · ← → 이동 · PDF 버튼)
- 다시 만들기: `python3 src/build.py` (판교 · 포항 둘 다) · `python3 src/build.py pangyo`
- 구성: `src/harness.py` (판본 차이는 `V == "pangyo"` 분기) · 그림 부품 `src/art.py` · 장면 `src/scenes_*.py`
- 실습: `labs/` — 설치와 실행은 `labs/README.md`
- 배포: main에 push하면 GitHub Actions(`.github/workflows/pages.yml`)가 Pages로 올린다.

모든 사람 · 회사 · 데이터 예시는 교육용 가상 자료다.
