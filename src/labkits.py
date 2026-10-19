"""실습 진행 장표 데이터 — 하네스 미적용 → 하네스 만들기 → 적용 → 비교.

steps: (라벨, 종류, 내용) · 종류 p = 대화창에 붙여 넣을 요청문, do = 사람이 직접 하는 일
files: (저장 이름, 화면 경로, 원본) · 원본이 @로 시작하면 src/lab_harness/, 아니면 labs/
"""

KITS = {
    "1-1": dict(folder="transport_bill", steps=[
        ("① 하네스 미적용", "p", "transport_bill 폴더 안에서 하네스 없이(claude -p --setting-sources \"\") 「data 폴더의 운송비 청구를 검증해 줘.」를 실행하고\n답을 labs 바로 아래 runs/1-1/미적용.md 로 저장해 줘"),
        ("② 하네스 만들기", "do", "탐색기에서 새 파일 <b>transport_bill/CLAUDE.md</b> → 오른쪽 「복사」 → 붙여 넣기 → 저장"),
        ("③ 하네스 적용", "p", "transport_bill 폴더 안에서 같은 요청을 claude -p --setting-sources project 로 실행하고\n답을 labs 바로 아래 runs/1-1/적용.md 로 저장해 줘"),
        ("④ 비교", "p", "runs/1-1/ 의 두 답과 transport_bill/out/ 을 보고 표로 비교해 줘:\n이의 제기 건 · 결과 파일이 있는지 · 지급 여부까지 판단했는지 · 답 길이"),
    ], files=[("CLAUDE.md", "transport_bill/CLAUDE.md", "@1-1/CLAUDE.md")],
        tip="미적용을 다시 할 땐 CLAUDE.md를 잠시 다른 이름으로"),

    "2-1": dict(folder="order_api", split=True, steps=[
        ("① Skill · 하네스 미적용", "p", "order_api 폴더 안에서 하네스 없이(claude -p --setting-sources \"\") 「어제 14시에 MES가 20분 멈췄어. 장애 보고서 양식으로 정리해 줘」를 실행하고\n답을 labs 바로 아래 runs/2-1/미적용.md 로 저장해 줘"),
        ("② 하네스 만들기", "do", "앞 장 파일 두 개를 화면의 경로대로 · 탐색기 새 파일에 <b>order_api/.claude/skills/incident-report/SKILL.md</b> 처럼 경로째 입력"),
        ("③ Skill · 하네스 적용", "p", "order_api 폴더 안에서 같은 요청을 claude -p --setting-sources project 로 실행해 runs/2-1/적용.md 로 저장하고\n미적용과 양식 · 「(확인 필요)」 표시를 비교해 줘"),
        ("④ Sub Agent 보기", "do", "VS Code로 <b>labs/order_api</b> 를 열고 Claude Code에 「src/order_api.py 리뷰해 줘」 → 입력창 아래 <b>N agents</b> 클릭 또는 <b>/tasks</b>"),
        ("⑤ 확인", "do", "reviewer가 따로 돌고 있는지 · 쓴 도구가 Read · Grep · Glob뿐인지 · 토큰 · 메인은 결과만 받는지"),
    ], files=[("SKILL.md", "order_api/.claude/skills/incident-report/SKILL.md", "@2-1/SKILL.md"),
              ("reviewer.md", "order_api/.claude/agents/reviewer.md", "@2-1/reviewer.md")],
        tip="/tasks · agent map은 VS Code 확장 v2.1.269 이상 · 안 보이면 확장 업데이트"),

    "2-2": dict(folder="db_guard", split=True, harness_note="③ 단계에서 대화창에 붙여 넣는 요청문 · 내 말로 바꿔도 됨", steps=[
        ("① 준비", "p", "db_guard/project 폴더에서 python3 tools/make_db.py 로 DB를 만들고\npython3 scripts/report.py 가 어떤 오류로 멈추는지 보여 줘"),
        ("② 하네스 미적용 · 채점", "p", "python3 db_guard/check_hook.py 를 실행해 점수를 보여 줘"),
        ("③ 하네스 만들기", "do", "앞 장 요청문 「복사」 → 대화창에 붙여 넣기 · .claude 쓰기 승인 요청은 내용을 읽고 승인"),
        ("④ 하네스 적용 · 채점", "p", "python3 db_guard/check_hook.py 를 다시 실행해 Hook 만들기 전 점수와 비교하고\n놓친 사례가 있으면 Hook을 고쳐서 다시 채점해 줘"),
        ("⑤ 실제 차단", "p", "db_guard/project 폴더 안에서\nclaude -p --setting-sources project --permission-mode acceptEdits \"리포트 오류 고쳐 줘\" 를 실행하고\n운영 DB 쓰기가 Hook에 막혔는지 · 허락을 구했는지 알려 줘"),
    ], files=[("prompt.md", "Hook 만들기 요청문", "@PROMPT22")],
        tip="하네스 미적용 6 / 15 (허용할 것만 맞음) → 목표 15 / 15"),

    "2-3": dict(folder="office_work/workspace", steps=[
        ("① 하네스 미적용", "p", "office_work/workspace 폴더 안에서 아래 두 요청을 하나씩\nclaude -p --setting-sources \"\" --permission-mode acceptEdits 로 실행하고\n각 답을 office_work/workspace/_final_T3.txt · _final_T4.txt 로 저장해 줘\n- inputs/T3 회의록에서 할 일 정리해 줘.\n- inputs/T4 이번 주 설비 점검 기록으로 주간 보고서 만들어 줘."),
        ("② 채점", "p", "python3 office_work/grade.py office_work/workspace --task T3 T4 를 실행해 점수를 보여 줘"),
        ("③ 하네스 만들기", "do", "앞 장 파일 세 개를 화면의 경로대로 (CLAUDE.md · Skill 두 개)"),
        ("④ 하네스 적용", "p", "office_work/workspace 의 out 폴더와 _final_*.txt 를 지우고, 그 폴더 안에서 아래 두 요청을 하나씩\nclaude -p --setting-sources project --permission-mode acceptEdits 로 실행해\n각 답을 office_work/workspace/_final_T3.txt · _final_T4.txt 로 저장한 뒤\npython3 office_work/grade.py office_work/workspace --task T3 T4 로 채점해 줘\n- inputs/T3 회의록에서 할 일 정리해 줘.\n- inputs/T4 이번 주 설비 점검 기록으로 주간 보고서 만들어 줘."),
        ("⑤ 비교", "p", "미적용 · 적용 점수와 결과 파일 위치 · 근거 표기 · 「확인 필요」 표시를 표로 비교해 줘"),
    ], files=[("CLAUDE.md", "office_work/workspace/CLAUDE.md", "office_work/harness/CLAUDE.md"),
              ("SKILL.md", "office_work/workspace/.claude/skills/meeting-actions/SKILL.md", "office_work/harness/.claude/skills/meeting-actions/SKILL.md"),
              ("SKILL.md", "office_work/workspace/.claude/skills/weekly-report/SKILL.md", "office_work/harness/.claude/skills/weekly-report/SKILL.md")],
        tip="다른 과제 · T1 문의 답변 · T2 견적 · T5 정책 비교 · T6 지연 안내 메일 · 나머지 Skill은 office_work/harness/.claude/skills/"),

    "3-1": dict(folder="", steps=[
        ("① 압축 전 정리", "p", "지금까지 이 대화에서 한 일을 정리해 줘.\n실습별로 만든 파일 · 비교 결과 숫자 · 내가 준 지시를 빠짐없이.\nlabs 바로 아래 runs/3-1/압축전.md 로 저장해 줘"),
        ("② 대화로만 규칙", "p", "앞으로 모든 답의 첫 줄에 [확인] 이라고 붙여 줘"),
        ("③ 토큰 보기", "do", "<b>/context</b> → 전체 · Messages 토큰을 적어 두기"),
        ("④ 압축", "do", "<b>/compact</b> (지시 없이 그대로)"),
        ("⑤ 압축 후 정리", "p", "지금까지 이 대화에서 한 일을 다시 정리해서 runs/3-1/압축후.md 로 저장하고,\nruns/3-1/압축전.md 와 비교해 빠지거나 달라진 것을 표로 보여 줘"),
        ("⑥ 확인", "do", "/context 다시 · 답 첫 줄에 [확인]이 남았나 · 숫자 · 지시 중 빠진 것 → 앞 장 표와 맞춰 보기"),
    ], tip="해 보기: 다시 쌓인 뒤 /compact 실습 결과 숫자와 내 지시를 남겨 → 차이 비교"),

    "4-1": dict(folder="my_tool", open="labs/my_tool", steps=[
        ("① Superpowers 설치", "p", "/plugin marketplace add obra/superpowers-marketplace\n/plugin install superpowers@superpowers-marketplace"),
        ("② gstack 설치", "p", "gstack 을 ~/.claude/skills/gstack 에 설치해 줘\n(github.com/garrytan/gstack 을 --depth 1 로 받고 ./setup)"),
        ("③ 다시 열기", "do", "Claude Code 창을 닫고 새로 열기 → <b>/plugin</b> · <b>/help</b> 로 설치된 Skill · 명령 확인"),
        ("④ gstack", "p", "/office-hours 〈사전 과제 주제 한 줄〉 을 툴로 만들고 싶어"),
        ("⑤ Superpowers", "p", "/clear 후: 〈같은 주제〉 를 툴로 만들고 싶어. brainstorming 부터 해 줘"),
        ("⑥ 비교", "p", "두 번의 대화에서 각 하네스가 무엇을 물었는지 · 질문 수 · 만든 문서 · 다음 단계 제안을 표로 비교해 줘"),
    ], tip="질문에는 실제로 답해 보기 · 플러그인 설치가 막히면 강사 시연 · 결과 문서는 Ch8에서 이어서 씀"),

    "5-1": dict(folder="pr_review", open="labs/pr_review", split=True, steps=[
        ("① 하네스 미적용 리뷰", "p", "이 변경(CHANGES.md)을 코드 리뷰해 줘. 끝나면 답을 review_미적용.md 로 저장하고 걸린 시간도 알려 줘"),
        ("② 토큰 보기", "do", "<b>/context</b> 로 토큰 적어 두기"),
        ("③ 하네스 만들기", "do", "앞 장 파일 다섯 개를 화면의 경로대로 만들기 → Claude Code 새로 열기"),
        ("④ 멀티에이전트 리뷰", "p", "이 변경(CHANGES.md)을 코드 리뷰해 줘."),
        ("⑤ 동시 실행 보기", "do", "입력창 아래 <b>N agents</b> 클릭 또는 <b>/tasks</b> → reviewer · qa · security 상태 · 도구 · 토큰"),
        ("⑥ 비교", "p", "review_미적용.md 와 review/리뷰결과.md 를 비교해서\n찾은 문제 수 · 하나만 찾은 문제 · 시간 · 토큰을 표로 정리해 줘"),
    ], files=[("CLAUDE.md", "CLAUDE.md", "@5-1/CLAUDE.md"),
              ("SKILL.md", ".claude/skills/code-review/SKILL.md", "@5-1/skills/code-review/SKILL.md"),
              ("reviewer.md", ".claude/agents/reviewer.md", "@5-1/agents/reviewer.md"),
              ("qa.md", ".claude/agents/qa.md", "@5-1/agents/qa.md"),
              ("security.md", ".claude/agents/security.md", "@5-1/agents/security.md")],
        tip="해 보기: labs/pr_review_large (18파일)로 같은 비교 · 결과는 다음 장 실측과 맞춰 보기"),

    "5-2": dict(folder="office_work/workspace", steps=[
        ("① 단일 하네스 완성", "do", "2-3 하네스에 앞 장 <b>spec-quote</b> Skill 추가"),
        ("② 단일 하네스 · 실행", "p", "office_work/workspace 폴더 안에서\nclaude -p --setting-sources project --permission-mode acceptEdits --output-format json 으로\n「inputs/T7 사양서 40건 견적 내 줘. 사양서별 금액과 전체 합계까지.」 를 실행하고\n답을 office_work/workspace/_final_T7.txt 로 저장 · 걸린 시간과 토큰도 알려 줘"),
        ("③ 채점", "p", "python3 office_work/grade.py office_work/workspace --task T7 을 실행해 점수를 보여 줘"),
        ("④ 멀티에이전트 만들기", "do", "앞 장 extractor · verifier 파일 만들기 · <b>office_work/workspace/CLAUDE.md</b> 끝에 덧붙임 내용 붙여 넣기"),
        ("⑤ 멀티에이전트 · 실행", "p", "office_work/workspace 의 out/T7 과 _final_T7.txt 를 지우고, 그 폴더 안에서\nclaude -p --setting-sources project --permission-mode acceptEdits --output-format json 으로\n「inputs/T7 사양서 40건 견적 내 줘. 사양서별 금액과 전체 합계까지.」 를 실행해\n답을 _final_T7.txt 로 저장 · 시간과 토큰을 알려 주고\npython3 office_work/grade.py office_work/workspace --task T7 로 채점해 줘"),
        ("⑥ 비교", "p", "단일 vs 멀티 점수 · 시간 · 토큰 · Sub Agent 호출 수를 표로 비교해 줘"),
    ], files=[("SKILL.md", "office_work/workspace/.claude/skills/spec-quote/SKILL.md", "office_work/harness/.claude/skills/spec-quote/SKILL.md"),
              ("extractor.md", "office_work/workspace/.claude/agents/extractor.md", "office_work/harness_multi/.claude/agents/extractor.md"),
              ("verifier.md", "office_work/workspace/.claude/agents/verifier.md", "office_work/harness_multi/.claude/agents/verifier.md"),
              ("CLAUDE_추가.md", "office_work/workspace/CLAUDE.md 끝에 덧붙임", "office_work/harness_multi/CLAUDE.md")]),

    "6-1": dict(folder="", steps=[
        ("① 플러그인 없이", "p", "labs/plugin_check 를 runs/6-1/기준 으로 복사하고, 그 폴더 안에서 플러그인 없이\n(claude -p --setting-sources \"\" --output-format json) 아래 두 요청을 차례로 실행해 줘.\n요청마다 입력 · 출력 토큰과 바뀐 코드 줄 수, 테스트 결과를 기록해 줘.\n1. src/settle.js 가 하는 일을 설명해 줘\n2. CHANGES.md 기준대로 원 미만 절사와 1% 경계를 고치고 테스트를 추가해 줘"),
        ("② 설치", "p", "/plugin marketplace add JuliusBrussee/caveman\n/plugin install caveman@caveman\n/plugin marketplace add DietrichGebert/ponytail\n/plugin install ponytail@ponytail"),
        ("③ 다시 열기", "do", "Claude Code 창을 닫고 새로 열기 → <b>/plugin</b> 으로 두 플러그인이 켜졌는지 확인"),
        ("④ 플러그인 켜고", "p", "labs/plugin_check 를 runs/6-1/플러그인 으로 복사하고, 그 안에서 이번엔 설치한 플러그인을 쓰도록\n(claude -p --setting-sources user --output-format json) 같은 두 요청을 실행해 똑같이 기록해 줘"),
        ("⑤ 비교", "p", "runs/6-1/기준 과 runs/6-1/플러그인 결과를 표로 비교해 줘:\n요청별 입력 · 출력 토큰, 바뀐 줄 수, 테스트 통과 여부, 줄어든 비율"),
        ("⑥ 사람 판정", "do", "짧아진 설명이 여전히 맞는지 · 줄어든 코드가 기준을 지키는지 직접 읽고 판정 → 쓸지 말지"),
    ], tip="--setting-sources user 는 내 개인 설정 · CLAUDE.md도 함께 켜짐 · 하나씩 켜면 플러그인별 효과를 나눠 볼 수 있음"),

    "7-1": dict(folder="build_gate", split=True, steps=[
        ("① 하네스 미적용", "p", "labs/build_gate 를 runs/7-1/미적용 으로 복사하고, 그 안에서 하네스 없이(claude -p --setting-sources \"\")\n「src/settle.js 의 정산액 계산을 CHANGES.md 기준대로 원 미만 절사로 고쳐 줘.」를 실행한 뒤\nnode --test 결과를 알려 줘"),
        ("② 하네스 만들기", "do", "앞 장 파일 세 개를 <b>labs/build_gate</b> 안에 화면의 경로대로 (CLAUDE.md · .claude/settings.json · .claude/hooks/test_gate.mjs)"),
        ("③ 하네스 적용", "p", "labs/build_gate 를 runs/7-1/적용 으로 복사하고, 그 안에서 claude -p --setting-sources project 로 같은 요청을 실행한 뒤\nnode --test 결과를 알려 주고 ①과 표로 비교해 줘"),
        ("④ CI 보기", "do", "앞 장 <b>ci.yml</b> → .github/workflows/ci.yml 로 두면 PR마다 같은 테스트 · 사내 Git도 같은 방식"),
        ("⑤ 사람 판정", "do", "테스트 기대값을 바꿨다면 그 계산 근거가 맞는지 직접 확인 · 게이트를 통과해도 기대값이 틀리면 위험"),
    ], files=[("CLAUDE.md", "CLAUDE.md", "@7-1/CLAUDE.md"),
              ("settings.json", ".claude/settings.json", "@7-1/settings.json"),
              ("test_gate.mjs", ".claude/hooks/test_gate.mjs", "@7-1/hooks/test_gate.mjs"),
              ("ci.yml", ".github/workflows/ci.yml", "@7-1/ci.yml")],
        tip="Stop Hook이 테스트 실패면 「끝내지 마」로 돌려보냄 · 8번 연속이면 Claude Code가 무시하므로 무한 반복은 없음"),

    "8-1": dict(folder="meta_harness", open="labs/meta_harness", steps=[
        ("① 메타 하네스 만들기", "do", "Ch8 「메타 하네스를 만드는 요청문」 붙여 넣기 → 만든 파일 확인 → Claude Code 새로 열기"),
        ("② 내 주제로 시작", "p", "내 하네스를 만들고 싶어: 〈사전 과제 주제 한 줄〉.\n예시 입력은 ../samples/〈분야〉/ 를 써. 인터뷰부터 시작해 줘"),
        ("③ 사람 승인", "do", "인터뷰 답 → docs/〈이름〉/spec.md 검토 → 괜찮으면 새 파일 <b>docs/〈이름〉/APPROVED</b> (사람만)"),
        ("④ 생성 · 시험", "p", "docs/〈이름〉/APPROVED 만들었어. 하네스를 만들고 검토 · 시험까지 해 줘"),
        ("⑤ 개발 주제라면", "do", "<b>labs/my_tool</b> 를 열고 Superpowers 설치 → 「Superpowers로 개발하기」 요청문 → 설계 승인 · DESIGN.md · 계획 승인 → 구현"),
        ("⑥ 사람 판정 · 공유", "do", "비교표 · 결과물을 직접 판정 → 다음 장 양식으로 패들릿에 올리기"),
    ], tip="샘플 데이터 labs/samples/ · 플러그인 설치가 막히면 Superpowers는 강사 시연"),
    "8-2": dict(folder="settle_check", open="labs/settle_check", steps=[
        ("① 첫 커밋", "p", "이 폴더를 git 저장소로 만들고 첫 커밋 해 줘"),
        ("② 하네스 만들기", "do", "앞 장 파일 네 개(CLAUDE.md · PROMPT.md · features.json · progress.md)를 같은 이름으로 만들기 → 커밋"),
        ("③ 루프 실행", "do", "VS Code 터미널에서 <b>node loop.mjs 8</b> · 한 번마다 남은 기능 · 시간 · 토큰이 찍힘"),
        ("④ 진행 보기", "do", "features.json 의 passes · progress.md · git log 가 한 칸씩 바뀌는지"),
        ("⑤ 정리", "p", "features.json · progress.md · git log 를 보고 기능별 결과 · 걸린 횟수 · 막힌 점을 표로 정리해 줘"),
        ("⑥ 사람 판정", "do", "터미널에서 node src/cli.js data/운송비청구.csv 를 직접 실행해 이의 제기 건이 맞는지 확인"),
    ], files=[("CLAUDE.md", "settle_check/CLAUDE.md", "@8-2/CLAUDE.md"),
              ("PROMPT.md", "settle_check/PROMPT.md", "@8-2/PROMPT.md"),
              ("features.json", "settle_check/features.json", "@8-2/features.json"),
              ("progress.md", "settle_check/progress.md", "@8-2/progress.md")],
        tip="최대 횟수를 꼭 정하기 · 허용 도구는 loop.mjs 안의 목록만"),
}
