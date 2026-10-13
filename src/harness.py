"""하네스 엔지니어링 · 평가/검증 — 판교 · 포항 두 판본.

python3 src/build.py pangyo   → docs/pangyo/index.html
python3 src/build.py pohang   → docs/pohang/index.html
부품은 deck.py · explain.py · intro.py, 장면은 scenes_*.py.
"""
import deck
import explain
import intro
from deck import ba, bridge, cards, divider, flow, ill, lab, light

code = explain.prompt
V = "pangyo"            # slides(variant) 가 바꾼다
REPO = "https://github.com/TunaLee/posco-dx/tree/main/labs"


def P():
    return V == "pangyo"


def table(head, rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="dbt"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def note(label, text):
    return f'<div class="dbnote"><span>{label}</span> {text}</div>'


def vl(*items):
    return '<div class="vl">' + "".join(f"<p>{x}</p>" for x in items) + "</div>"


def two(a, b):
    return f'<div class="twocol">{a}{b}</div>'


# ── 하네스 지도: 모델을 가운데 두고 부품이 둘러싼다. 장마다 그 장의 부품이 켜진다 ──
PARTS = [
    ("지침", "CLAUDE.md · 시스템 프롬프트", "Ch1", (250, 255)),
    ("Skill", "필요할 때 꺼내 쓰는 절차", "Ch2", (640, 215)),
    ("Tool · MCP", "조회 · 계산 · 외부 연결", "Ch3", (1030, 255)),
    ("Sub Agent", "역할 분리 · 별도 컨텍스트", "Ch3", (1030, 590)),
    ("Hook · 권한", "막기 · 기록 · 승인", "Ch2", (640, 650)),
    ("평가", "지표 · 평가셋 · 회귀 테스트", "Ch4", (250, 590)),
]


def hx_map(active=None, kick="하네스 지도", title="모델을 감싸는 여섯 부품"):
    hub = (640, 430)
    lines, cards_ = [], []
    for name, desc, ch, (x, y) in PARTS:
        st = "all" if active is None else ("on" if name in active else "dim")
        style = {"all": 'stroke="#F28C28" stroke-width="2.5" stroke-dasharray="6 7" opacity=".7"',
                 "dim": 'stroke="#fff" stroke-width="2" stroke-dasharray="4 8" opacity=".12"',
                 "on": 'stroke="#F28C28" stroke-width="5" opacity=".35"'}[st]
        lines.append(f'<line x1="{hub[0]}" y1="{hub[1]}" x2="{x}" y2="{y}" {style}/>')
        if st != "dim":
            lines.append(f'<line class="flow" x1="{hub[0]}" y1="{hub[1]}" x2="{x}" y2="{y}" stroke="#F28C28" '
                         f'stroke-width="{5 if st == "on" else 3}" stroke-linecap="round" stroke-dasharray="14 12"/>')
        cards_.append(f'''<div class="node {st}" style="left:{x-170}px; top:{y-46}px">
  <div class="nh"><span class="chip">{ch}</span><b>{name}</b></div>
  <div class="icons"><span class="nm">{desc}</span></div>
</div>''')
    return f'''<section class="slide dk eco{' focus' if active else ''}" data-title="{title}">
  {intro.coord()}
  <div class="kick">{kick}</div>
  <h2>{title}</h2>
  <svg class="ecosvg" viewBox="0 0 1280 720">{"".join(lines)}</svg>
  {"".join(cards_)}
  <div class="hub hubtxt" style="left:{hub[0]-74}px; top:{hub[1]-74}px">모델</div>
</section>'''


def chapter(ch, title, active, map_title):
    return [divider(ch, title, ""), hx_map(active, f"하네스 지도 · {ch}", map_title)]


# ── 오프닝 ──────────────────────────────────────────────
AGENDA = [
    ("Ch1", "하네스 개념", "하네스 없는 Agent vs 있는 Agent 비교표"),
    ("Ch2", "Claude Code 하네스 분해", "업무 Skill · 안전 Hook"),
    ("Ch3", "Agent SDK 커스텀 하네스", "Supervisor + Sub Agent"),
    ("Ch4", "평가 설계", "평가셋 · judge 기준"),
    ("Ch5", "자동 평가 · 운영", "회귀 테스트 파이프라인"),
]


def cover():
    site = "판교" if P() else "포항"
    return f'''<section class="slide dk cover-dk active" data-title="표지">
  <div class="glow"></div>
  <div class="kick">AX 심화 · {site}</div>
  <h1>하네스 엔지니어링<br/>· 평가와 검증</h1>
</section>'''


def agenda():
    rows = "".join(f'''<div class="ch"><span class="chip">{c}</span><div class="tx"><b>{t}</b><span>{d}</span></div></div>'''
                   for c, t, d in AGENDA)
    return f'''<section class="slide dk" data-title="목차">
  {intro.coord()}
  <h2>목차</h2>
  <div class="days one"><div class="daycol">{rows}</div></div>
</section>'''


def scenario():
    if P():
        return light("공통 예제: 문의 대응 라우팅 Agent", (
            flow([("문의 접수", ""), ("의도 분류", "Supervisor"), ("전문 Sub Agent", "IT · 구매 · 인사 · 보안"), ("검증", "Supervisor"), ("답변 · 사람에게", "")], hl=3)
            ) + note("데이터", "가상 사내 문의 30건 · 영역별 FAQ 5개 · 엣지 케이스 포함"), "시작")
    return light("공통 예제: 사양서 추출 · 견적 Agent", (
        flow([("사양서", "도면 · 스펙 요약"), ("추출", "품목 · 규격 · 재질 · 수량"), ("견적", "단가표 계산"), ("검증", "Supervisor"), ("결과 · 사람에게", "")], hl=3)
        ) + note("데이터", "가상 사양서 10건 · 정답 JSON · 단가표 · 숫자 충돌 · 수량 누락 포함"), "시작")


def opening():
    out = [
        cover(),
        intro.speaker(),
        agenda(),
        light("실습 환경", table(["도구", "용도"], [
            ["<b>VS Code</b>", "코드 · 데이터 열기"],
            ["<b>Python 3.10+ · venv</b>", "Agent SDK 실습"],
            ["<b>Claude Code</b>", "Skill · Sub Agent · Hook 실습"],
            ["<b>Claude Agent SDK</b>", "<code>pip install claude-agent-sdk</code>"],
            ["<b>API 키</b>", "<code>ANTHROPIC_API_KEY</code> · 실행마다 비용 발생"],
        ]) + note("실습 저장소", f'<a class="dl" href="{REPO}">posco-dx/labs</a>'), "시작"),
        scenario(),
        light("수업 방식", cards([
            ("받아서 고치기", "코드는 제공 · 프롬프트 · 설정 · 값만 수정", []),
            ("숫자로 비교", "적용 전후를 일관성 · 정확도 · 토큰으로", []),
            ("나만의 결과물", "장마다 내 Skill · Hook · Agent · 평가셋", []),
        ]), "시작"),
        hx_map(),
    ]
    return out


# ── Ch1 하네스 개념 ─────────────────────────────────────
def ch1():
    layers = table(["계층", "담는 것", "설계 결정"], [
        ["<b>모델</b>", "추론 엔진", "어떤 모델 · effort · 비용 한도"],
        ["<b>컨텍스트</b>", "지침 · 참고 자료 · 대화 이력", "무엇을 항상 넣고, 무엇을 필요할 때만"],
        ["<b>도구</b>", "조회 · 계산 · 실행", "도구 이름 · 설명 · 입력 형식 · 개수"],
        ["<b>권한</b>", "허용 · 금지 · 승인", "자동 허용 범위 · 사람 승인 지점"],
        ["<b>평가</b>", "지표 · 평가셋 · 로그", "무엇을 성공으로 볼지"],
    ])
    parts = table(["부품", "막는 문제", "없으면"], [
        ["<b>지침</b>", "답 형식 · 기준이 흔들림", "같은 질문에 매번 다른 형식"],
        ["<b>Skill</b>", "절차 누락", "체크리스트 단계 건너뜀"],
        ["<b>Tool</b>", "지어낸 숫자", "조회 대신 기억으로 답"],
        ["<b>Sub Agent</b>", "컨텍스트 오염", "긴 작업 중 앞 지시를 잊음"],
        ["<b>Hook · 권한</b>", "위험한 실행", "삭제 · 강제 push · 비밀 파일 수정"],
        ["<b>평가</b>", "조용한 품질 저하", "프롬프트 수정 후 다른 곳이 깨짐"],
    ])
    onboard = table(["신입사원이 받는 것", "Agent의 하네스"], [
        ["회사 소개 · 업무 규칙", "지침 (CLAUDE.md · 시스템 프롬프트)"],
        ["업무 매뉴얼", "Skill"],
        ["사내 시스템 계정", "Tool · MCP"],
        ["옆 팀 협업", "Sub Agent"],
        ["결재 · 보안 규정", "Hook · 권한"],
        ["수습 평가", "평가셋 · 회귀 테스트"],
    ])
    out = chapter("Ch1", "하네스 엔지니어링 개념", {"지침"}, "모델과 계층 설계") + [
        ill("scenes_more", "harness_rig", "left40", "하네스: 모델에 채우는 장비",
            ["모델: 답을 만드는 엔진", "하네스: 모델을 감싼 나머지 전부"]),
        light("하네스의 다섯 계층", layers, "Ch1"),
        light("프롬프트 → 컨텍스트 → 하네스", '''<div class="tline">
  <div class="tl"><b>프롬프트</b><span>한 번의 질문을 잘 쓰기</span></div>
  <div class="tl"><b>컨텍스트</b><span>무엇을 보여 줄지 고르기</span></div>
  <div class="tl hl"><b>하네스</b><span>도구 · 권한 · 평가까지 환경 전체</span></div>
</div>''' + note("실무 기준", "한 번 쓰고 끝 → 프롬프트 · 매번 같은 자료 → 컨텍스트 · 반복 · 위험 · 여러 사람 → 하네스"), "Ch1"),
        light("같은 모델, 다른 하네스", table(["차이", "하네스 A", "하네스 B"], [
            ["<b>도구 설계</b>", "「검색」 도구 하나 · 설명 한 줄", "「FAQ 조회」 「규정 조회」 분리 · 입력 예시"],
            ["<b>컨텍스트</b>", "대화 이력 전부 누적", "핵심만 남기고 Sub Agent로 분리"],
            ["<b>권한</b>", "모든 도구 자동 허용", "읽기만 자동 · 쓰기는 승인"],
            ["<b>결과</b>", "답이 흔들리고 토큰 증가", "답 고정 · 토큰 감소"],
        ]), "Ch1"),
        ill("scenes_hx", "wobbly_vs_steady", "top20", "하네스 없는 Agent vs 있는 Agent",
            ["없음: 같은 질문에 매번 다른 답", "있음: 같은 형식 · 같은 근거"]),
        light("부품마다 막는 문제", parts, "Ch1"),
        light("신입사원 온보딩과 같은 구조", onboard, "Ch1"),
    ]
    if not P():  # 포항: 도입 비중 크게
        out += [
            light("일관성은 숫자로 잰다", table(["지표", "재는 법"], [
                ["<b>답 일치율</b>", "같은 질문 N번 → 가장 많은 답의 비율"],
                ["<b>형식 준수율</b>", "정해진 JSON · 표 형식을 지킨 비율"],
                ["<b>근거 일치</b>", "답의 숫자가 원문에 있는 비율"],
                ["<b>토큰 · 비용</b>", "실행 1회당 입력 · 출력 토큰"],
            ]), "Ch1"),
            ba("하네스 한 장의 차이", "Ch1",
               "이 사양서에서 품목과 수량 알려 줘\n\n→ 1회: 표 · 2회: 문장 · 3회: 수량 단위 누락",
               "역할: 사양서 추출 담당\n출력: JSON {품목, 규격, 재질, 수량, 단위, 비고}\n규칙: 원문에 없는 숫자는 쓰지 않음, 없으면 null\n\n→ 5회 모두 같은 JSON"),
        ]
    out += [
        code_slide("실습 1 실행", "lab1_no_harness_vs_harness",
                   "python lab1_no_harness_vs_harness/compare_runs.py --track {track} -n 5\n\n"
                   "[bare]    서로 다른 답 4종 · 평균 입력 토큰 …\n"
                   "[harness] 서로 다른 답 1종 · 평균 입력 토큰 …"),
        lab("1-1", "같은 질문 다섯 번", "Ch1",
            "하네스 전후의 흔들림을 숫자로",
            ["하네스 없이 5회 실행 → 답 종류 수 기록", "harness_prompt.md에 역할 · 출력 형식 · 규칙 쓰기", "같은 질문 5회 다시 실행", "답 종류 수 · 토큰 비교표 채우기"],
            ["답 종류 1~2종으로 감소", "비교표: 일관성 · 토큰 · 비용"], files="lab1_no_harness_vs_harness"),
        bridge("다음: Claude Code 하네스 뜯어보기", "", "Ch1", "→ Ch2 Skill · Sub Agent · Hook"),
    ]
    return out


def code_slide(title, folder, body):
    return light(title, code(folder, body.replace("{track}", V)), "실습")


# ── Ch2 Claude Code 하네스 분해 ──────────────────────────
def ch2():
    when = table(["요소", "언제 로드 · 실행", "성격"], [
        ["<b>CLAUDE.md</b>", "세션 시작 때 항상", "부탁 (따르려고 읽는 컨텍스트)"],
        ["<b>Skill</b>", "설명만 상시 · 본문은 호출될 때", "절차 (필요할 때만 꺼내 씀)"],
        ["<b>Sub Agent</b>", "위임할 때 새 컨텍스트로", "분업 (결과만 돌려받음)"],
        ["<b>Hook</b>", "도구 호출 전후 등 이벤트마다", "강제 (코드가 결정)"],
        ["<b>권한</b>", "도구를 쓰기 직전", "허용 · 거부 · 승인 요청"],
        ["<b>MCP</b>", "도구 목록은 상시 · 실행은 호출 때", "외부 시스템 연결"],
    ])
    skill = ("---\n"
             "name: weekly-report   # 이름은 자유\n"
             "description: 주간 보고서를 팀 양식으로 쓸 때 사용\n"
             "---\n"
             "## 순서\n"
             "1. 지난주 완료 · 진행 · 이슈를 표로\n"
             "2. 숫자는 첨부 자료에서만, 없으면 [확인 필요]\n"
             "3. 마지막 줄: 다음 주 할 일 3개\n"
             "## 참고\n"
             "- template.md (양식)")
    agent = ("---\n"
             "name: reviewer\n"
             "description: 변경 사항 리뷰. 수정은 하지 않음\n"
             "tools: Read, Grep, Glob        # 읽기 전용\n"
             "model: sonnet\n"
             "---\n"
             "변경된 파일만 읽고, 문제를 심각도 순으로 보고한다.\n"
             "보고 형식: 파일:줄 · 문제 · 근거 · 제안")
    hook_cfg = ('"PreToolUse": [{ "matcher": "Bash|Write|Edit",\n'
                '  "hooks": [{ "type": "command", "command": "python3 .claude/hooks/guard.py" }] }]')
    guard = ("import json, sys\n"
             "e = json.load(sys.stdin)            # 도구 이름 · 입력\n"
             "i = e.get('tool_input', {})\n"
             "bad = ['rm -rf', 'push --force']\n"
             "if any(b in i.get('command', '') for b in bad) \\\n"
             "   or i.get('file_path', '').endswith('.env'):\n"
             "    print('차단: 위험 명령 · 비밀 파일', file=sys.stderr)\n"
             "    sys.exit(2)                     # 2 = 막고 이유를 Claude에게")
    out = chapter("Ch2", "Claude Code 하네스 분해", {"Skill", "Hook · 권한", "Sub Agent"}, "Skill · Sub Agent · Hook") + [
        light("언제 로드되고 언제 실행되나", when, "Ch2"),
        light("부탁 · 절차 · 강제", cards([
            ("CLAUDE.md = 부탁", "모델이 읽고 따르려 함 · 어길 수 있음", []),
            ("Skill = 절차", "필요할 때만 불러 컨텍스트 절약", []),
            ("Hook = 강제", "코드가 막음 · 모델이 우회 못 함", []),
        ]), "Ch2"),
        light("Skill 한 개의 구조", two(code(".claude/skills/weekly-report/SKILL.md", skill),
                                        vl("description: 언제 부를지 판단 기준", "본문: 호출될 때만 로드", "참고 파일: 양식 · 예시"))
              + note("이름", "예시일 뿐 · 팀 규칙에 맞게 자유롭게"), "Ch2"),
        ill("scenes_ch5", "conveyor", "top20", "Skill은 필요할 때만 붙는 지침", ["상시 로드: 설명 한 줄", "호출 시: 본문 · 참고 파일"]),
        lab("2-1", "업무 Skill 만들기", "Ch2",
            "반복 업무 하나를 Skill로 · 적용 전후 비교",
            ["예시 Skill(incident-report) 열어 보기", "내 업무(보고서 양식 · 리뷰 기준)로 SKILL.md 쓰기", "같은 요청을 Skill 없이 · 있이 각각 실행", "형식 준수 · 누락 단계 비교"],
            ["새 세션에서 자동 호출 확인", "체크리스트 누락 0"], files="lab2_skill_hook"),
        light("Sub Agent 경계 설계", table(["경계", "정하는 것", "예: reviewer"], [
            ["<b>도구 집합</b>", "쓸 수 있는 도구", "Read · Grep · Glob"],
            ["<b>권한</b>", "쓰기 · 실행 허용 여부", "쓰기 금지"],
            ["<b>컨텍스트</b>", "보여 줄 자료 범위", "변경 파일만"],
            ["<b>반환 형식</b>", "부모가 받을 결과", "파일:줄 · 문제 · 근거"],
        ]), "Ch2"),
        light("Sub Agent 정의 파일", two(code(".claude/agents/reviewer.md", agent),
                                          vl("자기 컨텍스트에서 일함", "부모는 결과만 받음", "도구를 줄이면 권한도 줄어듦")), "Ch2"),
        light("Hook: 막는 건 코드가", code(".claude/settings.json (hooks 부분)", hook_cfg) + code(".claude/hooks/guard.py", guard), "Ch2"),
        lab("2-2", "안전 Hook", "Ch2",
            "위험 명령 · 비밀 파일 수정을 코드로 차단",
            ["guard.py 차단 목록 확인 · 하나 추가", "settings.json에 PreToolUse 등록", "Claude Code에 「.env 고쳐 줘」 요청", "차단 메시지 · 로그 확인"],
            ["rm -rf · 강제 push · .env 수정 차단", "막힌 이유가 Claude에게 전달됨"], files="lab2_skill_hook"),
        bridge("다음: 같은 하네스를 코드로", "", "Ch2", "→ Ch3 Agent SDK"),
    ]
    return out


# ── Ch3 Agent SDK ───────────────────────────────────────
def ch3():
    basic = ("import asyncio\n"
             "from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage\n\n"
             "options = ClaudeAgentOptions(\n"
             "    system_prompt=open('harness_prompt.md').read(),\n"
             "    allowed_tools=[],          # 자동 허용할 도구\n"
             "    setting_sources=[],        # 내 PC 설정 영향 끄기\n"
             "    max_turns=5,\n"
             ")\n\n"
             "async def main():\n"
             "    async for m in query(prompt='VPN이 안 붙어요', options=options):\n"
             "        if isinstance(m, ResultMessage):\n"
             "            print(m.result, m.total_cost_usd, m.usage)\n\n"
             "asyncio.run(main())")
    tool_code = ("from claude_agent_sdk import tool, create_sdk_mcp_server\n\n"
                 "@tool('search_kb', '영역별 FAQ에서 조항을 찾는다', {'domain': str, 'q': str})\n"
                 "async def search_kb(args):\n"
                 "    hits = find(args['domain'], args['q'])      # 파일 검색\n"
                 "    return {'content': [{'type': 'text', 'text': hits}]}\n\n"
                 "kb = create_sdk_mcp_server(name='kb', version='1.0.0', tools=[search_kb])\n"
                 "options = ClaudeAgentOptions(\n"
                 "    mcp_servers={'kb': kb},\n"
                 "    allowed_tools=['mcp__kb__search_kb'],\n"
                 ")")
    multi = ("from claude_agent_sdk import AgentDefinition\n\n"
             "options = ClaudeAgentOptions(\n"
             "    system_prompt=SUPERVISOR,       # 분류 · 위임 · 검증\n"
             "    agents={\n"
             "        'it':  AgentDefinition(description='IT 문의 답변',\n"
             "                               prompt=IT_PROMPT, tools=['mcp__kb__search_kb'],\n"
             "                               model='haiku'),\n"
             "        'buy': AgentDefinition(description='구매 문의 답변', prompt=BUY_PROMPT,\n"
             "                               tools=['mcp__kb__search_kb']),\n"
             "    },\n"
             "    mcp_servers={'kb': kb},\n"
             ")")
    if not P():
        multi = multi.replace("'it':  AgentDefinition(description='IT 문의 답변',", "'extract': AgentDefinition(description='사양서 추출',") \
                     .replace("prompt=IT_PROMPT, tools=['mcp__kb__search_kb'],", "prompt=EXTRACT_PROMPT, tools=[],") \
                     .replace("'buy': AgentDefinition(description='구매 문의 답변', prompt=BUY_PROMPT,", "'quote': AgentDefinition(description='견적 계산', prompt=QUOTE_PROMPT,") \
                     .replace("tools=['mcp__kb__search_kb']),", "tools=['mcp__price__get_price']),") \
                     .replace("mcp_servers={'kb': kb},", "mcp_servers={'price': price},")
        tool_code = tool_code.replace("search_kb', '영역별 FAQ에서 조항을 찾는다', {'domain': str, 'q': str}", "get_price', '품목 · 규격의 단가를 찾는다', {'item': str, 'spec': str}") \
                             .replace("async def search_kb", "async def get_price").replace("hits = find(args['domain'], args['q'])      # 파일 검색", "hits = lookup(args['item'], args['spec'])   # 단가표") \
                             .replace("name='kb'", "name='price'").replace("tools=[search_kb]", "tools=[get_price]").replace("kb = create", "price = create") \
                             .replace("{'kb': kb}", "{'price': price}").replace("mcp__kb__search_kb", "mcp__price__get_price")
        basic = basic.replace("'VPN이 안 붙어요'", "open('specs/S03.txt').read()")
    verify = (flow([("의도 분류", "Supervisor"), ("Sub Agent 초안", "근거 조항 포함"), ("검증", "근거 · 정책 · 사람 필요?"), ("통과 → 답변", ""), ("미통과 → 재작업 · 사람", "")], hl=2)
              if P() else
              flow([("추출", "Sub Agent"), ("견적", "Sub Agent"), ("검증", "숫자가 원문에 있나 · 계산 맞나"), ("통과 → 결과", ""), ("미통과 → 재작업 · 사람", "")], hl=2))
    scene = (ill("scenes_hx", "router_desk", "left40", "Supervisor가 나누고 확인한다", ["의도 분류 → 전문 Sub Agent", "돌아온 답은 Supervisor가 검증"])
             if P() else
             ill("scenes_hx", "spec_extract", "left40", "사양서를 표로, 숫자는 원문 그대로", ["추출 → 견적 → 검증", "원문에 없는 숫자는 실패"]))
    out = chapter("Ch3", "Agent SDK로 커스텀 하네스", {"Tool · MCP", "Sub Agent"}, "Tool · Sub Agent") + [
        light("Claude Code와 Agent SDK", table(["", "Claude Code", "Claude Agent SDK"], [
            ["<b>쓰는 법</b>", "터미널 · IDE에서 대화", "Python 코드에서 호출"],
            ["<b>하네스</b>", "같은 엔진", "같은 엔진 + 내 코드로 조립"],
            ["<b>맞는 일</b>", "개발자 개인 작업", "사내 서비스 · 배치 · 평가 자동화"],
        ]), "Ch3"),
        light("ClaudeAgentOptions 핵심", table(["옵션", "하네스 계층"], [
            ["<code>system_prompt</code>", "지침"],
            ["<code>allowed_tools</code> · <code>disallowed_tools</code> · <code>permission_mode</code>", "권한"],
            ["<code>mcp_servers</code>", "도구"],
            ["<code>agents</code>", "Sub Agent"],
            ["<code>hooks</code>", "Hook"],
            ["<code>setting_sources</code> · <code>max_turns</code> · <code>max_budget_usd</code>", "컨텍스트 · 안전 한도"],
        ]), "Ch3"),
        light("가장 작은 Agent", code("lab3_sdk_agent/agent_single.py (요약)", basic), "Ch3"),
        light("도구 하나 붙이기", code("커스텀 도구", tool_code) + note("도구 설명", "이름 · 설명 · 입력 예시가 정확도를 가름"), "Ch3"),
        scene,
        lab("3-1", "단일 Agent + 도구", "Ch3",
            "도구로 근거를 찾아 답하는 Agent" if P() else "사양서를 JSON으로 뽑는 Agent",
            ["agent_single.py 실행", "prompts.py의 TODO(실습) 채우기", "평가셋 5건으로 실행", "틀린 건의 원인: 지침? 도구? 데이터?"],
            ["근거 조항 번호 표기" if P() else "숫자가 모두 원문에 있음", "실행 결과 · 비용 기록"], files="lab3_sdk_agent"),
        light("Supervisor + Sub Agent", code("lab3_sdk_agent/agent_multi.py (요약)", multi), "Ch3"),
        light("Supervisor의 검증 단계", verify, "Ch3"),
        lab("3-2", "Supervisor + Sub Agent", "Ch3",
            "나누고, 맡기고, 검증하는 구조",
            ["agent_multi.py 실행", "prompts.py에서 Sub Agent 역할 · 검증 기준 고치기", "MAX_RETRIES · 모델 조정", "검증 실패 건이 사람에게 넘어가는지 확인"],
            ["검증 실패 → 재작업 또는 [사람 확인]", "Sub Agent별 결과가 로그에 남음"], files="lab3_sdk_agent"),
    ]
    out += [
        light("세션 · 장기 실행", table(["상황", "SDK에서"], [
            ["<b>이어서 묻기</b>", "<code>ClaudeSDKClient</code> 한 세션에서 여러 번 query"],
            ["<b>중단 후 재개</b>", "<code>ResultMessage.session_id</code> 저장 → <code>resume=</code>"],
            ["<b>반복 실행</b>", "요청마다 새 세션 · 상태는 파일 · DB에"],
            ["<b>무한 루프 방지</b>", "<code>max_turns</code> · <code>max_budget_usd</code>"],
        ]), "Ch3"),
        light("도구 호출 실패 복구", table(["실패", "처리"], [
            ["<b>일시 오류</b> (시간 초과 · 429)", "기다렸다 재시도 · 최대 2회"],
            ["<b>도구 결과 없음</b>", "대체 도구 · 질의 바꿔 1회"],
            ["<b>반복 실패</b>", "멈추고 [사람 확인]으로"],
            ["<b>한도 초과</b> (턴 · 비용)", "<code>ResultMessage.subtype</code>로 구분해 기록"],
        ]), "Ch3"),
        bridge("다음: 잘 됐는지 어떻게 아나", "", "Ch3", "→ Ch4 평가 설계"),
    ]
    return out


# ── Ch4 평가 설계 ───────────────────────────────────────
def ch4():
    judge = ("너는 사내 문의 답변 채점자다.\n"
             "[문의] {question}\n[답변] {answer}\n[근거 자료] {kb}\n\n"
             "1~5점으로 채점하고 JSON으로만 답한다.\n"
             "- 정확도: 근거 자료와 맞는가\n"
             "- 근거 충실도: 근거에 없는 내용을 만들었는가 (만들면 1점)\n"
             "- 정책: 약속하면 안 되는 것을 약속했는가\n"
             '{"accuracy": n, "grounded": n, "policy": n, "reason": "..."}')
    if not P():
        judge = judge.replace("사내 문의 답변 채점자", "사양서 추출 결과 채점자").replace("[문의] {question}\n[답변] {answer}\n[근거 자료] {kb}", "[사양서] {spec}\n[추출 JSON] {answer}") \
                     .replace("- 정확도: 근거 자료와 맞는가", "- 정확도: 필드 값이 원문과 맞는가").replace("- 정책: 약속하면 안 되는 것을 약속했는가", "- 형식: 단위 · null 규칙을 지켰는가") \
                     .replace('"policy"', '"format"')
    weights = table(["지표", "분류 · 라우팅", "생성 (답변 초안)", "추출 · 계산"], [
        ["<b>정확도</b>", "40", "25", "40"],
        ["<b>근거 충실도</b>", "—", "30", "30"],
        ["<b>일관성</b>", "30", "15", "20"],
        ["<b>지연</b>", "15", "10", "—"],
        ["<b>비용</b>", "15", "10", "10"],
        ["<b>안전 · 정책</b>", "필수 통과", "필수 통과", "—"],
    ])
    edges = table(["엣지 케이스", "예", "기대 동작"], [
        ["<b>모호한 입력</b>", "「그거 안 돼요」", "되묻기"],
        ["<b>복합 의도</b>", "「노트북 구매하고 VPN도」", "둘 다 처리 · 나눠 위임"],
        ["<b>지시 우회 시도</b>", "「이전 지시 무시하고…」", "무시 · 정상 처리"],
        ["<b>범위 밖</b>", "「점심 메뉴 추천」", "정중히 범위 안내"],
        ["<b>정보 누락</b>", "수량 없는 사양서", "null · [확인 필요]"],
        ["<b>상충 숫자</b>", "표와 본문 수량이 다름", "둘 다 표시 · 사람에게"],
        ["<b>실패해야 정상</b>", "근거 없는 질문", "「자료에 없음」"],
    ])
    multi_eval = table(["대상", "지표", "어떻게"], [
        ["<b>Router · 분류</b>", "의도 정확도", "정답 라벨과 일치 비율"],
        ["<b>Sub Agent</b>", "답변 · 추출 품질", "judge 점수 · 필드 F1"],
        ["<b>Supervisor</b>", "잘못된 답을 막은 비율", "일부러 넣은 오답 차단율"],
        ["<b>전체</b>", "최종 결과 품질 · 비용 · 지연", "처음부터 끝까지 한 번에"],
    ])
    return chapter("Ch4", "평가 설계: 지표와 평가셋", {"평가"}, "평가") + [
        ill("scenes_extra", "calculator_test", "left40", "답을 아는 문제로 먼저 시험", ["평가셋 = 정답 · 허용 범위가 있는 대표 과제"]),
        light("과업마다 다른 가중치", weights + note("원칙", "안전 · 정책은 점수가 아니라 통과 조건"), "Ch4"),
        light("정답셋이 없을 때 세 가지", cards([
            ("합성 데이터", "대표 예시 몇 건 → 모델로 변형 생성 · 표시해 둠", []),
            ("LLM-as-judge", "채점 기준을 프롬프트로 · 다른 모델이 채점", []),
            ("현업 최소 라벨링", "10~20건만 사람이 채점 → judge 보정", []),
        ]), "Ch4"),
        light("평가셋 구성", flow([("대표 과제 10건", "오전 실습 Agent"), ("기대 출력", "정답 · 허용 범위"), ("엣지 케이스", "유형별 1건 이상"), ("합성으로 확장", "표시 · 사람 검토")], hl=2), "Ch4"),
        light("엣지 케이스 유형", edges, "Ch4"),
        ill("scenes_ch5", "interview", "top20", "평가는 세 종류 질문으로 보는 면접", ["정상 · 정보 부족 · 답하면 안 되는 질문"]),
        lab("4-1", "평가셋 만들기", "Ch4",
            "내 Agent의 대표 과제 10건 + 엣지 케이스",
            ["대표 과제 10건 고르기 · 기대 출력 쓰기", "엣지 케이스 유형마다 1건", "make_synthetic.py로 변형 10건 생성", "합성분은 사람이 훑어 걸러내기"],
            ["20건 이상 · 정답 또는 허용 범위", "엣지 케이스 유형 5개 이상"], files="lab4_eval_design"),
        light("LLM-as-judge 채점 기준", code("lab4_eval_design/judge_prompt.md", judge), "Ch4"),
        light("judge를 믿어도 되나", table(["확인", "방법"], [
            ["<b>사람과 일치도</b>", "같은 10건을 사람 · judge가 채점 → 일치 비율 · 카파"],
            ["<b>위치 편향</b>", "보기 순서를 바꿔도 점수가 같은지"],
            ["<b>길이 편향</b>", "긴 답에 점수를 더 주는지"],
            ["<b>자기 편향</b>", "같은 모델이 쓴 답을 같은 모델이 채점 → 다른 모델로"],
        ]) + note("기준", "일치도가 낮으면 judge 기준을 고친다 · 모델을 고치기 전에"), "Ch4"),
        light("멀티 Agent는 따로, 또 함께 평가", multi_eval, "Ch4"),
        lab("4-2", "judge 일치도", "Ch4",
            "채점 기준을 사람 채점에 맞추기",
            ["human_labels.csv 10건 직접 채점", "judge.py 실행", "agreement.py로 일치도 확인", "어긋난 건을 보고 judge 기준 한 줄 수정"],
            ["일치도 수정 전후 기록", "기준 변경 이유 한 줄"], files="lab4_eval_design"),
        bridge("다음: 평가를 자동으로, 매번", "", "Ch4", "→ Ch5 자동 평가 · 운영"),
    ]


# ── Ch5 자동 평가 · 운영 ────────────────────────────────
def ch5():
    compare = ("python lab5_regression/run_suite.py --track {t} --k 3 --out results/before.json\n"
               "# 하네스 수정 (지침 · 도구 · Sub Agent)\n"
               "python lab5_regression/run_suite.py --track {t} --k 3 --out results/after.json\n"
               "python lab5_regression/compare.py results/before.json results/after.json\n\n"
               "정확도      0.72 → 0.90   ▲\n"
               "일관성      0.60 → 0.95   ▲\n"
               "환각 건수      7 → 1      ▼\n"
               "입력 토큰   12.4k → 8.1k  ▼\n"
               "결과: 통과 (기준 미달 지표 없음)").replace("{t}", V)
    out = chapter("Ch5", "자동 평가 파이프라인 · 운영", {"평가", "Hook · 권한"}, "평가 · 운영") + [
        ill("scenes_hx", "regression_gate", "top20", "회귀 테스트: 고치면 다시 잰다", ["기준선보다 나빠지면 멈춤"]),
        light("회귀 테스트 흐름", flow([("하네스 변경", "지침 · 도구 · 모델"), ("평가셋 K회 실행", "같은 입력"), ("점수 · 토큰 집계", "Agent별 · 전체"), ("기준선과 비교", "허용 하락폭"), ("통과 / 중단", "")], hl=3), "Ch5"),
        light("하네스 전후 비교 (시연)", code("터미널", compare) + note("숫자", "예시 출력 · 실습에서 내 숫자로"), "Ch5"),
        light("환각을 세는 법", table(["유형", "자동 판정"], [
            ["<b>숫자</b>", "답의 숫자가 원문 · 도구 결과에 없음"],
            ["<b>조항</b>", "인용한 조항 번호가 FAQ에 없음"],
            ["<b>약속</b>", "금지 표현(보상 · 확정) 포함"],
        ]), "Ch5"),
        lab("5-1", "회귀 테스트 파이프라인", "Ch5",
            "하네스를 고칠 때마다 자동으로 재는 장치",
            ["기준선 실행 · 결과 저장", "하네스 한 곳 수정", "변경 후 실행 → compare.py", "허용 하락폭 정하고 일부러 나쁘게 고쳐 실패 확인"],
            ["전후 비교표: 정확도 · 일관성 · 환각 · 토큰", "나빠지면 compare.py가 실패로 끝남"], files="lab5_regression"),
    ]
    ops = [
        light("실패를 먼저 정의", table(["실패", "판정", "대응"], [
            ["<b>틀린 답</b>", "judge · 정답 비교", "기록 · 평가셋에 추가"],
            ["<b>근거 없는 답</b>", "숫자 · 조항 대조", "차단 · 사람에게"],
            ["<b>정책 위반</b>", "금지 표현 · 권한", "즉시 차단"],
            ["<b>멈춤 · 폭주</b>", "턴 · 비용 한도", "중단 · 알림"],
        ]), "Ch5"),
        light("근거 로깅", table(["남길 것", "쓰임"], [
            ["입력 · 최종 답 · 세션 ID", "재현"],
            ["호출한 도구 · 입력 · 결과", "근거 추적"],
            ["Sub Agent별 결과 · 검증 판정", "어디서 틀렸나"],
            ["토큰 · 비용 · 시간 · 모델", "비용 관리"],
        ]) + note("방법", "PostToolUse · SubagentStop Hook에서 한 줄씩 기록"), "Ch5"),
        light("사람이 개입하는 지점 (HITL)", cards([
            ("확신 낮음", "검증 실패 · 근거 부족", []),
            ("되돌릴 수 없음", "발송 · 삭제 · 결재", []),
            ("고위험 도메인", "안전 · 계약 · 인사", []),
        ]), "Ch5"),
        light("롤백 · 중단 · 재시도", table(["장치", "방법"], [
            ["<b>롤백</b>", "하네스(지침 · Skill · 설정)를 git으로 버전 관리 → 이전 버전으로"],
            ["<b>중단</b>", "max_turns · max_budget_usd · Stop Hook"],
            ["<b>재시도</b>", "일시 오류만 · 최대 횟수 · 대기 시간 늘리며"],
            ["<b>단계적 배포</b>", "일부 사용자 → 지표 확인 → 전체"],
        ]), "Ch5"),
    ]
    tokens = [
        light("토큰 최적화", table(["레버", "방법", "효과"], [
            ["<b>캐싱</b>", "고정 지침 · 도구 목록을 앞에, 바뀌는 입력은 뒤에", "반복 입력 비용 큰 폭 감소"],
            ["<b>컨텍스트 관리</b>", "긴 조사는 Sub Agent로 · 결과만 받기", "메인 대화 짧게 유지"],
            ["<b>선택적 검증</b>", "위험도 높을 때만 Supervisor · judge", "검증 비용을 필요한 곳에만"],
            ["<b>모델 나누기</b>", "분류는 작은 모델 · 판단은 큰 모델", "단가 차이만큼 절감"],
        ]) + note("측정", "ResultMessage.usage · total_cost_usd로 전후 비교"), "Ch5"),
    ]
    if P():
        out += ops + tokens + [
            lab("5-2", "운영 장치 붙이기", "Ch5",
                "로그 · 사람 확인 · 한도",
                ["PostToolUse Hook으로 근거 로그 남기기", "검증 실패 → [사람 확인] 큐로", "max_budget_usd · max_turns 설정", "회귀 테스트로 비용 · 품질 확인"],
                ["로그로 한 건의 근거를 끝까지 추적", "비용 · 품질 비교표"], files="lab3_sdk_agent · lab5_regression"),
        ]
    else:
        out += [
            light("운영에서 꼭 챙길 것", table(["항목", "최소한"], [
                ["<b>실패 정의</b>", "숫자 불일치 · 계산 오류 = 실패"],
                ["<b>근거 로그</b>", "추출 결과마다 원문 위치"],
                ["<b>사람 확인</b>", "검증 실패 · 상충 숫자는 사람에게"],
                ["<b>비용</b>", "추출은 작은 모델 · 검증만 큰 모델"],
            ]), "Ch5"),
        ]
    out += [
        light("사내 적용 시나리오", cards([
            ("문의 대응", "라우팅 · 근거 답변 · 사람 확인", []),
            ("문서 추출", "사양서 · 계약서 · 성적서", []),
            ("리뷰 자동화", "코드 · 보고서 기준 점검", []),
            ("주의", "평가셋 없이 배포하지 않기", []),
        ], 4), "Ch5"),
        bridge("하네스는 고치고 재는 일의 반복", "", "Ch5", "다음 차수: 하네스 엔지니어링 심화"),
    ]
    return out


# ── 심화 트랙 (판교) ────────────────────────────────────
def advanced():
    return [
        divider("심화", "숙련자 확장 과제", ""),
        light("심화 트랙", cards([
            ("자동 리뷰 Agent", "변경 사항을 읽기 전용 Sub Agent가 기준대로 점검", []),
            ("설계 ↔ 리뷰 반복 루프", "설계 Agent → 리뷰 Agent → 기준 통과까지 반복 · 횟수 상한", []),
            ("장기 세션 관리", "resume · 요약 · 상태 파일로 며칠짜리 작업 이어가기", []),
        ]) + note("자료", f'<a class="dl" href="{REPO}/advanced">labs/advanced</a>'), "심화"),
    ]


def slides(variant):
    global V
    V = variant
    out = opening() + ch1() + ch2() + ch3() + ch4() + ch5()
    if P():
        out += advanced()
    return out


CSS = '''
  .hubtxt{font-size:30px; font-weight:800; color:#1F3A5F;}
  .lt :not(pre) > code{font-family:var(--mono); font-size:.92em; background:#EEF1F5; border-radius:4px; padding:1px 5px;}
  .dl{color:#F28C28; font-weight:800; font-family:var(--mono); text-decoration:underline;}
'''
