"""하네스 엔지니어링 — 한 판본 (판교 · 포항 공통, 심화 난도).

python3 src/build.py → docs/index.html
Ch1 개념 · Ch2 Claude Code 분해 · Ch3 컨텍스트 엔지니어링 · Ch4 공개 하네스 · Ch5 멀티에이전트
Ch6 토큰 경제학 · Ch7 평가 · 회귀 테스트 · Ch8 내 하네스 플러그인 · 심화
"""
import importlib

import deck
import explain
import intro
from deck import ba, bridge, cards, divider, flow, ill, lab, light
from stats_hx import big, hbars, passk, quote, rings, stat

# 출처 (2026-10-14 확인)
A_SWE = ("Anthropic · SWE-bench Verified 2025.1", "https://www.anthropic.com/research/swe-bench-sonnet")
A_BEA = ("Anthropic · Building effective agents 2024.12", "https://www.anthropic.com/engineering/building-effective-agents")
A_LRH = ("Anthropic · Effective harnesses for long-running agents 2025.11", "https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents")
EPOCH = ("Epoch AI · Why benchmarking is hard 2025.12", "https://epoch.ai/gradient-updates/why-benchmarking-is-hard")
METR1 = ("METR 2025.3", "https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/")
METR2 = ("METR Time Horizon 1.1 2026.1", "https://metr.org/blog/2026-1-29-time-horizon-1-1/")
A_CTX = ("Anthropic · Effective context engineering 2025.9", "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents")
CHROMA = ("Chroma · Context Rot 2025.7", "https://www.trychroma.com/research/context-rot")
LITM = ("Liu et al. · Lost in the Middle (TACL)", "https://arxiv.org/abs/2307.03172")
A_CM = ("Anthropic · Managing context 2025.9", "https://claude.com/blog/context-management")
D_MODELS = ("Claude 모델 문서", "https://platform.claude.com/docs/en/about-claude/models/overview")
D_MODELCFG = ("Claude Code 모델 설정 문서", "https://code.claude.com/docs/en/model-config")
D_BP = ("Claude Code Best practices", "https://code.claude.com/docs/en/best-practices")
D_COSTS = ("Claude Code 비용 문서", "https://code.claude.com/docs/en/costs")
D_SKILLS = ("Agent Skills 문서", "https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview")
D_SUB = ("Claude Code Sub Agent 문서", "https://code.claude.com/docs/en/sub-agents")
D_TEAMS = ("Claude Code Agent Teams 문서", "https://code.claude.com/docs/en/agent-teams")
D_MCP = ("Claude Code MCP 문서", "https://code.claude.com/docs/en/mcp")
A_MAR = ("Anthropic · Multi-agent research system 2025.6", "https://www.anthropic.com/engineering/multi-agent-research-system")
A_CEMCP = ("Anthropic · Code execution with MCP 2025.11", "https://www.anthropic.com/engineering/code-execution-with-mcp")
A_ATU = ("Anthropic · Advanced tool use 2025.11", "https://www.anthropic.com/engineering/advanced-tool-use")
A_TOOLS = ("Anthropic · Writing tools for agents 2025.9", "https://www.anthropic.com/engineering/writing-tools-for-agents")
A_AAIF = ("Anthropic · MCP 기부 · AAIF 2025.12", "https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation")
SO26 = ("Stack Overflow 개발자 설문 2026", "https://survey.stackoverflow.co/2026/ai")
SO25 = ("Stack Overflow 개발자 설문 2025", "https://survey.stackoverflow.co/2025/ai")
DORA = ("Google DORA 2025", "https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report")
DORA2 = ("DORA 2025 보고서", "https://dora.dev/research/2025/dora-report/")
METR_RCT = ("METR 2025.7 무작위 대조 실험", "https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/")
A_ECON = ("Anthropic Economic Index 2025.4", "https://www.anthropic.com/research/impact-software-development")
D_PRICE = ("Claude 가격 문서", "https://platform.claude.com/docs/en/about-claude/pricing")
D_CACHE = ("프롬프트 캐싱 문서", "https://platform.claude.com/docs/en/build-with-claude/prompt-caching")
A_OPUS45 = ("Anthropic · Claude Opus 4.5 2025.11", "https://www.anthropic.com/news/claude-opus-4-5")
A_EVALS = ("Anthropic · Demystifying evals for AI agents 2026.1", "https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents")
TAU = ("Yao et al. · τ-bench 2024", "https://arxiv.org/abs/2406.12045")
MTB = ("Zheng et al. · LLM-as-a-Judge (MT-Bench) 2023", "https://arxiv.org/abs/2306.05685")
D_SUCCESS = ("Anthropic · 성공 기준 정하기 문서", "https://platform.claude.com/docs/en/test-and-evaluate/define-success")
OPUS5 = ("Claude Opus 5 System Card 2026.7", "https://www.anthropic.com/transparency")
A_SANDBOX = ("Anthropic · Claude Code sandboxing 2025.10", "https://www.anthropic.com/engineering/claude-code-sandboxing")
A_AUTO = ("Anthropic · Claude Code auto mode 2026.3", "https://www.anthropic.com/engineering/claude-code-auto-mode")
A_CONTAIN = ("Anthropic · How we contain Claude 2026.5", "https://www.anthropic.com/engineering/how-we-contain-claude")
A_PI = ("Anthropic · 브라우저 프롬프트 주입 방어 2025.11", "https://www.anthropic.com/research/prompt-injection-defenses")
D_HOOKS = ("Claude Code Hooks 문서", "https://code.claude.com/docs/en/hooks")
MCP1Y = ("MCP 블로그 · One Year of MCP 2025.11", "https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/")
OWN = ("직접 실측 2026.10 · labs/demo_quote", "https://github.com/TunaLee/posco-dx/tree/main/labs/demo_quote")

code = explain.prompt
REPO = "https://github.com/TunaLee/posco-dx/tree/main/labs"


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


def viz(name):
    """애니메이션 도해 (src/viz_hx.py). 없으면 회색 자리."""
    try:
        return getattr(importlib.import_module("viz_hx"), name)()
    except (ImportError, AttributeError):
        return f'<div class="capbox">도해 준비 중 · {name}</div>'


def u_curve():
    """Lost in the Middle — 위치별 정확도 개념도 (U자)."""
    pts = [(0, 92), (1, 70), (2, 52), (3, 47), (4, 52), (5, 64), (6, 80)]
    X = lambda i: 120 + i * 150
    Y = lambda v: 330 - (v - 30) * 4
    d = "M" + " L".join(f"{X(i)} {Y(v)}" for i, v in pts)
    y56 = Y(56)
    return f'''<svg class="ucurve" viewBox="0 0 1160 400">
  <line x1="100" y1="{y56}" x2="1060" y2="{y56}" stroke="#9AA5B1" stroke-width="2" stroke-dasharray="8 8"/>
  <text x="1064" y="{y56 + 5}" font-size="17" fill="#6B7785">문서 없이 답할 때 56.1%</text>
  <path d="{d}" fill="none" stroke="#F28C28" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" class="udraw"/>
  <text x="{X(0)}" y="{Y(92) - 18}" text-anchor="middle" font-size="18" font-weight="800" fill="#1F3A5F">맨 앞</text>
  <text x="{X(3)}" y="{Y(47) + 40}" text-anchor="middle" font-size="18" font-weight="800" fill="#E07A12">가운데 · 20%↓ 이상</text>
  <text x="{X(6)}" y="{Y(80) - 18}" text-anchor="middle" font-size="18" font-weight="800" fill="#1F3A5F">맨 뒤</text>
  <text x="580" y="392" text-anchor="middle" font-size="16" fill="#8A94A3">필요한 정보의 위치 → (개념도 · GPT-3.5-Turbo 다문서 QA)</text>
</svg>''' + note("하네스로", "중요한 지침은 앞에 · 긴 자료는 찾아서 필요한 부분만")


def labdir(d):
    return f'<a class="dl" href="{REPO}/{d}">{d}</a>'


# ── 하네스 지도 ──────────────────────────────────────────
PARTS = [
    ("지침 · 컨텍스트", "CLAUDE.md · 무엇을 올릴지", "Ch1 · Ch3", (250, 255)),
    ("Skill · 명령", "필요할 때 꺼내 쓰는 절차", "Ch2", (640, 215)),
    ("Tool · MCP", "조회 · 계산 · 외부 연결", "Ch2", (1030, 255)),
    ("Sub Agent · 팀", "역할 분리 · 오케스트레이션", "Ch5", (1030, 590)),
    ("Hook · 권한", "막기 · 기록 · 승인", "Ch2", (640, 650)),
    ("평가 · 비용", "평가셋 · 회귀 · 토큰", "Ch6 · Ch7", (250, 590)),
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


# ── 시작 ────────────────────────────────────────────────
AGENDA = [
    ("Ch1", "하네스 개념", "하네스 전후 비교표"),
    ("Ch2", "Claude Code 하네스 분해", "Skill · Sub Agent · Hook · 명령"),
    ("Ch3", "컨텍스트 엔지니어링", "컨텍스트 실험표"),
    ("Ch4", "공개 하네스 적용", "Superpowers · gstack 비교"),
    ("Ch5", "멀티에이전트 오케스트레이션", "Supervisor + Sub Agent · 실행 타임라인"),
    ("Ch6", "토큰 경제학", "토큰 절감 실측표"),
    ("Ch7", "평가 · 회귀 테스트", "평가셋 · 자동 비교"),
    ("Ch8", "내 하네스 플러그인", "최종 산출물 · GitHub"),
]


def cover():
    return '''<section class="slide dk cover-dk active" data-title="표지">
  <div class="glow"></div>
  <div class="kick">AX 심화 · 하네스</div>
  <h1>하네스 엔지니어링<br/>· 평가와 검증</h1>
</section>'''


def agenda():
    rows = "".join(f'''<div class="ch"><span class="chip">{c}</span><div class="tx"><b>{t}</b><span>{d}</span></div></div>'''
                   for c, t, d in AGENDA)
    return f'''<section class="slide dk" data-title="목차">
  {intro.coord()}
  <h2>목차</h2>
  <div class="days two"><div class="daycol">{rows}</div></div>
</section>'''


def opening():
    return [
        cover(),
        intro.speaker(),
        agenda(),
        stat("개발자는 이미 매일 쓴다", "시작",
             big([("73", "%", "코딩 도구 · 에이전트를 매일 사용", True),
                  ("90", "%", "업무에 AI 사용 (DORA)"),
                  ("66", "%", "코딩 에이전트 사용 1위: Claude Code")])
             + note("맡기는 방식", "Claude Code 대화의 79%가 「자동화」 (Claude.ai는 49%)"),
             SO26, DORA, A_ECON),
        stat("그런데 믿지는 못한다", "시작",
             rings([(66, "「거의 맞지만 틀린」 답이<br>가장 큰 불만"), (46, "정확도를<br>믿지 않음", False), (3, "높게 신뢰", False)])
             + note("2026 설문", "쉽게 검증할 수 있을 때만 믿는다 48% · DORA: AI 코드 거의 · 전혀 못 믿음 30%"),
             SO25, SO26, DORA),
        stat("체감과 실제는 다르다", "시작",
             hbars([("시작 전 예상", 24, False, "24% 빠름"), ("끝난 뒤 체감", 20, False, "20% 빠름"),
                    ("실제 측정", 19, True, "19% 느림")], top=30, title="숙련 오픈소스 개발자 16명 · 실제 이슈 246건 · 무작위 대조")
             + quote("AI는 증폭기다. 조직의 강점도 약점도 키운다", "DORA 2025"),
             METR_RCT, DORA2),
        light("최종 산출물", table(["산출물", "내용"], [
            ["<b>내 하네스 플러그인</b>", "CLAUDE.md · Skill · Sub Agent · Hook · 명령을 한 묶음으로"],
            ["<b>평가셋 · 회귀 테스트</b>", "대표 과제 20건 + 엣지 케이스 · 자동 비교"],
            ["<b>전후 비교표</b>", "맨몸 vs 내 하네스 vs 공개 하네스 · 일관성 · 정확도 · 토큰"],
            ["<b>GitHub 저장소</b>", "팀원이 설치해 쓸 수 있는 형태"],
        ]), "시작"),
        light("실습 환경", table(["도구", "용도"], [
            ["<b>Claude Code (비즈니스 계정)</b>", "하네스 만들기 · 대화형 실습"],
            ["<b>헤드리스</b> <code>claude -p</code>", "같은 작업 N번 자동 실행 · 토큰 측정"],
            ["<b>VS Code · Python 3.10+</b>", "실습 스크립트 · 데이터"],
            ["<b>Git · GitHub</b>", "하네스 버전 관리 · 공유"],
        ]) + note("실습 저장소", labdir("")), "시작"),
        light("헤드리스: 대화창 없이 한 줄로", code("터미널", 'claude -p "VPN이 안 붙어요" --output-format json\n\n'
                                                  '{ "result": "...", "num_turns": 2, "duration_ms": 8120,\n'
                                                  '  "usage": { "input_tokens": 3812, "output_tokens": 241,\n'
                                                  '             "cache_read_input_tokens": 3402 },\n'
                                                  '  "session_id": "...", "total_cost_usd": ... }')
              + note("쓰임", "같은 질문 50번 · 평가셋 자동 실행 · 토큰 비교 (비즈니스 요금제는 비용보다 토큰으로 비교)"), "시작"),
        light("공통 예제 두 가지 · 하나 선택", two(
            cards([("문의 대응 라우팅", "사내 문의 → 의도 분류 → 전문 Sub Agent → 검증 · 문의 30건 · FAQ 5개", [])], 2),
            cards([("사양서 추출 · 견적", "사양서 → JSON 추출 → 견적 → 검증 · 사양서 10건 · 정답 JSON · 단가표", [])], 2))
              + note("데이터", "모두 가상 자료 · 엣지 케이스 포함"), "시작"),
        hx_map(),
    ]


# ── Ch1 하네스 개념 ─────────────────────────────────────
def ch1():
    return chapter("Ch1", "하네스 엔지니어링 개념", {"지침 · 컨텍스트"}, "모델과 계층 설계") + [
        ill("scenes_more", "harness_rig", "left40", "하네스: 모델에 채우는 장비",
            ["모델: 답을 만드는 엔진", "하네스: 모델을 감싼 나머지 전부"]),
        stat("같은 모델, 하네스만 바꿔도", "Ch1",
             big([("15", "%", "스캐폴드만 바꿔 생긴 점수 차 (같은 모델)", True),
                  ("11", "%", "GPT-5에서 같은 실험"),
                  ("1위", "", "성능을 가장 크게 좌우한 요인: 스캐폴드")])
             + quote("전체 성능에 가장 큰 영향을 주는 것은 스캐폴드 선택이다", "Epoch AI, 2025"),
             EPOCH),
        stat("프롬프트 + 도구 두 개로 SWE-bench 49%", "Ch1",
             hbars([("Claude 3 Opus", 22), ("Claude 3.5 Sonnet (구)", 33), ("Claude 3.5 Sonnet (신)", 49, True)], "%", 60,
                   "같은 하네스 (프롬프트 · Bash · Edit) · SWE-bench Verified")
             + quote("프롬프트보다 도구를 다듬는 데 더 많은 시간을 썼다", "Anthropic, Building effective agents")
             + note("당시 최고", "45% → 단순한 하네스로 49%"), A_SWE, A_BEA),
        stat("에이전트가 맡는 일은 계속 길어진다", "Ch1",
             big([("7", "개월", "작업 길이가 2배 되는 주기 (2019~)"),
                  ("89", "일", "2024년 이후 2배 주기", True),
                  ("5.3", "시간", "Opus 4.5가 50% 성공하는 작업 길이 (사람 기준)")])
             + note("긴 작업의 흔한 실패", "너무 일찍 「다 했다」 선언 → 기능 목록 · 진행 기록 · 검증을 하네스로"),
             METR1, METR2, A_LRH),
        light("하네스의 다섯 계층", table(["계층", "담는 것", "설계 결정"], [
            ["<b>모델</b>", "추론 엔진", "어떤 모델 · effort · 한도"],
            ["<b>컨텍스트</b>", "지침 · 참고 자료 · 대화 이력", "항상 넣을 것 vs 필요할 때만"],
            ["<b>도구</b>", "조회 · 계산 · 실행", "이름 · 설명 · 입력 형식 · 개수"],
            ["<b>권한</b>", "허용 · 금지 · 승인", "자동 허용 범위 · 사람 승인 지점"],
            ["<b>평가</b>", "지표 · 평가셋 · 로그", "무엇을 성공으로 볼지"],
        ]), "Ch1"),
        light("프롬프트 → 컨텍스트 → 하네스 → 루프", '''<div class="tline t4">
  <div class="tl"><b>프롬프트</b><span>한 번의 질문을 잘 쓰기</span></div>
  <div class="tl"><b>컨텍스트</b><span>무엇을 보여 줄지 고르기</span></div>
  <div class="tl"><b>하네스</b><span>도구 · 권한 · 평가까지 환경 전체</span></div>
  <div class="tl hl"><b>루프</b><span>하네스를 재고 고치는 반복</span></div>
</div>''' + note("실무 기준", "한 번 쓰고 끝 → 프롬프트 · 매번 같은 자료 → 컨텍스트 · 반복 · 위험 · 여러 사람 → 하네스"), "Ch1"),
        light("같은 모델, 다른 하네스", table(["차이", "하네스 A", "하네스 B"], [
            ["<b>도구 설계</b>", "「검색」 하나 · 설명 한 줄", "「FAQ 조회」 「규정 조회」 분리 · 입력 예시"],
            ["<b>컨텍스트</b>", "대화 이력 전부 누적", "핵심만 남기고 Sub Agent로 분리"],
            ["<b>권한</b>", "모든 도구 자동 허용", "읽기만 자동 · 쓰기는 승인"],
            ["<b>결과</b>", "답이 흔들리고 토큰 증가", "답 고정 · 토큰 감소"],
        ]), "Ch1"),
        ill("scenes_hx", "wobbly_vs_steady", "top20", "하네스 없는 Agent vs 있는 Agent",
            ["없음: 같은 질문에 매번 다른 답", "있음: 같은 형식 · 같은 근거"]),
        light("부품마다 막는 문제", table(["부품", "막는 문제", "없으면"], [
            ["<b>지침</b>", "답 형식 · 기준이 흔들림", "같은 질문에 매번 다른 형식"],
            ["<b>Skill</b>", "절차 누락", "체크리스트 단계 건너뜀"],
            ["<b>Tool</b>", "지어낸 숫자", "조회 대신 기억으로 답"],
            ["<b>Sub Agent</b>", "컨텍스트 오염", "긴 작업 중 앞 지시를 잊음"],
            ["<b>Hook · 권한</b>", "위험한 실행", "삭제 · 강제 push · 비밀 파일 수정"],
            ["<b>평가</b>", "조용한 품질 저하", "프롬프트 수정 후 다른 곳이 깨짐"],
        ]), "Ch1"),
        light("신입사원 온보딩과 같은 구조", table(["신입사원이 받는 것", "Agent의 하네스"], [
            ["회사 소개 · 업무 규칙", "CLAUDE.md"], ["업무 매뉴얼", "Skill"], ["사내 시스템 계정", "Tool · MCP"],
            ["옆 팀 협업", "Sub Agent"], ["결재 · 보안 규정", "Hook · 권한"], ["수습 평가", "평가셋 · 회귀 테스트"],
        ]), "Ch1"),
        light("일관성은 숫자로 잰다", table(["지표", "재는 법"], [
            ["<b>답 일치율</b>", "같은 질문 N번 → 가장 많은 답의 비율"],
            ["<b>형식 준수율</b>", "정해진 JSON · 표 형식을 지킨 비율"],
            ["<b>근거 일치</b>", "답의 숫자 · 조항이 원문에 있는 비율"],
            ["<b>토큰</b>", "실행 1회당 입력 · 캐시 · 출력"],
        ]), "Ch1"),
        ba("하네스 한 장의 차이", "Ch1",
           "이 사양서에서 품목과 수량 알려 줘\n\n→ 1회: 표 · 2회: 문장 · 3회: 수량 단위 누락",
           "CLAUDE.md\n역할: 사양서 추출 담당\n출력: JSON {품목, 규격, 재질, 수량, 단위, 비고}\n규칙: 원문에 없는 숫자는 쓰지 않음, 없으면 null\n\n→ 10회 모두 같은 JSON"),
        lab("1-1", "같은 질문 열 번", "Ch1",
            "맨몸 vs CLAUDE.md 한 장의 차이를 숫자로",
            ["맨몸으로 헤드리스 10회 실행", "harness/CLAUDE.md에 역할 · 출력 형식 · 규칙 쓰기", "같은 입력 10회 다시 실행", "답 종류 수 · JSON 유효율 · 토큰 비교표"],
            ["답 종류 1~2종", "비교표를 최종 산출물 폴더에 저장"], files=labdir("lab1_harness_vs_bare")),
        bridge("다음: Claude Code 하네스 뜯어보기", "", "Ch1", "→ Ch2"),
    ]


# ── Ch2 Claude Code 분해 ────────────────────────────────
def ch2():
    skill = ("---\n"
             "name: incident-report   # 이름은 자유\n"
             "description: 장애 · 문의 처리 결과를 팀 양식 보고서로 쓸 때\n"
             "---\n"
             "## 순서\n"
             "1. 현상 · 원인 · 조치 · 재발 방지를 표로\n"
             "2. 숫자는 첨부 자료에서만, 없으면 [확인 필요]\n"
             "3. 마지막 줄: 후속 할 일 3개\n"
             "## 참고\n"
             "- template.md")
    agent = ("---\n"
             "name: reviewer\n"
             "description: 변경 사항 리뷰. 수정은 하지 않음\n"
             "tools: Read, Grep, Glob        # 읽기 전용\n"
             "model: sonnet\n"
             "---\n"
             "변경된 파일만 읽고, 문제를 심각도 순으로 보고한다.\n"
             "보고 형식: 파일:줄 · 문제 · 근거 · 제안")
    cmd = ("---\n"
           "description: 문의 하나를 분류 → 응대 → 검증 순서로 처리\n"
           "argument-hint: [문의 내용]\n"
           "---\n"
           "다음 문의를 처리한다: $ARGUMENTS\n"
           "1. 의도 분류 (classifier 에게 위임)\n"
           "2. 해당 영역 응대 Agent 에게 위임\n"
           "3. verifier 통과 전에는 답하지 않는다")
    hook_cfg = ('"PreToolUse": [{ "matcher": "Bash|Write|Edit",\n'
                '  "hooks": [{ "type": "command", "command": "python3 .claude/hooks/guard.py" }] }]')
    guard = ("import json, sys\n"
             "e = json.load(sys.stdin)            # 도구 이름 · 입력\n"
             "i = e.get('tool_input', {})\n"
             "bad = ['rm -rf', 'push --force', 'reset --hard']\n"
             "if any(b in i.get('command', '') for b in bad) \\\n"
             "   or i.get('file_path', '').endswith('.env'):\n"
             "    print('차단: 위험 명령 · 비밀 파일', file=sys.stderr)\n"
             "    sys.exit(2)                     # 2 = 막고 이유를 Claude에게")
    return chapter("Ch2", "Claude Code 하네스 분해", {"Skill · 명령", "Hook · 권한", "Tool · MCP"}, "Skill · 명령 · Hook · 도구") + [
        light("언제 로드되고 언제 실행되나", table(["요소", "언제 로드 · 실행", "성격"], [
            ["<b>CLAUDE.md</b>", "세션 시작 때 항상", "부탁 (따르려고 읽는 컨텍스트)"],
            ["<b>Skill</b>", "설명만 상시 · 본문은 호출될 때", "절차 (필요할 때만)"],
            ["<b>명령</b> (/이름)", "사람이 부를 때", "정해진 순서 실행"],
            ["<b>Sub Agent</b>", "위임할 때 새 컨텍스트로", "분업 (결과만 돌려받음)"],
            ["<b>Hook</b>", "도구 호출 전후 등 이벤트마다", "강제 (코드가 결정)"],
            ["<b>권한</b>", "도구를 쓰기 직전", "허용 · 거부 · 승인 요청"],
            ["<b>MCP</b>", "도구 목록 상시 · 실행은 호출 때", "외부 시스템 연결"],
        ]), "Ch2"),
        light("부탁 · 절차 · 강제", cards([
            ("CLAUDE.md = 부탁", "모델이 읽고 따르려 함 · 어길 수 있음", []),
            ("Skill · 명령 = 절차", "필요할 때만 불러 컨텍스트 절약", []),
            ("Hook · 권한 = 강제", "코드가 막음 · 모델이 우회 못 함", []),
        ]), "Ch2"),
        light("Skill 한 개의 구조", two(code(".claude/skills/incident-report/SKILL.md", skill),
                                        vl("description: 언제 부를지", "본문: 호출될 때만 로드", "참고 파일: 양식 · 예시"))
              + note("이름", "예시일 뿐 · 팀 규칙에 맞게 자유롭게"), "Ch2"),
        light("명령: 사람이 부르는 정해진 순서", code(".claude/commands/handle.md", cmd) + note("호출", "/handle VPN이 안 붙어요"), "Ch2"),
        light("Sub Agent 경계 설계", table(["경계", "정하는 것", "예: reviewer"], [
            ["<b>도구 집합</b>", "쓸 수 있는 도구", "Read · Grep · Glob"],
            ["<b>권한</b>", "쓰기 · 실행 허용 여부", "쓰기 금지"],
            ["<b>컨텍스트</b>", "보여 줄 자료 범위", "변경 파일만"],
            ["<b>반환 형식</b>", "부모가 받을 결과", "파일:줄 · 문제 · 근거"],
        ]), "Ch2"),
        light("Sub Agent 정의 파일", two(code(".claude/agents/reviewer.md", agent),
                                          vl("자기 컨텍스트에서 일함", "부모는 결과만 받음", "도구를 줄이면 권한도 줄어듦")), "Ch2"),
        light("Hook: 막는 건 코드가", code(".claude/settings.json (hooks 부분)", hook_cfg) + code(".claude/hooks/guard.py", guard), "Ch2"),
        stat("부품마다 드는 비용", "Ch2",
             big([("~100", "토큰", "Skill 하나가 항상 차지하는 설명"),
                  ("5천", "토큰 미만", "Skill 본문 (부를 때만)"),
                  ("200", "줄 이하", "CLAUDE.md 권장 길이", True),
                  ("2.5만", "토큰", "MCP 도구 출력 기본 한도 (1만부터 경고)")], 4)
             + note("설계 감각", "항상 올라가는 것은 짧게 · 필요할 때 부르는 것은 길어도 된다"),
             D_SKILLS, D_COSTS, D_MCP),
        stat("CLAUDE.md는 권고, Hook은 강제", "Ch2",
             quote("CLAUDE.md 지침은 권고일 뿐이다. Hook은 결정적이고, 그 동작이 반드시 일어나게 보장한다", "Claude Code Best practices")
             + big([("33", "개", "Hook을 걸 수 있는 이벤트"), ("exit 2", "", "PreToolUse에서 도구 호출 차단", True),
                    ("수만 → 수백", "토큰", "Hook으로 로그에서 ERROR 줄만 넘길 때")]),
             D_BP, D_HOOKS, D_COSTS),
        stat("사람 승인만으로는 부족하다", "Ch2",
             big([("93", "%", "승인 요청을 그대로 승인 (승인 피로)", True),
                  ("84", "%", "샌드박스로 줄어든 승인 요청"),
                  ("17", "%", "자동 모드가 놓친 과잉 행동 · 오차단은 0.4%")])
             + note("설계", "막을 것은 Hook · 권한 · 샌드박스로 강제 · 사람은 정말 중요한 곳만 승인"),
             A_AUTO, A_SANDBOX),
        stat("프롬프트 주입: 0이 되지 않는다", "Ch2",
             hbars([("1회 시도", 0.1, False, "0.1%"), ("100회 반복 시도", 5.5, True, "5~6%")], top=8,
                   title="최신 모델 대상 프롬프트 주입 성공률 (Opus 4.7, Anthropic 측정)")
             + quote("공격 성공률 1%도 여전히 의미 있는 위험이다", "Anthropic, 브라우저 사용 방어 연구")
             + note("하네스로", "외부 문서 · 웹 · 메일은 읽기 전용 Agent에 · 쓰기 · 전송은 Hook으로 막기"),
             A_CONTAIN, A_PI),
        stat("도구 연결의 표준이 된 MCP", "Ch2",
             big([("1만+", "개", "운영 중인 공개 MCP 서버", True),
                  ("9,700만+", "", "Python · TypeScript SDK 월간 다운로드"),
                  ("407", "%", "레지스트리 등록 증가 (출시 후 2개월)")])
             + note("2025.12", "Anthropic이 MCP를 리눅스 재단 산하 Agentic AI Foundation에 기부"),
             A_AAIF, MCP1Y),
        lab("2-1", "하네스 부품 네 개", "Ch2",
            "Skill · 명령 · Sub Agent · Hook을 내 예제에 붙이기",
            ["project/.claude 구조 살펴보기", "내 업무 Skill 하나 · 명령 하나 쓰기", "reviewer를 읽기 전용으로 정의", "guard 차단 목록에 규칙 하나 추가 → 헤드리스로 확인"],
            ["새 세션에서 Skill 자동 호출", ".env 수정 요청이 차단됨", "reviewer가 파일을 못 고침"], files=labdir("lab2_claude_code_parts")),
        bridge("다음: 무엇을 보여 줄 것인가", "", "Ch2", "→ Ch3 컨텍스트 엔지니어링"),
    ]


# ── Ch3 컨텍스트 엔지니어링 ─────────────────────────────
def ch3():
    return chapter("Ch3", "컨텍스트 엔지니어링", {"지침 · 컨텍스트", "Sub Agent · 팀"}, "컨텍스트") + [
        light("컨텍스트 창 = 책상", viz("context_window") + note("원칙", "책상에 올린 만큼 매번 다시 읽는다 · 올린 것이 많을수록 흐려진다"), "Ch3"),
        stat("길어질수록 흐려진다", "Ch3",
             big([("18", "개", "실험한 모델 · 전부 입력이 길수록 성능 하락", True),
                  ("1", "문장", "방해 문장 하나로도 정확도 하락"),
                  ("n²", "", "토큰 n개 → 주의를 나눌 관계 n² 개")])
             + quote("컨텍스트 창의 토큰이 늘수록, 그 안의 정보를 정확히 떠올리는 능력은 떨어진다", "Anthropic, Effective context engineering"),
             CHROMA, A_CTX),
        stat("가운데에 둔 정보는 잘 못 찾는다", "Ch3", u_curve(), LITM),
        light("책상에 오르는 것들", table(["항목", "언제", "크기를 좌우하는 것"], [
            ["<b>시스템 · 도구 목록</b>", "항상", "MCP · 도구 개수"],
            ["<b>CLAUDE.md</b>", "항상", "길이 · 중복"],
            ["<b>Skill 설명</b>", "항상 (본문은 호출 때)", "Skill 개수"],
            ["<b>대화 이력</b>", "쌓임", "세션 길이"],
            ["<b>도구 결과</b>", "쌓임 · 가장 큼", "파일 통째 읽기 · 긴 로그"],
        ]) + note("확인", "/context 로 지금 책상 상태 보기"), "Ch3"),
        light("네 가지 전략", cards([
            ("쓰기", "필요한 걸 밖에 적어 둠 · 메모 · 상태 파일", []),
            ("고르기", "필요한 것만 · 검색 · 부분 읽기", []),
            ("줄이기", "/compact · 요약 · 오래된 도구 결과 정리", []),
            ("나누기", "Sub Agent에 따로 맡기고 결과만", []),
        ], 4), "Ch3"),
        light("CLAUDE.md는 짧게, 매뉴얼은 Skill로", two(
            code("나쁜 예 · CLAUDE.md 600줄", "# 회사 규정 전문 (복사)\n# 업무 매뉴얼 전문 (복사)\n# 예전 회의록 …\n\n→ 매 요청마다 600줄을 다시 읽음"),
            code("좋은 예 · CLAUDE.md 30줄", "# 역할 · 출력 형식 · 금지 규칙\n# 자세한 절차는 Skill:\n#   incident-report, quote-rules\n\n→ 필요할 때만 Skill 본문 로드")), "Ch3"),
        light("통째로 읽지 말고 찾아서 읽기", ba_like("「data 폴더 다 읽고 답해 줘」\n→ 문의 30건 + FAQ 전부가 책상에", "「FAQ에서 VPN 조항만 찾아 읽어」\n→ 조항 한 개만 책상에"), "Ch3"),
        light("Sub Agent로 책상 나누기", viz("subagent_fanout"), "Ch3"),
        stat("정리하면 좋아지고 싸진다", "Ch3",
             hbars([("메모리 + 컨텍스트 편집", 39, True, "+39%"), ("컨텍스트 편집만", 29, False, "+29%")], top=50,
                   title="에이전트 검색 과제 성능 향상 (Anthropic 내부 평가)")
             + hbars([("100턴 작업 토큰 절감", 84, True, "−84%")], top=100)
             + note("Sub Agent", "수만 토큰을 탐색하고 1~2천 토큰으로 요약해 돌려준다"),
             A_CM, A_CTX),
        stat("Claude Code의 책상 크기", "Ch3",
             big([("100만", "토큰", "현재 모델 컨텍스트 창"),
                  ("96.7만", "토큰", "자동 압축이 시작되는 지점", True),
                  ("5", "개", "압축 후 남기는 최근 파일 (+ 요약)")])
             + quote("컨텍스트 창은 빨리 차고, 찰수록 성능이 떨어진다", "Claude Code Best practices"),
             D_MODELS, D_MODELCFG, A_CTX, D_BP),
        light("긴 세션의 함정", table(["증상", "원인", "처방"], [
            ["<b>앞 지시를 잊음</b>", "이력이 길어 중요한 줄이 묻힘", "새 작업 = 새 세션"],
            ["<b>엉뚱한 파일 수정</b>", "예전 작업의 흔적이 남음", "/clear 또는 세션 분리"],
            ["<b>점점 느리고 비쌈</b>", "매 턴 전체 이력 재전송", "/compact · 요약 후 이어가기"],
        ]), "Ch3"),
        lab("3-1", "컨텍스트 실험 네 가지", "Ch3",
            "같은 작업, 책상 상태만 바꿔 토큰 비교",
            ["CLAUDE.md 600줄 vs 30줄 + Skill", "폴더 통째 읽기 vs 검색해서 읽기", "직접 조사 vs Sub Agent 위임", "긴 세션 vs 새 세션 · 결과표 채우기"],
            ["변형 4종 입력 · 캐시 · 출력 토큰 표", "품질이 떨어진 변형 표시"], files=labdir("lab3_context")),
        bridge("다음: 남이 만든 하네스 입어 보기", "", "Ch3", "→ Ch4 공개 하네스"),
    ]


def ba_like(before, after):
    return f'''<div class="ba">
  <div class="b"><div class="lab">통째로</div><div class="q">{before.replace(chr(10), "<br/>")}</div></div>
  <div class="arr">→</div>
  <div class="a"><div class="lab">찾아서</div><div class="q">{after.replace(chr(10), "<br/>")}</div></div>
</div>'''


# ── Ch4 공개 하네스 ─────────────────────────────────────
def ch4():
    sp = ("/plugin marketplace add obra/superpowers-marketplace\n"
          "/plugin install superpowers@superpowers-marketplace\n\n"
          "/superpowers:brainstorm      # 설계 질문\n"
          "/superpowers:write-plan      # 구현 계획\n"
          "/superpowers:execute-plan    # Sub Agent 실행 · TDD · 리뷰")
    gs = ("git clone --single-branch --depth 1 \\\n"
          "  https://github.com/garrytan/gstack.git ~/.claude/skills/gstack \\\n"
          "  && cd ~/.claude/skills/gstack && ./setup\n\n"
          "/office-hours · /plan-eng-review   # 기획 · 설계 검토\n"
          "/review · /qa · /cso               # 리뷰 · QA · 보안")
    return chapter("Ch4", "공개 하네스 적용", {"Skill · 명령", "Sub Agent · 팀", "Hook · 권한"}, "남이 만든 하네스") + [
        light("하네스를 패키지로: 플러그인", cards([
            ("맨몸 모델", "매번 모델 재량 · 결과가 운에 흔들림", []),
            ("하네스 입은 모델", "규칙 · 역할 · 절차 · 강제로 품질 고정", []),
            ("플러그인", "Skill · 명령 · Agent · Hook 묶음을 한 줄 설치", []),
        ]), "Ch4"),
        light("많이 쓰는 공개 하네스", table(["하네스", "성격", "멀티에이전트"], [
            ["<b>Superpowers</b>", "방법론 강제 (설계 → 계획 → TDD → 리뷰)", "계획 후 Sub Agent 위임"],
            ["<b>gstack</b>", "역할 페르소나 (CEO · EM · QA · 보안)", "역할 분업"],
            ["<b>Everything Claude Code</b>", "Agent · Skill · Hook · 명령 한 벌", "역할별 Agent 다수"],
            ["<b>wshobson/agents</b>", "여러 도구 공용 플러그인 마켓", "전문 Agent 묶음"],
            ["<b>claude-flow</b>", "코드로 짜는 다수 Agent 오케스트레이션", "본격 멀티에이전트"],
            ["<b>공식 플러그인 마켓</b>", "Anthropic 공식 Skill · 플러그인", "용도별"],
        ]) + note("고르는 기준", "내 업무 흐름과 맞는가 · 강제 vs 선택 · 토큰 비용"), "Ch4"),
        light("Superpowers: 단계를 건너뛰지 못하게", code("Claude Code", sp), "Ch4"),
        light("gstack: 가상 개발 팀", code("터미널 · Claude Code", gs), "Ch4"),
        light("두 하네스의 성격", table(["", "Superpowers", "gstack"], [
            ["<b>방식</b>", "적은 명령 · 강제 흐름", "많은 명령 · 골라 쓰기"],
            ["<b>강점</b>", "계획 · TDD · 리뷰 누락 없음", "역할별 검토 · QA · 보안"],
            ["<b>약점</b>", "작은 일에도 단계가 많음", "흐름은 사람이 챙김"],
            ["<b>함께</b>", "gstack 기획 → Superpowers 실행 → gstack 리뷰 · QA", ""],
        ]), "Ch4"),
        light("받아 쓰기 전에 볼 것", table(["항목", "확인"], [
            ["<b>Hook · 명령</b>", "어떤 명령을 실행하는가 · 외부 전송은 없는가"],
            ["<b>권한</b>", "자동 허용 범위가 넓지 않은가"],
            ["<b>토큰</b>", "상시 로드되는 Skill · 지침 양"],
            ["<b>사내 규정</b>", "외부 저장소 설치 허용 여부"],
        ]) + note("원칙", "공개 하네스도 내 평가셋으로 잰 뒤에 쓴다"), "Ch4"),
        stat("실측: 같은 과제, 세 조건 (Sonnet)", "Ch4",
             hbars([("맨몸 ×3", 15, False, "15 · 15 · 15"), ("내 하네스 ×3", 15, False, "15 · 15 · 15"), ("Superpowers ×1", 0.2, True, "0 (질문하고 멈춤)")], top=15,
                   title="숨은 인수 테스트 통과 (15개 중) · 견적 할인 · 할증 과제")
             + hbars([("맨몸", 165, False, "165초 · 52만"), ("내 하네스", 289, True, "289초 · 72만"), ("Superpowers", 90, False, "90초 · 29만")], top=300,
                     title="평균 시간 (막대) · 전체 토큰 (캐시 포함)")
             + note("배운 점", "정보가 저장소에 다 있으면 Sonnet은 맨몸으로도 맞춤 · 하네스는 절차를 고정하지만 비용이 듦 · 대화형 하네스는 자동 실행에서 멈춤"),
             OWN),
        lab("4-1", "같은 과제, 네 가지 하네스", "Ch4",
            "맨몸 · 내 하네스 · Superpowers · gstack 비교",
            ["sample_app 과제 카드 읽기 (버그 2개)", "맨몸으로 해결 → 기록", "Superpowers · gstack 각각 설치 후 해결", "토큰 · 시간 · 테스트 통과 · 건너뛴 단계 비교"],
            ["compare.md 4열 완성", "내 하네스에 가져올 점 3개"], files=labdir("lab4_public_harness")),
        bridge("다음: 여러 Agent를 지휘하기", "", "Ch4", "→ Ch5 멀티에이전트"),
    ]


# ── Ch5 멀티에이전트 ───────────────────────────────────
def ch5():
    return chapter("Ch5", "멀티에이전트 오케스트레이션", {"Sub Agent · 팀"}, "오케스트레이션") + [
        light("단일 Agent의 한계", table(["한계", "증상"], [
            ["<b>컨텍스트 과부하</b>", "조사 · 구현 · 검증이 한 책상에 쌓임"],
            ["<b>자기 검증</b>", "자기가 쓴 답을 자기가 채점 → 관대함"],
            ["<b>순차 처리</b>", "독립 작업도 하나씩"],
        ]), "Ch5"),
        stat("멀티에이전트는 얼마나 나은가", "Ch5",
             big([("90.2", "%", "단일 Agent(Opus 4) 대비 성능 향상", True),
                  ("90", "%", "병렬 위임으로 줄인 조사 시간 (최대)"),
                  ("80", "%", "성능 차이를 토큰 사용량 하나로 설명")])
             + note("구성", "Opus 4 지휘 + Sonnet 4 Sub Agent 3~5개 병렬 · Anthropic 내부 리서치 평가"),
             A_MAR),
        stat("그만큼 토큰을 쓴다", "Ch5",
             hbars([("채팅", 1, False, "1×"), ("Agent", 4, False, "4×"), ("멀티에이전트", 15, True, "15×")], top=16,
                   title="채팅 대비 토큰 사용량")
             + note("Agent Teams", "일반 세션의 약 7배 (팀원이 plan 모드일 때) · 값어치 있는 일에만"),
             A_MAR, D_COSTS),
        stat("규모는 일의 크기에 맞춘다", "Ch5", table(["상황", "권장 · 한계"], [
            ["<b>단순 사실 찾기</b>", "Agent 1개 · 도구 호출 3~10번"],
            ["<b>복잡한 조사</b>", "Sub Agent 10개 이상 · 역할 분담"],
            ["<b>초기 실패 사례</b>", "단순 질문에 Sub Agent 50개 생성"],
            ["<b>Agent Teams</b>", "팀원 3~5명 · 1인당 작업 5~6개"],
            ["<b>Claude Code 한도</b>", "Sub Agent 동시 20개 · 3단계까지 중첩"],
        ]), A_MAR, D_TEAMS, D_SUB),
        light("오케스트레이션 패턴", viz("orchestration_patterns"), "Ch5"),
        light("Sub Agent: 위임하고 결과만 받기", viz("subagent_fanout"), "Ch5"),
        light("Agent Teams: 서로 말하는 팀", viz("agent_teams") + note("상태", "실험 기능 · 환경 변수로 켬 · 위임으로 충분하면 Sub Agent"), "Ch5"),
        light("Sub Agent vs Agent Teams", table(["", "Sub Agent", "Agent Teams"], [
            ["<b>소통</b>", "부모 ↔ 자식 한 방향", "구성원끼리 직접 · 공유 작업 목록"],
            ["<b>맞는 일</b>", "독립 조사 · 검증 · 분업", "서로 결과를 반박 · 보완해야 할 때"],
            ["<b>비용</b>", "자식마다 컨텍스트", "구성원마다 세션 · 더 큼"],
            ["<b>통제</b>", "부모가 순서 강제", "작업 목록 · 규칙으로 조율"],
        ]), "Ch5"),
        ill("scenes_hx", "router_desk", "left40", "예제 A: 문의 라우팅", ["분류 → 영역별 응대 → 검증", "검증 실패 → 재작업 · 사람"]),
        ill("scenes_hx", "spec_extract", "left40", "예제 B: 사양서 추출 · 견적", ["추출 → 견적 → 검증", "원문에 없는 숫자는 실패"]),
        light("검증은 다른 Agent가", two(
            flow([("분류", "classifier"), ("응대", "domain"), ("검증", "verifier"), ("통과 → 답", "")], hl=2),
            flow([("추출", "extractor"), ("견적", "estimator"), ("검증", "verifier"), ("통과 → 결과", "")], hl=2))
              + note("verifier", "읽기 전용 · 근거 · 숫자 · 정책만 판정 · 고치지 않음"), "Ch5"),
        light("실행을 눈으로 보기", viz("timeline_lanes") + note("만드는 법", "헤드리스 stream-json 이벤트 → visualize.py → 타임라인 HTML"), "Ch5"),
        light("실시간 대시보드: Agent Watch", '<img class="shot" src="img/agent_watch.png" alt="Agent Watch 화면">'
              + note("구성", "Hook → 로컬 서버 → 브라우저 · 메인 · Sub Agent 레인 · 에이전트별 토큰 · 효율 점검 · " + labdir("agent_watch")), "Ch5"),
        light("위임문 4요소", table(["요소", "빠지면"], [
            ["<b>목표 · 완료 기준</b>", "어디서 멈출지 모름"],
            ["<b>입력 범위</b>", "필요 없는 것까지 읽음"],
            ["<b>허용 도구</b>", "권한 밖 작업"],
            ["<b>반환 형식</b>", "부모가 결과를 못 합침"],
        ]), "Ch5"),
        lab("5-1", "Supervisor + Sub Agent + 검증", "Ch5",
            "예제 하나를 멀티에이전트로 · 실행을 시각화",
            ["예제 고르기 (라우팅 · 추출)", ".claude/agents 역할 · 도구 · 반환 형식 손보기", "run.py로 실행 (stream-json 저장)", "visualize.py → 타임라인에서 병목 · 실패 찾기"],
            ["verifier가 오답 1건 이상 차단", "타임라인 HTML · 레인별 토큰"], files=labdir("lab5_multiagent")),
        bridge("다음: 이 모든 것의 값", "", "Ch5", "→ Ch6 토큰 경제학"),
    ]


# ── Ch6 토큰 경제학 ─────────────────────────────────────
def ch6():
    return chapter("Ch6", "토큰 경제학", {"평가 · 비용", "지침 · 컨텍스트"}, "토큰") + [
        light("몇 토큰일까?", cards([
            ("「VPN 안 돼요」 한 번", "입력 · 출력 각각 몇 토큰?", []),
            ("CLAUDE.md 600줄", "매 요청마다 몇 토큰이 더 붙나?", []),
            ("파일 하나 통째 읽기", "출력의 몇 배?", []),
        ]) + note("퀴즈", "먼저 맞혀 보고 실습에서 실측"), "Ch6"),
        stat("출력은 입력의 5배 가격", "Ch6",
             hbars([("Haiku 5.5", 0.5, False, "$0.10 → $0.50"), ("Sonnet 5.5", 10, False, "$2 → $10"),
                    ("Opus 5.5", 20, False, "$4 → $20"), ("Fable 5.1", 50, True, "$10 → $50")], top=55,
                   title="100만 토큰당 가격 · 입력 → 출력 (막대 = 출력)")
             + note("Claude Code 실제 비용", "개발자 1인 하루 평균 약 $13 · 월 $150~250 · 90%는 하루 $30 미만"),
             D_PRICE, D_COSTS),
        stat("캐시와 배치: 할인 규칙", "Ch6",
             big([("1.25", "배", "캐시 쓰기 (5분 · 1시간은 2배)"),
                  ("0.1", "배", "캐시 읽기 (Opus · Sonnet 5.5는 0.05배)", True),
                  ("1", "번", "한 번만 다시 읽어도 캐시가 이득"),
                  ("50", "%", "배치 API 할인 (입력 · 출력 모두)")], 4)
             + note("기억할 것", "캐시 기본 수명 5분 · 쓸 때마다 갱신 · 앞부분이 1글자라도 바뀌면 새로 씀"),
             D_CACHE, D_PRICE),
        stat("공식 사례로 본 절감 폭", "Ch6",
             hbars([("MCP를 코드로 호출", 98.7, True, "−98.7%"), ("도구 검색 (Tool Search)", 85, False, "−85%"),
                    ("컨텍스트 편집 (100턴)", 84, False, "−84%"), ("effort 낮추기 (같은 점수)", 76, False, "출력 −76%"),
                    ("도구 호출을 코드로 묶기", 37, False, "−37%")], top=100, title="토큰 절감률")
             + note("도구 정의만으로", "도구 58개 = 대화 시작 전 약 5.5만 토큰 · Anthropic 내부는 13.4만 토큰까지"),
             A_CEMCP, A_ATU, A_CM, A_OPUS45),
        light("토큰은 어디서 새나", viz("token_levers"), "Ch6"),
        light("캐싱: 앞부분이 같으면 싸다", viz("cache_prefix") + note("규칙", "고정 지침 · 도구 목록은 앞에, 바뀌는 입력은 뒤에 · 시간 · ID를 앞에 넣지 않기"), "Ch6"),
        stat("도구 결과가 책상을 채운다", "Ch6",
             big([("2.5만", "토큰", "Claude Code 도구 응답 기본 한도"),
                  ("⅓", "", "「간결」 응답 형식이 쓰는 토큰", True),
                  ("40", "%", "도구 설명만 고쳐 줄인 작업 시간")])
             + note("세션 정리", "/compact도 큰 요청 한 번 · 새로 시작이면 /clear는 비용 0"),
             A_TOOLS, A_MAR, D_COSTS),
        light("레버 다섯 개", table(["레버", "방법", "주의"], [
            ["<b>① 입력 줄이기</b>", "짧은 CLAUDE.md · 찾아서 읽기 · Sub Agent 분리", "가장 큰 절감"],
            ["<b>② 출력 줄이기</b>", "「간결하게 · JSON으로」 · caveman", "설명이 필요한 곳은 예외"],
            ["<b>③ 코드량 줄이기</b>", "ponytail 같은 최소 구현 Skill", "필요한 기능 누락 확인"],
            ["<b>④ 도구 출력 줄이기</b>", "rtk 같은 명령 출력 압축", "필요한 오류 줄까지 지우지 않게"],
            ["<b>⑤ 모델 나누기</b>", "분류는 작은 모델 · 판단은 큰 모델", "품질은 평가셋으로 확인"],
        ]), "Ch6"),
        light("출력 줄이기: caveman", two(
            code("설치", "/plugin marketplace add JuliusBrussee/caveman\n/plugin install caveman@caveman"),
            ba_like2("좋은 질문이에요! 이 문제는 여러 가지 원인이 있을 수 있는데요, 우선 VPN 클라이언트가…", "원인: 인증서 만료. 조치: 재발급 (IT-3).")), "Ch6"),
        light("코드량 줄이기: ponytail", code("설치", "/plugin marketplace add DietrichGebert/ponytail\n/plugin install ponytail@ponytail")
              + note("효과", "요청한 것만 · 가장 단순한 해법부터 · 적은 코드 = 적은 버그"), "Ch6"),
        light("하네스 전후 토큰", viz("token_meter"), "Ch6"),
        light("토큰을 써야 할 때", table(["상황", "이유"], [
            ["<b>검증 · 리뷰</b>", "틀린 답의 비용이 토큰보다 큼"],
            ["<b>E2E 테스트</b>", "실제 흐름 확인 · 핵심 흐름에만"],
            ["<b>고위험 도메인</b>", "안전 · 계약 · 인사는 큰 모델 + 사람"],
        ]) + note("원칙", "토큰이 아니라 「완료된 작업 1건당 비용」으로 판단"), "Ch6"),
        lab("6-1", "토큰 절감 실측", "Ch6",
            "레버를 하나씩 켜며 토큰 · 품질 비교",
            ["quiz.md로 먼저 예상", "기준선 5개 과제 실행 (bench.py)", "레버 켜기: 간결 지시 · caveman · 모델 나누기 · Sub Agent", "토큰 · 정확도 함께 비교 → 남길 레버 고르기"],
            ["레버별 토큰 · 정확도 표", "품질이 떨어진 레버는 제외"], files=labdir("lab6_tokens")),
        bridge("다음: 좋아졌는지 어떻게 아나", "", "Ch6", "→ Ch7 평가 · 회귀 테스트"),
    ]


def ba_like2(before, after):
    return f'''<div class="ba">
  <div class="b"><div class="lab">기본</div><div class="q">{before}</div></div>
  <div class="arr">→</div>
  <div class="a"><div class="lab">caveman</div><div class="q">{after}</div></div>
</div>'''


# ── Ch7 평가 · 회귀 테스트 ──────────────────────────────
def ch7():
    judge = ("너는 채점자다. 1~5점, JSON으로만 답한다.\n"
             "[입력] {input}\n[출력] {output}\n[근거] {source}\n\n"
             "- 정확도: 근거와 맞는가\n"
             "- 근거 충실도: 근거에 없는 내용을 만들었는가 (만들면 1점)\n"
             "- 정책: 약속하면 안 되는 것 · 형식 위반\n"
             '{"accuracy": n, "grounded": n, "policy": n, "reason": "..."}')
    compare = ("python run_suite.py --engine headless --k 3 --out results/before.json\n"
               "# 하네스 수정\n"
               "python run_suite.py --engine headless --k 3 --out results/after.json\n"
               "python compare.py results/before.json results/after.json\n\n"
               "정확도      0.72 → 0.90   ▲\n"
               "일관성      0.60 → 0.95   ▲\n"
               "환각 건수      7 → 1      ▼\n"
               "입력 토큰   12.4k → 8.1k  ▼\n"
               "결과: 통과")
    return chapter("Ch7", "평가 · 회귀 테스트", {"평가 · 비용"}, "평가") + [
        stat("한 번 성공 ≠ 매번 성공", "Ch7", passk(0.75, 10)
             + note("τ-bench", "GPT-4o 소매 상담: 8번 연속 성공률 25% 미만"), A_EVALS, TAU),
        stat("평가셋은 작게, 실패에서 시작", "Ch7",
             big([("20~50", "개", "실제 실패에서 뽑은 첫 평가 과제", True),
                  ("~20", "개", "Anthropic 멀티에이전트 첫 평가셋"),
                  ("F1 ≥ 0.85", "", "성공 기준은 숫자로 (공식 예)")])
             + quote("손으로 채점한 적은 문항보다, 자동 채점한 많은 문항이 낫다", "Anthropic 문서, 성공 기준 정하기"),
             A_EVALS, A_MAR, D_SUCCESS),
        stat("채점기도 검증한다", "Ch7",
             big([("80+", "%", "LLM 심판과 사람의 일치율 = 사람끼리 일치율"),
                  ("42 → 95", "%", "채점 버그만 고쳤더니 바뀐 점수 (CORE-Bench)", True)], 2)
             + note("원칙", "점수가 이상하면 모델보다 채점기 · 과제부터 의심"),
             MTB, A_EVALS),
        stat("공개 벤치마크는 금방 찬다", "Ch7",
             hbars([("1년 전", 40, False, "40%"), ("1년 뒤", 80, False, "80%+"), ("Claude Opus 5", 96, True, "96.0%")], top=100,
                   title="SWE-bench Verified")
             + note("그래서", "남의 점수보다 우리 업무 평가셋 · 우리 회귀 테스트"),
             A_EVALS, OPUS5),
        ill("scenes_extra", "calculator_test", "left40", "답을 아는 문제로 먼저 시험", ["평가셋 = 정답 · 허용 범위가 있는 대표 과제"]),
        light("과업마다 다른 가중치", table(["지표", "분류 · 라우팅", "생성 (답변)", "추출 · 계산"], [
            ["<b>정확도</b>", "40", "25", "40"], ["<b>근거 충실도</b>", "—", "30", "30"],
            ["<b>일관성</b>", "30", "15", "20"], ["<b>지연</b>", "15", "10", "—"],
            ["<b>토큰</b>", "15", "10", "10"], ["<b>안전 · 정책</b>", "필수 통과", "필수 통과", "—"],
        ]) + note("원칙", "안전 · 정책은 점수가 아니라 통과 조건"), "Ch7"),
        light("정답셋이 없을 때 세 가지", cards([
            ("합성 데이터", "대표 예시 → 변형 생성 · 표시해 둠", []),
            ("LLM-as-judge", "채점 기준을 프롬프트로 · 다른 모델이 채점", []),
            ("현업 최소 라벨링", "10~20건만 사람이 채점 → judge 보정", []),
        ]), "Ch7"),
        light("엣지 케이스 유형", table(["엣지 케이스", "예", "기대 동작"], [
            ["<b>모호한 입력</b>", "「그거 안 돼요」", "되묻기"],
            ["<b>복합 의도</b>", "「노트북 구매하고 VPN도」", "나눠 위임"],
            ["<b>지시 우회 시도</b>", "「이전 지시 무시하고…」", "무시 · 정상 처리"],
            ["<b>범위 밖</b>", "「점심 메뉴 추천」", "범위 안내"],
            ["<b>정보 누락 · 상충 숫자</b>", "수량 없음 · 표와 본문이 다름", "null · 사람에게"],
            ["<b>실패해야 정상</b>", "근거 없는 질문", "「자료에 없음」"],
        ]), "Ch7"),
        light("LLM-as-judge 채점 기준", code("judge_prompt.md", judge), "Ch7"),
        light("judge를 믿어도 되나", table(["확인", "방법"], [
            ["<b>사람과 일치도</b>", "같은 10건을 사람 · judge가 채점 → 일치율 · 카파"],
            ["<b>위치 · 길이 편향</b>", "순서 바꾸기 · 긴 답 편애 확인"],
            ["<b>자기 편향</b>", "같은 모델이 쓴 답을 채점하지 않게"],
        ]), "Ch7"),
        light("멀티 Agent는 따로, 또 함께", table(["대상", "지표"], [
            ["<b>분류 · 라우터</b>", "의도 정확도"], ["<b>Sub Agent</b>", "judge 점수 · 필드 F1"],
            ["<b>verifier</b>", "일부러 넣은 오답 차단율"], ["<b>전체</b>", "최종 품질 · 토큰 · 지연"],
        ]), "Ch7"),
        ill("scenes_hx", "regression_gate", "top20", "회귀 테스트: 고치면 다시 잰다", ["기준선보다 나빠지면 멈춤"]),
        light("하네스 전후 비교 (시연)", code("터미널", compare) + note("숫자", "예시 출력 · 실습에서 내 숫자로"), "Ch7"),
        lab("7-1", "평가셋 + 회귀 테스트", "Ch7",
            "하네스를 고칠 때마다 자동으로 재는 장치",
            ["대표 10건 + 엣지 케이스 + 합성 10건", "judge 기준 → 사람 10건과 일치도", "기준선 실행 → 하네스 수정 → 재실행", "일부러 나쁘게 고쳐 compare.py 실패 확인"],
            ["평가셋 20건 이상", "전후 비교표 · 나빠지면 실패로 끝남"], files=labdir("lab7_eval_regression")),
        bridge("다음: 내 하네스를 내보내기", "", "Ch7", "→ Ch8 최종 산출물"),
    ]


# ── Ch8 내 하네스 플러그인 + 운영 ──────────────────────
def ch8():
    tree = ("my-harness/\n"
            "├── .claude-plugin/plugin.json\n"
            "├── CLAUDE.md                # 짧게 · 역할 · 형식 · 금지\n"
            "├── skills/<업무>/SKILL.md\n"
            "├── commands/<흐름>.md       # 오케스트레이터\n"
            "├── agents/{classifier, …, verifier}.md\n"
            "├── hooks/{hooks.json, guard.py}\n"
            "└── eval/{dataset.jsonl, judge_prompt.md, results/}")
    load = ("claude plugin validate ./my-harness     # 구조 검사\n"
            "claude --plugin-dir ./my-harness        # 불러서 실행\n"
            "# 팀 공유: GitHub + marketplace.json → /plugin install")
    return chapter("Ch8", "내 하네스 플러그인", {p[0] for p in PARTS}, "전체") + [
        light("최종 산출물 구조", two(code("my-harness", tree), vl("오늘 만든 부품을 한 폴더로", "평가셋과 결과를 함께", "GitHub에 올려 팀이 설치")), "Ch8"),
        light("불러오기 · 공유", code("터미널", load), "Ch8"),
        light("운영: 실패를 먼저 정의", table(["실패", "판정", "대응"], [
            ["<b>틀린 답</b>", "judge · 정답 비교", "평가셋에 추가"],
            ["<b>근거 없는 답</b>", "숫자 · 조항 대조", "차단 · 사람에게"],
            ["<b>정책 위반</b>", "금지 표현 · 권한", "Hook으로 즉시 차단"],
            ["<b>멈춤 · 폭주</b>", "턴 · 토큰 한도", "중단 · 알림"],
        ]), "Ch8"),
        light("운영 장치", table(["장치", "방법"], [
            ["<b>근거 로깅</b>", "PostToolUse · SubagentStop Hook으로 한 줄씩"],
            ["<b>사람 확인 (HITL)</b>", "확신 낮음 · 되돌릴 수 없음 · 고위험 도메인"],
            ["<b>롤백</b>", "하네스를 git으로 버전 관리 → 이전 태그로"],
            ["<b>재시도</b>", "일시 오류만 · 최대 횟수 · 대기 늘리며"],
            ["<b>단계적 배포</b>", "일부 사용자 → 지표 확인 → 전체"],
        ]), "Ch8"),
        lab("8-1", "내 하네스 플러그인 완성", "Ch8",
            "팀원이 설치해 쓰고, 숫자로 증명되는 하네스",
            ["my-harness 템플릿에 오늘 만든 부품 옮기기", "claude plugin validate 통과", "평가셋으로 맨몸 · 내 하네스 · 공개 하네스 비교", "GitHub에 올리고 README에 비교표"],
            ["옆 사람이 설치해 같은 결과", "전후 비교표 · 토큰 실측표 포함"], files=labdir("lab8_final_plugin")),
        light("발표 2분", flow([("문제", "무엇이 흔들렸나"), ("하네스", "무엇을 붙였나"), ("숫자", "전후 비교"), ("다음", "운영 계획")], hl=2), "Ch8"),
        bridge("하네스는 고치고 재는 일의 반복", "", "Ch8", "다음 차수: 하네스 엔지니어링 심화"),
    ]


# ── 심화 ───────────────────────────────────────────────
def advanced():
    sdk = ("from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition\n\n"
           "options = ClaudeAgentOptions(\n"
           "    system_prompt=SUPERVISOR,\n"
           "    agents={'verifier': AgentDefinition(description='검증', prompt=V,\n"
           "                                        tools=['Read'])},\n"
           "    hooks={'PreToolUse': [HookMatcher(matcher='Bash', hooks=[guard])]},\n"
           "    max_turns=8,\n"
           ")")
    return [
        divider("심화", "숙련자 확장 과제", ""),
        light("같은 하네스를 코드로: Agent SDK", code("Python · API 키 필요", sdk) + note("자료", labdir("sdk_optional")), "심화"),
        light("심화 트랙", cards([
            ("자동 리뷰 Agent", "변경 사항을 읽기 전용 Agent가 기준대로 점검", []),
            ("설계 ↔ 리뷰 루프", "통과할 때까지 반복 · 횟수 상한", []),
            ("장기 세션 관리", "resume · 요약 · 상태 파일로 며칠짜리 작업", []),
        ]) + note("자료", labdir("sdk_optional")), "심화"),
    ]


def slides():
    return opening() + ch1() + ch2() + ch3() + ch4() + ch5() + ch6() + ch7() + ch8() + advanced()


CSS = '''
  .hubtxt{font-size:30px; font-weight:800; color:#1F3A5F;}
  .lt :not(pre) > code{font-family:var(--mono); font-size:.92em; background:#EEF1F5; border-radius:4px; padding:1px 5px;}
  .shot{display:block; width:100%; max-height:400px; object-fit:cover; object-position:top; border-radius:12px; border:1px solid #E1E5EB; box-shadow:0 8px 24px rgba(31,58,95,.12); margin-bottom:14px;}
  .ucurve{width:100%; height:auto; margin-bottom:8px;}
  .ucurve .udraw{stroke-dasharray:1400; animation:udraw 1.6s ease-out both;}
  @keyframes udraw{from{stroke-dashoffset:1400}}
  @media print{.ucurve .udraw{animation:none}}
  .dl{color:#F28C28; font-weight:800; font-family:var(--mono); text-decoration:underline;}
  .days.two{grid-template-columns:1fr; max-width:900px;}
  .days.two .daycol{display:grid; grid-template-columns:1fr 1fr; gap:10px;}
'''
