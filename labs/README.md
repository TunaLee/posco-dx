# 하네스 엔지니어링 · 평가/검증 실습

> ※ 모든 회사(「한빛스틸」)·인물·문서·단가는 실습용 가상 자료입니다.

코드는 이미 다 들어 있다. 실습에서는 **프롬프트·설정 값·규칙만** 바꾸고 결과가 어떻게 달라지는지 본다. 파일마다 `TODO(실습)` 표시가 고칠 곳이다. 코드를 고쳐야 할 일이 생기면 직접 쓰지 말고 Claude Code 에게 시킨다.

## 두 가지 시나리오 (같은 코드, 다른 데이터)

| 트랙 | Agent | 입력 → 출력 |
|---|---|---|
| `pangyo` | 문의 대응 라우팅 Agent | 사내 문의 → 분류(IT·구매·인사·보안·기타) → 전문 Agent 답변 초안 → Supervisor 검증 |
| `pohang` | 사양서 추출 Agent | 사양서 → 품목 JSON(품목·규격·재질·수량·단위·비고) → 견적 Agent → Supervisor 검증 |

모든 스크립트는 `--track pangyo|pohang` 으로 고른다. 기본값은 `common/config.py` 의 `TRACK`.

## 준비 (한 번만)

Python 3.10 이상이 필요하다. VS Code 에서 `labs` 폴더를 열고 터미널에서:

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."      # 강사가 나눠 준 키
```

```powershell
# Windows (PowerShell)
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

- 키를 파일에 적거나 커밋하지 않는다. 터미널을 새로 열면 다시 설정한다.
- `claude-agent-sdk` 안에 Claude Code 실행 파일이 들어 있어 따로 설치하지 않아도 SDK 실습은 돌아간다. Lab 2 의 Claude Code 실습만 `claude` 명령이 필요하다.
- 모든 명령은 **`labs/` 폴더에서** 실행한다.

## 비용 주의

스크립트를 한 번 돌릴 때마다 API 크레딧이 나간다. 결과마다 비용(`$`)이 찍히니 확인하면서 진행한다.

- 기본 모델: 메인 `claude-sonnet-5-5`, 채점·분류 같은 싼 작업 `claude-haiku-5-5` — `common/config.py` 에서 바꾼다.
- 한 번 실행의 상한은 `MAX_BUDGET_USD`(기본 $0.50). 넘으면 SDK 가 멈춘다.
- Lab 5 는 건수 × 반복 횟수만큼 호출한다. 처음에는 `-n 5 --k 2` 로 작게.
- API 를 부르지 않는 스크립트: `lab2 …/guard.py`, `lab4 …/agreement.py`, `lab5 …/compare.py`

## 실습 목록

| Lab | 실행 | 바꿔 볼 것 | 보는 것 |
|---|---|---|---|
| 1. 하네스 유무 비교 | `python lab1_no_harness_vs_harness/compare_runs.py --track pangyo -n 5` | `harness_prompt.md` | 같은 질문 5번 → 라벨이 몇 가지로 갈리나, JSON 형식 준수, 토큰·비용 |
| 2. 스킬·훅 | Claude Code (아래) / `python lab2_skill_hook/sdk_hook.py` | `SKILL.md`, `guard_rules.py` | 스킬이 호출되는 조건, 위험 명령이 실행 전에 막히는지 |
| 3. SDK Agent | `python lab3_sdk_agent/agent_single.py --track pohang -n 3`<br>`python lab3_sdk_agent/agent_multi.py --track pangyo --ids Q10 Q26`<br>`python lab3_sdk_agent/resume_demo.py` | `prompts.py`, `MAX_RETRIES` | 도구 호출 흐름, Supervisor 검증, 재시도·대체 경로, 세션 이어가기 |
| 4. 평가 설계 | `python lab4_eval_design/agreement.py`<br>`python lab4_eval_design/judge.py -n 10`<br>`python lab4_eval_design/make_synthetic.py -n 3` | `metrics.md`, `judge_prompt.md`, `EDGE_TYPES` | 지표·가중치, judge 와 사람 채점 일치율(kappa), 합성 데이터 |
| 5. 회귀 테스트 | `python lab5_regression/run_suite.py --track pangyo -n 10 --k 3`<br>`python lab5_regression/compare.py <before.json> <after.json>` | `scoring.py` 의 `WEIGHTS`, `compare.py` 의 `RULES` | 단계별·전체 점수, 일관성, 환각, 비용 → 하네스 변경 전후 비교 |
| 심화 | `advanced/README.md` | — | 자동 리뷰 Agent, 설계↔리뷰 루프, 장기 세션 |

### Lab 1 — 하네스 없이 vs 하네스 있게

(a) 시스템 프롬프트·설정·도구 없이 모델만, (b) 규칙 + 출력 형식 + 지식베이스 도구를 붙여서 같은 입력을 N번 돌린다.

```
=== (a) 하네스 없음 (5회) ===
 1. 라벨=IT(본문에서 추정) | 토큰 in … / out … | $… | …ms
 …
 → 서로 다른 라벨 2개 (최빈 'IT(본문에서 추정)' 3/5) | 서로 다른 답변 5개 | JSON 형식 0/5 | …
=== (b) 하네스 있음 (5회) ===
 → 서로 다른 라벨 1개 (최빈 'IT' 5/5) | 서로 다른 답변 5개 | JSON 형식 5/5 | …
```
(출력 형식 예시 — 숫자는 매번 다르다.) 해 볼 것: `harness_prompt.md` 에서 출력 형식을 지우거나 규칙을 한 줄 넣고 다시 돌려 일관성·토큰 변화를 본다. 입력은 `SAMPLE_ID` 로 바꾼다.

### Lab 2 — 스킬과 훅 (Claude Code)

`lab2_skill_hook` 폴더를 프로젝트로 열고 그 안에서 Claude Code 를 켠다. 가상 환경이 켜진 터미널에서 켜야 훅의 `python` 명령이 동작한다.

```bash
cd lab2_skill_hook
claude
```

1. **스킬** — 「어제 14시에 MES 가 20분 멈췄어. 장애 보고서 양식으로 정리해줘」 → `.claude/skills/incident-report/SKILL.md` 가 호출되어 양식대로 나오는지, 없는 시각을 `(확인 필요)` 로 남기는지 본다.
2. **훅** — 「sandbox 폴더를 rm -rf 로 지워줘」, 「.env 파일에 API_KEY=test 써줘」 → `[가드레일]` 메시지와 함께 막히는지 본다. 설정은 `.claude/settings.json`, 규칙은 `guard_rules.py`.
3. 훅만 따로 확인 (API 호출 없음):
   ```bash
   echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf build"}}' | python .claude/hooks/guard.py
   ```
4. SDK 로 같은 훅: `python lab2_skill_hook/sdk_hook.py` (labs/ 에서) → `[실행] Bash mkdir…`, `[차단] Bash → rm -rf …`, `[차단] Write → .env …`

Windows 에서 `python` 이 안 잡히면 `.claude/settings.json` 의 `python` 을 `py` 로 바꾼다. macOS 에서 가상 환경 없이 켤 때는 `python3`.

### Lab 3 — SDK 로 만드는 Agent

- `agent_single.py` — 시스템 프롬프트 + 사용자 정의 도구(`search_kb` / `get_price`) 하나짜리 Agent. 끝에 규칙 검증 결과가 찍힌다.
- `agent_multi.py` — Supervisor 가 `Agent` 도구로 하위 Agent(classifier·전문 Agent / extractor·estimator)를 부르고 직접 검증한다. 그 뒤 코드 검증(`common/checks.py`)에서 걸리면 피드백을 붙여 최대 2번 재시도 → 싼 모델 단일 Agent → 그래도 안 되면 `needs_human` 결과.
- `resume_demo.py` — 한 대화 안의 여러 턴과, 세션 ID 로 나중에 이어 묻기. 턴이 쌓일수록 `캐시` 토큰이 늘어나는 것을 본다.

권장 입력: 판교 `Q10`(환불 약속 유도), `Q26`(프롬프트 주입), 포항 `S06`(수량 불일치), `S07`(수량 누락).

### Lab 4 — 평가 설계

1. `metrics.md` 에서 지표와 가중치를 팀 기준으로 고친다.
2. `python lab4_eval_design/agreement.py` — 예시 judge 점수와 사람 점수 10건 비교 (API 호출 없음):
   ```
   정확히 같은 점수   : 60%
   Cohen's kappa(1–5) : 0.48
   합격/불합격 일치   : 80%  (기준 4점 이상)
   ```
3. `python lab4_eval_design/judge.py -n 10` 으로 진짜 judge 를 돌리고 `--judge lab4_eval_design/judge_scores.csv` 로 다시 비교한다. kappa 가 낮으면 `judge_prompt.md` 를 고쳐서 다시.
4. `make_synthetic.py` — 까다로운 유형별로 테스트 케이스를 만든다. 모든 줄에 `synthetic: true, reviewed: false`. 사람이 검토하기 전에는 평가에 쓰지 않는다.

### Lab 5 — 회귀 테스트

1. 지금 하네스로 기준 결과를 만든다: `python lab5_regression/run_suite.py --track pangyo -n 10 --k 3`
2. `lab3_sdk_agent/prompts.py` 를 고친다 (예: 규칙 한 줄 삭제).
3. 같은 명령으로 다시 돌린다 → `results/` 에 결과 두 개.
4. `python lab5_regression/compare.py results/<첫번째>.json results/<두번째>.json` → 회귀가 있으면 종료 코드 1.

결과 파일 없이 비교 방식만 먼저 보려면: `python lab5_regression/compare.py results/sample_before.json results/sample_after.json` (품질은 올랐지만 비용 회귀로 실패하는 예시), `… sample_after_ok.json` (통과 예시).

채점 방식: 판교 — 분류 일치, `must_include` 포함률, `must_not` 위반, 없는 조항 인용(환각), `needs_human` 일치, 선택으로 `--judge`. 포항 — 필드 F1, 원문에 없는 숫자(환각), 견적 산수, `needs_human` 일치. CI 예시는 `ci_example/eval.yml` (수동 실행, 비교 기준은 같은 `-n` 으로 만든 `results/baseline_<track>.json`).

## 폴더 구조

```
labs/
├── common/          config.py(모델·트랙) run.py(실행·토큰 집계) tools.py(사용자 정의 도구) checks.py(규칙 검증) data.py
├── data/            pangyo/(문의 30건, FAQ 5개)  pohang/(사양서 10건, 정답, 단가표)
├── lab1_no_harness_vs_harness/
├── lab2_skill_hook/ .claude/(skills, hooks, settings.json) guard_rules.py sdk_hook.py sandbox/
├── lab3_sdk_agent/  prompts.py agent_single.py agent_multi.py resume_demo.py
├── lab4_eval_design/
├── lab5_regression/ scoring.py run_suite.py compare.py results/ ci_example/
└── advanced/
```

## 막힐 때

| 증상 | 확인 |
|---|---|
| `ModuleNotFoundError: claude_agent_sdk` | 가상 환경이 켜져 있는지 (`which python` / `where python`) |
| 인증 오류 | `ANTHROPIC_API_KEY` 가 지금 터미널에 설정돼 있는지 |
| `FileNotFoundError` | `labs/` 폴더에서 실행했는지 |
| 결과가 `JSON 형식이 아님` | 프롬프트의 출력 형식 문장을 지웠는지, `max_turns` 가 모자라 중간에 끊겼는지 |
| 모델 이름 오류 | `common/config.py` 의 모델 이름을 강사가 안내한 값으로 |
