너는 이 저장소에서 기능 하나만 구현하고 끝낸다.

1. `features.json` 에서 passes 가 false 인 첫 기능을 고른다.
2. `progress.md` 를 읽고 앞 세션이 남긴 내용을 이어 받는다.
3. 새 브랜치 `feature/<기능 id>` 에서 구현한다. 데이터는 미니 깃 API(127.0.0.1:8900)와 `data/reviews.json` 을 쓰고, 화면은 `web/` 에 페이지 하나를 더한다.
4. `tests/` 에 그 기능의 테스트를 추가하고 `python -m unittest discover -s tests` 가 모두 통과해야 한다. 실패하면 고친다.
5. 통과하면 features.json 의 그 기능 passes 를 true 로 바꾸고, progress.md 에 한 줄 기록하고, 커밋해서 `git push team feature/<기능 id>` 로 올린다 (PR 이 됨 · 병합은 사람이).
6. 다른 기능은 건드리지 않는다. `repos/` 와 `.claude/` 는 고치지 않는다. 승인 · 병합 도구는 부르지 않는다.
