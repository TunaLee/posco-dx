# 코일 품질 판정 — 하네스를 한 프로젝트에 쌓아 가기

> ※ 회사(「한빛스틸」) · 강종 · 규격 · 시험 결과는 모두 실습용 가상 자료입니다. 실제 KS · ASTM 수치와 다릅니다.

준비된 것은 가상 시험실(`sim/`)뿐이다. 앱 · MCP 서버 · Skill · Hook · 테스트는 모두 Claude Code 로 이 폴더에 만들어 간다.
API 키는 필요 없다. 판단은 **Claude Code(로그인 계정)** 가 하고, 시뮬레이터는 LLM 을 부르지 않는다.

## 처음 한 번 — 시뮬레이터 켜기

```
python sim/lims_sim.py          # http://127.0.0.1:8800 · 끄려면 Ctrl+C
```

- 몇 초마다 새 코일 시험 결과(C · Mn · P · S · 항복강도 · 인장강도 · 연신율)가 쌓인다.
- 브라우저에서 재생 · 일시정지 · 속도(×1 · ×5 · ×20)를 바꾼다.
- 규격 이탈 약 5% · 한계 근접 약 14% · 같은 라인 3연속 근접이 섞여 나온다.
- 같은 순서로 나온다(시드 고정). 판정 정답은 `/api/truth` 에 따로 있다 — 평가 · 테스트용.

| 주소 | 내용 |
|---|---|
| `/api/results?since=0` | 시험 결과 (`grade=HS-355` 로 강종 필터) |
| `/api/results/HB26-00012` | 코일 한 건 |
| `/api/specs` | 강종별 사내 규격 |
| `/api/state` · `POST /api/control` | 재생 상태 · 재생 / 일시정지 / 속도 |
| `/api/truth?since=0` | 판정 정답 (평가용) |

## 실습마다 생기는 탭

`labs/README.md` 표 참고. 실습 하나를 마칠 때마다 콘솔(브라우저)에 탭이 하나씩 생긴다.

## 막히면 — `solution/` (강사용 완성본)

수업에서는 Claude Code 에게 직접 만들게 한다. 막혔을 때만 열어 본다.

| 파일 | 쓰는 실습 |
|---|---|
| `CLAUDE.md` · `app/` (서버 · 탭 ① ~ ⑦) | 1-1 · 탭이 막히면 해당 탭 파일만 `app/tabs/` 로 |
| `judge.py` | 판정 로직 |
| `mcp_server.py` | 2-1 · `claude mcp add lims -- python solution/mcp_server.py` |
| `dot_claude/` (Skill · Agent · settings) | 2-2 · 2-3 · 5-1 · 7-1 · `.claude/` 로 복사 |
| `hooks/approve_guard.py` · `hooks/test_gate.py` | 2-3 · 7-1 |
| `tests/test_judge.py` | 7-1 · `tests/` 로 복사해도 됨 |
| `features.json` · `PROMPT.md` · `progress.md` · `loop.py` | 8-2 · 이 폴더 맨 위로 복사 후 `python loop.py 5` |

- Windows 에서 `python` 이 없다고 나오면 `py` 로 바꿔 실행한다.
- 시뮬레이터가 꺼져 있으면 MCP 도구가 「연결 거부」 오류를 돌려준다 — 시뮬레이터부터 켠다.
