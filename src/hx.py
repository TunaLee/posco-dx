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
EPOCH = ("Epoch AI · Why benchmarking is hard 2025.12", "https://epoch.ai/gradient-updates/why-benchmarking-is-hard")
D_MODELS = ("Claude 모델 문서", "https://platform.claude.com/docs/en/about-claude/models/overview")
D_MODELCFG = ("Claude Code 모델 설정 문서", "https://code.claude.com/docs/en/model-config")
D_BP = ("Claude Code Best practices", "https://code.claude.com/docs/en/best-practices")
D_COSTS = ("Claude Code 비용 문서", "https://code.claude.com/docs/en/costs")
D_SUB = ("Claude Code Sub Agent 문서", "https://code.claude.com/docs/en/sub-agents")
D_TEAMS = ("Claude Code Agent Teams 문서", "https://code.claude.com/docs/en/agent-teams")
D_MCP = ("Claude Code MCP 문서", "https://code.claude.com/docs/en/mcp")
SO26 = ("Stack Overflow 개발자 설문 2026", "https://survey.stackoverflow.co/2026/ai")
DORA = ("Google DORA 2025", "https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report")
D_PRICE = ("Claude 가격 문서", "https://platform.claude.com/docs/en/about-claude/pricing")
D_CACHE = ("프롬프트 캐싱 문서", "https://platform.claude.com/docs/en/build-with-claude/prompt-caching")
A_EVALS = ("Anthropic · Demystifying evals for AI agents 2026.1", "https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents")
D_SUCCESS = ("Anthropic · 성공 기준 정하기 문서", "https://platform.claude.com/docs/en/test-and-evaluate/define-success")
A_AUTO = ("Anthropic · Claude Code auto mode 2026.3", "https://www.anthropic.com/engineering/claude-code-auto-mode")
D_HOOKS = ("Claude Code Hooks 문서", "https://code.claude.com/docs/en/hooks")
SO26_DATA = ("Stack Overflow 2026 · 응답 데이터", "https://survey.stackoverflow.co/2026/ai/data")
METR26 = ("METR 2026.2 실험 설계 변경", "https://metr.org/blog/2026-02-24-uplift-update/")
METR26S = ("METR 2026.5 사용 설문", "https://metr.org/blog/2026-05-11-ai-usage-survey/")
A_ECON26 = ("Anthropic Economic Index 2026.6", "https://www.anthropic.com/research/economic-index-june-2026-report")
OAI_CODEX = ("OpenAI · Codex for knowledge work 2026.6", "https://openai.com/index/codex-for-knowledge-work")
SC_OPUS55 = ("Claude Opus 5.5 System Card 2026.9", "https://www.anthropic.com/claude-opus-5-5-system-card")
SC_SONNET55 = ("Claude Sonnet 5.5 System Card 2026.9", "https://www.anthropic.com/claude-sonnet-5-5-system-card")
SC_HAIKU55 = ("Claude Haiku 5.5 System Card 2026.10", "https://www.anthropic.com/claude-haiku-5-5-system-card")
SC_FABLE51 = ("Claude Fable 5.1 System Card 2026.9", "https://www.anthropic.com/claude-fable-5-1-mythos-5-1-system-card")
SC_GPT6 = ("OpenAI · GPT-6 Astra System Card 2026.9", "https://deploymentsafety.openai.com/gpt-6-astra")
OAI_SWEV = ("OpenAI · SWE-bench Verified 중단 2026.2", "https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/")
OAI_SWEP = ("OpenAI · Separating signal from noise 2026.7", "https://openai.com/index/separating-signal-from-noise-coding-evaluations")
GEM38 = ("Google DeepMind · Gemini 3.8 Flash 모델 카드 2026.9", "https://deepmind.google/models/model-cards/")
TB21 = ("Terminal-Bench 2.1 발표 2026.5", "https://www.tbench.ai/news/terminal-bench-2-1")
TBLB = ("Terminal-Bench 4.0 리더보드 2026.10", "https://www.tbench.ai/leaderboard")
HARBOR = ("Terminal-Bench · Harbor-Index 2026.6", "https://www.tbench.ai/news/harbor-index")
A_NOISE = ("Anthropic · Infrastructure noise 2026.2", "https://www.anthropic.com/engineering/infrastructure-noise")
A_SON55 = ("Anthropic · Claude Sonnet 5.5 발표 2026.9", "https://www.anthropic.com/news/claude-sonnet-5-5")
A_FABLE5 = ("Anthropic · Claude Fable 5 발표 2026.6", "https://www.anthropic.com/news/claude-fable-5-mythos-5")
SC_FABLE5 = ("Claude Fable 5 · Mythos 5 System Card 2026.6", "https://anthropic.com/claude-fable-5-mythos-5-system-card")
METR_FRR = ("METR Frontier Risk Report 2026.5", "https://metr.org/blog/2026-05-19-frontier-risk-report/")
METR_TH = ("METR Time Horizons 2026.9", "https://metr.org/time-horizons/")
GEM4 = ("Google DeepMind · Gemini 4 Argon 모델 카드 2026.10", "https://deepmind.google/models/model-cards/gemini-4-argon/")
GEM35F = ("Google DeepMind · Gemini 3.5 Flash 모델 카드 2026.5", "https://deepmind.google/models/model-cards/gemini-3-5-flash/")
OAI_GPT55 = ("OpenAI · Introducing GPT-5.5 2026.4", "https://openai.com/index/introducing-gpt-5-5/")
OAI_GPT6 = ("OpenAI · GPT-6 Astra 2026.9", "https://openai.com/index/gpt-6-astra/")
OAI_GPT6DOC = ("OpenAI · GPT-6 Astra 모델 문서", "https://developers.openai.com/api/docs/models/gpt-6-astra")
D_OPT = ("Anthropic 문서 · Optimizing for cost and intelligence (2026.9 측정)", "https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence")
D_EFFORT = ("Anthropic 문서 · Effort", "https://platform.claude.com/docs/en/build-with-claude/effort")
MCP26 = ("MCP 블로그 · 2026-07-28 Specification", "https://blog.modelcontextprotocol.io/posts/2026-07-28/")
MCPRM = ("MCP 블로그 · New MCP Roadmap 2026.8", "https://blog.modelcontextprotocol.io/posts/mcp-roadmap/")
SKILLSIO = ("agentskills.io (2026.10 기준)", "https://agentskills.io/home")
D_TOOLSEARCH = ("Anthropic 문서 · Tool search", "https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool")
D_PTC = ("Anthropic 문서 · Programmatic tool calling", "https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling")
D_CCSKILLS = ("Claude Code Skills 문서", "https://code.claude.com/docs/en/skills")
OAI_MA = ("OpenAI 문서 · Responses multi-agent", "https://developers.openai.com/api/docs/guides/responses-multi-agent")
OAI_SUB = ("OpenAI Codex 문서 · Subagents", "https://learn.chatgpt.com/docs/agent-configuration/subagents")
INC_POCKET = ("Decrypt · PocketOS 2026.4", "https://decrypt.co/365897/ai-agent-deletes-startup-database-9-seconds-founder-says")
INC_OPENCLAW = ("SF Standard · OpenClaw 2026.2", "https://sfstandard.com/2026/02/25/openclaw-goes-rogue/")
INC_CC_PUSH = ("Claude Code GitHub 이슈 #33402 2026.3", "https://github.com/anthropics/claude-code/issues/33402")
INC_CODEX = ("Simon Willison · Codex 파일 삭제 2026.7", "https://simonwillison.net/2026/Jul/16/bad-codex-bug/")
INC_REPLIT = ("The Register · Replit 2025.7", "https://www.theregister.com/2025/07/21/replit_saastr_vibe_coding_incident/")
INC_ANTIG = ("The Register · Antigravity 2025.12", "https://www.theregister.com/2025/12/01/google_antigravity_wipes_d_drive/")
INC_CVE = ("The Register · Claude Code CVE 2026.2", "https://www.theregister.com/2026/02/26/clade_code_cves/")
CYERA = ("Cyera · Agent-Inflicted Damage 2026.5", "https://www.cyera.com/research/agent-inflicted-damage-inside-the-real-world-failures-of-enterprise-ai-systems")
OWN_GUARD = ("직접 실측 2026.10.14 · Sonnet 5.5 · labs/lab2_hook_by_claude", "https://github.com/TunaLee/posco-dx/tree/main/labs/lab2_hook_by_claude")
OWN_TOK = ("직접 실측 2026.10.14 · Sonnet 5.5 · Claude Code 세션 기록", "https://github.com/TunaLee/posco-dx/tree/main/labs/demo_quote")
OWN_WORK = ("직접 실측 2026.10.15 · Sonnet 5.5 · labs/work_harness", "https://github.com/TunaLee/posco-dx/tree/main/labs/work_harness")
PH_WILD = ("사진 · U.S. Fish and Wildlife Service (퍼블릭 도메인)", "https://commons.wikimedia.org/wiki/File:Running_wild_horse_-_DPLA_-_cf88630cfe76c58a265153acb3defd01.jpg")
PH_HARNESS = ("사진 · Jude, CC BY-SA 2.0", "https://commons.wikimedia.org/wiki/File:Clydesdale_wagon.jpg")
PH_PARTS = ("그림 · Nouveau Larousse illustré 1898 (퍼블릭 도메인)", "https://commons.wikimedia.org/wiki/File:Parts_of_horse_harness_(in_French,_1898).jpg")
PH_TEAM = ("사진 · Bernard Spragg (퍼블릭 도메인)", "https://commons.wikimedia.org/wiki/File:The_draft_horse_team._(51174500032).jpg")
OWN = ("직접 실측 2026.10.14 · Sonnet 5.5 · labs/demo_quote", "https://github.com/TunaLee/posco-dx/tree/main/labs/demo_quote")

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


EVO = [
    ("챗봇", "2022~", "질문 하나에 답 하나", "더 잘 묻기", "프롬프트 엔지니어링"),
    ("긴 입력 · 검색", "2023~", "문서를 함께 읽고 답", "무엇을 보여 줄지", "컨텍스트 엔지니어링 · RAG"),
    ("도구 호출", "2023~24", "조회 · 계산 · 실행", "시스템 연결 방식 통일", "함수 호출 · MCP"),
    ("에이전트", "2025~", "계획 · 실행 · 확인을 스스로 반복", "반복해도 같은 품질 · 안전 · 비용", "하네스 엔지니어링"),
    ("멀티에이전트", "2026~", "여러 Agent가 나눠 동시에", "지휘 · 검증 · 측정", "오케스트레이션 · 평가"),
]


def evolution(hl=3):
    """모델 발전 단계별 — 할 수 있게 된 것 · 새 요구 · 대응."""
    rows = ["할 수 있게 된 것", "새로 생긴 요구", "대응"]
    head = '<div class="ev-rl"></div>' + "".join(
        f'<div class="ev-h{" hl" if i == hl else ""}" style="--d:{i * .18:.2f}s"><b>{n}</b><span>{y}</span></div>'
        for i, (n, y, *_) in enumerate(EVO))
    body = ""
    for r, label in enumerate(rows):
        body += f'<div class="ev-rl">{label}</div>' + "".join(
            f'<div class="ev-c r{r}{" hl" if i == hl else ""}" style="--d:{i * .18 + .1:.2f}s">{e[2 + r]}</div>'
            for i, e in enumerate(EVO))
    return f'<div class="evo">{head}{body}</div>'


def pages_grid(n=72, per=10):
    """A4 쪽수를 작은 종이로 — 한 칸 = per쪽."""
    cells = "".join(f'<i style="--d:{i * .02:.2f}s"></i>' for i in range(n))
    return f'<div class="pgrid">{cells}</div><div class="pgcap">▯ 한 칸 = A4 {per}쪽</div>'


# 실제 세션(견적 과제 · 내 하네스 · Sonnet 5.5) — 호출마다 컨텍스트 크기에서 계산
CTX_STEPS = [
    ("fix", "시스템 프롬프트", "Claude Code 기본 지침", 8.7),
    ("fix", "내장 도구 정의", "Read · Edit · Bash · Agent …", 22.2),
    ("fix", "하네스", "CLAUDE.md · Skill 목록 · Agent 정의", 0.7),
    ("mcp", "MCP 서버 5개 (연결했다면)", "도구 정의만 · 이번 세션엔 없음", 55.0),
    ("talk", "사용자 요청", "「할인 · 할증 반영해 주세요」 + 시작 정보", 2.6),
    ("tool", "Skill 본문 · 정책 확정본", "Skill 호출 → 참고 파일 읽기", 1.2),
    ("tool", "파일 6개 읽기", "코드 4 · 테스트 · 코딩 규칙", 4.4),
    ("out", "테스트 파일 작성", "Claude가 쓴 내용도 그대로 쌓임", 3.0),
    ("out", "코드 수정 2곳", "models.py · pricing.py", 3.1),
    ("tool", "테스트 실행 결과", "통과 · 실패 출력", 1.4),
    ("sub", "verifier 보고", "Sub Agent는 따로 21.8만 토큰 · 요약만 돌아옴", 0.5),
    ("tool", "검증 스크립트 · 재실행", "명령 출력", 4.3),
    ("out", "최종 보고", "", 1.7),
]
CTX_COL = {"fix": "#1F3A5F", "mcp": "#C9D1DB", "talk": "#9AA5B1", "tool": "#F28C28", "out": "#4B5D73", "sub": "#F6B26B"}
CTX_LABEL = {"fix": "시작 전부터", "mcp": "연결하면", "talk": "대화", "tool": "도구 결과", "out": "Claude 출력", "sub": "Sub Agent"}


def ctx_stack():
    rows, blocks, total, H, top = "", "", 0.0, 340, 60.0
    y = H
    for i, (k, name, desc, v) in enumerate(CTX_STEPS):
        d = f"{i * .45:.2f}s"
        ghost = k == "mcp"
        if not ghost:
            total += v
        rows += (f'<div class="cs-row{" ghost" if ghost else ""}" style="--d:{d}"><span class="cs-dot" style="background:{CTX_COL[k]}"></span>'
                 f'<b>{name}</b><em>{desc}</em><span class="cs-v">{"+" if i else ""}{(f"{v / 10:g}만") if v >= 10 else f"{v:g}천"}</span>'
                 f'<span class="cs-t">{"" if ghost else f"{total:.1f}천"}</span></div>')
        if not ghost:
            h = H * v / top
            y -= h
            blocks += (f'<rect class="cs-b" x="40" y="{y:.1f}" width="150" height="{max(h, 2):.1f}" fill="{CTX_COL[k]}" '
                       f'stroke="#fff" stroke-width="1.5" style="--d:{d}"/>')
    mcp_h = H * 55.0 / top
    ghost = (f'<rect class="cs-b" x="210" y="{H - mcp_h:.1f}" width="70" height="{mcp_h:.1f}" fill="none" stroke="#9AA5B1" '
             f'stroke-width="2" stroke-dasharray="6 5" style="--d:{3 * .45:.2f}s"/>'
             f'<text x="245" y="{H - mcp_h - 8:.1f}" text-anchor="middle" font-size="13" fill="#6B7785">MCP 5개</text>'
             f'<text x="245" y="{H - mcp_h + 18:.1f}" text-anchor="middle" font-size="13" fill="#6B7785">+5.5만</text>')
    ticks = "".join(f'<line x1="34" x2="40" y1="{H - H * t / top:.1f}" y2="{H - H * t / top:.1f}" stroke="#9AA5B1"/>'
                    f'<text x="30" y="{H - H * t / top + 4:.1f}" text-anchor="end" font-size="12" fill="#8A94A3">{t}천</text>'
                    for t in (0, 20, 40, 60))
    svg = (f'<svg class="cs-svg" viewBox="0 -16 300 {H + 56}">{ticks}{blocks}{ghost}'
           f'<text x="115" y="{H + 26}" text-anchor="middle" font-size="14" font-weight="800" fill="#1F3A5F">메인 Agent 컨텍스트</text></svg>')
    leg = "".join(f'<span><i style="background:{CTX_COL[k]}"></i>{v}</span>' for k, v in CTX_LABEL.items())
    return f'<div class="cs"><div class="cs-list">{rows}</div><div class="cs-side">{svg}<div class="cs-leg">{leg}</div></div></div>'


def checks(items, rule):
    """번호 붙은 체크 질문 + 판정 규칙."""
    li = "".join(f'<div class="ck" style="--d:{i * .12:.2f}s"><span>{i + 1}</span><b>{q}</b><em>{w}</em></div>'
                 for i, (q, w) in enumerate(items))
    return f'<div class="cks">{li}</div><div class="ckr">{rule}</div>'


def photo(src, cap, sub=""):
    return (f'<figure class="ph"><img src="img/{src}" alt="{cap}"><figcaption><b>{cap}</b>'
            f'{f"<span>{sub}</span>" if sub else ""}</figcaption></figure>')


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
        stat("코딩 에이전트 사용 현황", "시작",
             big([("73", "%", "코딩 도구 · 에이전트를 매일 사용", True), ("30.9", "%", "하루 4시간 이상 사용"),
                  ("500만+", "", "Codex 주간 사용자 (2026.6)")])
             + hbars([("Claude Code", 65.5, True, "65.5%"), ("GitHub Copilot", 58.7, False, "58.7%"), ("OpenAI Codex", 29.5, False, "29.5%"),
                      ("Cursor", 25.5, False, "25.5%"), ("Google Antigravity", 16.0, False, "16.0%")], top=70, title="쓰는 코딩 에이전트 (복수 응답)"),
             SO26, SO26_DATA, OAI_CODEX),
        stat("AI 답에 대한 신뢰 수준", "시작",
             rings([(48, "쉽게 검증될 때만<br>믿는다"), (76.5, "쓰기 전에<br>직접 실행해 본다", False), (6.6, "중요한 결정까지<br>맡긴다", False)])
             + note("2026 설문", "그대로 쓴다 9.6% · 복잡한 일엔 약하다 24% · 회사 방침 없이 개인 재량 29.7%"),
             SO26_DATA),
        stat("생산성 체감과 실측", "시작",
             big([("3", "배", "개발자가 느끼는 속도 향상 (중앙값)", True), ("1.4~2", "배", "느끼는 업무 가치 향상"),
                  ("30~50", "%", "「AI 없이」는 하기 싫어 실험에서 뺀 과제")])
             + quote("설문 결과가 반드시 현실에 근거한 것은 아니다", "METR, 2026 사용 설문")
             + note("그래서", "느낌 대신 우리 과제 · 우리 평가셋으로 잰다"),
             METR26S, METR26),
        light("최종 산출물", table(["산출물", "내용"], [
            ["<b>내 하네스 플러그인</b>", "CLAUDE.md · Skill · Sub Agent · Hook · 명령을 한 묶음으로"],
            ["<b>평가셋 · 회귀 테스트</b>", "대표 과제 20건 + 엣지 케이스 · 자동 비교"],
            ["<b>전후 비교표</b>", "맨몸 vs 내 하네스 vs 공개 하네스 · 일관성 · 정확도 · 토큰"],
            ["<b>GitHub 저장소</b>", "팀원이 설치해 쓸 수 있는 형태"],
        ]), "시작"),
        light("실습 환경", table(["도구", "용도"], [
            ["<b>Claude Code (비즈니스 계정)</b>", "하네스 만들기 · 대화형 실습"],
            ["<b>VS Code · Python 3.10+</b>", "실습 스크립트 · 데이터"],
            ["<b>Agent Watch</b>", "에이전트 실행 흐름 · 토큰 대시보드"],
            ["<b>Git · GitHub</b>", "하네스 버전 관리 · 공유"],
        ]) + note("실습 저장소", labdir("")), "시작"),
    ]


# ── Ch1 하네스 개념 ─────────────────────────────────────
def ch1():
    return [divider("Ch1", "하네스 엔지니어링 개념", "")] + [
        stat("Harness = 마구(馬具)", "Ch1",
             '<div class="ph2">' + photo("horse_wild.jpg", "마구 없는 말", "힘은 세지만 어디로 갈지 · 언제 멈출지 모름")
             + photo("horse_harness.jpg", "마구를 찬 말", "같은 힘이 수레를 끌고 · 마부가 방향을 잡음") + "</div>"
             + note("비유", "말 = 모델 (힘 · 지능) · 마구 = 하네스 (그 힘을 원하는 일로 바꾸는 장비 전부)"),
             PH_WILD, PH_HARNESS),
        stat("마구와 하네스 부품", "Ch1",
             '<div class="phmap">' + photo("harness_parts.jpg", "마구의 부품 (1898)")
             + table(["마구", "하는 일", "하네스에서는"], [
                 ["<b>굴레 · 고삐</b>", "방향을 정함", "지침 · CLAUDE.md"],
                 ["<b>눈가리개</b>", "볼 것만 보게 함", "컨텍스트 설계"],
                 ["<b>목사리 · 끄는 줄</b>", "힘을 수레에 전달", "도구 · Skill"],
                 ["<b>재갈</b>", "넘으면 바로 멈춤", "Hook · 권한"],
                 ["<b>마부</b>", "최종 판단 · 상태 확인", "사람 승인 · 평가"],
             ]) + "</div>"
             + note("말이 좋아질수록", "마구는 가벼워지지만 사라지지 않음 · 수레를 끄는 일이면 마구가 필요"),
             PH_PARTS),
        stat("여러 말, 한 마차", "Ch1",
             '<div class="phwide">' + photo("horse_team.jpg", "여러 말을 한 마차에", "마구로 묶여야 한 방향으로 끈다 → 멀티에이전트 (Ch5)") + "</div>",
             PH_TEAM),
        light("모델 발전과 요구의 변화", evolution(), "Ch1"),
        light("대화형 작업과 위임형 작업", two(
            cards([("대화형", "질문 → 답 → 사람이 읽고 다음 질문", []),
                   ("사람의 역할", "매 답을 확인 · 실수는 다음 턴에 바로잡음", [])], 1),
            cards([("위임형", "지시 1번 → 도구 수십 번 → 결과 보고", []),
                   ("사람의 역할", "최종 결과만 확인 · 같은 일을 매일 반복", [])], 1))
              + note("달라진 점", "중간 과정을 사람이 보지 않음 → 품질 · 안전을 확인하는 장치가 작업 안에 있어야 함"), "Ch1"),
        stat("채팅과 Claude Code의 작업 방식 차이", "Ch1",
             hbars([("채팅", 13, False, "13번 주고받음"), ("Claude Code", 1, True, "지시 1번")], top=14, title="블로그 글 하나 완성까지 (중앙값)")
             + big([("86", "%", "일이 빨라짐"), ("82", "%", "맡는 일의 범위가 넓어짐"), ("69", "%", "품질이 좋아짐")]),
             A_ECON26),
        stat("에이전트 작업 길이 추세", "Ch1",
             big([("105", "일", "해낼 수 있는 작업 길이가 2배 되는 주기", True),
                  ("5.7", "시간", "GPT-5.4 · 성공률 50% 기준 작업 길이"),
                  ("54", "분", "같은 모델 · 성공률 80% 기준")])
             + note("믿을 만하게 맡기려면", "성공률 기준을 올리면 맡길 수 있는 길이가 6분의 1로 · 그 사이를 하네스 · 검증이 메운다"),
             METR_FRR, METR_TH),
        light("하네스가 필요해진 이유", table(["위임형 작업의 문제", "필요해진 것", "하네스 부품"], [
            ["<b>같은 일을 반복</b>", "매번 같은 형식 · 같은 기준", "지침 · Skill · 평가"],
            ["<b>사람이 중간을 안 봄</b>", "위험한 실행은 강제로 차단", "Hook · 권한"],
            ["<b>길어진 작업</b>", "컨텍스트 · 토큰 관리", "Sub Agent · 압축 · 측정"],
            ["<b>회사만 아는 사실</b>", "확정된 규칙 · 자료 제공", "Skill 참고 자료 · 도구"],
        ]), "Ch1"),
        ill("scenes_more", "harness_rig", "left40", "하네스의 정의",
            ["모델: 답을 만드는 엔진", "하네스: 모델을 감싼 나머지 전부"]),
        hx_map(None, "하네스 지도", "하네스를 이루는 여섯 부품"),
        light("프롬프트 · 컨텍스트 · 하네스 선택 기준", '''<div class="tline t4">
  <div class="tl"><b>프롬프트</b><span>한 번의 질문을 잘 쓰기</span></div>
  <div class="tl"><b>컨텍스트</b><span>무엇을 보여 줄지 고르기</span></div>
  <div class="tl"><b>하네스</b><span>도구 · 권한 · 평가까지 환경 전체</span></div>
  <div class="tl hl"><b>루프</b><span>하네스를 재고 고치는 반복</span></div>
</div>''' + note("실무 기준", "한 번 쓰고 끝 → 프롬프트 · 매번 같은 자료 → 컨텍스트 · 반복 · 위험 · 여러 사람 → 하네스"), "Ch1"),
        light("하네스로 만들기 좋은 업무 · 덜 맞는 업무", two(
            table(["잘 맞음", "이유"], [
                ["<b>자주 반복</b>", "한 번 만든 지침 · Skill · Hook을 계속 재사용"],
                ["<b>규칙 · 기준이 분명</b>", "「잘했다」를 정해야 지침으로 고정 가능"],
                ["<b>결과 확인 가능</b>", "평가셋 · 검증 Agent · 테스트로 자동 확인"],
                ["<b>회사만 아는 지식 필요</b>", "규정 · 양식 · 확정 사항을 넣어 줘야 함"],
                ["<b>막아야 할 구간이 있음</b>", "Hook · 권한으로 강제"],
            ]),
            table(["덜 맞음", "이유"], [
                ["<b>한 번 하고 끝</b>", "대화로 시키는 편이 빠름"],
                ["<b>기준이 매번 다른 판단</b>", "기획 · 협상 · 아이디어"],
                ["<b>확인할 방법이 없음</b>", "좋아졌는지 알 수 없음"],
                ["<b>되돌릴 수 없고 확인 장치도 없음</b>", "결재 · 송금은 사람 승인이 기본"],
            ]))
              + note("근거", "하네스는 토큰 약 1.7배 (실측) → 반복해야 본전 · 회사 확정 정보가 저장소 밖이면 맨몸 5 · 13 · 5점 vs 하네스 15 · 15 · 15점"), "Ch1"),
        light("업무 고르기: 다섯 가지 질문", checks([
            ("한 달에 여러 번 하는가", "반복 → 만든 값을 함"),
            ("입력 · 출력 형식이 대체로 정해져 있는가", "형식 → 지침 · Skill로 고정"),
            ("「잘했다」를 숫자 · 체크리스트로 판단할 수 있는가", "기준 → 평가셋 · 검증 Agent"),
            ("사내 규칙 · 양식 · 기준 문서가 있는가", "지식 → Skill 참고 자료"),
            ("실수를 중간에 잡거나 막을 지점을 정할 수 있는가", "안전 → Hook · 권한 · 사람 확인"),
        ], "4개 이상 「예」 → 하네스 후보 · 1순위는 「자주 하고, 기준이 있고, 확인할 수 있는 일」"), "Ch1"),
        light("IT 업무 적용 사례", table(["업무", "지침 · Skill", "Sub Agent · 도구", "Hook · 권한", "평가"], [
            ["<b>장애 · 문의 1차 분류와 답변 초안</b>", "답변 형식 · 분류 기준 · FAQ", "분류 → 응대 → 검증", "외부 발송 차단", "지난 문의 50건 · 분류 정확도"],
            ["<b>코드 리뷰</b>", "팀 리뷰 기준 Skill", "reviewer (읽기 전용)", "끝내기 전 테스트 · force push 차단", "지난 PR 지적 사항 재현률"],
            ["<b>주간 운영 · 점검 보고서</b>", "보고 양식 · 이상치 기준", "DB 조회 (읽기 전용)", "운영 DB 쓰기 차단", "수치가 원본과 일치"],
            ["<b>사양서 · 도면 수량 · 스펙 추출</b>", "JSON 형식 · 단위 · 규격 규칙", "추출 → 견적 → 검증", "원본 파일 수정 차단", "정답셋 10건 · 필드 F1"],
            ["<b>배포 전 점검</b>", "점검 목록 Skill", "설정 · 보안 검사 Agent", "운영 환경 명령 승인", "놓친 점검 항목 0건"],
        ]), "Ch1"),
        light("작성: 내 업무 명세서", table(["항목", "예 (가상)", "연결되는 장"], [
            ["<b>업무 이름 · 빈도</b>", "주간 설비 점검 보고서 · 매주", "Ch1"],
            ["<b>입력</b>", "점검 체크리스트 엑셀 · 지난 보고서", "Ch3 컨텍스트"],
            ["<b>출력 · 형식</b>", "정해진 양식 보고서 1장", "Ch2 지침 · Skill"],
            ["<b>판단 기준 · 사내 규칙</b>", "이상치 기준 · 보고 양식 규정", "Ch2 Skill 참고 자료"],
            ["<b>쓰는 시스템 · 도구</b>", "사내 DB 조회 · 메일", "Ch2 도구"],
            ["<b>절대 하면 안 되는 것</b>", "운영 DB 수정 · 외부 전송", "Ch2 Hook · 권한"],
            ["<b>사람 확인 지점</b>", "최종 발송 전 팀장 확인", "Ch2 승인"],
            ["<b>잘했다의 기준</b>", "누락 0건 · 수치 원본 일치", "Ch7 평가셋"],
            ["<b>자주 나는 실수 · 예외</b>", "단위 혼동 · 빈 칸", "Ch7 엣지 케이스"],
        ]) + note("양식", labdir("my_work_spec") + " · 고객명 · 수치 · 시스템 주소는 가려서 작성 · 장마다 「내 업무 적용」 한 줄 추가"), "Ch1"),
        light("하네스의 다섯 계층", table(["계층", "담는 것", "설계 결정"], [
            ["<b>모델</b>", "추론 엔진", "어떤 모델 · effort · 한도"],
            ["<b>컨텍스트</b>", "지침 · 참고 자료 · 대화 이력", "항상 넣을 것 vs 필요할 때만"],
            ["<b>도구</b>", "조회 · 계산 · 실행", "이름 · 설명 · 입력 형식 · 개수"],
            ["<b>권한</b>", "허용 · 금지 · 승인", "자동 허용 범위 · 사람 승인 지점"],
            ["<b>평가</b>", "지표 · 평가셋 · 로그", "무엇을 성공으로 볼지"],
        ]), "Ch1"),
        stat("같은 모델의 하네스별 점수", "Ch1",
             hbars([("GPT-5.4 · Codex CLI", 77.3, True, "77.3%"), ("GPT-5.4 · Terminus 2", 54.8, False, "54.8%"),
                    ("GPT-5.4 mini · Codex CLI", 66.1, True, "66.1%"), ("GPT-5.4 mini · Terminus 2", 36.9, False, "36.9%"),
                    ("GPT-5.3-Codex · Codex CLI", 79.1, True, "79.1%"), ("GPT-5.3-Codex · Terminus 2", 68.5, False, "68.5%")], top=100,
                   title="Terminal-Bench 2.1 · 같은 모델, 하네스만 다름")
             + note("최대 22.5점 차이", "Epoch AI도 「성능을 가장 크게 좌우하는 것은 스캐폴드 선택」 (GPT-5 기준 최대 11%)"),
             TB21, EPOCH),
        stat("effort 설정별 점수", "Ch1",
             hbars([("low", 34.9, False, "34.9%"), ("medium", 44.9, False, "44.9%"), ("high", 50.3, False, "50.3%"),
                    ("max", 51.8, False, "51.8%"), ("xhigh", 53.9, True, "53.9%")], top=60,
                   title="Claude Opus 5 · Claude Code · Terminal-Bench 4.0 · effort 설정만 다름")
             + note("많이 생각시킨다고 늘 좋진 않다", "Sonnet 5.5: max 46.2% < xhigh 52.1% · Sub Agent를 남발해 시간 초과 · 범위 밖 수정 (FrontierCode)"),
             TBLB, A_SON55),
        stat("하네스 · 측정 환경별 비용과 점수", "Ch1",
             hbars([("Claude Code", 22.5, True, "도구 22.5회 · 11분"), ("Terminus-2", 41, False, "도구 41회 · 19분")], top=45,
                   title="같은 오픈 모델 6종 · 푼 과제 28 vs 26 · 실행 1회당")
             + big([("7", "%", "약한 모델: 하네스를 바꾸면 남는 정답", True), ("6", "점", "서버 자원 설정만 바꿔 생긴 점수 차"),
                    ("8.8", "점", "같은 모델(Sonnet 5.5), 측정 환경만 다름")]),
             HARBOR, A_NOISE, SC_SONNET55, TBLB),
        stat("모델 발전과 하네스 규모", "Ch1",
             quote("예전 Claude 모델은 포켓몬을 하려면 복잡한 도우미 하네스가 필요했다. Claude Fable 5는 화면만 보고 게임을 끝냈다", "Anthropic, Claude Fable 5 발표 2026.6")
             + hbars([("Mythos 5 · 단일 Agent", 88.0, False, "88.0%"), ("Mythos 5 · 멀티에이전트", 93.3, True, "93.3%")], top=100,
                     title="BrowseComp · 같은 모델, 구성만 다름")
             + note("그래서", "하네스는 한 번 만들고 끝이 아니라, 모델이 바뀔 때마다 재고 덜어 낸다"),
             A_FABLE5, SC_FABLE5),
        light("같은 모델, 다른 하네스", table(["차이", "하네스 A", "하네스 B"], [
            ["<b>도구 설계</b>", "「검색」 하나 · 설명 한 줄", "「FAQ 조회」 「규정 조회」 분리 · 입력 예시"],
            ["<b>컨텍스트</b>", "대화 이력 전부 누적", "핵심만 남기고 Sub Agent로 분리"],
            ["<b>권한</b>", "모든 도구 자동 허용", "읽기만 자동 · 쓰기는 승인"],
            ["<b>결과</b>", "답이 흔들리고 토큰 증가", "답 고정 · 토큰 감소"],
        ]), "Ch1"),
        ill("scenes_hx", "wobbly_vs_steady", "top20", "하네스 없는 Agent vs 있는 Agent",
            ["없음: 같은 질문에 매번 다른 답", "있음: 같은 형식 · 같은 근거"]),
        light("부품별로 막는 문제", table(["부품", "막는 문제", "없으면"], [
            ["<b>지침</b>", "답 형식 · 기준이 흔들림", "같은 질문에 매번 다른 형식"],
            ["<b>Skill</b>", "절차 누락", "체크리스트 단계 건너뜀"],
            ["<b>Tool</b>", "지어낸 숫자", "조회 대신 기억으로 답"],
            ["<b>Sub Agent</b>", "컨텍스트 오염", "긴 작업 중 앞 지시를 잊음"],
            ["<b>Hook · 권한</b>", "위험한 실행", "삭제 · 강제 push · 비밀 파일 수정"],
            ["<b>평가</b>", "조용한 품질 저하", "프롬프트 수정 후 다른 곳이 깨짐"],
        ]), "Ch1"),
        light("신입사원 온보딩과의 비교", table(["신입사원이 받는 것", "Agent의 하네스"], [
            ["회사 소개 · 업무 규칙", "CLAUDE.md"], ["업무 매뉴얼", "Skill"], ["사내 시스템 계정", "Tool · MCP"],
            ["옆 팀 협업", "Sub Agent"], ["결재 · 보안 규정", "Hook · 권한"], ["수습 평가", "평가셋 · 회귀 테스트"],
        ]), "Ch1"),
        light("일관성 측정 지표", table(["지표", "재는 법"], [
            ["<b>답 일치율</b>", "같은 질문 N번 → 가장 많은 답의 비율"],
            ["<b>형식 준수율</b>", "정해진 JSON · 표 형식을 지킨 비율"],
            ["<b>근거 일치</b>", "답의 숫자 · 조항이 원문에 있는 비율"],
            ["<b>토큰</b>", "실행 1회당 입력 · 캐시 · 출력"],
        ]), "Ch1"),
        ba("CLAUDE.md 한 장 전후 비교", "Ch1",
           "이 사양서에서 품목과 수량 알려 줘\n\n→ 1회: 표 · 2회: 문장 · 3회: 수량 단위 누락",
           "CLAUDE.md\n역할: 사양서 추출 담당\n출력: JSON {품목, 규격, 재질, 수량, 단위, 비고}\n규칙: 원문에 없는 숫자는 쓰지 않음, 없으면 null\n\n→ 10회 모두 같은 JSON"),
        lab("1-1", "같은 질문 열 번", "Ch1",
            "맨몸 vs CLAUDE.md 한 장의 차이를 숫자로",
            ["맨몸으로 같은 질문 10회 자동 실행 (run.py)", "harness/CLAUDE.md에 역할 · 출력 형식 · 규칙 쓰기", "같은 입력 10회 다시 실행", "답 종류 수 · JSON 유효율 · 토큰 비교표"],
            ["답 종류 1~2종", "비교표를 최종 산출물 폴더에 저장"], files=labdir("lab1_harness_vs_bare"), mine="내 업무의 답 형식 · 규칙을 CLAUDE.md 세 줄로"),
        bridge("다음: Claude Code 하네스 구조", "", "Ch1", "→ Ch2"),
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
        light("부품별 로드 · 실행 시점", table(["요소", "언제 로드 · 실행", "성격"], [
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
        light("명령(command)의 구조", code(".claude/commands/handle.md", cmd) + note("호출", "/handle VPN이 안 붙어요"), "Ch2"),
        light("Sub Agent 경계 설계", table(["경계", "정하는 것", "예: reviewer"], [
            ["<b>도구 집합</b>", "쓸 수 있는 도구", "Read · Grep · Glob"],
            ["<b>권한</b>", "쓰기 · 실행 허용 여부", "쓰기 금지"],
            ["<b>컨텍스트</b>", "보여 줄 자료 범위", "변경 파일만"],
            ["<b>반환 형식</b>", "부모가 받을 결과", "파일:줄 · 문제 · 근거"],
        ]), "Ch2"),
        light("Sub Agent 정의 파일", two(code(".claude/agents/reviewer.md", agent),
                                          vl("자기 컨텍스트에서 일함", "부모는 결과만 받음", "도구를 줄이면 권한도 줄어듦")), "Ch2"),
        stat("가드가 놓치는 비율", "Ch2",
             hbars([("오토 모드 · 실제 과잉 행동", 17, True, "17% 놓침"), ("오토 모드 · 데이터 유출 시도", 5.7, False, "5.7% 놓침"),
                    ("GPT-5.6 Sol · 확인 정책 없음", 2.9, False, "파괴적 행동 2.9%"), ("Opus 5.5 · 격리 환경", 1.5, False, "탈출 시도 1.5%"),
                    ("최신 모델 · 프롬프트 주입", 8.5, False, "1.0~8.5% 통과")], top=20,
                   title="모델 · 분류기 단계에서 걸러지지 않는 비율 (2026 공식 자료)")
             + note("계산해 보면", "하루 위험 행동 100건 · 17% 놓침 → 17건이 그대로 실행"),
             A_AUTO, SC_GPT6, SC_OPUS55, SC_HAIKU55),
        stat("사람 승인의 한계", "Ch2",
             big([("93", "%", "승인 요청을 그대로 승인 (승인 피로)", True),
                  ("17", "%", "자동 분류기가 놓친 과잉 행동"),
                  ("0.4", "%", "안전한 명령을 잘못 막은 비율")])
             + note("2026 현재", "Claude Code 대부분 사용자의 기본 권한 = 오토 모드 · 막을 것은 Hook · 권한으로 강제"),
             A_AUTO, SC_OPUS55),
        stat("모델별 프롬프트 주입 성공률", "Ch2",
             hbars([("Gemini 4 Argon", 0.7, False, "0.7%"), ("Claude Opus 5.5", 1.0, False, "1.0%"), ("Claude Fable 5.1", 1.0, False, "1.0%"),
                    ("Claude Sonnet 5.5", 3.4, False, "3.4%"), ("Gemini 3.8 Flash", 5.5, False, "5.5%"), ("Claude Haiku 5.5", 7.1, False, "7.1%"),
                    ("GPT-6 Astra", 8.5, True, "8.5%")], top=10, title="간접 프롬프트 주입 성공률 · 15번 시도 · 같은 공격 세트 (Anthropic 측정)")
             + note("하네스로", "외부 문서 · 웹 · 메일은 읽기 전용 Agent에 · 쓰기 · 전송은 Hook으로 막기"),
             SC_HAIKU55, SC_GPT6),
        stat("안전장치 유무별 공격 성공률", "Ch2",
             hbars([("Opus 5.5 · 모델만", 54.6, False, "54.6%"), ("Opus 5.5 · 탐지기 추가", 11.1, True, "11.1%")], top=60,
                   title="코딩 Agent 대상 적응형 공격 성공률 (200번 × 40개 시나리오)")
             + hbars([("GPT-5.6 Sol · 확인 정책 없음", 2.9, False, "2.9%"), ("GPT-5.6 Sol · 확인 정책 있음", 0.0, True, "0%")], top=4,
                     title="파괴적 행동 비율")
             + note("브라우저", "안전장치 없이 0.09~3.64% → 오토 모드 켜면 모든 모델 0% (110개 시나리오)"),
             SC_OPUS55, SC_GPT6),
        light("놓치면 생기는 문제", table(["유형", "예", "피해"], [
            ["<b>운영 데이터 변경 · 삭제</b>", "DROP · DELETE · 볼륨 삭제 API", "서비스 중단 · 복구 불가"],
            ["<b>파일 · 드라이브 삭제</b>", "홈 폴더 · 드라이브 전체 삭제 명령", "작업물 · 설정 전부 손실"],
            ["<b>이력 파괴</b>", "git push --force", "팀 커밋 이력 덮어씀"],
            ["<b>비밀 유출</b>", "비밀 파일 · 토큰을 읽고 출력 · 전송", "계정 탈취 · 과금"],
            ["<b>스스로 권한 올리기</b>", "설정 · Hook 파일 수정", "다른 가드가 모두 꺼짐"],
            ["<b>검증 무력화</b>", "실패하는 테스트를 고쳐 통과", "버그가 그대로 배포"],
        ]), "Ch2"),
        stat("실제 사고 사례 (2026)", "Ch2", table(["시기 · 도구", "무슨 일", "없었던 가드"], [
            ["<b>2026.4</b> Cursor + Opus 4.6", "스테이징 작업 중 찾은 토큰으로 API 한 번 → 운영 DB와 백업 9초 만에 삭제", "자격 증명 분리 · 파괴적 API 차단"],
            ["<b>2026.2</b> OpenClaw (메일 Agent)", "「실행 전 확인」 지시가 압축으로 사라져 메일 200+ 삭제 · STOP 무시", "지시 밖의 강제 장치"],
            ["<b>2026.3</b> Claude Code", "push 거절 → rebase 후 force push로 원격 이력 덮어씀", "force push 차단 규칙"],
            ["<b>2026.7</b> Codex + GPT-5.6", "임시 폴더 처리 중 홈 경로를 덮어써 홈 폴더 삭제", "샌드박스 (Full Access 모드)"],
        ]) + note("통계", "실제 피해 137건 중 65건이 삭제 · 코드 파괴 · 대부분 확인 관문 없는 코딩 에이전트 (Cyera 2026.5)"),
             INC_POCKET, INC_OPENCLAW, INC_CC_PUSH, INC_CODEX, CYERA),
        stat("이전 사고 사례 (2025)", "Ch2", table(["시기 · 도구", "무슨 일", "없었던 가드"], [
            ["<b>2025.7</b> Replit Agent", "코드 동결을 대문자로 11번 지시했는데도 운영 DB 삭제", "개발 · 운영 분리 · 차단 규칙"],
            ["<b>2025.11</b> Google Antigravity", "캐시 정리 요청에 D: 드라이브 전체 삭제 (자동 실행 모드)", "파괴적 명령 승인"],
            ["<b>2025~26</b> Claude Code · Copilot · Cursor", "저장소의 설정 · Hook 파일로 명령 실행 · 자기 권한 올리기 (CVE 다수, 패치됨)", "설정 파일 보호"],
        ]) + quote("모든 대문자로 열한 번이나 하지 말라고 했다", "Jason Lemkin (Replit 사고 당사자)"),
             INC_REPLIT, INC_ANTIG, INC_CVE),
        light("사고에서 배운 점", table(["교훈", "사례", "가드"], [
            ["<b>지시는 잠금장치가 아님</b>", "Replit · OpenClaw", "Hook · 권한 deny 규칙"],
            ["<b>닿는 자격 증명 = 권한</b>", "PocketOS", "운영 · 개발 계정 분리 · 최소 권한"],
            ["<b>자동 실행 + 경로 실수 = 전체 삭제</b>", "Codex · Antigravity", "샌드박스 · 파괴적 명령 승인"],
            ["<b>가드 자체도 공격 대상</b>", "설정 · Hook 파일 CVE", "설정 파일 보호 · 신뢰 확인"],
        ]), "Ch2"),
        light("Hook 설정과 차단 코드", code(".claude/settings.json (hooks 부분)", hook_cfg) + code(".claude/hooks/guard.py", guard), "Ch2"),
        stat("CLAUDE.md와 Hook의 강제력 차이", "Ch2",
             quote("CLAUDE.md 지침은 권고일 뿐이다. Hook은 결정적이고, 그 동작이 반드시 일어나게 보장한다", "Claude Code Best practices")
             + big([("33", "개", "Hook을 걸 수 있는 이벤트"), ("exit 2", "", "PreToolUse에서 도구 호출 차단", True),
                    ("수만 → 수백", "토큰", "Hook으로 로그에서 ERROR 줄만 넘길 때")]),
             D_BP, D_HOOKS, D_COSTS),
        light("가드 4단계", table(["단계", "성격", "한계"], [
            ["<b>① 모델의 조심성</b>", "확률적 · 지시를 잘 따름", "압축 · 긴 작업에서 지시가 묻힘"],
            ["<b>② 오토 모드 분류기</b>", "확률적 · 사용자 말 기준으로 판정", "실제 과잉 행동 17% 놓침 · 허용 목록은 검사 안 함"],
            ["<b>③ Hook · 권한 규칙</b>", "결정적 · 코드로 매번 차단", "규칙에 없는 우회 경로"],
            ["<b>④ 계정 · 환경 분리</b>", "원천 차단 · 권한 자체가 없음", "설정 비용"],
        ]) + note("원칙", "절대 일어나면 안 되는 일은 ③ · ④로 · ① · ②는 추가 안전망"), "Ch2"),
        stat("실측: 짧은 과제에서의 운영 DB 보호", "Ch2",
             big([("0/18", "회", "운영 DB가 바뀐 실행 (규칙 없음 · 지시만 · 오토 모드 · Hook)"),
                  ("5/5", "회", "오토 모드가 운영 DB 조회(SELECT)까지 막음", True),
                  ("15/15", "", "Claude가 만든 Hook의 시험 사례 통과")])
             + note("해석", "짧고 분명한 과제는 최신 모델도 잘 지킴 · 사고는 긴 작업 · 압축 · 찾아낸 자격 증명 · 경로 실수에서 → 확률이 아니라 코드로 막음"),
             OWN_GUARD),
        stat("부품별 컨텍스트 비용", "Ch2",
             big([("1", "%", "Skill 목록이 쓰는 컨텍스트 (상한)"),
                  ("5천", "토큰", "압축 후 Skill마다 남기는 앞부분"),
                  ("200", "줄 이하", "CLAUDE.md 권장 길이", True),
                  ("2.5만", "토큰", "MCP 도구 출력 기본 한도 (1만부터 경고)")], 4)
             + note("설계 감각", "항상 올라가는 것은 짧게 · 필요할 때 부르는 것은 길어도 된다"),
             D_CCSKILLS, D_COSTS, D_MCP),
        stat("MCP · Skills 확산 현황", "Ch2",
             big([("5억", "회", "MCP SDK 월 다운로드 (대표 SDK 합계)", True),
                  ("10억+", "회", "TypeScript · Python SDK 각각 누적"),
                  ("46", "개", "Agent Skills 형식을 지원하는 도구")])
             + quote("도구 100개짜리 서버에 연결하면, 사용자가 묻기도 전에 그 전부의 값을 치르고 목록이 길수록 도구 고르기도 나빠진다", "MCP 로드맵, 2026.8"),
             MCP26, MCPRM, SKILLSIO),
        lab("2-1", "하네스 부품 네 개", "Ch2",
            "Skill · 명령 · Sub Agent · Hook을 내 예제에 붙이기",
            ["project/.claude 구조 살펴보기", "내 업무 Skill 하나 · 명령 하나 쓰기", "reviewer를 읽기 전용으로 정의", "guard 차단 목록에 규칙 하나 추가 → check.py로 확인"],
            ["새 세션에서 Skill 자동 호출", ".env 수정 요청이 차단됨", "reviewer가 파일을 못 고침"], files=labdir("lab2_claude_code_parts"), mine="내 업무 절차 하나를 Skill 이름 · 단계로"),
        lab("2-2", "Claude로 Hook 만들기", "Ch2",
            "「운영 DB 쓰기 전 허락」을 지시가 아니라 코드로",
            ["막을 것 · 허용할 것 목록 정하기 (prompt.md)", "Claude에게 Hook 생성 요청 · .claude 쓰기 승인", "check_hook.py로 채점 → 놓친 사례를 Claude가 수정", "우회 명령 추가 · 대화에서 실제 차단 확인"],
            ["check_hook.py 15/15", "운영 DB 쓰기가 Hook으로 막히는 것 확인"], files=labdir("lab2_hook_by_claude"), mine="내 업무에서 Hook으로 막을 것 세 가지"),
        stat("Claude Code로 하는 두 종류의 일", "Ch2", two(
            cards([("코드 작업", "기능 구현 · 테스트 · 코드 리뷰 · 배포 전 점검", [])], 1),
            cards([("업무 처리", "문의 답변 · 견적 · 회의록 정리 · 보고서 · 문서 비교 · 메일 초안", [])], 1))
             + note("공통", "같은 부품: 지침 · Skill · Sub Agent · Hook · 평가 → 파일을 읽고 규칙대로 결과물을 만드는 일이면 모두 대상")
             + big([("20", "%", "Codex 주간 사용자 중 개발자가 아닌 지식 노동자"), ("1", "번", "Claude Code로 블로그 글 하나 · 채팅은 13번 주고받음", True)], 2),
             OAI_CODEX, A_ECON26),
        light("업무 처리 하네스 구성", code("labs/work_harness", 'workspace/\n├── CLAUDE.md              # 업무 원칙: 결과는 out/ · 원본 수정 금지 · 근거 표기 · 확정 아닌 건 표시\n├── .claude/\n│   ├── skills/            # 업무 종류마다 절차 · 결과 양식\n│   │   ├── inquiry-answer · spec-quote · meeting-actions\n│   │   └── weekly-report · doc-diff · mail-draft\n│   ├── agents/verifier.md # 원본과 대조 · 고치지 않음\n│   └── hooks/guard.py     # 원본(inputs/) 수정 · 메일 발송 · 외부 전송 차단\n└── inputs/T1 ~ T6         # 업무 자료 (원본)'), "Ch2"),
        light("하네스 만드는 순서", flow([
            ("① 업무 명세서", "입력 · 출력 · 기준 · 금지"),
            ("② CLAUDE.md", "모든 업무 공통 원칙 · 짧게"),
            ("③ Skill", "업무 하나에 하나 · 절차 · 양식"),
            ("④ Hook · 권한", "어기면 사고인 것만 차단"),
            ("⑤ 검증 Agent", "숫자 · 발송 등 틀리면 곤란한 일"),
            ("⑥ 평가 → 고치기", "과거 사례 5~10건으로 채점"),
        ], hl=2) + table(["단계", "work_harness에서 한 일", "결과"], [
            ["<b>② CLAUDE.md</b>", "결과는 out/과제/ · 원본 수정 금지 · 근거 표기", "파일로 남김 12/12 (맨몸 2/12)"],
            ["<b>③ Skill</b>", "spec-quote: 「수량 불일치면 견적 보류」", "회사 규칙대로 보류 (맨몸은 금액 계산 2/2)"],
            ["<b>④ Hook</b>", "inputs/ 수정 · 메일 발송 · 외부 전송 차단", "원본 보존 12/12"],
            ["<b>⑥ 평가</b>", "grade.py · 과제 6개 정답 검사", "112/114 · 시간 · 토큰도 함께"],
        ]) + note("하네스 ≠ Skill", "Skill · CLAUDE.md는 부탁(확률) · Hook은 강제 · 평가는 확인 → 셋이 붙어야 하네스"), "Ch2"),
        light("내용별 넣을 위치", table(["이런 내용이면", "여기에", "예"], [
            ["<b>모든 업무에 해당</b>", "CLAUDE.md", "결과 위치 · 근거 표기 · 확정 아닌 건 표시"],
            ["<b>특정 업무의 방법 · 양식 · 판단 기준</b>", "Skill (긴 원본은 참고 파일)", "견적 절차 · 메일 필수 요소 · 점검 기준"],
            ["<b>어기면 사고</b>", "Hook · 권한", "원본 수정 · 메일 발송 · 운영 DB 쓰기"],
            ["<b>결과를 한 번 더 따져 봐야 함</b>", "검증 Sub Agent", "금액 · 날짜 · 고객 발송물"],
            ["<b>좋아졌는지 알아야 함</b>", "평가 문항 · 채점", "과거 사례 · 엣지 케이스"],
        ]) + note("시작은 작게", "Skill 하나로 시작 → 사고 날 지점은 Hook → 확인은 평가 · Skill의 description에 「언제 쓰는지」를 분명히"), "Ch2"),
        light("실무 과제 여섯 가지", table(["과제", "요청 한마디", "검증 포인트"], [
            ["<b>T1 문의 답변</b>", "「사내 문의 5건에 답변 초안 써 줘」", "규정 조항 근거 · 환불 문의는 담당자에게"],
            ["<b>T2 사양서 견적</b>", "「사양서 두 건으로 견적 내 줘」", "단가표 대조 · 수량 불일치 사양서는 보류"],
            ["<b>T3 회의록 → 할 일</b>", "「회의록에서 할 일 정리해 줘」", "「다음 주 화요일」 → 날짜 · 취소 항목 제외"],
            ["<b>T4 점검 → 주간 보고서</b>", "「점검 기록으로 주간 보고서 만들어 줘」", "「초과」 기준 · 빈 값 · 이틀 연속 → 정비 요청"],
            ["<b>T5 규정 개정 비교</b>", "「작년이랑 뭐가 달라졌는지 정리해 줘」", "초안 + 확정 회의록 반영"],
            ["<b>T6 납기 지연 메일</b>", "「고객사에 납기 지연 안내 메일 초안」", "확정 안 된 날짜 · 보상 약속 금지"],
        ]) + note("자료", labdir("work_harness") + " · 모든 회사 · 인물 · 수치는 가상"), "Ch2"),
        stat("실측: 맨몸 vs 업무 처리 하네스", "Ch2",
             hbars([("맨몸 · 정답 검사", 97.4, False, "111 / 114"), ("하네스 · 정답 검사", 98.2, False, "112 / 114"),
                    ("맨몸 · 결과를 파일로 남김", 16.7, False, "2 / 12"), ("하네스 · 결과를 파일로 남김", 100, True, "12 / 12 (out/과제/)")], top=100,
                   title="Claude Sonnet 5.5 · 실무 과제 6개 × 2회")
             + note("차이가 난 곳", "수량 불일치 사양서: 맨몸은 「확인 필요」라면서도 견적 금액을 냄 (2/2) · 하네스는 회사 규칙대로 보류 · 대신 시간 2.5배 · 토큰 1.6배"),
             OWN_WORK),
        lab("2-3", "업무 처리 하네스로 실무 과제", "Ch2",
            "코드가 아닌 업무도 같은 하네스로 · 맨몸과 비교",
            ["맨몸으로 과제 2개 요청 → grade.py로 채점", "harness/의 CLAUDE.md · .claude를 workspace에 복사", "새 대화로 같은 과제 → 채점 · 결과 위치 · 근거 비교 (Agent Watch)", "내 업무용 Skill 하나를 Claude에게 만들게 하고 처리"],
            ["과제 2개 이상 하네스로 처리 · 채점", "내 업무 Skill 1개"], files=labdir("work_harness"),
            mine="내 업무 하나를 이 하네스에 Skill로 추가"),
        bridge("다음: 컨텍스트 설계", "", "Ch2", "→ Ch3 컨텍스트 엔지니어링"),
    ]


# ── Ch3 컨텍스트 엔지니어링 ─────────────────────────────
def ch3():
    return chapter("Ch3", "컨텍스트 엔지니어링", {"지침 · 컨텍스트", "Sub Agent · 팀"}, "컨텍스트") + [
        light("컨텍스트 창의 구성", viz("context_window") + note("원칙", "책상에 올린 만큼 매번 다시 읽는다 · 올린 것이 많을수록 흐려진다"), "Ch3"),
        stat("1M 토큰의 분량", "Ch3",
             big([("55.5만", "단어", "영어 (Anthropic 공식)"),
                  ("129만", "자", "한국어 (실측 0.77토큰/자)", True),
                  ("2.9만", "줄", "파이썬 코드 (실측 34토큰/줄)"),
                  ("18", "번", "실습 세션 1번 = 5.4만 토큰")], 4)
             + pages_grid(72, 10)
             + note("한국어로", "A4 한 장 1,800자로 잡으면 약 720쪽 · 책 2~3권"),
             D_MODELS, OWN_TOK),
        stat("컨텍스트에 실제로 쌓이는 것", "Ch3", ctx_stack()
             + note("포인트", "말 한마디 하기 전에 이미 3만+ · 대화보다 도구 결과 · Claude 출력이 더 많이 쌓임 · MCP를 붙이면 시작부터 수만"),
             OWN_TOK, D_TOOLSEARCH),
        stat("입력 길이별 정확도 (GraphWalks)", "Ch3",
             hbars([("Gemini 4 Argon", 84.2, False, "99.7 → 84.2"), ("GPT-6 Astra", 71.8, False, "98.7 → 71.8"),
                    ("Claude Opus 5.5", 66.8, True, "90.6 → 66.8"), ("Claude Fable 5.1", 65.0, False, "91.4 → 65.0")], top=100,
                   title="GraphWalks BFS (F1) · 128K 이하 → 256K~1M (막대 = 긴 쪽)")
             + quote("컨텍스트 창은 빨리 차고, 찰수록 성능이 떨어진다", "Claude Code Best practices"),
             GEM4, D_BP),
        stat("입력 길이별 정확도 (MRCR)", "Ch3",
             hbars([("4K~8K", 98.1, False, "98.1%"), ("32K~64K", 90.0, False, "90.0%"), ("128K~256K", 87.5, False, "87.5%"),
                    ("256K~512K", 81.5, False, "81.5%"), ("512K~1M", 74.0, True, "74.0%")], top=100,
                   title="GPT-5.5 · MRCR v2 (8개 단서 찾기) · 입력 길이별")
             + note("더 큰 낙폭", "GPT-5.4: 97.3% → 36.6% · Gemini 3.5 Flash: 128K 77.3% → 1M 26.6%"),
             OAI_GPT55, GEM35F),
        light("컨텍스트에 올라가는 항목", table(["항목", "언제", "크기를 좌우하는 것"], [
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
        light("CLAUDE.md와 Skill의 역할 분리", two(
            code("나쁜 예 · CLAUDE.md 600줄", "# 회사 규정 전문 (복사)\n# 업무 매뉴얼 전문 (복사)\n# 예전 회의록 …\n\n→ 매 요청마다 600줄을 다시 읽음"),
            code("좋은 예 · CLAUDE.md 30줄", "# 역할 · 출력 형식 · 금지 규칙\n# 자세한 절차는 Skill:\n#   incident-report, quote-rules\n\n→ 필요할 때만 Skill 본문 로드")), "Ch3"),
        light("통째 읽기와 검색 읽기 비교", ba_like("「data 폴더 다 읽고 답해 줘」\n→ 문의 30건 + FAQ 전부가 책상에", "「FAQ에서 VPN 조항만 찾아 읽어」\n→ 조항 한 개만 책상에"), "Ch3"),
        light("Sub Agent를 통한 컨텍스트 분리", viz("subagent_fanout"), "Ch3"),
        stat("압축의 비용과 손실", "Ch3",
             quote("압축할 때마다 왜 고치기에 실패했는지, 부품이 어떻게 동작하는지 같은 세부가 빠질 수 있다", "OpenAI, GPT-6 Astra 발표 2026.9")
             + big([("400K", "", "Codex에서 실제 쓰는 창 (API는 1M)"), ("272K", "토큰", "넘으면 입력 가격 2배 (GPT-6 Astra)", True),
                    ("100K", "토큰", "넘으면 서버에서 압축 (Anthropic OSWorld 하네스)")])
             + note("하네스로", "압축만 믿지 말고 노트 · 진행 기록 파일 · Sub Agent로 책상을 나눈다"),
             OAI_GPT6, OAI_GPT55, OAI_GPT6DOC, SC_OPUS55),
        stat("주요 3사 컨텍스트 창 크기", "Ch3",
             big([("100만", "토큰", "Claude 현재 모델 전부 (출력 12.8만)"), ("105만", "토큰", "GPT-6 Astra · GPT-5.5"),
                  ("100만", "토큰", "Gemini 4 Argon (입력+출력)"), ("96.7만", "토큰", "Claude Code 자동 압축 시작", True)], 4)
             + note("크기보다 내용", "창이 커져도 1M 구간에서 정확도는 떨어진다 → 무엇을 올릴지가 여전히 핵심"),
             D_MODELS, OAI_GPT6DOC, GEM4, D_MODELCFG),
        light("긴 세션의 문제와 처방", table(["증상", "원인", "처방"], [
            ["<b>앞 지시를 잊음</b>", "이력이 길어 중요한 줄이 묻힘", "새 작업 = 새 세션"],
            ["<b>엉뚱한 파일 수정</b>", "예전 작업의 흔적이 남음", "/clear 또는 세션 분리"],
            ["<b>점점 느리고 비쌈</b>", "매 턴 전체 이력 재전송", "/compact · 요약 후 이어가기"],
        ]), "Ch3"),
        lab("3-1", "컨텍스트 실험 네 가지", "Ch3",
            "같은 작업, 책상 상태만 바꿔 토큰 비교",
            ["CLAUDE.md 600줄 vs 30줄 + Skill", "폴더 통째 읽기 vs 검색해서 읽기", "직접 조사 vs Sub Agent 위임", "긴 세션 vs 새 세션 · 결과표 채우기"],
            ["변형 4종 입력 · 캐시 · 출력 토큰 표", "품질이 떨어진 변형 표시"], files=labdir("lab3_context"), mine="내 업무 입력 중 항상 올릴 것 vs 필요할 때만 올릴 것"),
        bridge("다음: 공개 하네스", "", "Ch3", "→ Ch4 공개 하네스"),
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
        light("플러그인: 하네스 묶음", cards([
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
        light("Superpowers 설치와 명령", code("Claude Code", sp), "Ch4"),
        light("gstack 설치와 명령", code("터미널 · Claude Code", gs), "Ch4"),
        light("두 하네스의 성격", table(["", "Superpowers", "gstack"], [
            ["<b>방식</b>", "적은 명령 · 강제 흐름", "많은 명령 · 골라 쓰기"],
            ["<b>강점</b>", "계획 · TDD · 리뷰 누락 없음", "역할별 검토 · QA · 보안"],
            ["<b>약점</b>", "작은 일에도 단계가 많음", "흐름은 사람이 챙김"],
            ["<b>함께</b>", "gstack 기획 → Superpowers 실행 → gstack 리뷰 · QA", ""],
        ]), "Ch4"),
        light("설치 전 점검 항목", table(["항목", "확인"], [
            ["<b>Hook · 명령</b>", "어떤 명령을 실행하는가 · 외부 전송은 없는가"],
            ["<b>권한</b>", "자동 허용 범위가 넓지 않은가"],
            ["<b>토큰</b>", "상시 로드되는 Skill · 지침 양"],
            ["<b>사내 규정</b>", "외부 저장소 설치 허용 여부"],
        ]) + note("원칙", "공개 하네스도 내 평가셋으로 잰 뒤에 쓴다"), "Ch4"),
        stat("실측 ①: 정보가 저장소 안에 있는 경우", "Ch4",
             hbars([("맨몸 ×5", 15, False, "15 · 15 · 15 · 15 · 15"), ("내 하네스 ×5", 15, False, "15 · 15 · 15 · 15 · 15"),
                    ("Superpowers ×3", 0.2, True, "0 · 0 · 0 (질문하고 멈춤)")], top=15,
                   title="Claude Sonnet 5.5 · 견적 할인 · 할증 과제 · 숨은 인수 테스트 (15개 중)")
             + hbars([("맨몸", 31, False, "31만 토큰 · 43초"), ("내 하네스", 52, True, "52만 토큰 · 92초"), ("Superpowers", 20, False, "20만 토큰 · 29초")], top=60,
                     title="실행 1회 평균 토큰 (캐시 포함) · 시간 (중앙값)")
             + note("배운 점", "답이 저장소에 있으면 Sonnet 5.5는 맨몸으로도 맞춘다 · 하네스는 절차를 고정하는 대신 토큰 1.7배 · 대화형 하네스는 자동 실행에서 멈춘다"),
             OWN),
        stat("실측 ②: 확정 정보가 저장소 밖에 있는 경우", "Ch4",
             hbars([("맨몸 ×3", 7.7, False, "5 · 13 · 5"), ("내 하네스 ×3", 15, True, "15 · 15 · 15")], top=15,
                   title="같은 과제 · 확정 회의록만 저장소에서 뺌 (확정본은 하네스 Skill에만)")
             + quote("2026Q3 개정안은 「검토 중」인 초안이라 쓰지 않았습니다. 2025 시행본을 적용했습니다", "맨몸 Sonnet 5.5의 작업 보고 (3회 중 2회)")
             + note("배운 점", "모델은 신중했고 가정도 밝혔지만, 회사가 확정한 사실은 모른다 → 그 지식을 넣는 것이 하네스"),
             OWN),
        lab("4-1", "같은 과제, 네 가지 하네스", "Ch4",
            "맨몸 · 내 하네스 · Superpowers · gstack 비교",
            ["sample_app 과제 카드 읽기 (버그 2개)", "맨몸으로 해결 → 기록", "Superpowers · gstack 각각 설치 후 해결", "토큰 · 시간 · 테스트 통과 · 건너뛴 단계 비교"],
            ["compare.md 4열 완성", "내 하네스에 가져올 점 3개"], files=labdir("lab4_public_harness"), mine="공개 하네스에서 내 업무에 가져올 것 하나"),
        bridge("다음: 멀티에이전트", "", "Ch4", "→ Ch5 멀티에이전트"),
    ]


# ── Ch5 멀티에이전트 ───────────────────────────────────
def ch5():
    return chapter("Ch5", "멀티에이전트 오케스트레이션", {"Sub Agent · 팀"}, "오케스트레이션") + [
        light("단일 Agent의 한계", table(["한계", "증상"], [
            ["<b>컨텍스트 과부하</b>", "조사 · 구현 · 검증이 한 책상에 쌓임"],
            ["<b>자기 검증</b>", "자기가 쓴 답을 자기가 채점 → 관대함"],
            ["<b>순차 처리</b>", "독립 작업도 하나씩"],
        ]), "Ch5"),
        stat("멀티에이전트의 효과와 한계", "Ch5",
             big([("2.7", "배", "Opus 5.5 5인 팀 · 같은 점수에 도달하는 속도", True),
                  ("+5.3", "점", "Mythos 5 · 멀티에이전트 구성 (88.0 → 93.3)"),
                  ("느려짐", "", "짧은 과제 · 조율 비용이 이득보다 큼")])
             + note("원칙", "길고 나눌 수 있는 일에만 팀 · 짧은 일은 Agent 하나"),
             SC_OPUS55, SC_FABLE5),
        stat("멀티에이전트 구성별 토큰과 비용", "Ch5",
             hbars([("단일 세션", 1, False, "1×"), ("Agent Teams", 7, True, "약 7×")], top=8, title="Claude Code 토큰 (팀원이 plan 모드일 때)")
             + big([("1.5", "배", "리더 1 + 작업자 25 · 캐시 토큰"), ("½", "", "같은 구성 비용 (작업자는 싼 모델)", True),
                    ("2.3", "시간", "작업 시간 (단일은 15~20시간) · 대신 점수 10~12점↓")])
             + note("OpenAI도", "「Sub Agent 작업은 단일 Agent보다 토큰을 더 쓴다」"),
             D_COSTS, D_OPT, OAI_SUB),
        stat("작업 유형별 권장 구성", "Ch5", table(["상황", "측정 결과 · 권장"], [
            ["<b>한 줄기로 이어지는 일</b>", "오케스트레이터를 만들지 않는다 · 단일 모델 + 낮은 effort가 매번 이김"],
            ["<b>어렵지만 하나인 과제</b>", "단일 Agent가 같은 정확도에 22~30% 더 쌈"],
            ["<b>쉬운 일 위임</b>", "평균 비용 ½ · 비싼 상위 10%는 $33 → $12"],
            ["<b>크고 나눌 수 있는 일</b>", "리더 1 + 작업자 25 · 시간 15~20h → 2.3h · 점수 10~12점↓"],
            ["<b>도구 한도</b>", "Claude Code Sub Agent 동시 20 · 3단계 · OpenAI 기본 동시 3"],
            ["<b>Agent Teams</b>", "실험 기능 · 팀원 3~5명 · 1인당 작업 5~6개"],
        ]), D_OPT, D_SUB, OAI_MA, D_TEAMS),
        light("오케스트레이션 패턴", viz("orchestration_patterns"), "Ch5"),
        light("Sub Agent 위임 구조", viz("subagent_fanout"), "Ch5"),
        light("Agent Teams 구조", viz("agent_teams") + note("상태", "실험 기능 · 환경 변수로 켬 · 위임으로 충분하면 Sub Agent"), "Ch5"),
        light("Sub Agent vs Agent Teams", table(["", "Sub Agent", "Agent Teams"], [
            ["<b>소통</b>", "부모 ↔ 자식 한 방향", "구성원끼리 직접 · 공유 작업 목록"],
            ["<b>맞는 일</b>", "독립 조사 · 검증 · 분업", "서로 결과를 반박 · 보완해야 할 때"],
            ["<b>비용</b>", "자식마다 컨텍스트", "구성원마다 세션 · 더 큼"],
            ["<b>통제</b>", "부모가 순서 강제", "작업 목록 · 규칙으로 조율"],
        ]), "Ch5"),
        ill("scenes_hx", "router_desk", "left40", "예제 A: 문의 라우팅", ["분류 → 영역별 응대 → 검증", "검증 실패 → 재작업 · 사람"]),
        ill("scenes_hx", "spec_extract", "left40", "예제 B: 사양서 추출 · 견적", ["추출 → 견적 → 검증", "원문에 없는 숫자는 실패"]),
        light("검증 Agent 분리", two(
            flow([("분류", "classifier"), ("응대", "domain"), ("검증", "verifier"), ("통과 → 답", "")], hl=2),
            flow([("추출", "extractor"), ("견적", "estimator"), ("검증", "verifier"), ("통과 → 결과", "")], hl=2))
              + note("verifier", "읽기 전용 · 근거 · 숫자 · 정책만 판정 · 고치지 않음"), "Ch5"),
        light("실행 타임라인", viz("timeline_lanes") + note("만드는 법", "실행 기록 → visualize.py → 타임라인 HTML · 실시간은 Agent Watch"), "Ch5"),
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
            ["예제 고르기 (라우팅 · 추출)", ".claude/agents 역할 · 도구 · 반환 형식 손보기", "run.py로 실행 · 실행 기록 저장", "visualize.py → 타임라인에서 병목 · 실패 찾기"],
            ["verifier가 오답 1건 이상 차단", "타임라인 HTML · 레인별 토큰"], files=labdir("lab5_multiagent"), mine="내 업무를 나눌 Agent 역할 (나눌 필요 없으면 「단일」)"),
        bridge("다음: 토큰 경제학", "", "Ch5", "→ Ch6 토큰 경제학"),
    ]


# ── Ch6 토큰 경제학 ─────────────────────────────────────
def ch6():
    return chapter("Ch6", "토큰 경제학", {"평가 · 비용", "지침 · 컨텍스트"}, "토큰") + [
        light("토큰 양 예상 퀴즈", cards([
            ("「VPN 안 돼요」 한 번", "입력 · 출력 각각 몇 토큰?", []),
            ("CLAUDE.md 600줄", "매 요청마다 몇 토큰이 더 붙나?", []),
            ("파일 하나 통째 읽기", "출력의 몇 배?", []),
        ]) + note("퀴즈", "먼저 맞혀 보고 실습에서 실측"), "Ch6"),
        stat("모델별 토큰 가격", "Ch6",
             hbars([("Haiku 5.5", 0.5, False, "$0.10 → $0.50"), ("Sonnet 5.5", 10, False, "$2 → $10"),
                    ("Opus 5.5", 20, False, "$4 → $20"), ("Fable 5.1", 50, True, "$10 → $50")], top=55,
                   title="100만 토큰당 가격 · 입력 → 출력 (막대 = 출력)")
             + note("Claude Code 실제 비용", "개발자 1인 하루 평균 약 $13 · 월 $150~250 · 90%는 하루 $30 미만"),
             D_PRICE, D_COSTS),
        stat("캐시 · 배치 할인 규칙", "Ch6",
             big([("1.25", "배", "캐시 쓰기 (5분 · 1시간은 2배)"),
                  ("0.1", "배", "캐시 읽기 (Opus · Sonnet 5.5는 0.05배)", True),
                  ("1", "번", "한 번만 다시 읽어도 캐시가 이득"),
                  ("50", "%", "배치 API 할인 (입력 · 출력 모두)")], 4)
             + note("기억할 것", "캐시 기본 수명 5분 · 쓸 때마다 갱신 · 앞부분이 1글자라도 바뀌면 새로 씀"),
             D_CACHE, D_PRICE),
        stat("공식 사례로 본 절감 폭", "Ch6",
             hbars([("같은 점수 · 모델 · effort 조정", 81, True, "$1.19 → $0.22"), ("남은 시간 알려 주기", 60, False, "비용 −60%"),
                    ("도구 검색 (도구 502개)", 45, False, "$1.02 → $0.56"), ("오래된 도구 결과 정리", 39, False, "−39%"),
                    ("코드로 도구 호출 묶기", 38, False, "입력 −38%"), ("압축 (긴 작업)", 32, False, "−32%"), ("MCP 도구 지연 로딩", 20, False, "−20%")],
                   top=100, title="Opus 5.5 세대 · Anthropic 측정 (2026.9) · 비용 절감률")
             + note("주의", "짧은 작업에 컨텍스트 편집을 켜면 오히려 +74% · 측정은 「방향」이지 보장이 아님"),
             D_OPT, D_PTC),
        stat("effort별 비용과 점수", "Ch6",
             hbars([("low", 33, False, "비용 ⅓ · −8점"), ("medium (기본)", 70, False, "비용 70% · −2.5점"),
                    ("high", 100, False, "기준"), ("xhigh", 250, False, "비용 2.5배 · +1.4점")], top=260,
                   title="Opus 5.5 · SWE-bench Pro · high 대비 비용과 점수")
             + hbars([("전부 high", 29, False, "95.3% · $0.29"), ("low 먼저 → 실패만 high", 17, True, "약 97% · $0.17")], top=32,
                     title="과제 1건당 비용 · 통과율"),
             D_OPT, D_EFFORT),
        light("토큰 절감 지점", viz("token_levers"), "Ch6"),
        light("캐싱 원리", viz("cache_prefix") + note("규칙", "고정 지침 · 도구 목록은 앞에, 바뀌는 입력은 뒤에 · 시간 · ID를 앞에 넣지 않기"), "Ch6"),
        stat("도구 정의 · 결과의 토큰 비중", "Ch6",
             big([("5.5만", "토큰", "MCP 서버 5개의 도구 정의만"), ("85", "%+", "도구 검색으로 줄어드는 정의 토큰", True),
                  ("84", "%", "실제 에이전트 입력 중 캐시 읽기 (중앙값)")])
             + note("Claude Code 기본값", "도구 검색 켜짐 · 정의가 컨텍스트 10%를 넘으면 지연 로딩 · 새로 시작이면 /clear는 비용 0"),
             D_TOOLSEARCH, D_MCP, D_OPT, D_COSTS),
        light("토큰 절감 레버 다섯 가지", table(["레버", "방법", "주의"], [
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
        light("토큰을 더 써야 하는 상황", table(["상황", "이유"], [
            ["<b>검증 · 리뷰</b>", "틀린 답의 비용이 토큰보다 큼"],
            ["<b>E2E 테스트</b>", "실제 흐름 확인 · 핵심 흐름에만"],
            ["<b>고위험 도메인</b>", "안전 · 계약 · 인사는 큰 모델 + 사람"],
        ]) + note("원칙", "토큰이 아니라 「완료된 작업 1건당 비용」으로 판단"), "Ch6"),
        lab("6-1", "토큰 절감 실측", "Ch6",
            "레버를 하나씩 켜며 토큰 · 품질 비교",
            ["quiz.md로 먼저 예상", "기준선 5개 과제 실행 (bench.py)", "레버 켜기: 간결 지시 · caveman · 모델 나누기 · Sub Agent", "토큰 · 정확도 함께 비교 → 남길 레버 고르기"],
            ["레버별 토큰 · 정확도 표", "품질이 떨어진 레버는 제외"], files=labdir("lab6_tokens"), mine="내 업무 1회 토큰 예상 · 쓸 레버 하나"),
        bridge("다음: 평가 · 회귀 테스트", "", "Ch6", "→ Ch7 평가 · 회귀 테스트"),
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
    compare = ("python run_suite.py --k 3 --out results/before.json\n"
               "# 하네스 수정\n"
               "python run_suite.py --k 3 --out results/after.json\n"
               "python compare.py results/before.json results/after.json\n\n"
               "정확도      0.72 → 0.90   ▲\n"
               "일관성      0.60 → 0.95   ▲\n"
               "환각 건수      7 → 1      ▼\n"
               "입력 토큰   12.4k → 8.1k  ▼\n"
               "결과: 통과")
    return chapter("Ch7", "평가 · 회귀 테스트", {"평가 · 비용"}, "평가") + [
        stat("pass@k와 pass^k", "Ch7", passk(0.75, 10)
             + note("같은 모델", "1회 75% → 10번 모두 성공은 약 6% · 업무 자동화는 「매번」이 기준"), A_EVALS),
        stat("평가셋 시작 규모와 기준", "Ch7",
             big([("20~50", "개", "실제 실패에서 뽑은 첫 평가 과제", True),
                  ("0", "%", "통과율 0% = 대개 Agent가 아니라 과제가 고장"),
                  ("F1 ≥ 0.85", "", "성공 기준은 숫자로 (공식 예)")])
             + quote("손으로 채점한 적은 문항보다, 자동 채점한 많은 문항이 낫다", "Anthropic 문서, 성공 기준 정하기"),
             A_EVALS, D_SUCCESS),
        stat("채점기 검증", "Ch7",
             big([("0.07", "점", "Claude 작품이라고 알려 주면 후하게 주는 점수 (10점 만점)"),
                  ("9.6", "%", "평가받는 중임을 알아챈 비율 (GPT-6 Astra)", True)], 2)
             + quote("LLM 채점기는 사람 전문가 판정과 맞춰 보정해야 한다", "Anthropic, Demystifying evals for AI agents")
             + note("원칙", "점수가 이상하면 모델보다 채점기 · 과제부터 의심"),
             SC_OPUS55, SC_GPT6, A_EVALS),
        stat("과제 결함과 편법 시도", "Ch7",
             big([("20~28", "%", "학습 중 편법을 시도한 비율"), ("0.06", "%", "편법이 실제 통한 비율 (Mythos 5.1)"),
                  ("3~6", "배", "불가능한 과제에서 늘어난 편법 시도", True)])
             + note("하네스로", "테스트 수정 금지 Hook · 숨은 테스트 · 과제부터 검증"),
             SC_FABLE51, SC_OPUS55),
        stat("공개 벤치마크의 포화와 결함", "Ch7",
             hbars([("Verified · 문제 있는 문항", 59.4, False, "59.4%"), ("Pro · 고장 난 과제", 30, False, "약 30%"),
                    ("Pro · Opus 5.5 점수", 89.9, True, "89.9%")], top=100, title="SWE-bench · OpenAI 감사 · Anthropic 시스템 카드 (2026)")
             + hbars([("Terminal-bench 2.1", 89.4, False, "89.4%"), ("Terminal-bench 4.0", 19.1, True, "19.1%")], top=100,
                     title="같은 모델(Gemini 3.8 Flash), 벤치마크 버전만 다름")
             + note("그래서", "남의 점수보다 우리 업무 평가셋 · 우리 회귀 테스트"),
             OAI_SWEV, OAI_SWEP, SC_OPUS55, GEM38),
        ill("scenes_extra", "calculator_test", "left40", "정답셋 평가", ["평가셋 = 정답 · 허용 범위가 있는 대표 과제"]),
        light("과업마다 다른 가중치", table(["지표", "분류 · 라우팅", "생성 (답변)", "추출 · 계산"], [
            ["<b>정확도</b>", "40", "25", "40"], ["<b>근거 충실도</b>", "—", "30", "30"],
            ["<b>일관성</b>", "30", "15", "20"], ["<b>지연</b>", "15", "10", "—"],
            ["<b>토큰</b>", "15", "10", "10"], ["<b>안전 · 정책</b>", "필수 통과", "필수 통과", "—"],
        ]) + note("원칙", "안전 · 정책은 점수가 아니라 통과 조건"), "Ch7"),
        light("정답셋이 없을 때의 방법 세 가지", cards([
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
        light("judge 신뢰도 확인 방법", table(["확인", "방법"], [
            ["<b>사람과 일치도</b>", "같은 10건을 사람 · judge가 채점 → 일치율 · 카파"],
            ["<b>위치 · 길이 편향</b>", "순서 바꾸기 · 긴 답 편애 확인"],
            ["<b>자기 편향</b>", "같은 모델이 쓴 답을 채점하지 않게"],
        ]), "Ch7"),
        light("멀티 Agent 평가 대상과 지표", table(["대상", "지표"], [
            ["<b>분류 · 라우터</b>", "의도 정확도"], ["<b>Sub Agent</b>", "judge 점수 · 필드 F1"],
            ["<b>verifier</b>", "일부러 넣은 오답 차단율"], ["<b>전체</b>", "최종 품질 · 토큰 · 지연"],
        ]), "Ch7"),
        ill("scenes_hx", "regression_gate", "top20", "회귀 테스트 구조", ["기준선보다 나빠지면 멈춤"]),
        light("하네스 전후 비교 (시연)", code("터미널", compare) + note("숫자", "예시 출력 · 실습에서 내 숫자로"), "Ch7"),
        lab("7-1", "평가셋 + 회귀 테스트", "Ch7",
            "하네스를 고칠 때마다 자동으로 재는 장치",
            ["대표 10건 + 엣지 케이스 + 합성 10건", "judge 기준 → 사람 10건과 일치도", "기준선 실행 → 하네스 수정 → 재실행", "일부러 나쁘게 고쳐 compare.py 실패 확인"],
            ["평가셋 20건 이상", "전후 비교표 · 나빠지면 실패로 끝남"], files=labdir("lab7_eval_regression"), mine="내 업무 평가 문항 다섯 개 · 엣지 케이스 두 개"),
        bridge("다음: 내 하네스 플러그인", "", "Ch7", "→ Ch8 최종 산출물"),
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
        light("운영: 실패 유형 정의", table(["실패", "판정", "대응"], [
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
        light("업무 명세서 → 하네스 파일", table(["명세서 항목", "하네스 파일", "부품"], [
            ["<b>출력 · 형식</b>", "CLAUDE.md", "지침"],
            ["<b>판단 기준 · 사내 규칙</b>", "skills/&lt;업무&gt;/SKILL.md + 참고 자료", "Skill"],
            ["<b>쓰는 시스템 · 도구</b>", "읽기 전용 조회 스크립트 · 도구 정의", "Tool"],
            ["<b>절대 하면 안 되는 것</b>", "hooks/guard.py · 권한 deny 규칙", "Hook · 권한"],
            ["<b>사람 확인 지점</b>", "권한 ask 규칙 · 승인 단계", "권한"],
            ["<b>잘했다의 기준 · 자주 나는 실수</b>", "eval/dataset.jsonl · 엣지 케이스", "평가"],
        ]) + code("Claude Code에 요청", "업무명세서.md를 읽고 이 업무용 하네스 초안을 my-harness/에 만들어 줘.\n"
                  "CLAUDE.md · Skill 1개 · Hook 규칙 · 평가 문항 5개 (엣지 케이스 2개 포함).\n"
                  "명세서에 없는 규칙은 지어내지 말고 TODO로 남겨."), "Ch8"),
        lab("8-1", "내 업무 하네스 플러그인", "Ch8",
            "내 업무 명세서를 설치해 쓰는 하네스로 · 숫자로 증명",
            ["명세서를 Claude에 주고 CLAUDE.md · Skill · Hook · 평가 문항 초안 생성", "my-harness 템플릿에 넣기 · claude plugin validate", "평가 문항으로 맨몸 vs 내 하네스 비교 (Agent Watch로 흐름 확인)", "README에 명세서 요약 · 비교표"],
            ["내 업무 플러그인 설치 · 실행", "비교표 (정답 · 토큰 · 시간) · 막은 것 목록"], files=labdir("lab8_final_plugin"), mine="명세서 → 내 업무용 하네스 초안 · 맨몸과 비교"),
        light("발표 2분", flow([("문제", "무엇이 흔들렸나"), ("하네스", "무엇을 붙였나"), ("숫자", "전후 비교"), ("다음", "운영 계획")], hl=2), "Ch8"),
        bridge("정리: 하네스 개선 루프", "", "Ch8", "다음 차수: 하네스 엔지니어링 심화"),
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
        light("Agent SDK로 구현한 하네스", code("Python · API 키 필요", sdk) + note("자료", labdir("sdk_optional")), "심화"),
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
  .evo{display:grid; grid-template-columns:140px repeat(5, 1fr); gap:14px 16px; margin:4px 0 6px;}
  .evo .ev-rl{font-size:16px; font-weight:700; color:#6B7785; display:flex; align-items:center;}
  .evo .ev-h{background:#1F3A5F; color:#fff; border-radius:12px; padding:16px 16px; position:relative; animation:bnIn .6s both; animation-delay:var(--d);}
  .evo .ev-h b{display:block; font-size:22px;} .evo .ev-h span{font-size:15px; opacity:.75;}
  .evo .ev-h:not(:nth-child(6))::after{content:"→"; position:absolute; right:-14px; top:50%; transform:translateY(-50%); color:#9AA5B1; font-weight:800;}
  .evo .ev-h.hl{background:#F28C28;}
  .evo .ev-c{background:#fff; border:1px solid #E1E5EB; border-radius:10px; padding:16px 16px; font-size:18px; line-height:1.4; min-height:84px; color:#1F2A37; font-weight:600; animation:bnIn .6s both; animation-delay:var(--d);}
  .evo .ev-c.r2{background:#F6F8FA; color:#1F3A5F; font-weight:800;}
  .evo .ev-c.hl{border-color:#F28C28; background:#FFF8F1;} .evo .ev-c.r2.hl{background:#F28C28; color:#fff;}
  @media print{.evo .ev-h,.evo .ev-c{animation:none}}
  .pgrid{display:grid; grid-template-columns:repeat(36, 1fr); gap:4px; margin:2px 0 4px; max-width:1000px;}
  .pgrid i{display:block; aspect-ratio:1/1.414; background:#fff; border:1.5px solid #9AA5B1; border-radius:2px; max-height:34px; animation:bnIn .4s both; animation-delay:var(--d);}
  .pgcap{font-size:13px; color:#8A94A3; margin-bottom:10px;}
  .cs{display:grid; grid-template-columns:1fr 300px; gap:22px; align-items:end;}
  .cs-list{display:grid; gap:4px;}
  .cs-row{display:grid; grid-template-columns:14px 190px 1fr 70px 70px; gap:10px; align-items:center; font-size:14px; padding:3px 10px;
          background:#fff; border:1px solid #E1E5EB; border-radius:8px; animation:bnIn .45s both; animation-delay:var(--d);}
  .cs-row.ghost{border-style:dashed; background:#F6F8FA; color:#8A94A3;}
  .cs-dot{width:12px; height:12px; border-radius:3px;}
  .cs-row b{color:#1F3A5F;} .cs-row.ghost b{color:#8A94A3;}
  .cs-row em{font-style:normal; color:#6B7785; font-size:13px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}
  .cs-v{font-weight:800; color:#E07A12; text-align:right;} .cs-t{font-weight:800; color:#1F3A5F; text-align:right;}
  .cs-svg{width:100%; height:auto;}
  .cs-b{transform-box:fill-box; transform-origin:bottom; animation:csGrow .45s both; animation-delay:var(--d);}
  @keyframes csGrow{from{transform:scaleY(0); opacity:0} to{transform:scaleY(1); opacity:1}}
  .cs-leg{display:flex; flex-wrap:wrap; gap:6px 12px; font-size:12px; color:#6B7785; justify-content:center;}
  .cs-leg i{display:inline-block; width:10px; height:10px; border-radius:2px; margin-right:4px; vertical-align:-1px;}
  @media print{.pgrid i,.cs-row,.cs-b{animation:none}}
  .cks{display:grid; gap:10px; margin:2px 0 14px;}
  .ck{display:grid; grid-template-columns:44px 1fr 340px; gap:16px; align-items:center; background:#fff; border:1px solid #E1E5EB; border-radius:12px; padding:12px 18px; animation:bnIn .5s both; animation-delay:var(--d);}
  .ck span{width:36px; height:36px; border-radius:50%; background:#1F3A5F; color:#fff; display:grid; place-items:center; font-weight:800; font-size:18px;}
  .ck b{font-size:20px; color:#1F3A5F;} .ck em{font-style:normal; color:#6B7785; font-size:15px;}
  .ckr{background:#F28C28; color:#fff; font-weight:800; font-size:19px; border-radius:12px; padding:12px 18px; text-align:center;}
  @media print{.ck{animation:none}}
  .ph2{display:grid; grid-template-columns:1fr 1fr; gap:18px; margin-bottom:12px;}
  .ph{margin:0; background:#fff; border:1px solid #E1E5EB; border-radius:14px; overflow:hidden;}
  .ph img{display:block; width:100%; height:330px; object-fit:cover;}
  .ph figcaption{padding:12px 16px;} .ph figcaption b{font-size:19px; color:#1F3A5F; display:block;}
  .ph figcaption span{font-size:15px; color:#6B7785;}
  .phmap{display:grid; grid-template-columns:430px 1fr; gap:22px; align-items:center;}
  .phmap .ph img{height:auto; object-fit:contain; background:#fff;}
  .phwide .ph img{height:360px;}
  .dl{color:#F28C28; font-weight:800; font-family:var(--mono); text-decoration:underline;}
  .days.two{grid-template-columns:1fr; max-width:900px;}
  .days.two .daycol{display:grid; grid-template-columns:1fr 1fr; gap:10px;}
'''
