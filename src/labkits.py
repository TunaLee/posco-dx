"""실습 진행 장표 데이터 — 하네스 미적용 → 하네스 만들기 → 적용 → 비교.

steps: (라벨, 종류, 내용) · 종류 p = 대화창에 붙여 넣을 요청문, do = 사람이 직접 하는 일
files: (저장 이름, 화면 경로, 원본) · 원본이 @로 시작하면 src/lab_harness/, 아니면 labs/
"""

KITS = {
    "1-1": dict(folder="lab1_1_same_question", steps=[
        ("① 하네스 미적용 · 10번", "p", "lab1_1_same_question 폴더 안에서 질문.txt 의 질문을\nclaude -p --setting-sources \"\" --tools \"\" 로 10번 실행해\n답을 labs 바로 아래 runs/1-1/미적용_01.txt ~ 10.txt 로 저장해 줘"),
        ("② 하네스 만들기", "do", "탐색기에서 새 파일 <b>lab1_1_same_question/CLAUDE.md</b> → 오른쪽 「복사」 → 붙여 넣기 → 저장"),
        ("③ 하네스 적용 · 10번", "p", "lab1_1_same_question 폴더 안에서 같은 질문을\nclaude -p --setting-sources project --tools \"\" 로 10번 실행해\n답을 labs 바로 아래 runs/1-1/적용_01.txt ~ 10.txt 로 저장해 줘"),
        ("④ 비교", "p", "runs/1-1/ 의 미적용 · 적용 답을 비교해 표로 정리해 줘:\n분야 판단 종류 수 · 같은 형식(JSON) 답 수 · 교체를 약속한 답 수 · 평균 글자 수"),
    ], files=[("CLAUDE.md", "lab1_1_same_question/CLAUDE.md", "@1-1/CLAUDE.md")],
        tip="결과는 lab 폴더 밖 runs/ 에 · 미적용을 다시 하려면 CLAUDE.md를 잠시 다른 이름으로 (폴더 안 파일은 Claude가 읽음)"),

    "2-1": dict(folder="lab2_1_parts", steps=[
        ("① 하네스 미적용", "p", "lab2_1_parts 폴더 안에서 아래 두 요청을 하나씩\nclaude -p --setting-sources \"\" --output-format stream-json --verbose 로 실행해\nlabs 바로 아래 runs/2-1/미적용_1.jsonl · 2.jsonl 로 저장해 줘\n1. 어제 14시에 MES가 20분 멈췄어. 장애 보고서 양식으로 정리해 줘\n2. src/order_api.py 리뷰해 줘"),
        ("② 하네스 만들기", "do", "오른쪽 파일 두 개를 화면의 경로대로 · 탐색기 새 파일에 <b>lab2_1_parts/.claude/skills/incident-report/SKILL.md</b> 처럼 경로째 입력"),
        ("③ 하네스 적용", "p", "①의 두 요청을 --setting-sources project 로 바꿔 같은 방법으로 실행해\nlabs 바로 아래 runs/2-1/적용_1.jsonl · 2.jsonl 로 저장해 줘"),
        ("④ 비교", "p", "runs/2-1/ 의 미적용 · 적용 기록을 비교해 표로 정리해 줘:\n보고서 양식 · 「(확인 필요)」 표시 · Skill 호출 여부 · reviewer 위임 여부 · 파일 수정 여부"),
    ], files=[("SKILL.md", "lab2_1_parts/.claude/skills/incident-report/SKILL.md", "@2-1/SKILL.md"),
              ("reviewer.md", "lab2_1_parts/.claude/agents/reviewer.md", "@2-1/reviewer.md")]),

    "2-2": dict(folder="lab2_hook_by_claude", steps=[
        ("① 준비", "p", "lab2_hook_by_claude/project 폴더에서 python3 tools/make_db.py 로 DB를 만들고\npython3 scripts/report.py 가 어떤 오류로 멈추는지 보여 줘"),
        ("② 하네스 미적용 · 채점", "p", "python3 lab2_hook_by_claude/check_hook.py 를 실행해 점수를 보여 줘"),
        ("③ 하네스 만들기", "do", "오른쪽 요청문 「복사」 → 대화창에 붙여 넣기 · .claude 쓰기 승인 요청은 내용을 읽고 승인"),
        ("④ 하네스 적용 · 채점", "p", "python3 lab2_hook_by_claude/check_hook.py 를 다시 실행해 ②와 비교하고\n놓친 사례가 있으면 Hook을 고쳐서 다시 채점해 줘"),
        ("⑤ 실제 차단", "p", "lab2_hook_by_claude/project 폴더 안에서\nclaude -p --setting-sources project --permission-mode acceptEdits \"리포트 오류 고쳐 줘\" 를 실행하고\n운영 DB 쓰기가 Hook에 막혔는지 · 허락을 구했는지 알려 줘"),
    ], files=[("prompt.md", "Hook 만들기 요청문", "@PROMPT22")],
        tip="하네스 미적용 6 / 15 (허용할 것만 맞음) → 목표 15 / 15"),

    "2-3": dict(folder="work_harness/workspace", steps=[
        ("① 하네스 미적용", "p", "work_harness/workspace 폴더 안에서 아래 두 요청을 하나씩\nclaude -p --setting-sources \"\" --permission-mode acceptEdits 로 실행하고\n각 답을 work_harness/workspace/_final_T3.txt · _final_T4.txt 로 저장해 줘\n- inputs/T3 회의록에서 할 일 정리해 줘.\n- inputs/T4 이번 주 설비 점검 기록으로 주간 보고서 만들어 줘."),
        ("② 채점", "p", "python3 work_harness/grade.py work_harness/workspace --task T3 T4 를 실행해 점수를 보여 줘"),
        ("③ 하네스 만들기", "do", "앞 장 파일 세 개를 화면의 경로대로 (CLAUDE.md · Skill 두 개)"),
        ("④ 하네스 적용", "p", "work_harness/workspace 의 out 폴더와 _final_*.txt 를 지우고\n①의 두 요청을 --setting-sources project 로 바꿔 같은 방법으로 실행한 뒤 ②처럼 채점해 줘"),
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

    "5-1": dict(folder="", steps=[
        ("① 실행", "p", "lab5_multiagent/run.py --ids Q10 을 실행하고\n위임 순서 · 줄별 토큰 · 검증 결과를 정리해 줘"),
        ("② 타임라인", "p", "방금 저장된 runs/ 기록으로 lab5_multiagent/visualize.py 를 돌려\n타임라인 HTML을 만들고 열어 줘"),
        ("③ 검증 빼 보기", "p", "lab5_multiagent/project 의 지휘 Skill 에서 검증 단계를 지우고 ①을 다시 →\n타임라인 비교 · 끝나면 되돌려 줘"),
        ("④ 까다로운 입력", "p", "run.py 를 --ids Q26 (프롬프트 주입) 로도 돌려\nverifier가 막았는지 알려 줘"),
    ], files=[("SKILL.md", "지휘 Skill", "lab5_multiagent/project/.claude/skills/orchestrate-pangyo/SKILL.md"),
              ("verifier.md", "검증 Agent", "lab5_multiagent/project/.claude/agents/verifier-pangyo.md")]),

    "5-2": dict(folder="work_harness/workspace", steps=[
        ("① 단일 하네스 완성", "do", "2-3 하네스에 앞 장 <b>spec-quote</b> Skill 추가"),
        ("② 단일 하네스 · 실행", "p", "work_harness/workspace 폴더 안에서\nclaude -p --setting-sources project --permission-mode acceptEdits --output-format json 으로\n「inputs/T7 사양서 40건 견적 내 줘. 사양서별 금액과 전체 합계까지.」 를 실행하고\n답을 work_harness/workspace/_final_T7.txt 로 저장 · 걸린 시간과 토큰도 알려 줘"),
        ("③ 채점", "p", "python3 work_harness/grade.py work_harness/workspace --task T7 을 실행해 점수를 보여 줘"),
        ("④ 멀티에이전트 만들기", "do", "앞 장 extractor · verifier 파일 만들기 · <b>work_harness/workspace/CLAUDE.md</b> 끝에 덧붙임 내용 붙여 넣기"),
        ("⑤ 멀티에이전트 · 실행", "p", "work_harness/workspace 의 out/T7 과 _final_T7.txt 를 지우고 ②③을 다시 해 줘"),
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

    "7-1": dict(folder="", steps=[
        ("① judge 일치도", "p", "lab7_eval_regression/agreement.py 를 실행해\njudge와 사람 채점 일치도를 설명해 줘"),
        ("② 기준선", "p", "lab7_eval_regression/run_suite.py -n 10 --k 3 실행 →\n결과 파일 경로와 점수 요약"),
        ("③ 일부러 나쁘게", "p", "lab1_harness_vs_bare/harness/CLAUDE.md 에서\n환불 · 징계를 약속하지 않는다는 줄을 지우고 ②를 다시 실행해 줘"),
        ("④ 회귀 확인", "p", "lab7_eval_regression/compare.py 로 ②③ 결과를 비교해\n무엇이 나빠졌는지 · 회귀로 실패했는지 알려 줘. 끝나면 CLAUDE.md 되돌려 줘"),
        ("⑤ 내 평가 문항", "p", "내 업무 평가 문항 5개 (엣지 케이스 2개 포함) 를 eval/cases.jsonl 로 만들어 줘:\n입력 · 기대 결과 · 꼭 들어갈 말 · 들어가면 안 되는 말"),
    ]),

    "7-2": dict(folder="my_work_harness", steps=[
        ("① 설계표", "p", "my_work_spec/내_하네스_설계표.md 의 다섯 유형 중 내 업무 〈한 줄 설명〉 과 가장 비슷한 예시를 골라\n내 업무 값으로 채워 줘. 모르는 칸은 TODO · 고객명 · 실제 수치는 가상 값으로"),
        ("② 예시 입력", "do", "<b>my_work_harness/inputs/</b> 에 내 업무의 가상 예시 입력 3~5개 (실제 고객 정보 넣지 않기)"),
        ("③ 하네스 미적용", "p", "my_work_harness 폴더 안에서 inputs/ 의 입력마다 〈내 업무 요청 한 줄〉 을\nclaude -p --setting-sources \"\" --permission-mode acceptEdits 로 실행해\n답을 labs 바로 아래 runs/7-2/미적용_<입력 이름>.md 로 저장해 줘"),
        ("④ 하네스 만들기", "p", "my_work_spec/내_하네스_설계표.md 를 읽고 my_work_harness 에 하네스를 만들어 줘.\n- CLAUDE.md (공통 원칙 30줄 이내) · Skill 1개 (절차 · 판단 기준 · 결과 양식)\n- Hook (설계표의 「막을 것」만 차단)\n설계표에 없는 규칙은 지어내지 말고 TODO로"),
        ("⑤ 하네스 적용", "p", "③과 같은 입력 · 같은 요청을 --setting-sources project 로 실행해\nlabs 바로 아래 runs/7-2/적용_<입력 이름>.md 로 저장해 줘"),
        ("⑥ 사람 판정", "do", "runs/7-2 의 미적용 · 적용을 나란히 놓고 설계표의 「잘했다의 기준」으로 직접 O / X · 자동 채점 · Claude 의견은 참고만"),
    ], tip="이 실습의 하네스와 설계표가 내 업무용 최종 결과물 · 요청문 ①②③ · 부록 ①~⑥을 재료로"),

    "8-1": dict(folder="final_dev_harness", open="labs/final_dev_harness", steps=[
        ("① 첫 커밋", "p", "이 폴더를 git 저장소로 만들고 첫 커밋 해 줘"),
        ("② 하네스 만들기", "do", "앞 장 「개발 하네스를 만드는 요청문」 붙여 넣기 → 만든 파일 확인 → 커밋 → Claude Code 새로 열기"),
        ("③ 브레인스토밍 · 기획", "p", "아이디어.md 를 읽고 브레인스토밍부터 시작해 줘"),
        ("④ 사람 승인", "do", "docs/plan.md 검토 · 고칠 점은 대화로 → 괜찮으면 탐색기에서 새 파일 <b>docs/APPROVED</b> (사람만)"),
        ("⑤ 병렬 구현", "p", "docs/APPROVED 만들었어. CLAUDE.md 순서대로 구현을 진행해 줘"),
        ("⑥ 사람 판정", "do", "직접 실행해 보고 내 합격 기준으로 판정 · 아니면 무엇이 틀렸는지 말하고 다시"),
    ], tip="Node 18 이상 · git · 워크트리 · .claude 쓰기 승인 요청은 내용을 읽고 승인"),
}
