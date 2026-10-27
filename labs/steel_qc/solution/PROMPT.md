너는 이 저장소에서 기능 하나만 구현하고 끝낸다.

1. `features.json` 에서 passes 가 false 인 첫 기능을 고른다.
2. `progress.md` 를 읽고 앞 세션이 남긴 내용을 이어 받는다.
3. 그 기능을 `reports/` 아래 파이썬 모듈로 구현한다. 판정은 앞에서 만든 판정 코드를 재사용하고(없으면 `solution/judge.py`), 데이터는 127.0.0.1:8800 시뮬레이터 API 를 쓴다.
4. `tests/` 에 그 기능의 테스트를 추가하고 `python -m unittest discover -s tests` 가 모두 통과해야 한다. 실패하면 고친다.
5. 통과하면 features.json 의 그 기능 passes 를 true 로 바꾸고, progress.md 에 한 줄 기록하고, git 커밋한다.
6. 다른 기능은 건드리지 않는다. `sim/` 과 `.claude/` 는 고치지 않는다.
