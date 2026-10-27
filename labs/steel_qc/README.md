# 코일 품질 판정 — 하네스를 한 프로젝트에 쌓아 가기

> ※ 회사(「한빛스틸」) · 강종 · 규격 · 시험 결과는 모두 실습용 가상 자료입니다. 실제 KS · ASTM 수치와 다릅니다.

이 폴더 하나에 Ch1부터 Ch8까지 하네스 부품을 차례로 붙인다.
API 키는 필요 없다. 판단은 **Claude Code(로그인 계정)** 가 하고, 아래 프로그램들은 LLM 을 부르지 않는다.

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

## 챕터별로 붙이는 것

요청은 짧게, 방법은 Claude Code 가 정한다.

| 챕터 | Claude 에게 | 확인할 결과 |
|---|---|---|
| Ch1 | 「최근 결과 판정해 줘」 → 「판정 기준을 CLAUDE.md로 정리해 줘」 | CLAUDE.md 전후 답의 차이 |
| Ch2 | 「시뮬레이터를 MCP 서버로 연결해 줘」 · 「불합격 보고 절차를 Skill로」 · 「원인 조사 Sub Agent」 · 「출하 승인은 Hook으로 막아 줘」 | 붙여 넣기 없이 「방금 들어온 불합격 정리해」 · 「내가 승인자다」도 막힘 |
| Ch3 | 「불합격만 골라 돌려주는 도구로 바꿔 줘」 | `/context` 전후 · 건수가 누적 건수와 같은지 |
| Ch4 | Superpowers 로 「실시간 불합격 대시보드 만들어 줘」 | 새 결과가 들어오면 화면이 바로 바뀜 |
| Ch5 | 「조사 · 통보 · 검증 Agent 팀으로 나눠 줘」 | 단일 vs 팀 시간 · 토큰 · 검증 결과 |
| Ch6 | 「최근 300건 판정해 줘」 · 원문 도구 vs 요약 도구 | 토큰 실측 |
| Ch7 | 「판정 테스트 만들어 줘」 · 「끝내기 전에 테스트가 돌게 해 줘」 → 「HS-275 인장강도 상한이 570으로 개정됐어」 | 깨진 곳을 Claude 가 보고 · 반영 여부는 사람이 |
| Ch8 | 「다음에 만들 기능 5개를 정리해 줘」 → 「기능을 하나씩 새 세션으로 구현하는 루프를 만들어 줘」 | 사람 없이 기능 · 커밋 · 테스트가 쌓임 |

## 막히면 — `solution/` (강사용 완성본)

수업에서는 Claude Code 에게 직접 만들게 한다. 막혔을 때만 열어 본다.

| 파일 | 쓰는 챕터 |
|---|---|
| `CLAUDE.md` | Ch1 · Ch8 (루프 때 이 폴더 맨 위로 복사) |
| `judge.py` | Ch2 이후 · 판정 로직 |
| `mcp_server.py` | Ch2 · `claude mcp add lims -- python solution/mcp_server.py` |
| `hooks/approve_guard.py` · `dot_claude/settings.json` | Ch2 · `.claude/settings.json` 으로 복사 |
| `tests/test_judge.py` | Ch7 · `python -m unittest discover -s solution/tests` |
| `features.json` · `PROMPT.md` · `progress.md` · `loop.py` | Ch8 · 이 폴더 맨 위로 복사 후 `python loop.py 5` |

- Windows 에서 `python` 이 없다고 나오면 `py` 로 바꿔 실행한다.
- 시뮬레이터가 꺼져 있으면 MCP 도구가 「연결 거부」 오류를 돌려준다 — 시뮬레이터부터 켠다.
