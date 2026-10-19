"""실습 진행 장표 데이터 — 하네스 미적용 → 하네스 만들기 → 적용 → 비교.

steps: (라벨, 종류, 내용) · 종류 p = 대화창에 붙여 넣을 요청문, do = 사람이 직접 하는 일
files: (저장 이름, 화면 경로, 원본) · 원본이 @로 시작하면 src/lab_harness/, 아니면 labs/
"""

KITS = {
    "1-1": dict(folder="lab1_1_bill_check", steps=[
        ("① 하네스 미적용", "p", "lab1_1_bill_check 폴더 안에서 하네스 없이(claude -p --setting-sources \"\") 「data 폴더의 운송비 청구를 검증해 줘.」를 실행하고\n답을 labs 바로 아래 runs/1-1/미적용.md 로 저장해 줘"),
        ("② 하네스 만들기", "do", "탐색기에서 새 파일 <b>lab1_1_bill_check/CLAUDE.md</b> → 오른쪽 「복사」 → 붙여 넣기 → 저장"),
        ("③ 하네스 적용", "p", "lab1_1_bill_check 폴더 안에서 같은 요청을 claude -p --setting-sources project 로 실행하고\n답을 labs 바로 아래 runs/1-1/적용.md 로 저장해 줘"),
        ("④ 비교", "p", "runs/1-1/ 의 두 답과 lab1_1_bill_check/out/ 을 보고 표로 비교해 줘:\n이의 제기 건 · 결과 파일이 있는지 · 지급 여부까지 판단했는지 · 답 길이"),
    ], files=[("CLAUDE.md", "lab1_1_bill_check/CLAUDE.md", "@1-1/CLAUDE.md")],
        tip="미적용을 다시 할 땐 CLAUDE.md를 잠시 다른 이름으로"),

    "2-1": dict(folder="lab2_1_parts", split=True, steps=[
        ("① 하네스 미적용", "p", "lab2_1_parts 폴더 안에서 아래 두 요청을 하나씩\nclaude -p --setting-sources \"\" --output-format stream-json --verbose 로 실행해\nlabs 바로 아래 runs/2-1/미적용_1.jsonl · 2.jsonl 로 저장해 줘\n1. 어제 14시에 MES가 20분 멈췄어. 장애 보고서 양식으로 정리해 줘\n2. src/order_api.py 리뷰해 줘"),
        ("② 하네스 만들기", "do", "앞 장 파일 두 개를 화면의 경로대로 · 탐색기 새 파일에 <b>lab2_1_parts/.claude/skills/incident-report/SKILL.md</b> 처럼 경로째 입력"),
        ("③ 하네스 적용", "p", "lab2_1_parts 폴더 안에서 아래 두 요청을 하나씩\nclaude -p --setting-sources project --output-format stream-json --verbose 로 실행해\nlabs 바로 아래 runs/2-1/적용_1.jsonl · 2.jsonl 로 저장해 줘\n1. 어제 14시에 MES가 20분 멈췄어. 장애 보고서 양식으로 정리해 줘\n2. src/order_api.py 리뷰해 줘"),
        ("④ 비교", "p", "runs/2-1/ 의 미적용 · 적용 기록을 비교해 표로 정리해 줘:\n보고서 양식 · 「(확인 필요)」 표시 · Skill 호출 여부 · reviewer 위임 여부 · 파일 수정 여부"),
    ], files=[("SKILL.md", "lab2_1_parts/.claude/skills/incident-report/SKILL.md", "@2-1/SKILL.md"),
              ("reviewer.md", "lab2_1_parts/.claude/agents/reviewer.md", "@2-1/reviewer.md")]),

    "2-2": dict(folder="lab2_hook_by_claude", split=True, harness_note="③ 단계에서 대화창에 붙여 넣는 요청문 · 내 말로 바꿔도 됨", steps=[
        ("① 준비", "p", "lab2_hook_by_claude/project 폴더에서 python3 tools/make_db.py 로 DB를 만들고\npython3 scripts/report.py 가 어떤 오류로 멈추는지 보여 줘"),
        ("② 하네스 미적용 · 채점", "p", "python3 lab2_hook_by_claude/check_hook.py 를 실행해 점수를 보여 줘"),
        ("③ 하네스 만들기", "do", "앞 장 요청문 「복사」 → 대화창에 붙여 넣기 · .claude 쓰기 승인 요청은 내용을 읽고 승인"),
        ("④ 하네스 적용 · 채점", "p", "python3 lab2_hook_by_claude/check_hook.py 를 다시 실행해 Hook 만들기 전 점수와 비교하고\n놓친 사례가 있으면 Hook을 고쳐서 다시 채점해 줘"),
        ("⑤ 실제 차단", "p", "lab2_hook_by_claude/project 폴더 안에서\nclaude -p --setting-sources project --permission-mode acceptEdits \"리포트 오류 고쳐 줘\" 를 실행하고\n운영 DB 쓰기가 Hook에 막혔는지 · 허락을 구했는지 알려 줘"),
    ], files=[("prompt.md", "Hook 만들기 요청문", "@PROMPT22")],
        tip="하네스 미적용 6 / 15 (허용할 것만 맞음) → 목표 15 / 15"),

    "2-3": dict(folder="work_harness/workspace", steps=[
        ("① 하네스 미적용", "p", "work_harness/workspace 폴더 안에서 아래 두 요청을 하나씩\nclaude -p --setting-sources \"\" --permission-mode acceptEdits 로 실행하고\n각 답을 work_harness/workspace/_final_T3.txt · _final_T4.txt 로 저장해 줘\n- inputs/T3 회의록에서 할 일 정리해 줘.\n- inputs/T4 이번 주 설비 점검 기록으로 주간 보고서 만들어 줘."),
        ("② 채점", "p", "python3 work_harness/grade.py work_harness/workspace --task T3 T4 를 실행해 점수를 보여 줘"),
        ("③ 하네스 만들기", "do", "앞 장 파일 세 개를 화면의 경로대로 (CLAUDE.md · Skill 두 개)"),
        ("④ 하네스 적용", "p", "work_harness/workspace 의 out 폴더와 _final_*.txt 를 지우고, 그 폴더 안에서 아래 두 요청을 하나씩\nclaude -p --setting-sources project --permission-mode acceptEdits 로 실행해\n각 답을 work_harness/workspace/_final_T3.txt · _final_T4.txt 로 저장한 뒤\npython3 work_harness/grade.py work_harness/workspace --task T3 T4 로 채점해 줘\n- inputs/T3 회의록에서 할 일 정리해 줘.\n- inputs/T4 이번 주 설비 점검 기록으로 주간 보고서 만들어 줘."),
        ("⑤ 비교", "p", "미적용 · 적용 점수와 결과 파일 위치 · 근거 표기 · 「확인 필요」 표시를 표로 비교해 줘"),
    ], files=[("CLAUDE.md", "work_harness/workspace/CLAUDE.md", "work_harness/harness/CLAUDE.md"),
              ("SKILL.md", "work_harness/workspace/.claude/skills/meeting-actions/SKILL.md", "work_harness/harness/.claude/skills/meeting-actions/SKILL.md"),
              ("SKILL.md", "work_harness/workspace/.claude/skills/weekly-report/SKILL.md", "work_harness/harness/.claude/skills/weekly-report/SKILL.md")],
        tip="다른 과제 · T1 문의 답변 · T2 견적 · T5 정책 비교 · T6 지연 안내 메일 · 나머지 Skill은 부록 ②~④"),

    "3-1": dict(folder="", steps=[
        ("① 실험 네 가지", "p", "lab3_context/run.py --exp all 을 실행하고 변형별\n메인 토큰 · 전체 토큰 · 턴을 표로, 답이 달라진 변형은 표시해 줘"),
        ("② 지금 대화의 컨텍스트", "p", "/context"),
        ("③ 압축", "p", "/compact 결정 사항과 설비 ID만 남겨"),
        ("④ Skill 설명 줄이기", "p", "lab3_context/a_lean/SKILL.md 의 description 을 「매뉴얼」 한 단어로,\nrun.py 의 QUESTION[\"a\"] 를 「P-210 점검 주기는?」 으로 바꿔\n실험 a 다시 → Skill이 호출됐는지 · 끝나면 되돌려 줘"),
    ], files=[("CLAUDE.md", "a_lean/CLAUDE.md", "lab3_context/a_lean/CLAUDE.md"),
              ("SKILL.md", "a_lean/SKILL.md", "lab3_context/a_lean/SKILL.md")]),

    "4-1": dict(folder="", steps=[
        ("① Superpowers 설치", "p", "/plugin marketplace add obra/superpowers-marketplace\n/plugin install superpowers@superpowers-marketplace"),
        ("② gstack 설치", "p", "gstack 을 ~/.claude/skills/gstack 에 설치해 줘\n(github.com/garrytan/gstack 을 --depth 1 로 받고 ./setup)"),
        ("③ 네 가지로 실행", "p", "lab4_public_harness/run_task.py 를 bare · mine · superpowers · gstack 순서로\n실행하고 토큰 · 시간 · 테스트 통과 · 건너뛴 단계를 compare.md 에 채워 줘"),
        ("④ 가져올 점", "p", "compare.md 를 보고 내 하네스에 가져올 점 3개를 이유와 함께 적어 줘"),
    ], files=[("task.md", "과제 카드", "lab4_public_harness/task.md")],
        tip="플러그인 설치가 막혀 있으면 bare · mine 두 가지만"),

    "5-1": dict(folder="lab5_multiagent", split=True, harness_note="이미 들어 있는 파일 · VS Code 탐색기에서 열어 확인", tree=("lab5_multiagent/project/ 구조",
        "lab5_multiagent/project/\n"
        "├── CLAUDE.md                     「지휘 Skill 순서대로 · 메인은 직접 답 안 씀」\n"
        "└── .claude/\n"
        "    ├── skills/\n"
        "    │   ├── orchestrate-inquiry/\n"
        "    │   │   └── SKILL.md          지휘: 분류 → 응대 → 검증\n"
        "    │   └── orchestrate-quote/\n"
        "    │       └── SKILL.md          지휘: 추출 → 견적 → 검증\n"
        "    └── agents/                   Sub Agent 하나 = 파일 하나\n"
        "        ├── classifier.md         분류 (haiku)\n"
        "        ├── responder-it.md 외 4개  분야별 응대 (Read · Grep)\n"
        "        ├── verifier-inquiry.md   문의 답 검증 (읽기 전용)\n"
        "        ├── extractor.md · estimator.md\n"
        "        └── verifier-quote.md     견적 검증 (읽기 전용)"), steps=[
        ("① 실행", "p", "lab5_multiagent/run.py --ids Q10 을 실행하고\n위임 순서 · 줄별 토큰 · 검증 결과를 정리해 줘"),
        ("② 타임라인", "p", "방금 저장된 lab5_multiagent/runs/ 기록으로 lab5_multiagent/visualize.py 를 돌려\n타임라인 HTML을 만들고 열어 줘"),
        ("③ 검증 빼 보기", "p", "lab5_multiagent/project/.claude/skills/orchestrate-inquiry/SKILL.md 에서 검증 단계를 지우고\nlab5_multiagent/run.py --ids Q10 을 다시 실행해 타임라인을 비교해 줘 · 끝나면 되돌려 줘"),
        ("④ 까다로운 입력", "p", "lab5_multiagent/run.py --ids Q26 (프롬프트 주입) 을 실행해\nverifier-inquiry 가 막았는지 알려 줘"),
    ], files=[("SKILL.md", "lab5_multiagent/project/.claude/skills/orchestrate-inquiry/SKILL.md", "lab5_multiagent/project/.claude/skills/orchestrate-inquiry/SKILL.md"),
              ("verifier-inquiry.md", "lab5_multiagent/project/.claude/agents/verifier-inquiry.md", "lab5_multiagent/project/.claude/agents/verifier-inquiry.md")]),

    "5-2": dict(folder="work_harness/workspace", steps=[
        ("① 단일 하네스 완성", "do", "2-3 하네스에 앞 장 <b>spec-quote</b> Skill 추가"),
        ("② 단일 하네스 · 실행", "p", "work_harness/workspace 폴더 안에서\nclaude -p --setting-sources project --permission-mode acceptEdits --output-format json 으로\n「inputs/T7 사양서 40건 견적 내 줘. 사양서별 금액과 전체 합계까지.」 를 실행하고\n답을 work_harness/workspace/_final_T7.txt 로 저장 · 걸린 시간과 토큰도 알려 줘"),
        ("③ 채점", "p", "python3 work_harness/grade.py work_harness/workspace --task T7 을 실행해 점수를 보여 줘"),
        ("④ 멀티에이전트 만들기", "do", "앞 장 extractor · verifier 파일 만들기 · <b>work_harness/workspace/CLAUDE.md</b> 끝에 덧붙임 내용 붙여 넣기"),
        ("⑤ 멀티에이전트 · 실행", "p", "work_harness/workspace 의 out/T7 과 _final_T7.txt 를 지우고, 그 폴더 안에서\nclaude -p --setting-sources project --permission-mode acceptEdits --output-format json 으로\n「inputs/T7 사양서 40건 견적 내 줘. 사양서별 금액과 전체 합계까지.」 를 실행해\n답을 _final_T7.txt 로 저장 · 시간과 토큰을 알려 주고\npython3 work_harness/grade.py work_harness/workspace --task T7 로 채점해 줘"),
        ("⑥ 비교", "p", "단일 vs 멀티 점수 · 시간 · 토큰 · Sub Agent 호출 수를 표로 비교해 줘"),
    ], files=[("SKILL.md", "work_harness/workspace/.claude/skills/spec-quote/SKILL.md", "work_harness/harness/.claude/skills/spec-quote/SKILL.md"),
              ("extractor.md", "work_harness/workspace/.claude/agents/extractor.md", "work_harness/harness_multi/.claude/agents/extractor.md"),
              ("verifier.md", "work_harness/workspace/.claude/agents/verifier.md", "work_harness/harness_multi/.claude/agents/verifier.md"),
              ("CLAUDE_추가.md", "work_harness/workspace/CLAUDE.md 끝에 덧붙임", "work_harness/harness_multi/CLAUDE.md")]),

    "6-1": dict(folder="", steps=[
        ("① 기준선", "p", "lab6_tokens/bench.py --levers baseline,brief 를 실행하고\n과제별 토큰 · 정답 여부를 표로"),
        ("② 모델 나누기", "p", "bench.py --levers haiku,sonnet,opus 실행 → 과제별 토큰 · 정답 비교"),
        ("③ 캐시 · Sub Agent", "p", "bench.py --levers cache,subagent 실행 → 기준선 대비 변화"),
        ("④ 고르기", "p", "세 결과를 합쳐 품질이 떨어지지 않은 레버만 골라\n내 업무에 쓸 순서로 추천해 줘"),
    ], files=[("quiz.md", "quiz.md · 먼저 예상", "lab6_tokens/quiz.md")]),

    "6-2": dict(folder="token_harness", steps=[
        ("① 하네스 미적용", "p", "token_harness 폴더 안에서, 하네스 없이(claude -p --setting-sources \"\" --output-format json) 아래 요청을 실행하고\n토큰 · 턴 · 시간 · 답을 알려 줘.\n「data 폴더 자료로 이번 주 MES 장애를 코드별 건수와 지속 시간 합계로 정리하고,\n건수가 가장 많은 코드의 처리 기준을 매뉴얼에서 찾아 알려 줘.」"),
        ("② 하네스 만들기", "p", "방금 그 집계와 처리 기준 찾기를 다음부터 한 번에 끝낼 수 있게,\npython 스크립트로 만들어 token_harness/.claude/skills/mes-summary 에 Skill로 등록해 줘.\nCLAUDE.md 에는 「이 일은 그 Skill부터 쓰고 답은 5줄 안으로」라고 적어 줘."),
        ("③ 하네스 적용", "p", "같은 요청을 이번엔 token_harness 폴더 안에서 claude -p --setting-sources project --output-format json 으로 실행해서\n하네스 없을 때와 토큰 · 턴 · 시간 · 정답을 표로 비교해 줘."),
        ("④ 해 보기", "do", "Skill 대신 「300줄 넘는 파일 통째 읽기 금지」 Hook만 넣으면 토큰이 어떻게 되는지 · 다음 장 결과와 비교"),
    ], files=[("CLAUDE.md", "token_harness/CLAUDE.md (예)", "@6-2/CLAUDE.md"),
              ("SKILL.md", "token_harness/.claude/skills/mes-summary/SKILL.md (예)", "@6-2/skills/mes-summary/SKILL.md"),
              ("summary.py", "token_harness/.claude/skills/mes-summary/summary.py (예)", "@6-2/skills/mes-summary/summary.py")],
        split=True, harness_note="②에서 Claude가 만든 결과의 예 · 막히면 「파일로 저장」"),

    "7-1": dict(folder="work_harness", steps=[
        ("① 기준선", "p", "work_harness/run_tasks.py --cond single --tasks T1 T2 T3 T4 T5 T6 을 실행하고\n과제별 점수 · 시간 · 토큰을 표로 정리해 줘"),
        ("② 일부러 나쁘게", "p", "work_harness/harness/CLAUDE.md 를 CLAUDE.md.bak 으로 복사해 두고\n「결과는 out/<과제번호>/ 에 만든다」 줄을 지워 줘"),
        ("③ 회귀 찾기", "p", "work_harness/run_tasks.py --cond single --tasks T1 T2 T3 T4 T5 T6 을 다시 실행해\n바로 전 실행과 과제별 점수를 비교하고 나빠진 과제와 이유를 표로 정리해 줘"),
        ("④ 사람 판정", "do", "점수가 같은 과제도 결과물 2개를 직접 열어 읽고 O / X · 자동 채점과 다른 판정을 적기"),
        ("⑤ 되돌리기", "p", "work_harness/harness/CLAUDE.md 를 CLAUDE.md.bak 내용으로 되돌려 줘"),
    ], tip="자동 채점은 사람이 볼 곳을 좁혀 줌 · 합격 여부는 사람이"),

    "8-1": dict(folder="meta_harness", open="labs/meta_harness", steps=[
        ("① 메타 하네스 만들기", "do", "Ch8 「메타 하네스를 만드는 요청문」 붙여 넣기 → 만든 파일 확인 → Claude Code 새로 열기"),
        ("② 내 주제로 시작", "p", "내 하네스를 만들고 싶어: 〈사전 과제 주제 한 줄〉.\n예시 입력은 ../samples/〈분야〉/ 를 써. 인터뷰부터 시작해 줘"),
        ("③ 사람 승인", "do", "인터뷰 답 → docs/〈이름〉/spec.md 검토 → 괜찮으면 새 파일 <b>docs/〈이름〉/APPROVED</b> (사람만)"),
        ("④ 생성 · 시험", "p", "docs/〈이름〉/APPROVED 만들었어. 하네스를 만들고 검토 · 시험까지 해 줘"),
        ("⑤ 개발 주제라면", "do", "<b>labs/final_dev_harness</b> 를 열고 Superpowers 설치 → 「Superpowers로 개발하기」 요청문 → 설계 승인 · DESIGN.md · 계획 승인 → 구현"),
        ("⑥ 사람 판정 · 공유", "do", "비교표 · 결과물을 직접 판정 → 다음 장 양식으로 패들릿에 올리기"),
    ], tip="샘플 데이터 labs/samples/ · 요청문이 막히면 부록 ⑦ ⑧ 「파일로 저장」 · 플러그인 설치가 막히면 Superpowers는 강사 시연"),
    "8-2": dict(folder="loop_harness", open="labs/loop_harness", steps=[
        ("① 첫 커밋", "p", "이 폴더를 git 저장소로 만들고 첫 커밋 해 줘"),
        ("② 하네스 만들기", "do", "앞 장 파일 네 개(CLAUDE.md · PROMPT.md · features.json · progress.md)를 같은 이름으로 만들기 → 커밋"),
        ("③ 루프 실행", "do", "VS Code 터미널에서 <b>node loop.mjs 8</b> · 한 번마다 남은 기능 · 시간 · 토큰이 찍힘"),
        ("④ 진행 보기", "do", "features.json 의 passes · progress.md · git log 가 한 칸씩 바뀌는지"),
        ("⑤ 정리", "p", "features.json · progress.md · git log 를 보고 기능별 결과 · 걸린 횟수 · 막힌 점을 표로 정리해 줘"),
        ("⑥ 사람 판정", "do", "터미널에서 node src/cli.js data/운송비청구.csv 를 직접 실행해 이의 제기 건이 맞는지 확인"),
    ], files=[("CLAUDE.md", "loop_harness/CLAUDE.md", "@8-2/CLAUDE.md"),
              ("PROMPT.md", "loop_harness/PROMPT.md", "@8-2/PROMPT.md"),
              ("features.json", "loop_harness/features.json", "@8-2/features.json"),
              ("progress.md", "loop_harness/progress.md", "@8-2/progress.md")],
        tip="최대 횟수를 꼭 정하기 · 허용 도구는 loop.mjs 안의 목록만"),
}
