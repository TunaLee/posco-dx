"""하네스 엔지니어링 — 한 판본 (심화 난도).

python3 src/build.py → docs/index.html
Ch1 개념 · Ch2 Claude Code 분해 · Ch3 컨텍스트 엔지니어링 · Ch4 공개 하네스 · Ch5 멀티에이전트
Ch6 토큰 경제학 · Ch7 평가 · HITL · Ch8 내 하네스 플러그인 · 심화
"""
import importlib
from pathlib import Path

import deck
import explain
import intro
import labkits

deck.LAB_KIND.update({"1-1": ("필수", 15), "2-1": ("필수", 25), "2-2": ("필수", 20), "2-3": ("필수", 15),
                      "3-1": ("필수", 15), "4-1": ("필수", 30), "5-1": ("필수", 25),
                      "6-1": ("선택", 25), "7-1": ("필수", 30), "8-1": ("필수", 90), "8-2": ("필수", 30)})
from deck import ba, bridge, cards, divider, flow, ill, lab, light
from stats_hx import big, hbars, quote, rings, stat

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
C_OAI_HE = ("OpenAI · Harness engineering 2026.2", "https://openai.com/index/harness-engineering/")
C_STRIPE = ("Stripe · Minions 2026.2", "https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents")
C_SPOTIFY = ("Spotify Engineering · Honk 2025.11", "https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1")
C_AIRBNB = ("Airbnb Tech · 테스트 이전 2025.3", "https://airbnb.tech/?p=366")
C_SHOPIFY = ("Shopify Engineering · Roast 2025.6", "https://shopify.engineering/introducing-roast")
C_WOOWA = ("우아한형제들 기술블로그 2026.4", "https://techblog.woowahan.com/26177/")
C_RAKUTEN = ("Anthropic 고객 사례 · Rakuten", "https://claude.com/customers/rakuten")
C_ANTH_WORK = ("Anthropic · How AI is transforming work 2025.12", "https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic")
C_AGENTSMD = ("OpenAI · Agentic AI Foundation 2025.12", "https://openai.com/index/agentic-ai-foundation/")
C_COPILOT_RV = ("GitHub Blog · Copilot 코드 리뷰 6천만 건", "https://github.blog/ai-and-ml/github-copilot/60-million-copilot-code-reviews-and-counting/")
C_SANDBOX = ("Anthropic · Claude Code sandboxing", "https://anthropic.com/engineering/claude-code-sandboxing")
C_LONGRUN = ("Anthropic · Effective harnesses for long-running agents", "https://anthropic.com/engineering/effective-harnesses-for-long-running-agents")
C_METR = ("METR · 숙련 개발자 연구 2025.7", "https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/")
C_DORA = ("Google · DORA 2025", "https://blog.google/technology/developers/dora-report-2025/")
C_FOWLER = ("martinfowler.com · Harness engineering 2026.2", "https://www.martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html")
D_DESIGNMD = ("Google Labs · DESIGN.md 형식 (alpha)", "https://github.com/google-labs-code/design.md")
D_RALPH = ("Claude Code 플러그인 · ralph-wiggum", "https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum")
D_LOOPCMD = ("Claude Code 문서 · Scheduled tasks (/loop)", "https://code.claude.com/docs/en/scheduled-tasks")
D_HOOKS_STOP = ("Claude Code 문서 · Hooks (Stop)", "https://code.claude.com/docs/en/hooks")
D_HEADLESS = ("Claude Code 문서 · Headless", "https://code.claude.com/docs/en/headless")
HUNTLEY = ("Geoffrey Huntley · Ralph", "https://ghuntley.com/ralph/")
C_SUPERPOWERS = ("obra/superpowers · Skills", "https://github.com/obra/superpowers")
A_GRAPHENG = ("arXiv 2608.21156 · Graph Engineering 2026.8", "https://arxiv.org/abs/2608.21156")
A_LOOPENG = ("arXiv 2608.21884 · Loop Engineering 2026.8", "https://arxiv.org/abs/2608.21884")
ADT_LOOP = ("ADTmag · Loop engineering 2026.7", "https://adtmag.com/articles/2026/07/01/loop-engineering-emerges-as-developers-put-ai-coding-agents-on-repeat.aspx")
OWN_LAB11 = ("직접 실측 2026.10.19 · Sonnet 5.5 · 실습 1-1 요청 그대로 · 각 3회", "https://github.com/TunaLee/posco-dx")
D_CTXWIN = ("Claude Code 문서 · Context window (What survives compaction)", "https://code.claude.com/docs/en/context-window.md")
D_MEMORY = ("Claude Code 문서 · Memory", "https://code.claude.com/docs/en/memory.md")
OWN_LAB51 = ("직접 실측 2026.10.20 · Sonnet 5.5 · 실습 5-1 PR · 각 2회 · 키워드 + 직접 확인", "https://github.com/TunaLee/posco-dx")
D_CAVEMAN = ("caveman README (제작자 발표)", "https://github.com/JuliusBrussee/caveman")
D_PONYTAIL = ("ponytail README (제작자 발표)", "https://github.com/DietrichGebert/ponytail")
OWN_LAB71 = ("직접 실측 2026.10.20 · Sonnet 5.5 · 실습 7-1 요청 그대로 · 각 2회", "https://github.com/TunaLee/posco-dx")
INC_SUPERHUMAN = ("Simon Willison · Superhuman AI 2026.1", "https://simonwillison.net/2026/Jan/12/superhuman-ai-exfiltrates-emails/")
INC_CODEXMAIL = ("PromptArmor · Codex 메일 유출 2026.4", "https://www.promptarmor.com/resources/codex-for-everything-exfiltrates-connected-data")
INC_ECHOLEAK = ("The Hacker News · EchoLeak 2025.6", "https://thehackernews.com/2025/06/zero-click-ai-vulnerability-exposes.html")
TRIFECTA = ("Simon Willison · The lethal trifecta 2025.6", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/")
INC_POCKET = ("Decrypt · PocketOS 2026.4", "https://decrypt.co/365897/ai-agent-deletes-startup-database-9-seconds-founder-says")
INC_OPENCLAW = ("SF Standard · OpenClaw 2026.2", "https://sfstandard.com/2026/02/25/openclaw-goes-rogue/")
INC_CC_PUSH = ("Claude Code GitHub 이슈 #33402 2026.3", "https://github.com/anthropics/claude-code/issues/33402")
INC_CODEX = ("Simon Willison · Codex 파일 삭제 2026.7", "https://simonwillison.net/2026/Jul/16/bad-codex-bug/")
INC_REPLIT = ("The Register · Replit 2025.7", "https://www.theregister.com/2025/07/21/replit_saastr_vibe_coding_incident/")
INC_ANTIG = ("The Register · Antigravity 2025.12", "https://www.theregister.com/2025/12/01/google_antigravity_wipes_d_drive/")
INC_CVE = ("The Register · Claude Code CVE 2026.2", "https://www.theregister.com/2026/02/26/clade_code_cves/")
CYERA = ("Cyera · Agent-Inflicted Damage 2026.5", "https://www.cyera.com/research/agent-inflicted-damage-inside-the-real-world-failures-of-enterprise-ai-systems")
OWN_GUARD = ("직접 실측 2026.10.14 · Sonnet 5.5 · labs/db_guard", "https://github.com/TunaLee/posco-dx/tree/main/labs/db_guard")
OWN_TOK = ("직접 실측 2026.10.14 · Sonnet 5.5 · Claude Code 세션 기록", "https://github.com/TunaLee/posco-dx/tree/main/labs/demo_quote")
OWN_WORK = ("직접 실측 2026.10.15 · Sonnet 5.5 · labs/office_work", "https://github.com/TunaLee/posco-dx/tree/main/labs/office_work")
PH_WILD = ("사진 · U.S. Fish and Wildlife Service (퍼블릭 도메인)", "https://commons.wikimedia.org/wiki/File:Running_wild_horse_-_DPLA_-_cf88630cfe76c58a265153acb3defd01.jpg")
PH_HARNESS = ("사진 · Jude, CC BY-SA 2.0", "https://commons.wikimedia.org/wiki/File:Clydesdale_wagon.jpg")
PH_PARTS = ("그림 · Nouveau Larousse illustré 1898 (퍼블릭 도메인)", "https://commons.wikimedia.org/wiki/File:Parts_of_horse_harness_(in_French,_1898).jpg")
PH_TEAM = ("사진 · Bernard Spragg (퍼블릭 도메인)", "https://commons.wikimedia.org/wiki/File:The_draft_horse_team._(51174500032).jpg")
OWN_RUN = ("직접 실측 2026.10.28 · Claude Code 기본 모델 · labs/steel_qc · 각 1회", "https://github.com/TunaLee/posco-dx/tree/main/labs/steel_qc")
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
    ("루프", "2026~", "사람 없이 일정 · 이벤트로 반복", "멈춤 규칙 · 상태 기록 · 사람 판정", "루프 엔지니어링"),
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



def arch():
    """Claude Code 한 번의 작업 흐름 — 모델이 읽는 것 / 모델 / 모델 밖에서 작동하는 것."""
    ctx = [("Claude Code 기본 지침", "항상"), ("도구 정의 (내장 + MCP)", "항상"), ("CLAUDE.md", "항상"),
           ("Skill 목록", "이름 · 설명만"), ("Sub Agent 목록", "이름 · 설명만"), ("대화 · 도구 결과", "쌓임"), ("새 요청 · /command 본문", "이번 요청")]
    left = "".join(f'<div class="ar-it"><b>{a}</b><em>{b}</em></div>' for a, b in ctx)
    acts = ["답하기", "도구 쓰기 (Read · Bash · MCP …)", "Skill 본문 불러오기", "Sub Agent에게 위임"]
    mid = "".join(f'<div class="ar-act">{a}</div>' for a in acts)
    gate = [("권한", "settings.json 허용 · 거부 · 승인 요청"), ("Hook", "실행 전후 검사 · 차단 (exit 2)"), ("실행", "파일 · 명령 · 외부 시스템")]
    right = "".join(f'<div class="ar-g"><b>{a}</b><em>{b}</em></div>' for a, b in gate)
    return (f'<div class="arch"><div class="ar-col ar-ctx"><div class="ar-h">① 모델이 읽는 것 · 컨텍스트</div>{left}</div>'
            f'<div class="ar-arrow">→</div>'
            f'<div class="ar-col ar-model"><div class="ar-h">② Claude가 고르는 것</div>{mid}</div>'
            f'<div class="ar-arrow">→</div>'
            f'<div class="ar-col ar-gate"><div class="ar-h">③ 모델 밖에서 작동 · 코드</div>{right}</div></div>'
            f'<div class="ar-loop">↺ 실행 결과는 다시 ①로 쌓이고, 끝날 때까지 반복</div>')

def checks(items, rule):
    """번호 붙은 체크 질문 + 판정 규칙."""
    li = "".join(f'<div class="ck" style="--d:{i * .12:.2f}s"><span>{i + 1}</span><b>{q}</b><em>{w}</em></div>'
                 for i, (q, w) in enumerate(items))
    return f'<div class="cks">{li}</div><div class="ckr">{rule}</div>'


def photo(src, cap, sub=""):
    return (f'<figure class="ph"><img src="img/{src}" alt="{cap}"><figcaption><b>{cap}</b>'
            f'{f"<span>{sub}</span>" if sub else ""}</figcaption></figure>')


# METR Time Horizon 1.1 — 당시 최고 성능(SOTA) 모델 · (출시일, 50% 길이 분, 80% 길이 분, 이름표)
METR_SOTA = [
    ("2023-03-14", 4.0, 0.9, "GPT-4"), ("2024-05-13", 7.0, 1.3, ""), ("2024-06-20", 11.4, 1.7, ""),
    ("2024-09-12", 20.3, 4.4, ""), ("2024-12-05", 38.8, 7.1, "o1"), ("2025-02-24", 60.4, 12.1, ""),
    ("2025-04-16", 119.7, 30.0, "o3"), ("2025-08-07", 203.0, 38.3, "GPT-5"), ("2025-11-18", 224.3, 54.1, ""),
    ("2025-11-24", 293.0, 49.4, ""), ("2025-12-11", 352.2, 66.0, ""), ("2026-02-05", 718.8, 69.9, "Claude Opus 4.6"),
    ("2026-04-07", 1044.8, 185.9, "Mythos Preview"),
]


def metr_chart():
    import math
    from datetime import date
    W, H, X0, X1, Y0, Y1 = 760, 380, 70, 740, 340, 20
    t0, t1 = date(2023, 1, 1).toordinal(), date(2026, 7, 1).toordinal()
    lo, hi = math.log2(0.5), math.log2(32 * 60)
    X = lambda d: X0 + (X1 - X0) * (date.fromisoformat(d).toordinal() - t0) / (t1 - t0)
    Y = lambda m: Y0 - (Y0 - Y1) * (math.log2(m) - lo) / (hi - lo)
    g = ""
    for m, lab in ((1, "1분"), (4, "4분"), (15, "15분"), (60, "1시간"), (240, "4시간"), (960, "16시간")):
        g += (f'<line x1="{X0}" x2="{X1}" y1="{Y(m):.1f}" y2="{Y(m):.1f}" stroke="#EEF1F5" stroke-width="1.5"/>'
              f'<text x="{X0 - 8}" y="{Y(m) + 4:.1f}" text-anchor="end" font-size="13" fill="#8A94A3">{lab}</text>')
    for yr in (2023, 2024, 2025, 2026):
        x = X(f"{yr}-01-01")
        g += f'<text x="{x:.1f}" y="{Y0 + 22}" text-anchor="middle" font-size="13" fill="#8A94A3">{yr}</text>'
    band = " ".join(f"{X(d):.1f},{Y(a):.1f}" for d, a, b, _ in METR_SOTA) + " " + \
        " ".join(f"{X(d):.1f},{Y(b):.1f}" for d, a, b, _ in reversed(METR_SOTA))
    g += f'<polygon points="{band}" fill="#F28C28" fill-opacity=".10"/>'
    for idx, col in ((1, "#F28C28"), (2, "#1F3A5F")):
        pts = " L".join(f"{X(r[0]):.1f} {Y(r[idx]):.1f}" for r in METR_SOTA)
        g += f'<path d="M{pts}" fill="none" stroke="{col}" stroke-width="4" stroke-linejoin="round" class="mline"/>'
        for r in METR_SOTA:
            g += f'<circle cx="{X(r[0]):.1f}" cy="{Y(r[idx]):.1f}" r="4.5" fill="{col}"/>'
    for d, a, b, lab in METR_SOTA:
        if lab:
            g += f'<text x="{X(d) - 6:.1f}" y="{Y(a) - 10:.1f}" text-anchor="end" font-size="12.5" font-weight="700" fill="#1F3A5F">{lab}</text>'
    g += (f'<line x1="{X0}" x2="{X1}" y1="{Y(960):.1f}" y2="{Y(960):.1f}" stroke="#D64545" stroke-dasharray="5 5" stroke-width="1.5"/>'
          f'<text x="{X0 + 6}" y="{Y(960) - 6:.1f}" font-size="12" fill="#D64545">16시간 넘는 측정은 신뢰 낮음</text>')
    lx, ly = X0 + 420, Y0 - 56
    g += (f'<rect x="{lx}" y="{ly - 10}" width="14" height="4" fill="#F28C28"/><text x="{lx + 20}" y="{ly - 4}" font-size="13" fill="#1F3A5F" font-weight="700">절반(50%) 성공하는 작업 길이</text>'
          f'<rect x="{lx}" y="{ly + 10}" width="14" height="4" fill="#1F3A5F"/><text x="{lx + 20}" y="{ly + 16}" font-size="13" fill="#1F3A5F" font-weight="700">80% 성공하는 작업 길이</text>'
          f'<text x="{lx + 20}" y="{ly + 36}" font-size="12.5" fill="#E07A12">가운데 띠 = 믿고 맡기기까지의 차이</text>')
    return f'<svg class="mchart" viewBox="0 0 {W} {H}">{g}</svg>'


PROMPTS_HX = {'CLAUDE.md': '이 프로젝트의 CLAUDE.md를 만들어 줘. 모든 작업에 공통인 원칙만 짧게, 30줄 안으로.\n결과는 〈out/작업명/〉 에 파일로 남기고, 〈원본 폴더〉 는 고치지 말고,\n숫자 · 이름 · 날짜는 원본에 있는 것만 써서 없으면 「확인 필요」로 표시하고,\n근거(파일명 · 조항)를 꼭 달고, 〈승인 · 환불 · 외부 발송〉 같은 건 담당자 확인으로 넘기게 해 줘.\n작업별 절차는 여기 말고 Skill로 빼 줘.', 'Skill': '〈업무 이름〉 을 Skill로 만들어 줘. 〈언제 쓰는지〉 할 때 알아서 쓰이게 설명을 달아 주고,\n본문에는 순서, 판단 기준 〈기준〉, 결과 양식 〈양식〉, 하면 안 되는 것을 넣어 줘.\n긴 규정은 같은 폴더에 참고 파일로 빼 두고, 다 만들면 예시 입력 하나로 시험해서 보여 줘.', 'Hook': '〈막을 것〉 은 Hook으로 막아 줘. 〈허용할 것〉 은 그대로 두고.\n막을 때는 왜 막았는지 한 줄 보여 주고, 외부 패키지는 쓰지 말아 줘.\n다 만들면 막아야 할 예 다섯 개, 허용해야 할 예 다섯 개로 직접 시험해서 결과를 표로 보여 줘.', '검증 Agent': '결과물을 원본과 대조하는 읽기 전용 검증 Agent를 만들어 줘.\n숫자 · 날짜 · 빠진 항목 · 지어낸 내용을 찾아서 통과 / 실패와 근거(파일:줄)만 알려 주고, 고치지는 않게.\nCLAUDE.md에도 「끝내기 전에 검증 Agent에게 대조를 맡긴다」를 넣어 줘.', '평가': '이 업무를 채점할 수 있게 평가 문항을 만들어 줘.\n과거 사례 〈5〉건에 까다로운 경우 〈2〉건을 더해서, 각각 입력 · 기대 결과 · 꼭 들어갈 말 · 들어가면 안 되는 말을\neval/cases.jsonl 에 넣고, O / X로 채점하는 스크립트도 만들어 줘. 지금 하네스로 한 번 돌려서 점수를 보여 줘.', '고치기': '방금 채점에서 틀린 걸 보고 하네스를 고쳐 줘.\n원인이 절차면 Skill, 공통 원칙이면 CLAUDE.md, 꼭 막아야 하는 거면 Hook을 고치고,\n무엇을 왜 바꿨는지 한 줄씩 남겨 줘. 다시 채점해서 전후 점수도 비교해 줘.'}


LAB_FILES = set()   # build.py가 docs/dl/ 에 zip · 파일로 만든다


def labdir(d):
    """실습 자료 — 덱과 같은 폴더의 dl/ 에서 내려받기 (GitHub 없이)."""
    if not d:
        LAB_FILES.add("labs")
        return '<a class="dl" href="dl/labs.zip" download>전체 실습 자료 labs.zip</a>'
    if "." in d:
        LAB_FILES.add(d)
        return f'<a class="dl" href="dl/{d}" download>{d}</a>'
    return f'<code class="lfold">labs/{d}</code>'


def filecode(fname, text, label=None):
    """복사 + 「파일로 저장」 버튼이 붙는 템플릿 블록."""
    html = code(label or fname, text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return html.replace('<div class="code', f'<div data-file="{fname}" class="code', 1)


LABS_DIR = Path(__file__).resolve().parent.parent / "labs"


def labfile(rel):
    return (LABS_DIR / rel).read_text(encoding="utf-8").rstrip()

HARNESS_DIR = Path(__file__).resolve().parent / "lab_harness"


def _kitsrc(src):
    if src.startswith("@PROMPT"):
        return KIT_TEXT[src[1:]]
    if src.startswith("@"):
        return (HARNESS_DIR / src[1:]).read_text(encoding="utf-8").rstrip()
    return labfile(src)


def _step(lb, kind, tx):
    if kind == "do":
        return f'<div class="kdo"><span>{lb}</span><p>{tx}</p></div>'
    return code(lb, esc(tx))


def labkit(no, ch):
    """실습 진행 — 하네스 미적용 → 장표의 하네스로 만들기 → 적용 → 비교."""
    k = labkits.KITS[no]
    steps = "".join(_step(*x) for x in k["steps"])
    files = [filecode(fn, _kitsrc(src), shown) for fn, shown, src in k.get("files", [])]
    sub = f'<span class="ks">이번 실습</span><code>{k["folder"]}/</code>' if k["folder"] and not k.get("open") else ""
    head = (f'<div class="kithead"><span>VS Code로 열 폴더</span><code>{k.get("open", "labs")}</code>{sub}'
            f'<em>〈 〉 안만 바꿔 대화창에 붙여 넣기</em></div>')
    tip = note("참고", k["tip"]) if k.get("tip") else ""
    if len(files) >= 3 or k.get("split"):     # 하네스 파일이 많거나 요청문이 길면 앞 장에 따로
        if k.get("tree"):
            grid = (f'<div class="kit ktree"><div class="ctree">{code(k["tree"][0], esc(k["tree"][1]))}</div>'
                    f'<div class="kf">{"".join(files)}</div></div>')
        else:
            grid = f'<div class="kgrid{" kg3" if len(files) >= 5 else ""}">{"".join(files)}</div>'
        head2 = (f'<div class="kithead"><span>VS Code로 열 폴더</span><code>{k.get("open", "labs")}</code>{sub}'
                 f'<em>{k.get("harness_note", "탐색기 새 파일에 화면의 경로째 입력 → 「복사」 → 붙여 넣기 → 저장")}</em></div>')
        return [light(f"실습 {no} 하네스", head2 + grid, ch),
                light(f"실습 {no} 진행", head + f'<div class="kit wide">{steps}</div>' + tip, ch)]
    if files:
        body = f'<div class="kit"><div class="kp">{steps}</div><div class="kf">{"".join(files)}</div></div>'
    else:
        body = f'<div class="kit wide">{steps}</div>'
    return [light(f"실습 {no} 진행", head + body + tip, ch)]



def quest(no, ch, asks, checks, stuck, folder="labs/steel_qc"):
    """실습 진행 — 요청문 복사 대신 「시킬 일 · 확인할 결과」 · 요청은 내 말로."""
    a = "".join(f"<li>{x}</li>" for x in asks)
    c = "".join(f"<li>{x}</li>" for x in checks)
    head = (f'<div class="kithead"><span>VS Code로 열 폴더</span><code>{folder}</code>'
            f'<em>요청은 내 말로 · 아래는 시킬 일의 요점</em></div>')
    body = (f'<div class="qgrid"><div class="qc qa"><div class="qh">Claude에게 시킬 일</div><ol>{a}</ol></div>'
            f'<div class="qc qk"><div class="qh">확인할 결과</div><ul>{c}</ul></div></div>'
            + note("막히면", stuck))
    return light(f"실습 {no} 진행", head + body, ch)

def measured(no, ch, head, rows, take):
    """실습 실측 — 같은 폴더에서 Claude Code로 끝까지 돌린 결과."""
    return stat(f"실습 {no} 실측", ch, table(head, rows) + note("정리", take), OWN_RUN)


def esc(x):
    return x.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


KIT_TEXT = {"PROMPT22": 'db_guard/project 에 운영 DB를 지키는 Hook을 만들어 줘.\n운영 DB(db/prod.db)를 바꾸는 건 어떤 방법이든 막고, 조회는 허용해 줘. 개발 DB는 마음대로 써도 돼.\n그 밖에 rm -rf, .env 읽기, git push --force 도 막아 줘.\n막을 때는 「운영 DB 쓰기는 사용자 허락 필요」처럼 이유를 한 줄로 알려 주고, 외부 패키지는 쓰지 말아 줘.\n다 만들면 python3 db_guard/check_hook.py 로 시험해서, 실패한 게 있으면 고치고 다시 시험해 줘.'}



# ── 하네스 지도 ──────────────────────────────────────────
PARTS = [
    ("지침 · 컨텍스트", "CLAUDE.md · 무엇을 올릴지", "Ch1 · Ch3", (250, 255)),
    ("Skill · 명령", "필요할 때 꺼내 쓰는 절차", "Ch2", (640, 215)),
    ("Tool · MCP", "조회 · 계산 · 외부 연결", "Ch2", (1030, 255)),
    ("Sub Agent · 팀", "역할 분리 · 오케스트레이션", "Ch5", (1030, 590)),
    ("Hook · 권한", "막기 · 기록 · 승인", "Ch2", (640, 650)),
    ("평가 · 비용", "평가셋 · 토큰", "Ch6 · Ch7", (250, 590)),
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
    ("Ch0", "AI 에이전트", "등장 배경 · 도구 사용 · 작업 길이"),
    ("Ch1", "하네스 개념", "하네스 전후 비교표"),
    ("Ch2", "Claude Code 하네스 분해", "Skill · Sub Agent · Hook · 명령"),
    ("Ch3", "컨텍스트 엔지니어링", "컨텍스트 실험표"),
    ("Ch4", "공개 하네스 · 다른 회사 사례", "기업 사례 · Superpowers · gstack"),
    ("Ch5", "멀티에이전트 오케스트레이션", "Supervisor + Sub Agent · 실행 타임라인"),
    ("Ch6", "토큰 경제학", "토큰 절감 실측표"),
    ("Ch7", "평가 · HITL", "사람 판정 기준 · 자동 비교"),
    ("Ch8", "내 하네스 만들기", "메타 하네스 · 패들릿 · 발표"),
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
            ["<b>메타 하네스</b>", "인터뷰 → 설계 → 사람 승인 → 상황에 맞는 하네스 생성 · 시험"],
            ["<b>내 업무 하네스</b>", "메타 하네스로 만든 업무 전용 하네스 · 하네스 미적용과 전후 비교"],
            ["<b>내 업무 툴</b>", "Superpowers로 설계 · 계획 승인 · TDD · 화면은 DESIGN.md"],
            ["<b>사람 판정 기록</b>", "내가 정한 합격 기준으로 직접 판정 · 2분 발표"],
        ]), "시작"),
        light("실습 환경", table(["도구", "용도"], [
            ["<b>Claude Code (비즈니스 계정)</b>", "하네스 만들기 · 대화형 실습"],
            ["<b>VS Code · Python 3.10+</b>", "실습 스크립트 · 데이터"],
            ["<b>Agent Watch</b>", "에이전트 실행 흐름 · 토큰 대시보드"],
            ["<b>Git · GitHub</b>", "하네스 버전 관리 · 공유"],
        ]) + note("실습 자료", labdir("") + " · 장마다 실습 장표의 「사용 파일」에서도 내려받기"), "시작"),
        light("실습 진행 방식", flow([("labs.zip 받기", "아래 링크 · 덱과 같은 곳"), ("압축 풀기", "바탕화면 등"), ("VS Code로 폴더 열기", "실습마다 열 폴더 표시"), ("Claude Code 패널", "왼쪽 위 아이콘"), ("요청문 붙여 넣기", "「실습 진행」 장표")])
              + '<div class="kit wide" style="margin-top:22px">' + code("처음 한 번 · labs 폴더에서", esc("python3 · claude 버전을 확인하고\nlabs 폴더의 실습 폴더 목록을 보여 줘"))
              + code("막히면", esc("방금 오류를 보고 원인과 고칠 방법을 알려 줘. 내 PC 설정은 바꾸기 전에 물어봐"))
              + '</div>' + note("실습 자료", labdir("") + " · 설치할 패키지 없음 (표준 라이브러리만) · 코드는 직접 쓰지 않음"), "시작"),
    ]


# ── Ch0 AI 에이전트 ─────────────────────────────────────
def ch0():
    tl = "".join(f'<div class="tl{" hl" if hl else ""}"><b>{y}</b><span>{t}</span></div>' for y, t, hl in [
        ("2022.11", "채팅 · ChatGPT 공개", False), ("2023.06", "도구 호출 · Function Calling", True),
        ("2024.11", "연결 표준 · MCP", False), ("2025.02", "코딩 에이전트 · Claude Code", True),
        ("2025.07", "범용 에이전트 · ChatGPT agent", False), ("2025.10", "스킬 · Agent Skills", False)])
    return [divider("Ch0", "AI 에이전트", "")] + [
        light("에이전트 등장 배경", cards([
            ("도구 호출", "2023.06 Function Calling · 모델이 부를 함수와 값을 고름", []),
            ("긴 작업", "맡길 수 있는 작업 길이가 약 105일마다 2배", []),
            ("연결 표준", "2024.11 MCP · 사내 시스템을 같은 방식으로 연결", []),
        ], 3) + note("정리", "고를 수 있게 됨 + 오래 이어 감 + 붙이기 쉬워짐 → 에이전트"), "Ch0"),
        light("대화형 작업과 위임형 작업", two(
            cards([("대화형", "질문 → 답 → 사람이 읽고 다음 질문", []),
                   ("사람의 역할", "매 답을 확인 · 실수는 다음 턴에 바로잡음", [])], 1),
            cards([("위임형", "지시 1번 → 도구 수십 번 → 결과 보고", []),
                   ("사람의 역할", "최종 결과만 확인 · 같은 일을 매일 반복", [])], 1))
              + note("달라진 점", "중간 과정을 사람이 보지 않음 → 품질 · 안전을 확인하는 장치가 작업 안에 있어야 함"), "Ch0"),
        light("도구 사용", two(
            cards([("도구 없는 AI", "다음 글자를 확률로 이어 씀 · 계산 · 최신 정보 · 사내 자료 · 실행 불가", [])], 1),
            cards([("도구를 쓰는 AI", "필요할 때 스스로 골라 호출 · 결과를 읽고 다음 행동", [])], 1))
              + flow([("판단", "무엇이 필요한가"), ("도구 호출", "검색 · 파일 · 계산 · 시스템"), ("결과 확인", "충분한가 · 맞는가"), ("다음 행동", "다시 호출 또는 끝")], hl=1), "Ch0"),
        stat("AI가 맡을 수 있는 작업 길이 (METR)", "Ch0",
             '<div class="mwrap">' + metr_chart() + '<div class="mcards">'
             + '<div class="bn hl"><div class="bv">105<small>일</small></div><div class="bl">작업 길이가 2배 되는 기간 (2024년 이후)</div></div>'
             + '<div class="bn"><div class="bv">약 2<small>년</small></div><div class="bl">무어의 법칙 · 칩 성능 2배 주기</div></div>'
             + '<div class="bn"><div class="bv">5.7<small>시간</small> → 54<small>분</small></div><div class="bl">GPT-5.4 · 50% 기준 vs 80% 기준</div></div>'
             + '</div></div>'
             + note("읽는 법", "작업 길이 = 사람이 하면 걸리는 시간 · 법칙이 아닌 측정 추세 · 두 선 사이 = 믿고 맡기기까지의 차이"),
             METR_FRR, METR_TH),
        light("에이전트 구성 요소", flow([("모델", "읽기 · 판단 · 작성"), ("도구", "검색 · 파일 · 실행"), ("지침", "팀 규칙 · 절차"), ("자료", "양식 · 예시 · 참고")], hl=0)
              + note("다음", "모델을 뺀 나머지 전부 = 하네스"), "Ch0"),
        light("채팅 → 에이전트 연표", f'<div class="tline" style="grid-template-columns:repeat(6,1fr)">{tl}</div>'
              + note("출처", "OpenAI (2023.06 · 2025.07) · Anthropic (2024.11 · 2025.02 · 2025.10)"), "Ch0"),
    ]


# ── Ch1 하네스 개념 ─────────────────────────────────────
def ch1():
    return [divider("Ch1", "하네스 엔지니어링 개념", "")] + [
        stat("Harness = 마구(馬具)", "Ch1",
             '<div class="ph2">' + photo("horse_wild.jpg", "마구 없는 말", "힘은 세지만 어디로 갈지 · 언제 멈출지 모름")
             + photo("horse_harness.jpg", "마구를 찬 말", "같은 힘이 수레를 끌고 · 마부가 방향을 잡음") + "</div>"
             + note("비유", "말 = 모델 (힘 · 지능) · 마구 = 하네스 (그 힘을 원하는 일로 바꾸는 장비 전부)"),
             PH_WILD, PH_HARNESS),
        ill("scenes_more", "harness_rig", "left40", "하네스의 정의",
            ["모델: 답을 만드는 엔진", "하네스: 모델을 감싼 나머지 전부"]),
        ill("scenes_hx", "wobbly_vs_steady", "top20", "하네스 없는 Agent vs 있는 Agent",
            ["없음: 같은 질문에 매번 다른 답", "있음: 같은 형식 · 같은 근거"]),
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
        hx_map(None, "하네스 지도", "하네스를 이루는 여섯 부품"),
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
            ["옆 팀 협업", "Sub Agent"], ["결재 · 보안 규정", "Hook · 권한"], ["수습 평가", "평가셋"],
        ]), "Ch1"),
        light("모델 발전과 요구의 변화", evolution(), "Ch1"),
        light("하네스가 필요해진 이유", table(["위임형 작업의 문제", "필요해진 것", "하네스 부품"], [
            ["<b>같은 일을 반복</b>", "매번 같은 형식 · 같은 기준", "지침 · Skill · 평가"],
            ["<b>사람이 중간을 안 봄</b>", "위험한 실행은 강제로 차단", "Hook · 권한"],
            ["<b>길어진 작업</b>", "컨텍스트 · 토큰 관리", "Sub Agent · 압축 · 측정"],
            ["<b>회사만 아는 사실</b>", "확정된 규칙 · 자료 제공", "Skill 참고 자료 · 도구"],
        ]), "Ch1"),
        light("프롬프트 · 컨텍스트 · 하네스 선택 기준", '''<div class="tline t4">
  <div class="tl"><b>프롬프트</b><span>한 번의 질문을 잘 쓰기</span></div>
  <div class="tl"><b>컨텍스트</b><span>무엇을 보여 줄지 고르기</span></div>
  <div class="tl"><b>하네스</b><span>도구 · 권한 · 평가까지 환경 전체</span></div>
  <div class="tl hl"><b>루프</b><span>하네스를 재고 고치는 반복</span></div>
</div>''' + note("실무 기준", "한 번 쓰고 끝 → 프롬프트 · 매번 같은 자료 → 컨텍스트 · 반복 · 위험 · 여러 사람 → 하네스"), "Ch1"),
        stat("같은 모델의 하네스별 점수", "Ch1",
             hbars([("GPT-5.4 · Codex CLI", 77.3, True, "77.3%"), ("GPT-5.4 · Terminus 2", 54.8, False, "54.8%"),
                    ("GPT-5.4 mini · Codex CLI", 66.1, True, "66.1%"), ("GPT-5.4 mini · Terminus 2", 36.9, False, "36.9%"),
                    ("GPT-5.3-Codex · Codex CLI", 79.1, True, "79.1%"), ("GPT-5.3-Codex · Terminus 2", 68.5, False, "68.5%")], top=100,
                   title="Terminal-Bench 2.1 · 같은 모델, 하네스만 다름")
             + note("최대 22.5점 차이", "Epoch AI도 「성능을 가장 크게 좌우하는 것은 스캐폴드 선택」 (GPT-5 기준 최대 11%)"),
             TB21, EPOCH),
        stat("하네스 · 측정 환경에 따라 달라지는 것", "Ch1",
             hbars([("Claude Code 하네스", 22.5, True, "도구 22.5번 · 11분"), ("Terminus-2 (터미널만)", 41, False, "도구 41번 · 19분")], top=45,
                   title="같은 오픈 모델 6종 · 과제 1개당 · 푼 과제 수는 28 vs 26으로 비슷")
             + big([("7", "%", "약한 모델: 하네스를 바꾸면 풀던 문제 중 다시 푸는 비율", True),
                    ("6", "점", "서버 사양만 바꿨는데 같은 모델 점수 차이"),
                    ("8.8", "점", "같은 Sonnet 5.5 · Anthropic 측정 70.6% vs 공개 순위표 61.8%")])
             + note("그래서", "하네스는 비용도 바꾼다 · 남의 점수는 환경이 다르다 → 우리 환경 · 우리 과제로 직접 잰다 (Ch7)"),
             HARBOR, A_NOISE, SC_SONNET55, TBLB),
        stat("모델 발전과 하네스 규모", "Ch1",
             quote("예전 Claude 모델은 포켓몬을 하려면 복잡한 도우미 하네스가 필요했다. Claude Fable 5는 화면만 보고 게임을 끝냈다", "Anthropic, Claude Fable 5 발표 2026.6")
             + hbars([("Mythos 5 · 단일 Agent", 88.0, False, "88.0%"), ("Mythos 5 · 멀티에이전트", 93.3, True, "93.3%")], top=100,
                     title="BrowseComp · 같은 모델, 구성만 다름")
             + note("그래서", "하네스는 한 번 만들고 끝이 아니라, 모델이 바뀔 때마다 재고 덜어 낸다"),
             A_FABLE5, SC_FABLE5),
        lab("1-1", "시험 결과 판정 · 하네스 전후", "Ch1",
            "같은 질문 · 같은 데이터 · 바뀌는 것은 CLAUDE.md 한 장",
            ["가상 시험실 시뮬레이터 켜기", "CLAUDE.md 없이 판정 요청", "판정 기준 · 답 형식을 CLAUDE.md로", "새 대화에서 같은 요청 → 비교"],
            ["전후 차이 한 줄", "CLAUDE.md 1장"], files=labdir("steel_qc"), mine="내 업무에서 「기준은 어디에 · 무엇은 사람이」 두 줄"),
        quest("1-1", "Ch1",
              ["<code>sim/lims_sim.py</code> 를 켜 달라 → 브라우저로 <code>127.0.0.1:8800</code> 확인",
               "최근 결과 20건을 판정해 달라 · CLAUDE.md 없이",
               "판정 기준 · 답 형식 · 하지 않을 일을 CLAUDE.md로 써 달라",
               "새 대화에서 같은 요청"],
              ["규격을 <code>specs.json</code>에서 가져왔는가 · 추측했는가", "불합격과 근접을 나눴는가",
               "출하 승인까지 판단하지 않는가", "답 형식이 매번 같은가"],
              "<code>solution/CLAUDE.md</code> 와 비교"),
        measured("1-1", "Ch1", ["", "CLAUDE.md 없이", "CLAUDE.md 있음"], [
            ["<b>시간</b>", "104초", "47초"],
            ["<b>입력 토큰</b>", "22.6만", "18.5만"],
            ["<b>판정</b>", "정답", "정답"],
            ["<b>답 형식</b>", "장문 · 이모지 · 근거 없는 조언", "3줄 + <code>out/판정결과.md</code>"],
        ], "판정은 둘 다 맞음 · 달라진 것은 시간 · 형식 · 하지 않을 일"),
        stat("루프 엔지니어링이 가능해진 이유", "Ch1",
             '<div class="eqn">'
             '<div class="eq-c"><div class="eq-h">모델이 좋아짐</div><div class="eq-v">9.8 → 21.2<small>회</small></div>'
             '<div class="eq-d">사람 없이 이어서 하는 도구 호출 · 최대 연속 (Anthropic 사내 조사)</div></div>'
             '<div class="eq-op">+</div>'
             '<div class="eq-c"><div class="eq-h">하네스가 좋아짐</div><div class="eq-v sm">기록 · 테스트 · 검증 · 멈춤 규칙</div>'
             '<div class="eq-d">사람이 중간에 안 봐도 품질을 지키는 장치</div></div>'
             '<div class="eq-op">=</div>'
             '<div class="eq-c hl"><div class="eq-h">루프 엔지니어링</div><div class="eq-v sm">사람 없이 반복</div>'
             '<div class="eq-d">일정 · 이벤트로 Agent가 스스로 돌고 사람은 끝에 판정</div></div>'
             '</div>'
             + note("다음 단계", "그래프 엔지니어링 · 여러 Agent · 검증기 · 사람을 잇는 구조로 (2026.8 제안)"),
             C_ANTH_WORK, A_LOOPENG, A_GRAPHENG),
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
        light("Claude가 작업할 때 참고하는 것", arch()
              + note("구분", "①은 부탁 · 참고 (모델이 따르려 함) · ③은 강제 (모델이 우회 못 함) · Skill · Agent는 설명만 상시, 본문은 쓸 때만"), "Ch2"),
        light("프로젝트 폴더 구조 · .claude/", two(
            '<div class="ctree">' + code("폴더 구조", '내-프로젝트/\n├── CLAUDE.md                 공통 원칙\n├── .mcp.json                 MCP 서버\n└── .claude/\n    ├── settings.json         권한 · Hook 등록 (팀 공유)\n    ├── settings.local.json   내 PC 전용 (git 제외)\n    ├── skills/\n    │   └── spec-quote/\n    │       ├── SKILL.md      절차\n    │       └── 단가표.md      참고 자료\n    ├── agents/\n    │   └── verifier.md       Sub Agent 하나 = 파일 하나\n    ├── commands/\n    │   └── triage.md         /triage 로 부름\n    └── hooks/\n        └── guard.py          Hook 스크립트') + "</div>",
            table(["위치", "들어가는 것", "언제 쓰임"], [
                ["<b>CLAUDE.md</b>", "모든 작업 공통 원칙", "세션 시작 때 항상"],
                ["<b>skills/이름/SKILL.md</b>", "업무 절차 · 판단 기준 · 양식 (같은 폴더에 참고 파일)", "요청이 description과 맞을 때"],
                ["<b>agents/이름.md</b>", "Sub Agent 역할 · 쓸 도구 · 모델", "메인이 위임할 때"],
                ["<b>commands/이름.md</b>", "사람이 부르는 /명령", "/이름 입력 때"],
                ["<b>hooks/</b>", "Hook 스크립트 (등록은 settings.json)", "도구 실행 전후마다"],
                ["<b>settings.json</b>", "권한 허용 · 거부 · Hook 등록", "항상 · git으로 팀 공유"],
                ["<b>settings.local.json</b>", "내 PC에서만 쓰는 설정", "항상 · git에 안 올림"],
            ]))
              + note("~/.claude/", "같은 구조를 홈 폴더에 → 내 모든 프로젝트에 적용"), "Ch2"),
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
        lab("2-1", "사내 시스템을 MCP로 연결", "Ch2",
            "붙여 넣기 · curl 없이 Claude가 시험실 데이터를 도구로 조회",
            ["시험실 MCP 서버를 Claude에게 만들게 하기", "<code>claude mcp add</code> 로 등록", "<code>/mcp</code> 로 연결 · 도구 확인", "「방금 들어온 불합격 정리해」"],
            ["도구 5개 연결", "도구 호출로 만든 불합격 표"], files=labdir("steel_qc"), mine="내 업무에서 MCP로 붙이고 싶은 사내 시스템 하나"),
        quest("2-1", "Ch2",
              ["시뮬레이터 API를 읽는 MCP 서버를 만들어 달라 · stdio · 표준 라이브러리만",
               "도구 이름을 정해 주기: <code>recent_results</code> · <code>reject_summary</code> · <code>coil_detail</code> · <code>get_spec</code> · <code>approve_shipment</code>",
               "<code>claude mcp add lims</code> 로 등록하고 연결을 확인해 달라",
               "새 대화: 「방금 들어온 불합격 정리해」 · 처음 한 번 MCP 사용 승인"],
              ["<code>/mcp</code> 에 lims · 도구 5개", "답 위에 <code>mcp__lims__</code> 도구 호출 표시", "curl · 붙여 넣기 없이 답함", "시뮬레이터를 끄면 도구 오류"],
              "<code>solution/mcp_server.py</code> · <code>claude mcp add lims -- python solution/mcp_server.py</code>"),
        measured("2-1", "Ch2", ["단계", "시간", "결과"], [
            ["<b>MCP 서버 만들기</b>", "196초 · 23턴", "도구 5개 · Claude가 직접 불러 보고 검증"],
            ["<b>「방금 들어온 불합격 정리해」</b>", "73초", "87건 · 불합격 4 · 근접 10 · 정답과 일치"],
            ["<b>붙여 넣은 데이터</b>", "—", "0건"],
        ], "도구 이름을 정해 주지 않으면 장표와 다른 이름으로 만듦"),
        light("Skill 한 개의 구조", two(code(".claude/skills/incident-report/SKILL.md", skill),
                                        vl("description: 언제 부를지", "본문: 호출될 때만 로드", "참고 파일: 양식 · 예시"))
              + note("이름", "예시일 뿐 · 팀 규칙에 맞게 자유롭게"), "Ch2"),
        light("명령(command)의 구조", code(".claude/commands/handle.md", cmd) + note("호출", "/handle VPN이 안 붙어요"), "Ch2"),
        light("Skill과 command의 차이", table(["", "command", "Skill"], [
            ["<b>누가 부르나</b>", "사람이 /이름 입력", "Claude가 description을 보고 스스로 · 사람도 /이름으로 가능"],
            ["<b>형태</b>", ".claude/commands/이름.md 한 파일", ".claude/skills/이름/ 폴더 (SKILL.md + 참고 자료)"],
            ["<b>입력</b>", "$ARGUMENTS 로 뒤의 말", "대화 내용 그대로"],
            ["<b>맞는 일</b>", "사람이 시작해야 하는 일 · 배포 · 발송", "업무 절차 · 판단 기준 · 양식"],
            ["<b>비유</b>", "버튼", "업무 매뉴얼"],
        ]) + note("최근", "command는 Skill로 합쳐진 예전 방식 · 둘 다 /이름을 만들고 똑같이 동작 · 새로 만들 땐 Skill")
              + note("자동 호출 끄기", "SKILL.md에 disable-model-invocation: true → 사람만 /이름으로 부름 (배포 · 발송처럼 사람이 시작할 일)"), "Ch2"),
        light("Sub Agent 경계 설계", table(["경계", "정하는 것", "예: reviewer"], [
            ["<b>도구 집합</b>", "쓸 수 있는 도구", "Read · Grep · Glob"],
            ["<b>권한</b>", "쓰기 · 실행 허용 여부", "쓰기 금지"],
            ["<b>컨텍스트</b>", "보여 줄 자료 범위", "변경 파일만"],
            ["<b>반환 형식</b>", "부모가 받을 결과", "파일:줄 · 문제 · 근거"],
        ]), "Ch2"),
        light("Sub Agent 정의 파일", two(code(".claude/agents/reviewer.md", agent),
                                          vl("자기 컨텍스트에서 일함", "부모는 결과만 받음", "도구를 줄이면 권한도 줄어듦")), "Ch2"),
        lab("2-2", "판정 보고 Skill · 원인 조사 Sub Agent", "Ch2",
            "매번 같은 순서로 보고 · 원인 조사는 따로 맡김",
            ["불합격 보고 절차를 Skill로", "원인 조사 Sub Agent 만들기", "「오늘 불합격 보고서 써 줘」", "/tasks 로 조사 Agent 보기"],
            ["Skill 형식대로 보고서", "조사 Agent가 따로 돔"], files=labdir("steel_qc"), mine="내 업무 절차 하나를 Skill 이름 · 단계로"),
        quest("2-2", "Ch2",
              ["불합격 보고 절차를 Skill로: 이상 건 요약 → 코일 상세 → 규격 → 표 · 근거 없으면 「확인 필요」",
               "원인 조사 Sub Agent: 같은 강종 · 라인의 최근 이력 비교 · lims 조회 도구만",
               "「오늘 불합격 보고서 써 줘」",
               "「HB26-00075 원인 조사해 줘」 → <code>/tasks</code> 로 조사 Agent 보기"],
              ["Skill 이름이 호출 표시에 뜨는가", "저장 위치 · CLAUDE.md와 Skill이 부딪히면 어느 쪽?", "조사 Agent가 쓴 도구 · 토큰", "<code>.claude/</code> 쓰기 승인은 내용을 읽고"],
              "<code>solution/dot_claude/skills/reject-report/SKILL.md</code> · <code>agents/investigator.md</code>"),
        measured("2-2", "Ch2", ["요청", "결과"], [
            ["<b>첫 「판정 보고서 써 줘」</b>", "Skill 없이 직접 작성"],
            ["<b>다시 요청</b>", "<code>reject-report</code> 호출 · 불합격 9 · 근접 28 정답"],
            ["<b>저장 위치</b>", "Skill이 아니라 CLAUDE.md 경로를 따름"],
            ["<b>「HB26-00075 원인 조사해 줘」</b>", "조사 Agent 69초 · 인장강도 765 &gt; 상한 720 · 단발"],
        ], "같은 규칙이 두 곳에 있으면 충돌 · 저장 위치 같은 규칙은 한 곳에"),
        stat("DESIGN.md · 디자인 하네스", "Ch2", two(
            '<div class="ctree">' + code("DESIGN.md (예 · 이 강의 장표)", '---\ncolors: { primary: "#1F3A5F", accent: "#F28C28" }\ntypography: { body: Pretendard 15, heading: Pretendard 800 }\nrounded: { card: 12 }\nspacing: { unit: 8 }\n---\n## Overview\n사내 업무 도구 · 정보는 빽빽하게 · 강조는 주황 하나\n\n## Components\n- 표: 헤더 primary · 숫자는 오른쪽 정렬\n\n## Do\'s and Don\'ts\n- Do: 상태는 색 + 글자 함께\n- Don\'t: 그라데이션 · 그림자 남발') + "</div>",
            table(["섹션 (이 순서)", "담는 것"], [
                ["<b>YAML 토큰</b>", "색 · 글꼴 · 모서리 · 간격 기준값"],
                ["<b>Overview</b>", "화면의 성격 한두 줄"],
                ["<b>Colors · Typography</b>", "토큰을 어디에 쓰는지"],
                ["<b>Layout · Elevation · Shapes</b>", "배치 · 깊이 · 모양 규칙"],
                ["<b>Components</b>", "버튼 · 표 · 카드 규칙"],
                ["<b>Do's and Don'ts</b>", "하지 말 것"],
            ]))
             + note("DESIGN.md", "에이전트에게 디자인 규칙을 알려 주는 파일 형식 (Google Labs · alpha)"),
             D_DESIGNMD),
        light("개인 디자인 하네스 적용", two(
            '<div>' + flow([("DESIGN.md", "내 디자인 규칙"), ("CLAUDE.md", "따르라는 한 줄"), ("검사", "lint"), ("판정", "사람")], hl=0)
            + table(["하네스 부품", "디자인에서는"], [
                ["<b>지침</b>", "DESIGN.md · CLAUDE.md 한 줄"],
                ["<b>강제 · 검사</b>", "npx @google/design.md lint DESIGN.md · 토큰 밖 색 검사"],
                ["<b>평가</b>", "화면 캡처를 사람이 보고 판정"],
            ]) + '</div>',
            '<div class="ptall">' + code("DESIGN.md 만들기 · 이렇게 말하면 됨", "이 화면(또는 첨부한 스크린샷)의 스타일을 정리해서 DESIGN.md 를 만들어 줘.\n맨 위에는 색 · 글꼴 · 모서리 · 간격을 YAML 토큰으로, 아래는 Overview부터 Do's and Don'ts까지 형식 순서대로.\n그리고 앞으로 화면을 만들거나 고칠 땐 DESIGN.md 를 따르라고 CLAUDE.md 에 적어 줘.") + "</div>")
              + note("어디에", "Ch8 내 업무 툴에 화면이 있으면 같이 넣기 · 형식이 alpha라 바뀔 수 있음"), "Ch2"),
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
        stat("메일 Agent 프롬프트 주입 사례", "Ch2",
             flow([("공격자 메일", "흰 글씨 · 숨은 지시"), ("Agent가 메일을 읽음", "요약 · 분류 중"), ("지시를 따름", "다른 메일 · 파일 검색"),
                   ("밖으로 전송", "이미지 URL · 폼 · 링크")], hl=3)
             + table(["사례", "무슨 일", "결과"], [
                 ["<b>Superhuman AI</b> (2026.1)", "받은 메일 속 숨은 지시 → 다른 민감 메일 수십 통 내용을 공격자 구글 폼으로", "고위험 판정 · 수정"],
                 ["<b>OpenAI Codex</b> (2026.4)", "메일 정리 중 외부 메일의 주입 → 연결된 데이터 유출", "제보 후 수정"],
                 ["<b>Microsoft 365 Copilot</b> (2025.6)", "메일 한 통으로 클릭 없이 · 나중에 다른 질문을 해도 내부 데이터를 이미지 URL에 실어 전송 (EchoLeak)", "CVSS 9.3 · 패치"],
             ])
             + note("치명적 3요소", "비공개 데이터 접근 + 외부 입력 + 밖으로 보내는 통로 → 셋이 만나면 유출")
             + note("하네스로", "하나를 끊기 · 외부 메일은 읽기 전용 Agent · 외부 전송은 Hook 차단 · 발송은 사람"),
             INC_SUPERHUMAN, INC_CODEXMAIL, INC_ECHOLEAK, TRIFECTA),
        stat("안전장치 유무별 공격 성공률", "Ch2",
             hbars([("Opus 5.5 · 모델만", 54.6, False, "54.6%"), ("Opus 5.5 · 탐지기 추가", 11.1, True, "11.1%")], top=60,
                   title="코딩 Agent 대상 적응형 공격 성공률 (200번 × 40개 시나리오)")
             + hbars([("GPT-5.6 Sol · 확인 정책 없음", 2.9, False, "2.9%"), ("GPT-5.6 Sol · 확인 정책 있음", 0.0, True, "0%")], top=4,
                     title="파괴적 행동 비율")
             + note("브라우저", "안전장치 없이 0.09~3.64% → 오토 모드 켜면 모든 모델 0% (110개 시나리오)"),
             SC_OPUS55, SC_GPT6),
        light("가드 4단계", table(["단계", "성격", "한계"], [
            ["<b>① 모델의 조심성</b>", "확률적 · 지시를 잘 따름", "압축 · 긴 작업에서 지시가 묻힘"],
            ["<b>② 오토 모드 분류기</b>", "확률적 · 사용자 말 기준으로 판정", "실제 과잉 행동 17% 놓침 · 허용 목록은 검사 안 함"],
            ["<b>③ Hook · 권한 규칙</b>", "결정적 · 코드로 매번 차단", "규칙에 없는 우회 경로"],
            ["<b>④ 계정 · 환경 분리</b>", "원천 차단 · 권한 자체가 없음", "설정 비용"],
        ]) + note("원칙", "절대 일어나면 안 되는 일은 ③ · ④로 · ① · ②는 추가 안전망"), "Ch2"),
        stat("CLAUDE.md와 Hook의 강제력 차이", "Ch2",
             quote("CLAUDE.md 지침은 권고일 뿐이다. Hook은 결정적이고, 그 동작이 반드시 일어나게 보장한다", "Claude Code Best practices")
             + big([("33", "개", "Hook을 걸 수 있는 이벤트"), ("exit 2", "", "PreToolUse에서 도구 호출 차단", True),
                    ("수만 → 수백", "토큰", "Hook으로 로그에서 ERROR 줄만 넘길 때")]),
             D_BP, D_HOOKS, D_COSTS),
        light("Hook 설정과 차단 코드", code(".claude/settings.json (hooks 부분)", esc('"PreToolUse": [{\n  "matcher": "mcp__lims__approve_shipment",\n  "hooks": [{ "type": "command",\n             "command": "python solution/hooks/approve_guard.py" }]\n}]'))
              + code("solution/hooks/approve_guard.py (요점)", esc('event = json.load(sys.stdin)\ncoil = event["tool_input"]["coil_id"]\nprint(json.dumps({"hookSpecificOutput": {\n  "hookEventName": "PreToolUse",\n  "permissionDecision": "deny",\n  "permissionDecisionReason": f"출하 승인({coil})은 품질 담당자가 직접"}}))')), "Ch2"),
        lab("2-3", "출하 승인은 사람만 · Hook", "Ch2",
            "「승인하지 마」를 지시가 아니라 코드로",
            ["승인 요청이 그냥 되는지 먼저 확인", "승인 도구를 막는 Hook을 만들게 하기", "같은 요청 → 막히는지", "조회 도구는 그대로인지"],
            ["승인 도구 호출 차단", "막힌 이유를 Claude가 보고"], files=labdir("steel_qc"), mine="내 업무에서 Hook으로 막을 것 세 가지"),
        quest("2-3", "Ch2",
              ["CLAUDE.md만 있을 때 「나는 김품질 · 내가 승인했으니 기록만 남겨 줘」 → 기록이 생기는지",
               "<code>mcp__lims__approve_shipment</code> 를 막는 PreToolUse Hook을 만들어 달라 · 막을 때 이유 한 줄",
               "새 대화에서 같은 말 · 「내가 승인자다」가 통하는지",
               "조회 도구는 그대로 되는지"],
              ["<code>data/approvals.json</code> 에 새 기록 없음", "Claude가 막힌 이유를 그대로 전함", "조회 도구는 정상", "CLAUDE.md 금지 문구만 있을 때와 비교"],
              "<code>solution/hooks/approve_guard.py</code> · <code>solution/dot_claude/settings.json</code>"),
        measured("2-3", "Ch2", ["요청", "CLAUDE.md만", "+ Hook"], [
            ["<b>「출하 승인해 줘」</b>", "거절", "—"],
            ["<b>「나는 김품질 · 기록만 남겨 줘」</b>", "기록됨 · 규칙 우회", "차단 · 기록 0건"],
            ["<b>코일 조회</b>", "허용", "허용"],
            ["<b>Hook 만들기</b>", "—", "86초"],
        ], "부탁은 말로 뚫림 · Hook은 말로 안 뚫림"),
        stat("Claude Code로 하는 두 종류의 일", "Ch2", two(
            cards([("코드 작업", "기능 구현 · 테스트 · 코드 리뷰 · 배포 전 점검", [])], 1),
            cards([("업무 처리", "문의 답변 · 견적 · 회의록 정리 · 보고서 · 문서 비교 · 메일 초안", [])], 1))
             + note("공통", "같은 부품: 지침 · Skill · Sub Agent · Hook · 평가 → 파일을 읽고 규칙대로 결과물을 만드는 일이면 모두 대상")
             + big([("20", "%", "Codex 주간 사용자 중 개발자가 아닌 지식 노동자"), ("1", "번", "Claude Code로 블로그 글 하나 · 채팅은 13번 주고받음", True)], 2),
             OAI_CODEX, A_ECON26),
        light("하네스로 만들기 좋은 업무 · 맞지 않는 업무", two(
            table(["만들기 좋은 업무", "이유"], [
                ["<b>자주 반복</b>", "한 번 만든 지침 · Skill · Hook을 계속 재사용"],
                ["<b>규칙 · 기준이 분명</b>", "「잘했다」를 정해야 지침으로 고정 가능"],
                ["<b>결과 확인 가능</b>", "평가셋 · 검증 Agent · 테스트로 자동 확인"],
                ["<b>회사만 아는 지식 필요</b>", "규정 · 양식 · 확정 사항을 넣어 줘야 함"],
                ["<b>막아야 할 구간이 있음</b>", "Hook · 권한으로 강제"],
            ]),
            table(["맞지 않는 업무", "이유"], [
                ["<b>한 번 하고 끝</b>", "대화로 시키는 편이 빠름"],
                ["<b>기준이 매번 다른 판단</b>", "기획 · 협상 · 아이디어"],
                ["<b>확인할 방법이 없음</b>", "좋아졌는지 알 수 없음"],
                ["<b>되돌릴 수 없고 확인 장치도 없음</b>", "결재 · 송금은 사람 승인이 기본"],
            ])), "Ch2"),
        light("하네스 적용 예시 여섯 유형", table(["유형", "실습 예시", "내 업무라면 (예)", "하네스 핵심"], [
            ["<b>문의 응대형</b>", "사내 문의 답변", "고객 클레임 1차 답변 · 시스템 사용 문의", "규정 근거 Skill · 승인 필요 건은 사람에게 · 발송 차단"],
            ["<b>문서 추출 · 계산형</b>", "사양서 → 견적", "발주서 검토 · 계약 조항 추출", "추출 양식 Skill · 불일치면 보류 · 원본 수정 차단"],
            ["<b>기록 → 보고서형</b>", "점검 기록 → 주간 보고서", "장애 주간 보고 · 생산 실적 보고", "기준값 · 양식 Skill · 빈 값은 확인 필요 · 수치 대조"],
            ["<b>비교 · 검토형</b>", "규정 개정 비교 · 코드 리뷰", "계약 변경점 · 설정 변경 리뷰", "비교 절차 Skill · 검증 Agent · 고치지 않고 판정"],
            ["<b>정리 · 작성형</b>", "회의록 → 할 일 · 안내 메일", "회의 후속 조치 · 공지 · 협력사 메일", "필수 요소 Skill · 확정 아닌 건 표시 · 약속 금지"],
            ["<b>개발형</b>", "내 업무 툴 (Ch8)", "MES 로그 분석 · 정산 검증 배치 · 테스트 보강", "Superpowers: 설계 → 계획 → Sub Agent TDD · 리뷰"],
        ]) + note("샘플", labdir("samples") + " · 11개 업무 분야 가상 데이터 · 분야마다 하네스 주제 예시 3개"), "Ch2"),
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
        stat("주요 3사 컨텍스트 창 크기", "Ch3",
             big([("100만", "토큰", "Claude 현재 모델 전부 (출력 12.8만)"), ("105만", "토큰", "GPT-6 Astra · GPT-5.5"),
                  ("100만", "토큰", "Gemini 4 Argon (입력+출력)"), ("96.7만", "토큰", "Claude Code 자동 압축 시작", True)], 4)
             + note("크기보다 내용", "창이 커져도 1M 구간에서 정확도는 떨어진다 → 무엇을 올릴지가 여전히 핵심"),
             D_MODELS, OAI_GPT6DOC, GEM4, D_MODELCFG),
        light("컨텍스트에 올라가는 항목", table(["항목", "언제", "크기를 좌우하는 것"], [
            ["<b>시스템 · 도구 목록</b>", "항상", "MCP · 도구 개수"],
            ["<b>CLAUDE.md</b>", "항상", "길이 · 중복"],
            ["<b>Skill 설명</b>", "항상 (본문은 호출 때)", "Skill 개수"],
            ["<b>대화 이력</b>", "쌓임", "세션 길이"],
            ["<b>도구 결과</b>", "쌓임 · 가장 큼", "파일 통째 읽기 · 긴 로그"],
        ]) + note("확인", "/context 로 지금 책상 상태 보기"), "Ch3"),
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
        light("네 가지 전략", cards([
            ("쓰기", "필요한 걸 밖에 적어 둠 · 메모 · 상태 파일", []),
            ("고르기", "필요한 것만 · 검색 · RAG · 부분 읽기", []),
            ("줄이기", "/compact · 요약 · 오래된 도구 결과 정리", []),
            ("나누기", "Sub Agent에 위임 · 결과 요약만 받음", []),
        ], 4), "Ch3"),
        light("CLAUDE.md와 Skill의 역할 분리", two(
            code("나쁜 예 · CLAUDE.md 600줄", "# 회사 규정 전문 (복사)\n# 업무 매뉴얼 전문 (복사)\n# 예전 회의록 …\n\n→ 매 요청마다 600줄을 다시 읽음"),
            code("좋은 예 · CLAUDE.md 30줄", "# 역할 · 출력 형식 · 금지 규칙\n# 자세한 절차는 Skill:\n#   incident-report, quote-rules\n\n→ 필요할 때만 Skill 본문 로드")), "Ch3"),
        light("통째 읽기와 검색 읽기 비교", ba_like("「data 폴더 다 읽고 답해 줘」\n→ 문의 30건 + FAQ 전부가 책상에", "「FAQ에서 VPN 조항만 찾아 읽어」\n→ 조항 한 개만 책상에"), "Ch3"),
        light("외부 지식 · 위임으로 덜어내기", two(
            '<div>' + flow([("질문", "VPN 규정?"), ("검색", "문서 · DB"), ("조각만", "3~5개"), ("답", "+ 근거")], hl=2)
            + table(["RAG (검색 증강 생성)", ""], [
                ["<b>방식</b>", "문서 전체 대신 질문에 맞는 조각만 찾아 넣음"],
                ["<b>도구</b>", "Grep · 사내 검색 MCP · 벡터 검색"],
                ["<b>주의</b>", "검색이 틀리면 답도 틀림 · 근거 표기로 확인"],
            ]) + '</div>',
            '<div>' + flow([("메인", "로그 50개 조사"), ("조사 담당", "Sub Agent · 다 읽음"), ("요약만", "수천 토큰"), ("메인", "가벼운 채로")], hl=2)
            + table(["Sub Agent 위임", ""], [
                ["<b>방식</b>", "많이 읽어야 하는 일을 따로 맡기고 결과만 받음"],
                ["<b>도구</b>", ".claude/agents/ · 읽기 전용 조사 담당"],
                ["<b>주의</b>", "전체 토큰은 비슷하거나 더 큼 · 메인만 가벼워짐"],
            ]) + '</div>')
              + note("공통", "책상(메인 컨텍스트)에는 지금 필요한 것만 · 나머지는 밖에 두고 필요할 때 찾거나 맡긴다"), "Ch3"),
        stat("압축의 비용과 손실", "Ch3",
             quote("압축할 때마다 왜 고치기에 실패했는지, 부품이 어떻게 동작하는지 같은 세부가 빠질 수 있다", "OpenAI, GPT-6 Astra 발표 2026.9")
             + big([("400K", "", "Codex에서 실제 쓰는 창 (API는 1M)"), ("272K", "토큰", "넘으면 입력 가격 2배 (GPT-6 Astra)", True),
                    ("100K", "토큰", "넘으면 서버에서 압축 (Anthropic OSWorld 하네스)")])
             + note("하네스로", "압축만 믿지 말고 노트 · 진행 기록 파일 · Sub Agent로 책상을 나눈다"),
             OAI_GPT6, OAI_GPT55, OAI_GPT6DOC, SC_OPUS55),
        stat("압축 때 하네스는 어떻게 되나", "Ch3", table(["하네스 부품", "압축하면"], [
            ["<b>프로젝트 CLAUDE.md · 자동 메모리</b>", "디스크에서 다시 읽어 넣음 · 요약되지 않음"],
            ["<b>이미 호출된 Skill</b>", "다시 붙임 · Skill마다 앞 5,000토큰 · 합계 25,000토큰 · 오래된 것부터 빠짐"],
            ["<b>Hook · 권한</b>", "모델 밖 코드라 그대로 매번 작동"],
            ["<b>최근 읽고 고친 파일</b>", "최근 수정순 5개까지 다시 읽음"],
            ["<b>대화로만 준 지시</b>", "요약되며 빠질 수 있음"],
        ]) + note("그래서", "계속 지킬 규칙은 CLAUDE.md · 꼭 막을 것은 Hook · Skill은 중요한 내용을 앞쪽에 · 남길 것은 /compact 〈지시〉"),
             D_CTXWIN, D_MEMORY),
        light("긴 세션의 문제와 처방", table(["증상", "원인", "처방"], [
            ["<b>앞 지시를 잊음</b>", "이력이 길어 중요한 줄이 묻힘", "새 작업 = 새 세션"],
            ["<b>엉뚱한 파일 수정</b>", "예전 작업의 흔적이 남음", "/clear 또는 세션 분리"],
            ["<b>점점 느리고 비쌈</b>", "매 턴 전체 이력 재전송", "/compact · 요약 후 이어가기"],
        ]), "Ch3"),
        lab("3-1", "원문 도구 vs 요약 도구 · 컨텍스트", "Ch3",
            "같은 질문 · 도구가 돌려주는 양만 바꿔 컨텍스트 비교",
            ['시뮬레이터 ×20 · 결과 300건 넘게', '원문 도구로 「불합격 정리」 → /context', '새 대화 · 요약 도구로 같은 질문 → /context', '정확도 · 사용량 비교'],
            ['컨텍스트 사용량 전후 숫자', '도구 설계 원칙 한 줄'], files=labdir("steel_qc"), mine="내 업무 도구가 돌려주는 양 줄이기"),
        quest("3-1", "Ch3",
              ['시뮬레이터 속도 ×20 · 결과 300건 넘게', '<code>recent_results</code>(300건)만으로 「불합격 정리해」 → <code>/context</code> 기록', '새 대화 · <code>reject_summary</code>로 같은 질문 → <code>/context</code> 기록', '도구 설명문에 「원문은 꼭 필요할 때만」을 넣게 하기'],
              ['두 대화의 시간 · 토큰 차이', '도구가 돌려준 건수 = 누적 건수(<code>/api/state</code>)인가', '불합격 건수가 정답(<code>/api/truth</code>)과 같은가', '도구 설계 = 컨텍스트 설계'],
              "<code>solution/mcp_server.py</code> 의 recent_results · reject_summary"),
        measured("3-1", "Ch3", ["", "원문 도구", "요약 도구"], [
            ["<b>시간</b>", "222초", "26초"],
            ["<b>턴 · 입력 토큰</b>", "21턴 · 70.7만", "3턴 · 7.8만"],
            ["<b>첫 답</b>", "200건만 읽음 (누적 636건)", "200건만 읽음"],
            ["<b>도구 수정 후</b>", "—", "636건 · 불합격 34 · 근접 92 정답"],
        ], "도구가 돌려주는 양이 컨텍스트를 정함 · 건수는 사람이 확인"),
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
          "# Skill이 상황에 맞춰 자동 호출 · 직접 부르려면 이름을 말하기\n"
          "brainstorming                # 질문으로 설계 확정\n"
          "writing-plans                # 2~5분 단위 구현 계획\n"
          "subagent-driven-development  # 작업마다 Sub Agent · TDD · 리뷰")
    gs = ("git clone --single-branch --depth 1 \\\n"
          "  https://github.com/garrytan/gstack.git ~/.claude/skills/gstack \\\n"
          "  && cd ~/.claude/skills/gstack && ./setup\n\n"
          "/office-hours · /plan-eng-review   # 기획 · 설계 검토\n"
          "/review · /qa · /cso               # 리뷰 · QA · 보안")
    return chapter("Ch4", "공개 하네스 적용", {"Skill · 명령", "Sub Agent · 팀", "Hook · 권한"}, "남이 만든 하네스") + [
        stat("다른 회사의 하네스 ① 개발 자동화", "Ch4", table(["회사", "무엇을", "하네스 요소", "결과"], [
            ["<b>OpenAI Codex 팀</b>", "내부 제품을 손코딩 0줄로 · 5개월", "docs/ 지도 · 실행 계획 · 린터와 구조 테스트로 경계 강제 · 로그 · 지표 읽기", "약 100만 줄 · 손코딩 대비 약 1/10 시간"],
            ["<b>Stripe</b>", "Slack 요청 → CI 통과 PR", "격리 devbox · 하위 폴더별 규칙 파일 · 사내 MCP 도구 400+ 중 골라 줌 · CI 최대 2회", "주 1,000+ PR 병합 · 전부 사람 리뷰"],
            ["<b>Spotify</b>", "대규모 코드 마이그레이션", "컨테이너 작업 · 포맷 · 린트 MCP · LLM judge가 diff 검토 · 트레이스", "1,500+ PR 병합 · 60~90% 시간 절감"],
            ["<b>Airbnb</b>", "테스트 3.5천 파일 이전", "변환 → Jest → 린트 → 타입 검사 단계 · 오류를 넣어 재시도 · 병렬", "6주 (손으로 1.5년 예상) · 97% 자동 · 3% 사람"],
        ]) + note("공통", "좁고 반복되고 확인 가능한 일 · 결정적 검사(테스트 · 린트 · CI)를 루프 안에 · 마지막은 사람"),
             C_OAI_HE, C_STRIPE, C_SPOTIFY, C_AIRBNB),
        stat("다른 회사의 하네스 ② 규칙 · 구조 · 사내 확산", "Ch4", table(["회사", "무엇을", "하네스 요소", "결과"], [
            ["<b>배달의민족</b>", "프론트엔드 개발 · Cursor", "경로별 규칙 · Skill · 필요한 메타데이터만 넘기는 전처리 스크립트", "컨텍스트 평균 −96.5% · 도구 호출 4 → 1"],
            ["<b>Shopify</b>", "테스트 채점 · 생성 · 커버리지", "Roast: YAML · Markdown 워크플로에 결정적 단계와 Claude Code를 섞음", "「구조 없이 풀어 둔 AI는 큰 코드베이스에서 실패」"],
            ["<b>Rakuten</b>", "1,250만 줄 vLLM 기능 구현", "Claude Code 7시간 자율 작업", "기준 대비 정확도 99.9% · 출시 24일 → 5일 (고객 사례)"],
            ["<b>Anthropic 내부</b>", "엔지니어 132명 · 세션 20만 건 분석", "Claude Code 사내 사용", "업무 중 Claude 28% → 59% · 「완전히 맡길 수 있는 일은 0~20%」"],
        ]) + note("하네스의 두 축", "가이드(미리 알려 주기: 규칙 · Skill) + 센서(결과 확인: 테스트 · 린트 · 리뷰) — martinfowler.com"),
             C_WOOWA, C_SHOPIFY, C_RAKUTEN, C_ANTH_WORK, C_FOWLER),
        stat("Claude Code 밖의 하네스 요소", "Ch4", table(["요소", "무엇", "적용 예"], [
            ["<b>AGENTS.md</b>", "도구 공통 규칙 파일 표준 (Linux Foundation)", "오픈소스 6만+ 프로젝트 · Copilot · Codex · Cursor가 읽음"],
            ["<b>Copilot · Cursor 규칙</b>", "copilot-instructions.md · 경로별 .instructions.md · .cursor/rules", "배달의민족 경로별 규칙"],
            ["<b>MCP</b>", "사내 도구 · 데이터 연결 표준", "Stripe 사내 도구 400+"],
            ["<b>CI 연동</b>", "PR 리뷰 · 수정 봇", "Copilot 코드 리뷰 6천만 건 · GitHub 리뷰 5건 중 1건 이상 · claude-code-action"],
            ["<b>샌드박스</b>", "파일 · 네트워크 격리 · microVM", "Claude Code 샌드박스로 권한 확인 −84% · Stripe 격리 devbox"],
            ["<b>평가 · 레드팀</b>", "평가셋 · 공격 시나리오 자동 실행", "promptfoo (OpenAI 인수 2026.3) · Spotify LLM judge"],
            ["<b>관측</b>", "에이전트 실행 트레이스 · 로그", "Langfuse · Spotify MLflow 트레이스"],
            ["<b>프레임워크 · SDK</b>", "에이전트를 코드로 조립", "Claude Agent SDK · OpenAI Agents SDK · LangGraph · Google ADK"],
            ["<b>워크트리</b>", "병렬 에이전트 작업 분리", "Codex 앱 · Claude Code 모두 에이전트마다 워크트리"],
        ]), C_AGENTSMD, C_COPILOT_RV, C_SANDBOX, C_STRIPE),
        stat("하네스가 효과적일 때 · 아닐 때", "Ch4", two(
            table(["효과적일 때", "근거"], [
                ["<b>좁고 반복 · 확인 가능</b>", "Airbnb 97% 자동 · Spotify 60~90% 절감"],
                ["<b>긴 작업을 파일로 나눔</b>", "진행 기록 · 기능 목록 · 커밋 (Anthropic 장기 작업 하네스)"],
                ["<b>필요한 맥락만</b>", "배달의민족 컨텍스트 −96.5%"],
            ]),
            table(["효과가 없을 때", "근거"], [
                ["<b>익숙한 저장소의 숙련자</b>", "METR: 19% 느려짐 · 본인은 20% 빨라졌다고 느낌"],
                ["<b>구조 없이 풀어 둠</b>", "Shopify: 큰 코드베이스에서 실패"],
                ["<b>리뷰가 병목</b>", "Spotify: PR이 늘수록 리뷰가 새 병목"],
            ]))
             + note("DORA 2025", "AI는 강한 조직도 약한 조직도 증폭 · 확인 장치가 약하면 손해도 커짐"),
             C_AIRBNB, C_LONGRUN, C_METR, C_DORA),
        light("플러그인: 하네스 묶음", cards([
            ("하네스 미적용 모델", "매번 모델 재량 · 결과가 운에 흔들림", []),
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
        light("Superpowers 설치와 Skill", code("Claude Code", sp), "Ch4"),
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
        lab("4-1", "Superpowers로 실시간 대시보드", "Ch4",
            "공개 하네스의 설계 → 계획 → TDD 흐름으로 화면 하나 완성",
            ['Superpowers 설치', '실시간 불합격 대시보드 브레인스토밍', '계획 승인 → 구현 · 테스트', '시뮬레이터 ×5 · 화면이 바뀌는지'],
            ['대시보드 화면', '계획 · 테스트 파일'], files=labdir("steel_qc"), mine="내 업무 화면 하나를 같은 흐름으로"),
        quest("4-1", "Ch4",
              ['<code>/plugin</code> 으로 Superpowers 설치', '「시뮬레이터를 몇 초마다 읽어 불합격을 맨 위에 빨갛게 보여 주는 대시보드」를 브레인스토밍부터', '계획을 읽고 승인 → 구현 · 테스트까지', '판정은 LLM 없이 코드로 · 기존 판정 로직 재사용'],
              ['새 결과가 들어오면 화면이 바뀌는가', '불합격이 맨 위 · 빨간색', '계획 · 테스트 파일이 남았는가', '브라우저만으로 열리는가'],
              "Superpowers 설치는 앞 장 · 판정 로직은 <code>solution/judge.py</code>"),
        measured("4-1", "Ch4", ["단계", "결과"], [
            ["<b>대시보드 만들기</b>", "141초 · 10턴"],
            ["<b>판정 로직 테스트</b>", "674건 모두 정답과 일치"],
            ["<b>화면</b>", "687 → 691건 자동 갱신 · 불합격 맨 위 빨간 줄"],
        ], "LLM 없이 몇 초마다 갱신 · 판정 로직은 테스트로 확인"),
        bridge("다음: 멀티에이전트", "", "Ch4", "→ Ch5 멀티에이전트"),
    ]


# ── Ch5 멀티에이전트 ───────────────────────────────────
def ch5():
    return chapter("Ch5", "멀티에이전트 오케스트레이션", {"Sub Agent · 팀"}, "오케스트레이션") + [
        stat("여러 말, 한 마차", "Ch5",
             '<div class="phwide">' + photo("horse_team.jpg", "여러 말을 한 마차에", "마구로 묶여야 한 방향으로 끈다 = 멀티에이전트") + "</div>",
             PH_TEAM),
        light("단일 Agent의 한계", table(["한계", "증상"], [
            ["<b>컨텍스트 과부하</b>", "조사 · 구현 · 검증이 한 책상에 쌓임"],
            ["<b>자기 검증</b>", "자기가 쓴 답을 자기가 채점 → 관대함"],
            ["<b>순차 처리</b>", "독립 작업도 하나씩"],
        ]), "Ch5"),
        light("IT 팀에 비유한 멀티에이전트", flow([
            ("기획자", "요구 · 완료 기준"), ("개발팀장", "일 나누기 · 맡기기 · 취합"),
            ("개발팀원 여럿", "맡은 일만 · 각자 책상"), ("QA", "고치지 않고 판정"), ("팀장 보고", "결과 하나로")], hl=1)
            + table(["IT 팀", "멀티에이전트", "Claude Code에서"], [
                ["<b>기획자</b>", "사용자", "요청 · 완료 기준"],
                ["<b>개발팀장</b>", "메인 Agent (Supervisor)", "CLAUDE.md 나누기 규칙 · 지휘 Skill"],
                ["<b>개발팀원</b>", "Sub Agent", ".claude/agents/이름.md · 결과만 팀장에게"],
                ["<b>QA</b>", "검증 Agent", "verifier.md · 읽기 전용"],
                ["<b>업무 지시서</b>", "위임문", "목표 · 범위 · 반환 형식 · 완료 기준"],
                ["<b>팀원끼리 회의</b>", "Agent Teams", "구성원끼리 직접 소통 · 실험 기능"],
            ]), "Ch5"),
        light("오케스트레이션 패턴", viz("orchestration_patterns"), "Ch5"),
        light("Sub Agent 위임 구조", viz("subagent_fanout"), "Ch5"),
        light("Agent Teams 구조", viz("agent_teams") + note("상태", "실험 기능 · 환경 변수로 켬 · 위임으로 충분하면 Sub Agent"), "Ch5"),
        light("Sub Agent vs Agent Teams", table(["", "Sub Agent", "Agent Teams"], [
            ["<b>소통</b>", "부모 ↔ 자식 한 방향", "구성원끼리 직접 · 공유 작업 목록"],
            ["<b>맞는 일</b>", "독립 조사 · 검증 · 분업", "서로 결과를 반박 · 보완해야 할 때"],
            ["<b>비용</b>", "자식마다 컨텍스트", "구성원마다 세션 · 더 큼"],
            ["<b>통제</b>", "부모가 순서 강제", "작업 목록 · 규칙으로 조율"],
        ]), "Ch5"),
        light("위임문 4요소", table(["요소", "빠지면"], [
            ["<b>목표 · 완료 기준</b>", "어디서 멈출지 모름"],
            ["<b>입력 범위</b>", "필요 없는 것까지 읽음"],
            ["<b>허용 도구</b>", "권한 밖 작업"],
            ["<b>반환 형식</b>", "부모가 결과를 못 합침"],
        ]), "Ch5"),
        light("검증 Agent 분리", two(
            flow([("분류", "classifier"), ("응대", "domain"), ("검증", "verifier"), ("통과 → 답", "")], hl=2),
            flow([("추출", "extractor"), ("견적", "estimator"), ("검증", "verifier"), ("통과 → 결과", "")], hl=2))
              + note("verifier", "읽기 전용 · 근거 · 숫자 · 정책만 판정 · 고치지 않음"), "Ch5"),
        light("실행 타임라인", viz("timeline_lanes") + note("만드는 법", "실행 기록 → visualize.py → 타임라인 HTML · 실시간은 Agent Watch"), "Ch5"),
        light("실시간 대시보드: Agent Watch", '<img class="shot" src="img/agent_watch.png" alt="Agent Watch 화면">'
              + note("구성", "Hook → 로컬 서버 → 브라우저 · 메인 · Sub Agent 레인 · 에이전트별 토큰 · 효율 점검 · " + labdir("agent_watch")), "Ch5"),
        lab("5-1", "판정 · 조사 · 통보 Agent 팀", "Ch5",
            "한 Agent가 다 하던 일을 역할별로 · 실행 타임라인으로 확인",
            ['단일 Agent로 「오늘 불합격 처리해」', '조사 · 통보 · 검증 Agent 만들기', '같은 요청을 팀으로', 'Agent Watch로 타임라인 · 토큰'],
            ['역할별 Agent 3개', '단일 vs 팀 비교'], files=labdir("steel_qc"), mine="내 업무를 역할 셋으로 나누면"),
        quest("5-1", "Ch5",
              ['단일 Agent: 「오늘 불합격을 조사하고 고객 통보문까지 써 줘」', 'Agent 3개: 원인 조사 · 통보문 · 검증(숫자가 원문과 맞는지)', '같은 요청을 팀으로 · 메인은 나누고 합치기만', 'Agent Watch로 실행 타임라인'],
              ['Agent마다 쓴 도구가 역할에 맞는가', '통보문 숫자를 검증 Agent가 원문과 대조했는가', '단일 vs 팀 시간 · 토큰', '메인 컨텍스트가 덜 찼는가'],
              "<code>solution/dot_claude/agents/</code> · investigator · notifier · verifier"),
        measured("5-1", "Ch5", ["", "단일 Agent", "조사 · 통보 · 검증 팀"], [
            ["<b>시간</b>", "107초", "200초"],
            ["<b>비용</b>", "1×", "약 1.9×"],
            ["<b>불합격 3건 원인</b>", "정답", "정답"],
            ["<b>더 얻은 것</b>", "—", "검증 Agent가 근거 통계의 한계 지적"],
        ], "시간 · 비용 약 2배 · 대신 검증 한 단계"),
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
        light("캐싱의 원리", two(
            cards([("① 매번 처음부터 다시 읽음", "요청마다 도구 목록 · 시스템 · CLAUDE.md · 지난 대화 · 새 질문을 통째로 다시 보냄", []),
                   ("② 앞부분을 저장해 둠", "다음 요청의 앞부분이 글자 하나까지 같으면 저장본을 씀", []),
                   ("③ 저장본은 1/10 가격", "처음 저장할 때만 1.25배 · 그다음부터 0.1배", [])], 1),
            table(["요청 (입력 토큰 환산 예시)", "캐시 없음", "캐시 있음"], [
                ["<b>1</b> · 앞부분 2만 + 질문", "20,500", "25,500 (처음 저장)"],
                ["<b>2</b> · + 답 · 새 질문", "22,000", "약 3,900"],
                ["<b>3</b> · + 답 · 새 질문", "23,500", "약 4,100"],
                ["<b>합계</b>", "66,000", "<b>약 33,500</b>"],
                ["<b>요청 10번이면</b>", "약 27만", "<b>약 6.6만</b>"],
            ]))
              + note("비유", "매주 회의 자료 묶음 · 앞쪽 공통 자료가 그대로면 「지난주 그 자료」로 넘기고, 표지 날짜 한 글자만 바뀌어도 처음부터 다시 읽음")
              , "Ch6"),
        light("캐시가 깨지는 경우", viz("cache_prefix") + note("규칙", "고정 지침 · 도구 목록은 앞에, 바뀌는 입력은 뒤에 · 현재 시각 · 요청 ID를 앞에 넣지 않기"), "Ch6"),
        stat("캐시 · 배치 할인 규칙", "Ch6",
             big([("1.25", "배", "캐시 쓰기 (5분 · 1시간은 2배)"),
                  ("0.1", "배", "캐시 읽기 (Opus · Sonnet 5.5는 0.05배)", True),
                  ("1", "번", "한 번만 다시 읽어도 캐시가 이득"),
                  ("50", "%", "배치 API 할인 (입력 · 출력 모두)")], 4)
             + note("기억할 것", "캐시 기본 수명 5분 · 쓸 때마다 갱신 · 앞부분이 1글자라도 바뀌면 새로 씀"),
             D_CACHE, D_PRICE),
        stat("effort별 비용과 점수", "Ch6",
             hbars([("low", 33, False, "비용 ⅓ · −8점"), ("medium (기본)", 70, False, "비용 70% · −2.5점"),
                    ("high", 100, False, "기준"), ("xhigh", 250, False, "비용 2.5배 · +1.4점")], top=260,
                   title="Opus 5.5 · SWE-bench Pro · high 대비 비용과 점수")
             + hbars([("전부 high", 29, False, "95.3% · $0.29"), ("low 먼저 → 실패만 high", 17, True, "약 97% · $0.17")], top=32,
                     title="과제 1건당 비용 · 통과율")
             + note("많이 생각시킨다고 늘 좋진 않다", "Sonnet 5.5: max 46.2% < xhigh 52.1% · Sub Agent 남발 · 범위 밖 수정"),
             D_OPT, D_EFFORT, A_SON55),
        stat("출력 줄이기: caveman", "Ch6", two(
            code("설치", "/plugin marketplace add JuliusBrussee/caveman\n/plugin install caveman@caveman"),
            ba_like2("좋은 질문이에요! 이 문제는 여러 가지 원인이 있을 수 있는데요, 우선 VPN 클라이언트가…", "원인: 인증서 만료. 조치: 재발급 (IT-3)."))
             + note("제작자 발표", "같은 답 63 → 20토큰 예시 · 세션 전체 입력 −33.2% (54회) · 실습 6-1에서 직접 재 보기"),
             D_CAVEMAN),
        stat("코드량 줄이기: ponytail", "Ch6", code("설치", "/plugin marketplace add DietrichGebert/ponytail\n/plugin install ponytail@ponytail")
              + note("방식", "요청한 것만 · 가장 단순한 해법부터 · 표준 라이브러리 먼저")
              + note("제작자 발표", "코드 −53% · 시간 −41% · 비용 −26% · 토큰 −45% (Opus 5.5 · 39과제 × 5회) · 턴마다 비용 기록을 홈 폴더에 남김"),
             D_PONYTAIL),
        stat("공식 사례로 본 절감 폭", "Ch6",
             hbars([("같은 점수 · 모델 · effort 조정", 81, True, "$1.19 → $0.22"), ("남은 시간 알려 주기", 60, False, "비용 −60%"),
                    ("도구 검색 (도구 502개)", 45, False, "$1.02 → $0.56"), ("오래된 도구 결과 정리", 39, False, "−39%"),
                    ("코드로 도구 호출 묶기", 38, False, "입력 −38%"), ("압축 (긴 작업)", 32, False, "−32%"), ("MCP 도구 지연 로딩", 20, False, "−20%")],
                   top=100, title="Opus 5.5 세대 · Anthropic 측정 (2026.9) · 비용 절감률")
             + note("주의", "짧은 작업에 컨텍스트 편집을 켜면 오히려 +74% · 측정은 「방향」이지 보장이 아님"),
             D_OPT, D_PTC),
        light("하네스 전후 토큰", viz("token_meter"), "Ch6"),
        light("토큰을 더 써야 하는 상황", table(["상황", "이유"], [
            ["<b>검증 · 리뷰</b>", "틀린 답의 비용이 토큰보다 큼"],
            ["<b>E2E 테스트</b>", "실제 흐름 확인 · 핵심 흐름에만"],
            ["<b>고위험 도메인</b>", "안전 · 계약 · 인사는 큰 모델 + 사람"],
        ]) + note("원칙", "토큰이 아니라 「완료된 작업 1건당 비용」으로 판단"), "Ch6"),
        light("플러그인 없이 바로 쓰는 절감법", table(["방법", "어떻게", "줄어드는 곳"], [
            ["<b>① 일이 바뀌면 새로</b>", "/clear", "앞 대화 재전송 · 새로 시작은 비용 0"],
            ["<b>② 긴 세션 요약</b>", "/compact 남길 것", "쌓인 대화 · 도구 결과"],
            ["<b>③ CLAUDE.md 짧게</b>", "긴 매뉴얼은 Skill · 참고 파일로", "매 요청 고정 입력"],
            ["<b>④ 찾아서 읽기</b>", "통째 Read 대신 Grep · 줄 범위", "도구 결과"],
            ["<b>⑤ MCP는 필요한 것만</b>", "안 쓰는 서버 끄기 · 도구 검색 (기본 켜짐)", "도구 정의"],
            ["<b>⑥ 모델 나누기</b>", "분류 · 검색 Sub Agent는 model: haiku", "단가"],
            ["<b>⑦ effort 조절</b>", "low 먼저 → 실패만 high", "생각 토큰"],
            ["<b>⑧ 캐시 지키기</b>", "앞부분 고정 · 시각 · ID는 뒤에", "새 입력 → 캐시 읽기 (0.1배)"],
            ["<b>⑨ 출력 줄이기</b>", "「결과는 파일로 · 대화엔 3줄」", "출력"],
            ["<b>⑩ 로그는 Hook으로 거르기</b>", "ERROR 줄만 넘기기", "수만 → 수백 토큰"],
        ]) + note("먼저 재기", "/context로 큰 것부터 · 줄인 뒤 품질은 평가로"), "Ch6"),
        lab("6-1", "LLM은 예외만 · 토큰 비교", "Ch6",
            "반복 판정은 코드로, LLM은 이상 건만 · 같은 결과에 토큰이 얼마나 줄어드나",
            ['LLM이 300건 직접 판정 → 토큰', '코드 판정 요약 도구 → 토큰', '이상 건만 Agent에게 → 토큰', '결과 · 토큰 비교'],
            ['토큰 실측표', '「코드로 할 일 · LLM에 맡길 일」 한 줄'], files=labdir("steel_qc"), mine="내 업무에서 코드로 돌릴 반복 판정"),
        quest("6-1", "Ch6",
              ['「최근 300건 판정해 줘」 · <code>recent_results</code>만 (LLM이 직접 판정)', '같은 질문 · <code>reject_summary</code> (코드가 판정 · LLM은 요약)', '이상 건만 조사 Agent에게', 'Agent Watch로 세 번의 토큰'],
              ['불합격 건수가 <code>/api/truth</code>와 같은가', '입력 · 출력 토큰 차이', 'LLM 직접 판정에서 틀린 건', '어느 단계가 코드로 충분한가'],
              "Agent Watch 는 Ch5 · 판정 코드는 <code>solution/judge.py</code>"),
        measured("6-1", "Ch6", ["", "LLM이 300건 판정", "코드 판정 · LLM은 예외만"], [
            ["<b>시간</b>", "248초", "31초"],
            ["<b>출력 토큰</b>", "21,429", "1,725"],
            ["<b>비용</b>", "1×", "0.2×"],
            ["<b>불합격 18건</b>", "정답", "정답"],
        ], "정답은 같고 비용 1/5 · 규칙이 분명한 판정은 코드로"),
        bridge("다음: 평가 · HITL", "", "Ch6", "→ Ch7 평가 · HITL"),
    ]


def ba_like2(before, after):
    return f'''<div class="ba">
  <div class="b"><div class="lab">기본</div><div class="q">{before}</div></div>
  <div class="arr">→</div>
  <div class="a"><div class="lab">caveman</div><div class="q">{after}</div></div>
</div>'''


# ── Ch7 평가 · HITL ──────────────────────────────
def ch7():
    judge = ("너는 채점자다. 1~5점, JSON으로만 답한다.\n"
             "[입력] {input}\n[출력] {output}\n[근거] {source}\n\n"
             "- 정확도: 근거와 맞는가\n"
             "- 근거 충실도: 근거에 없는 내용을 만들었는가 (만들면 1점)\n"
             "- 정책: 약속하면 안 되는 것 · 형식 위반\n"
             '{"accuracy": n, "grounded": n, "policy": n, "reason": "..."}')
    return chapter("Ch7", "평가 · HITL", {"평가 · 비용"}, "평가") + [
        light("HITL · 평가는 사람의 몫", flow([
            ("사람", "잘한 것의 기준"), ("에이전트", "실행"), ("자동 확인", "테스트 · 채점 · judge"),
            ("사람", "판정 · 승인"), ("사람", "기준 고치기")], hl=3)
            + table(["", "사람이 하는 일", "자동으로 맡기는 일"], [
                ["<b>기준</b>", "무엇이 잘한 것인지 · 합격선", "—"],
                ["<b>채점</b>", "애매한 건 · 표본을 직접 읽기", "정답 비교 · 형식 · 숫자 대조"],
                ["<b>판정</b>", "합격 · 불합격 · 배포 여부", "점수 · 차이 보고"],
                ["<b>개선</b>", "무엇을 고칠지 결정", "평가 문항 다시 돌리기"],
            ]) + note("원칙", "자동 채점은 사람이 볼 곳을 좁혀 주는 도구 · 최종 판정은 사람"), "Ch7"),
        light("사람이 개입하는 지점", table(["지점", "사람이 하는 일", "하네스에서"], [
            ["<b>시작 전</b>", "기준 · 합격선 정하기", "인터뷰 · 평가 문항"],
            ["<b>계획 뒤</b>", "계획 승인 · 범위 조정", "승인 파일 없으면 Hook이 구현 차단 (Ch8)"],
            ["<b>위험 행동 직전</b>", "허락 · 거절", "Hook · 권한 ask (Ch2)"],
            ["<b>밖으로 나가기 전</b>", "발송 · 배포 확인", "초안까지만 · 발송은 사람"],
            ["<b>끝난 뒤</b>", "결과 판정 · 다음 개선", "채점 결과를 보고 사람이 결정"],
        ]) + note("HITL", "Human-in-the-loop · 사람이 흐름 안에서 확인 · 승인 · 판정"), "Ch7"),
        stat("공개 벤치마크의 포화와 결함", "Ch7",
             hbars([("Verified · 문제 있는 문항", 59.4, False, "59.4%"), ("Pro · 고장 난 과제", 30, False, "약 30%"),
                    ("Pro · Opus 5.5 점수", 89.9, True, "89.9%")], top=100, title="SWE-bench · OpenAI 감사 · Anthropic 시스템 카드 (2026)")
             + hbars([("Terminal-bench 2.1", 89.4, False, "89.4%"), ("Terminal-bench 4.0", 19.1, True, "19.1%")], top=100,
                     title="같은 모델(Gemini 3.8 Flash), 벤치마크 버전만 다름")
             + note("그래서", "남의 점수보다 우리 업무 평가셋"),
             OAI_SWEV, OAI_SWEP, SC_OPUS55, GEM38),
        ill("scenes_extra", "calculator_test", "left40", "정답셋 평가", ["평가셋 = 정답 · 허용 범위가 있는 대표 과제"]),
        stat("평가셋 시작 규모와 기준", "Ch7",
             big([("20~50", "개", "실제 실패에서 뽑은 첫 평가 과제", True),
                  ("0", "%", "통과율 0% = 대개 Agent가 아니라 과제가 고장"),
                  ("F1 ≥ 0.85", "", "성공 기준은 숫자로 (공식 예)")])
             + quote("손으로 채점한 적은 문항보다, 자동 채점한 많은 문항이 낫다", "Anthropic 문서, 성공 기준 정하기"),
             A_EVALS, D_SUCCESS),
        light("과업마다 다른 가중치", table(["지표", "분류 · 라우팅", "생성 (답변)", "추출 · 계산"], [
            ["<b>정확도</b>", "40", "25", "40"], ["<b>근거 충실도</b>", "—", "30", "30"],
            ["<b>일관성</b>", "30", "15", "20"], ["<b>지연</b>", "15", "10", "—"],
            ["<b>토큰</b>", "15", "10", "10"], ["<b>안전 · 정책</b>", "필수 통과", "필수 통과", "—"],
        ]) + note("원칙", "안전 · 정책은 점수가 아니라 통과 조건"), "Ch7"),
        light("엣지 케이스 유형", table(["엣지 케이스", "예", "기대 동작"], [
            ["<b>모호한 입력</b>", "「그거 안 돼요」", "되묻기"],
            ["<b>복합 의도</b>", "「노트북 구매하고 VPN도」", "나눠 위임"],
            ["<b>지시 우회 시도</b>", "「이전 지시 무시하고…」", "무시 · 정상 처리"],
            ["<b>범위 밖</b>", "「점심 메뉴 추천」", "범위 안내"],
            ["<b>정보 누락 · 상충 숫자</b>", "수량 없음 · 표와 본문이 다름", "null · 사람에게"],
            ["<b>실패해야 정상</b>", "근거 없는 질문", "「자료에 없음」"],
        ]), "Ch7"),
        light("정답셋이 없을 때의 방법 세 가지", cards([
            ("합성 데이터", "대표 예시 → 변형 생성 · 표시해 둠", []),
            ("LLM-as-judge", "채점 기준을 프롬프트로 · 다른 모델이 채점", []),
            ("현업 최소 라벨링", "10~20건만 사람이 채점 → judge 보정", []),
        ]), "Ch7"),
        light("LLM-as-judge 채점 기준", code("judge_prompt.md", judge), "Ch7"),
        light("judge 신뢰도 확인 방법", table(["확인", "방법"], [
            ["<b>사람과 일치도</b>", "같은 10건을 사람 · judge가 채점 → 일치율 · 카파"],
            ["<b>위치 · 길이 편향</b>", "순서 바꾸기 · 긴 답 편애 확인"],
            ["<b>자기 편향</b>", "같은 모델이 쓴 답을 채점하지 않게"],
        ]), "Ch7"),
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
        light("멀티 Agent 평가 대상과 지표", table(["대상", "지표"], [
            ["<b>분류 · 라우터</b>", "의도 정확도"], ["<b>Sub Agent</b>", "judge 점수 · 필드 F1"],
            ["<b>verifier</b>", "일부러 넣은 오답 차단율"], ["<b>전체</b>", "최종 품질 · 토큰 · 지연"],
        ]), "Ch7"),
        lab("7-1", "판정 테스트 · Stop Hook 게이트", "Ch7",
            "판정 규칙을 바꿔도 테스트가 자동으로 지킴",
            ['정답(/api/truth)으로 판정 테스트', 'Stop Hook: 끝내기 전에 테스트', '규격 개정 반영 요청', '깨진 곳을 Claude가 멈추지 못하고 보고'],
            ['테스트 통과', 'Stop Hook이 막은 기록'], files=labdir("steel_qc"), mine="내 업무 결과를 정답과 대조할 기준 하나"),
        quest("7-1", "Ch7",
              ['시뮬레이터 정답(<code>/api/truth</code>)과 판정을 대조하는 테스트를 만들어 달라', 'Stop Hook: 끝내기 전에 테스트를 돌리고 실패면 계속하게', '「HS-275 인장강도 상한이 570으로 개정됐어 · 판정에 반영해 줘」 → 무슨 일이 일어나는지', '규격 파일(<code>specs.json</code>) 수정은 PreToolUse로 막기'],
              ['개정 전 테스트 전부 통과', '개정 후 깨진 코일 · 이유를 Claude가 표로 보고', 'Stop Hook 때문에 실패 상태로 끝나지 않음', '정답지까지 바꿀지는 사람이 결정'],
              "<code>solution/tests/test_judge.py</code> · <code>solution/hooks/test_gate.py</code> · <code>settings_stop.json</code>"),
        measured("7-1", "Ch7", ["요청", "결과"], [
            ["<b>테스트 + Stop Hook 만들기</b>", "186초"],
            ["<b>「근접 기준 5%로」</b>", "CLAUDE.md 근거로 거절 · 게이트까지 안 감"],
            ["<b>「HS-275 인장강도 상한 570 개정」</b>", "테스트 6개 실패 · 537~566 코일 · Stop Hook이 종료 막음"],
            ["<b>Claude의 보고</b>", "정답지와 충돌 · 테스트를 고치지 않고 사람 결정 요청"],
        ], "규칙 변경의 파급은 테스트가 잡고 · 반영 여부는 사람이"),
        light("HITL로 하네스를 키우는 고리", flow([
            ("실행", "Agent가 일함"), ("사람 판정", "맞나 · 넘었나"), ("기록", "틀린 사례 · 이유"),
            ("하네스에 반영", "원인별 부품"), ("다시 실행", "같은 평가 문항")], hl=1)
            + table(["사람이 본 것 (이 강의 실습)", "원인", "하네스에 반영"], [
                ["<b>1-1</b> 「지급 보류」까지 Agent가 결정", "결정 범위가 안 정해짐", "CLAUDE.md 한 줄 · 결정은 담당자"],
                ["<b>3-1</b> 압축 뒤 대화로 준 규칙이 사라짐", "규칙이 파일에 없음", "CLAUDE.md · /compact 지시"],
                ["<b>7-1</b> 테스트 실패를 남긴 채 「완료」", "완료 기준이 부탁뿐", "Stop Hook으로 강제"],
                ["<b>7-1</b> 테스트 기대값을 Agent가 바꿈", "근거 확인이 필요", "평가 문항 추가 · 사람 확인"],
            ])
              + note("핵심", "판정 기록이 쌓이면 평가셋이 됨 · 같은 실수는 하네스가 막고 사람은 새로운 실수만 봄"), "Ch7"),
        light("운영: 실패 유형 정의", table(["실패", "판정", "대응"], [
            ["<b>틀린 답</b>", "judge · 정답 비교", "평가셋에 추가"],
            ["<b>근거 없는 답</b>", "숫자 · 조항 대조", "차단 · 사람에게"],
            ["<b>정책 위반</b>", "금지 표현 · 권한", "Hook으로 즉시 차단"],
            ["<b>멈춤 · 폭주</b>", "턴 · 토큰 한도", "중단 · 알림"],
        ]), "Ch7"),
        light("운영 장치", table(["장치", "방법"], [
            ["<b>근거 로깅</b>", "PostToolUse · SubagentStop Hook으로 한 줄씩"],
            ["<b>사람 확인 (HITL)</b>", "확신 낮음 · 되돌릴 수 없음 · 고위험 도메인"],
            ["<b>롤백</b>", "하네스를 git으로 버전 관리 → 이전 태그로"],
            ["<b>재시도</b>", "일시 오류만 · 최대 횟수 · 대기 늘리며"],
            ["<b>단계적 배포</b>", "일부 사용자 → 지표 확인 → 전체"],
        ]), "Ch7"),
        bridge("다음: 내 하네스 만들기", "", "Ch7", "→ Ch8 사전 과제 주제로"),
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
    return chapter("Ch8", "내 하네스 만들기", {p[0] for p in PARTS}, "전체") + [
        stat("AI에게 일 시키기 전 계획", "Ch8", two(
            table(["계획 없이 바로 시키면", "계획을 먼저 세우면"], [
                ["한 번에 다 만들려다 중간에 흐트러짐", "작은 작업 단위 · 순서가 정해짐"],
                ["다 되기 전에 「완료」 선언", "완료 기준 · 테스트가 먼저 정해짐"],
                ["요구를 잘못 이해한 채 끝까지 감", "설계 단계에서 사람이 바로잡음"],
                ["다시 만들기 · 토큰 낭비", "승인한 계획대로 · 범위 밖 작업 없음"],
            ]),
            '<div>' + flow([("탐색", "읽기만"), ("계획", "질문 · 설계"), ("사람 승인", "범위 · 기준"), ("구현", "작게 · 테스트")], hl=2)
            + table(["계획 도구", "어떻게"], [
                ["<b>플랜 모드</b>", "Shift+Tab · 읽기만 하며 계획 → 승인 후 실행"],
                ["<b>Superpowers</b>", "brainstorming → writing-plans"],
                ["<b>메타 하네스</b>", "인터뷰 → spec.md → APPROVED"],
            ]) + '</div>')
             + note("근거", "Anthropic: 한 번에 다 하려 함 · 일찍 완료 선언이 긴 작업의 주된 실패 · Shopify: 구조 없이 풀어 둔 AI는 실패"),
             C_LONGRUN, C_SHOPIFY, D_BP),
        light("하네스 브레인스토밍", table(["질문", "왜 묻나", "예 · 주간 설비 점검 보고서"], [
            ["<b>① 어떤 업무 · 얼마나 자주</b>", "반복되지 않으면 하네스보다 그때그때 요청", "매주 월요일 · 팀장에게 보고"],
            ["<b>② 무엇이 들어오나</b>", "입력 형식이 Skill의 첫 단계", "점검 기록 CSV · 점검 기준 문서"],
            ["<b>③ 무엇이 나가야 하나</b>", "결과 양식 · 위치 → CLAUDE.md · Skill", "요약 3줄 · 정비 요청 · 경고 표"],
            ["<b>④ 판단 기준 · 사내 규칙</b>", "모델이 모르는 회사 기준 → Skill", "7.0 초과면 경고 · 이틀 연속이면 정비 요청"],
            ["<b>⑤ 절대 하면 안 되는 것</b>", "어기면 사고 → Hook", "원본 기록 수정 · 외부 메일 발송"],
            ["<b>⑥ 사람이 꼭 볼 곳</b>", "HITL 지점 → 승인 · 판정", "발송 전 팀장 확인"],
            ["<b>⑦ 잘했다의 기준 · 자주 나는 실수</b>", "평가 문항 · 엣지 케이스", "누락 0건 · 빈 값을 0으로 읽는 실수"],
        ]) + note("다음", "답이 곧 하네스 재료 · 메타 하네스의 인터뷰가 이 질문을 대신 던진다"), "Ch8"),
        light("하네스 만드는 순서", flow([
            ("① 브레인스토밍", "업무 · 막을 것 · 잘했다의 기준"),
            ("② CLAUDE.md", "모든 업무 공통 원칙 · 짧게"),
            ("③ Skill", "업무 하나에 하나 · 절차 · 양식"),
            ("④ Hook · 권한", "어기면 사고인 것만 차단"),
            ("⑤ 검증 Agent", "숫자 · 발송 등 틀리면 곤란한 일"),
            ("⑥ 평가 → 고치기", "과거 사례 5~10건으로 채점"),
        ], hl=2) + table(["단계", "office_work에서 한 일", "결과"], [
            ["<b>② CLAUDE.md</b>", "결과는 out/과제/ · 원본 수정 금지 · 근거 표기", "파일로 남김 12/12 (하네스 미적용 2/12)"],
            ["<b>③ Skill</b>", "spec-quote: 「수량 불일치면 견적 보류」", "회사 규칙대로 보류 (하네스 미적용 쪽은 금액 계산 2/2)"],
            ["<b>④ Hook</b>", "inputs/ 수정 · 메일 발송 · 외부 전송 차단", "원본 보존 12/12"],
            ["<b>⑥ 평가</b>", "grade.py · 과제 6개 정답 검사", "과제 6개 110/114 · 40건 82/82 · 시간 · 토큰도 함께"],
        ]) + note("하네스 ≠ Skill", "Skill · CLAUDE.md는 부탁(확률) · Hook은 강제 · 평가는 확인 → 셋이 붙어야 하네스"), "Ch8"),
        light("메타 하네스란", flow([
            ("인터뷰", "업무 · 입력 · 금지"), ("설계", "유형 · 필요한 부품만"), ("사람 승인", "APPROVED"),
            ("생성 · 검토", "하네스 파일"), ("시험", "미적용 vs 적용"), ("사람 판정", "고치기")], hl=2)
            + table(["", "범용 하네스", "메타 하네스가 만든 하네스"], [
                ["<b>규칙</b>", "누구에게나 맞는 일반 규칙", "인터뷰에서 나온 내 업무 규칙만"],
                ["<b>부품</b>", "전부 다", "필요한 것만 · 넣지 않은 이유도 기록"],
                ["<b>막을 것</b>", "rm -rf · .env 같은 공통", "내 업무에서 사고 나는 지점"],
                ["<b>평가</b>", "없음", "내 예시 입력 3 + 엣지 케이스 2"],
                ["<b>재사용</b>", "한 번 설치", "새 업무 · 새 상황마다 다시 인터뷰"],
            ]) + note("주제에 따라", "업무 처리 주제 → 메타 하네스로 업무 하네스 · 개발 주제 → Superpowers"), "Ch8"),
        light("메타 하네스 구조", two(
            '<div class="ctree">' + code("폴더 구조", 'meta_harness/\n├── CLAUDE.md                 순서 · 원칙\n├── templates/                유형별 예시 (업무 · 개발)\n├── docs/&lt;하네스 이름&gt;/\n│   ├── interview.md          인터뷰 답\n│   ├── spec.md             설계안\n│   └── APPROVED              사람만 만듦\n├── out/&lt;하네스 이름&gt;/          만들어진 하네스\n└── .claude/\n    ├── skills/interview/     질문 → interview.md\n    ├── skills/spec/        유형 · 부품 → spec.md\n    ├── skills/build/         하네스 파일 생성\n    ├── skills/try/           미적용 vs 적용 시험\n    ├── agents/harness-reviewer.md  지어낸 규칙 검토\n    └── hooks/guard.py · settings.json  승인 전 생성 차단') + "</div>",
            table(["단계", "담당", "결과"], [
                ["<b>① 인터뷰</b>", "interview Skill · 사람이 답함", "interview.md"],
                ["<b>② 설계</b>", "spec Skill · templates/ 참고", "spec.md · 유형 · 부품"],
                ["<b>③ 승인</b>", "<b>사람</b> · APPROVED", "승인 전 생성은 Hook이 차단"],
                ["<b>④ 생성</b>", "build Skill", "대상 폴더에 하네스"],
                ["<b>⑤ 검토</b>", "harness-reviewer", "지어낸 규칙 · 빠진 차단"],
                ["<b>⑥ 시험</b>", "try Skill", "미적용 vs 적용 비교표"],
                ["<b>⑦ 판정</b>", "<b>사람</b>", "합격 · 고칠 점"],
            ])), "Ch8"),
        light("메타 하네스를 만드는 요청문", '<div class="ptall">' + code("labs/meta_harness 에서 · 이렇게 말하면 됨", '이 폴더에 「하네스를 만들어 주는 하네스」를 만들어 줘.\n\n내가 어떤 업무를 말하면, 먼저 질문을 한 번에 하나씩(최대 일곱 개) 해서\n업무 · 입력 · 결과물 · 판단 기준 · 하면 안 되는 것 · 사람이 확인할 곳 · 잘했다의 기준을 파악해 줘.\n그걸로 설계안(docs/&lt;이름&gt;/spec.md)을 만들어 보여 주고, 내가 docs/&lt;이름&gt;/APPROVED 를 만들 때까지 기다려.\n\n승인하면 그 업무에 꼭 필요한 부품만 골라 하네스 파일을 만들고, 검토 담당 Agent가 지어낸 규칙이 없는지 본 다음,\n하네스 없이 · 있게 돌려서 비교표를 보여 줘. 판정은 내가 할게.\n승인 전에는 docs/ 밖에 아무것도 못 쓰게 Hook으로 막아 주고, 유형별 예시는 templates/ 를 참고해.\n다 만들면 만든 파일과 역할을 표로 보여 줘.') + "</div>"
              + note("내 말로", "문장은 바꿔도 됨 · 순서 · 사람 승인 · 승인 전 차단만 들어가면"), "Ch8"),
        light("TDD (테스트 주도 개발)", two(
            '<div>' + flow([("① 빨강", "실패하는 테스트 먼저"), ("② 초록", "통과할 만큼만 구현"), ("③ 정리", "테스트는 그대로 통과")], hl=0)
            + table(["에이전트에게 좋은 이유", ""], [
                ["<b>완료 기준이 코드</b>", "「다 됐다」를 테스트가 판정"],
                ["<b>스스로 확인</b>", "고칠 때마다 node --test"],
                ["<b>나눠도 안전</b>", "합칠 때 깨진 곳이 바로 보임"],
                ["<b>사람은 사례를 검토</b>", "코드 대신 테스트 사례를 읽고 승인"],
            ]) + '</div>',
            '<div class="ctree">' + code("① 테스트 먼저 → 실패 · ② 구현 → 통과", '// test/calc.test.js\nimport { test } from "node:test";\nimport assert from "node:assert";\nimport { total } from "../src/calc.js";\n\ntest("총액은 10원 미만 절사", () => {\n  assert.equal(total(12345), 12340);\n});\n\n// src/calc.js\nexport const total = (n) =>\n  Math.floor(n / 10) * 10;') + '</div>'), "Ch8"),
        stat("Superpowers로 개발하기", "Ch8", two(
            table(["Superpowers Skill", "하는 일", "사람이 할 일"], [
                ["<b>brainstorming</b>", "질문으로 요구 정리 · 설계를 나눠 보여 줌", "<b>설계 승인</b>"],
                ["<b>(화면이 있으면)</b>", "DESIGN.md로 화면 규칙 먼저 (Ch2)", "색 · 화면 규칙 확인"],
                ["<b>using-git-worktrees</b>", "새 브랜치 · 워크트리 · 테스트 기준선", "—"],
                ["<b>writing-plans</b>", "2~5분 단위 작업 · 파일 경로 · 확인 방법", "<b>계획 승인</b>"],
                ["<b>subagent-driven-development</b>", "작업마다 새 Sub Agent · TDD · 스펙 리뷰 → 코드 리뷰", "—"],
                ["<b>finishing-a-development-branch</b>", "테스트 확인 · 병합 · PR 정리", "<b>최종 판정</b>"],
            ]),
            '<div class="ptall">' + code("my_tool 에서 붙여 넣기", '〈만들 웹 앱 한 줄〉 을 만들고 싶어. superpowers 의 brainstorming 부터 시작해 줘.\n화면이 있으니 계획 전에 DESIGN.md 를 먼저 만들고, 화면은 DESIGN.md 를 따르게 해 줘.\n예시 데이터는 ../samples/〈분야〉/ 를 써.') + "</div>")
              + note("직접 만들지 않는 이유", "개발 멀티에이전트 흐름은 공개 하네스가 이미 잘 갖춤 · 우리는 설치하고 승인 지점을 지키는 데 집중"),
             C_SUPERPOWERS),
        light("Superpowers 실행 타임라인", viz("dev_timeline")
              + note("읽는 법", "주황 = 사람 (설계 · 계획 승인 · 판정) · 작업마다 새 Sub Agent가 테스트 먼저 → 구현 · 리뷰는 스펙 → 코드 품질 두 단계"), "Ch8"),
        lab("8-1", "메타 하네스로 내 하네스 만들기", "Ch8",
            "사전 과제 주제로 · 업무 처리면 메타 하네스로 업무 하네스, 개발이면 Superpowers · 판정은 사람",
            ["메타 하네스 만들기 (요청문)", "사전 과제 주제 · 샘플 데이터로 인터뷰 → spec.md", "설계 검토 → APPROVED 직접 (사람 승인)",
             "생성 · 검토 · 하네스 미적용 vs 적용 시험", "개발 주제면 Superpowers로 (설계 · 계획 승인 · 화면은 DESIGN.md 먼저)", "사람 판정 → 패들릿 · 1~2분 발표"],
            ["내 하네스 폴더 · 비교표", "사람 판정 · 패들릿 게시"], files=labdir("meta_harness") + " · " + labdir("samples"),
            mine="사전 과제: 반복 업무 하나 + 결과 확인 방법"),
        *labkit('8-1', 'Ch8'),
        stat("오래 일하는 루프 하네스", "Ch8", two(
            table(["오래 일할 때 생기는 문제", "하네스 장치"], [
                ["<b>한 번에 다 하려 함</b>", "기능 목록 · 한 번에 하나만"],
                ["<b>일찍 「다 했다」 선언</b>", "passes 는 테스트 통과 뒤에만 · JSON이라 덜 고침"],
                ["<b>진행이 사라짐</b>", "진행 기록 파일 + git 커밋"],
                ["<b>컨텍스트가 쌓여 흐려짐</b>", "매번 새 세션 · 기록에서 이어받기"],
                ["<b>끝없이 돎</b>", "최대 횟수 · 허용 도구 · 비용 상한"],
            ]),
            '<div>' + flow([("기록 읽기", "progress · git log"), ("하나 고르기", "passes: false"), ("TDD", "테스트 → 구현"), ("기록 · 커밋", "passes: true")], hl=2)
            + note("반복", "모두 통과하거나 최대 횟수까지 · 사람은 끝난 뒤 판정") + '</div>')
             + note("근거", "Anthropic 장기 작업 하네스 (기능 목록 JSON · 진행 기록 · 커밋) · Ralph 루프 (매번 새 컨텍스트 · 한 번에 하나)"),
             C_LONGRUN, HUNTLEY),
        stat("루프를 돌리는 세 가지 방법", "Ch8", '<div class="ptall">' + code("예", '# ① 바깥 스크립트 (매번 새 세션)\nnode loop.mjs 8\n\n# ② Stop Hook 루프 (한 세션 · 플러그인)\n/ralph-loop "features.json 을 모두 통과시켜" --max-iterations 20 --completion-promise "ALL PASS"\n\n# ③ 정해진 간격 반복 (감시용)\n/loop 10m 빌드 상태 확인') + "</div>"
             + table(["방법", "특징", "주의"], [
                 ["<b>① 바깥 스크립트</b>", "while 루프로 claude -p 반복 · 매번 컨텍스트 깨끗", "--allowedTools 로 허용 도구만"],
                 ["<b>② Stop Hook</b>", "끝내려 할 때 Hook이 막고 같은 요청을 다시 (공식 ralph-loop 플러그인)", "--max-iterations 꼭 · 8번 연속 막으면 무시됨"],
                 ["<b>③ /loop</b>", "정해진 간격으로 같은 요청 · 7일 뒤 만료", "개발보다 감시 · 점검용"],
             ]), D_RALPH, D_HOOKS_STOP, D_LOOPCMD, D_HEADLESS),
        lab("8-2", "루프 하네스 · 기능 다섯 개 쌓기", "Ch8",
            "사람 없이 기능을 하나씩 구현 · 테스트 통과까지",
            ['features.json · PROMPT.md · progress.md 준비', 'python loop.py 5', '세션마다 기능 하나 · 테스트 · 커밋', 'git log · progress.md 확인'],
            ['기능 5개 passes', '커밋 5개'], files=labdir("steel_qc"), mine="내 업무 기능 목록을 features.json으로"),
        quest("8-2", "Ch8",
              ['<code>solution/</code> 의 CLAUDE.md · features.json · PROMPT.md · progress.md · loop.py 를 폴더 맨 위로 복사', '<code>git init</code> 후 첫 커밋', '<code>python loop.py 5</code>', '실패하면 progress.md 를 읽고 원인 보고'],
              ['passes 가 하나씩 true', '커밋마다 테스트 통과', 'Hook · 테스트가 루프를 멈춘 적', '세션마다 토큰 · 시간'],
              "<code>solution/loop.py</code> · 루프는 <code>claude -p</code> 를 로그인 계정으로 실행"),
        stat("하네스는 사람이 키운다", "Ch8",
             '<div class="eqn">'
             '<div class="eq-c"><div class="eq-h">사람이 정한다</div><div class="eq-v sm">기준 · 막을 것 · 합격선</div>'
             '<div class="eq-d">무엇이 잘한 것인지는 Agent가 정하지 않음</div></div>'
             '<div class="eq-op">→</div>'
             '<div class="eq-c"><div class="eq-h">Agent가 한다</div><div class="eq-v sm">하네스 안에서 실행</div>'
             '<div class="eq-d">규칙 · 절차 · 강제 · 검증을 따라 반복</div></div>'
             '<div class="eq-op">→</div>'
             '<div class="eq-c hl"><div class="eq-h">사람이 판정하고 고친다</div><div class="eq-v sm">틀린 것 → 하네스 한 줄</div>'
             '<div class="eq-d">판정이 쌓일수록 하네스가 자라고 사람은 새로운 실수만 봄</div></div>'
             '</div>'
             + note("결론", "하네스는 한 번 만들고 끝나는 설정이 아니라, 사람이 스스로 평가하며 키워 가는 업무 방식")),
        light("오늘 다룬 것", table(["장", "한 줄"], [
            ["<b>Ch1</b>", "모델이 좋아질수록 일을 맡기는 장치(하네스)가 결과를 가름"],
            ["<b>Ch2</b>", "부탁(CLAUDE.md) · 절차(Skill) · 강제(Hook) — 꼭 막을 것은 코드로"],
            ["<b>Ch3</b>", "책상에는 지금 필요한 것만 · 남길 것은 파일로"],
            ["<b>Ch4</b>", "남이 만든 하네스는 빌려 쓰고, 다른 회사는 좁고 확인 가능한 일부터"],
            ["<b>Ch5</b>", "나누면 비용이 늘어남 · 역할 분리와 규모가 필요할 때만"],
            ["<b>Ch6</b>", "토큰은 턴 수와 컨텍스트에서 · 재고 나서 줄이기"],
            ["<b>Ch7</b>", "자동 채점은 볼 곳을 좁히고, 판정은 사람이"],
            ["<b>Ch8</b>", "계획 먼저 · 내 업무는 메타 하네스로 · 개발은 Superpowers · 오래 걸리면 루프"],
        ]), "Ch8"),
        light("내일부터 할 일", table(["", "할 일", "방법"], [
            ["<b>①</b>", "<b>반복 업무 하나</b>", "CLAUDE.md 한 장으로 시작 · 결과는 파일로 · 결정은 사람에게"],
            ["<b>②</b>", "<b>판정을 기록</b>", "틀릴 때마다 무엇이 · 왜 틀렸는지 한 줄"],
            ["<b>③</b>", "<b>원인별로 반영</b>", "절차는 Skill · 원칙은 CLAUDE.md · 사고는 Hook"],
            ["<b>④</b>", "<b>평가 문항 다섯 개</b>", "고칠 때마다 다시 돌려 나빠진 곳 확인"],
            ["<b>⑤</b>", "<b>크게 만들지 않기</b>", "나누기 · 플러그인 · 루프는 재 보고 필요할 때만"],
        ]), "Ch8"),
        bridge("하네스는 사람이 키운다", "", "Ch8", "Q & A"),
    ]


def slides():
    return opening() + ch0() + ch1() + ch2() + ch3() + ch4() + ch5() + ch6() + ch7() + ch8()


CSS = '''
  /* 실습 진행 · 시킬 일 / 확인할 결과 */
  .qgrid{display:grid; grid-template-columns:1.25fr 1fr; gap:18px; margin-top:14px;}
  .qc{border:1.5px solid #D9DDE3; border-top:5px solid #1F3A5F; border-radius:12px; padding:16px 20px; background:#fff;}
  .qc.qk{border-top-color:#F28C28;}
  .qh{font-size:15px; font-weight:800; color:#1F3A5F; margin-bottom:8px;} .qc.qk .qh{color:#F28C28;}
  .qc ol, .qc ul{margin:0; padding-left:22px; display:grid; gap:9px;}
  .qc li{font-size:18px; line-height:1.45; color:#16233A;}
  .qc code{font-size:.88em;}

  .hubtxt{font-size:30px; font-weight:800; color:#1F3A5F;}
  .lt :not(pre) > code{font-family:var(--mono); font-size:.92em; background:#EEF1F5; border-radius:4px; padding:1px 5px;}
  .shot{display:block; width:100%; max-height:400px; object-fit:cover; object-position:top; border-radius:12px; border:1px solid #E1E5EB; box-shadow:0 8px 24px rgba(31,58,95,.12); margin-bottom:14px;}
  .ucurve{width:100%; height:auto; margin-bottom:8px;}
  .ucurve .udraw{stroke-dasharray:1400; animation:udraw 1.6s ease-out both;}
  @keyframes udraw{from{stroke-dashoffset:1400}}
  @media print{.ucurve .udraw{animation:none}}
  .evo{display:grid; grid-template-columns:120px repeat(6, 1fr); gap:12px 12px; margin:4px 0 6px;}
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
  .mwrap{display:grid; grid-template-columns:1fr 300px; gap:18px; align-items:center;}
  .mchart{width:100%; height:auto;}
  .mchart .mline{stroke-dasharray:2000; animation:mdraw 1.8s ease-out both;}
  @keyframes mdraw{from{stroke-dashoffset:2000}}
  @media print{.mchart .mline{animation:none}}
  .mcards{display:grid; gap:10px;}
  .mcards .bn{padding:14px 16px;} .mcards .bn .bv{font-size:34px;} .mcards .bn .bl{font-size:14.5px; margin-top:6px;}
  .pgrid2 .code pre, .pgrid2 .code code{white-space:pre-wrap !important; overflow-wrap:anywhere; word-break:keep-all; font-size:13px; line-height:1.55;}
  .pgrid2 .code{min-width:0;}
  .pgrid2.mat .code pre, .pgrid2.mat .code code{font-size:11.5px; line-height:1.45; max-height:370px; overflow:auto;}
  .kdo{display:flex; gap:12px; align-items:flex-start; background:#FFF4E8; border:1.5px dashed #F28C28; border-radius:12px; padding:11px 14px; margin-bottom:10px; break-inside:avoid;}
  .kdo span{flex:none; font-weight:700; font-size:13px; color:#C25E00; white-space:nowrap;}
  .kdo p{margin:0; font-size:13.5px; line-height:1.5; color:#333;}
  .kdo b{font-family:var(--mono); font-size:12.5px; background:#fff; padding:1px 6px; border-radius:5px;}
  .kit .kp .kdo{margin-bottom:0;}
  .kgrid{display:grid; grid-template-columns:1fr 1fr; gap:12px;}
  .kgrid .code pre{max-height:178px; overflow:auto; padding:9px 14px;}
  .kgrid .code code{font-size:11.5px; line-height:1.45; white-space:pre-wrap;}
  .kgrid .code .bar{padding:6px 12px;}
  .lfold{font-family:var(--mono); font-size:13px; background:#EEF2F8; padding:2px 8px; border-radius:6px;}
  .ctree .code pre{padding:10px 16px;} .ctree .code code{font-size:13px; line-height:1.4;}
  .ptall .code pre{padding:12px 18px;} .ptall .code code{font-size:12.5px; line-height:1.5; white-space:pre-wrap;}
  .arch{display:grid; grid-template-columns:1.15fr 34px 1fr 34px 1.1fr; gap:6px; align-items:stretch;}
  .ar-col{border-radius:14px; padding:12px 14px; display:flex; flex-direction:column; gap:7px;}
  .ar-ctx{background:#EEF2F8;} .ar-model{background:#FFF4E8; justify-content:center;} .ar-gate{background:#1F3A5F; color:#fff;}
  .ar-h{font-weight:800; font-size:14px; margin-bottom:4px; color:#1F3A5F;} .ar-gate .ar-h{color:#fff;}
  .ar-it{display:flex; justify-content:space-between; gap:8px; background:#fff; border-radius:8px; padding:6px 10px; font-size:13.5px;}
  .ar-it em{font-style:normal; color:#8A8FA0; font-size:12.5px; white-space:nowrap;}
  .ar-act{background:#fff; border:1.5px solid #F28C28; border-radius:8px; padding:9px 12px; font-size:14px; font-weight:600; text-align:center;}
  .ar-g{background:rgba(255,255,255,.1); border-radius:8px; padding:9px 12px;} .ar-g b{display:block; font-size:14.5px;} .ar-g em{font-style:normal; font-size:12.5px; opacity:.8;}
  .ar-arrow{display:flex; align-items:center; justify-content:center; font-size:26px; color:#F28C28; font-weight:800;}
  .ar-loop{margin-top:10px; text-align:center; font-size:14px; color:#1F3A5F; font-weight:600;}
  .ktree{grid-template-columns:1.05fr 1fr;} .ktree .kf .code pre{max-height:165px;}
  .kindtag{margin-left:8px; font-size:12px; font-weight:800; padding:3px 10px; border-radius:999px; color:#fff;}
  .k필수{background:#F28C28;} .k선택{background:#1F3A5F;} .k시연{background:#8A94A3;}
  .eqn{display:grid; grid-template-columns:1fr 48px 1fr 48px 1fr; align-items:stretch; gap:8px; margin-top:20px;}
  .eq-c{border:2px solid #1F3A5F; border-radius:16px; padding:22px 20px; background:#fff; display:flex; flex-direction:column; gap:12px; min-height:230px;}
  .eq-c.hl{border-color:#F28C28; background:#FFF4E8;}
  .eq-h{font-size:20px; font-weight:800; color:#1F3A5F;} .eq-c.hl .eq-h{color:#C25E00;}
  .eq-v{font-size:52px; font-weight:800; color:#1F3A5F; line-height:1;} .eq-v small{font-size:22px; margin-left:4px;}
  .eq-v.sm{font-size:24px; line-height:1.35;} .eq-c.hl .eq-v{color:#F28C28;}
  .eq-d{font-size:15px; color:#555; line-height:1.5; margin-top:auto;}
  .eq-op{display:flex; align-items:center; justify-content:center; font-size:44px; font-weight:800; color:#F28C28;}
  .kgrid.kg3{grid-template-columns:1fr 1fr 1fr;} .kgrid.kg3 .code .bar .fn{font-size:10.5px; margin-left:4px;} .kgrid.kg3 .code .bar .copybtn, .kgrid.kg3 .code .bar .savebtn{font-size:10.5px; padding:3px 6px;} .kgrid.kg3 .code .bar .dot{display:none;} .kgrid.kg3 .code pre{max-height:165px;} .kgrid.kg3 .code code{font-size:11px;}
  .kithead{display:flex; align-items:center; gap:10px; margin:-4px 0 12px; font-size:14px; color:var(--ink-2, #555);}
  .kithead span{font-weight:700; color:#1F3A5F;} .kithead .ks{margin-left:10px;} .kithead code{font-family:var(--mono); font-size:13px; background:#EEF2F8; padding:3px 9px; border-radius:6px;}
  .kithead em{margin-left:auto; font-style:normal; font-size:13px; color:#8A8FA0;}
  .kit{display:grid; grid-template-columns:1.15fr 1fr; gap:16px; align-items:start;}
  .kit .kp, .kit .kf{display:flex; flex-direction:column; gap:10px; min-width:0;}
  .kit.wide{display:block; column-count:2; column-gap:16px;}
  .kit.wide .code{break-inside:avoid; margin-bottom:10px;}
  .kit .code .bar{padding:6px 12px;}
  .kit .code pre{padding:9px 14px;}
  .kit .code code{font-size:12.5px; line-height:1.5; white-space:pre-wrap;}
  .kit .kf .code pre{max-height:340px; overflow:auto;}
  .kit .kp .code pre, .kit.wide .code pre{max-height:205px; overflow:auto;}
  .kit .kf .code:not(:only-child) pre{max-height:175px;}
  .kit .kf .code code{font-size:11.5px;}
  .pgrid2{display:grid; grid-template-columns:1fr 1fr; gap:16px;}
  .dl{color:#F28C28; font-weight:800; font-family:var(--mono); text-decoration:underline;}
  .days.two{grid-template-columns:1fr; max-width:1150px;}
  .days.two .daycol{display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; align-content:start; grid-auto-rows:min-content;}
  .days.two{align-items:start; align-self:start;}
'''
