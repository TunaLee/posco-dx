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
import mcp_fig
import viz2

deck.LAB_KIND.update({"3-1": ("필수", 40), "4-1": ("필수", 10), "4-2": ("필수", 30), "4-3": ("필수", 20), "4-4": ("필수", 15), "5-1": ("필수", 15),
                      "6-1": ("필수", 25), "7-1": ("선택", 20), "8-1": ("필수", 20), "8-2": ("필수", 25), "9-1": ("필수", 90), "9-2": ("필수", 30)})
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
A_37 = ("Anthropic · Claude 3.7 Sonnet 포켓몬 실험 2025.2", "https://www.anthropic.com/news/visible-extended-thinking")
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
D_CTXWIN = ("Claude Code 문서 · Context window (What survives compaction)", "https://code.claude.com/docs/en/context-window.md")
D_MEMORY = ("Claude Code 문서 · Memory", "https://code.claude.com/docs/en/memory.md")
D_CAVEMAN = ("caveman README (제작자 발표)", "https://github.com/JuliusBrussee/caveman")
D_PONYTAIL = ("ponytail README (제작자 발표)", "https://github.com/DietrichGebert/ponytail")
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
OWN_TOK = ("직접 실측 2026.10.14 · Sonnet 5.5 · Claude Code 세션 기록", "https://github.com/TunaLee/posco-dx")
PH_WILD = ("사진 · U.S. Fish and Wildlife Service (퍼블릭 도메인)", "https://commons.wikimedia.org/wiki/File:Running_wild_horse_-_DPLA_-_cf88630cfe76c58a265153acb3defd01.jpg")
PH_HARNESS = ("사진 · Jude, CC BY-SA 2.0", "https://commons.wikimedia.org/wiki/File:Clydesdale_wagon.jpg")
PH_PARTS = ("그림 · Nouveau Larousse illustré 1898 (퍼블릭 도메인)", "https://commons.wikimedia.org/wiki/File:Parts_of_horse_harness_(in_French,_1898).jpg")
PH_TEAM = ("사진 · Bernard Spragg (퍼블릭 도메인)", "https://commons.wikimedia.org/wiki/File:The_draft_horse_team._(51174500032).jpg")
OWN_RUN = ("직접 실측 2026.10.28 · Claude Code 기본 모델 · labs/mini_git · 각 1회", "https://github.com/TunaLee/posco-dx/tree/main/labs/mini_git")

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


TL = [("2022.11", "채팅 · ChatGPT 공개"), ("2023.06", "도구 호출 · Function Calling"),
      ("2024.11", "연결 표준 · MCP"), ("2025.02", "코딩 에이전트 · Claude Code"),
      ("2025.07", "범용 에이전트 · ChatGPT agent"), ("2025.10", "스킬 · Agent Skills")]
TL_HX = [("2025~", "하네스 엔지니어링"), ("2026~", "루프 엔지니어링")]


def timeline(extra=()):
    """Ch0 연표 · extra 를 주면 앞 연표는 흐리게 두고 뒤에 덧붙임."""
    hl = {"2023.06", "2025.02"} if not extra else set()
    items = [(y, t, "hl" if y in hl else ("dim" if extra else "")) for y, t in TL] + [(y, t, "hl") for y, t in extra]
    tl = "".join(f'<div class="tl {c}"><b>{y}</b><span>{t}</span></div>' for y, t, c in items)
    return f'<div class="tline{" t8" if extra else ""}" style="grid-template-columns:repeat({len(items)},1fr)">{tl}</div>'


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

def _kitsrc(src):
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



def quest(no, ch, asks, checks, stuck, folder="labs/mini_git"):
    """실습 진행 — Claude에게 할 말(큰 카드) · 확인할 것 · 막히면."""
    a = "".join(f'<div class="qa2"><span>{i}</span><p>{x}</p></div>' for i, x in enumerate(asks, 1))
    c = "".join(f"<li>{x}</li>" for x in checks)
    head = (f'<div class="kithead"><span>VS Code로 열 폴더</span><code>{folder}</code>'
            f'<em>요청은 짧게 · 방법은 Claude가 정함</em></div>')
    body = (f'<div class="qh2">Claude에게</div><div class="qas">{a}</div>'
            f'<div class="qk2"><b>확인</b><ul>{c}</ul></div>' + note("막히면", stuck))
    return light(f"실습 {no} 진행", head + body, ch)


def result(no, ch, cards, take, pair=None, img=None):
    """실습 결과 — 큰 숫자 카드. 값에 「→」가 있으면 전 → 후 (후는 주황)."""
    def val(v):
        if "→" in v:
            x, y = [z.strip() for z in v.split("→", 1)]
            return f'<span class="rb">{x}</span><i>→</i><span class="ra">{y}</span>'
        return f'<span class="ra">{v}</span>'
    cs = "".join(f'<div class="rc" style="--d:{i * .12:.2f}s"><b>{k}</b><div class="rv">{val(v)}</div></div>'
                 for i, (k, v) in enumerate(cards))
    leg = (f'<div class="rleg"><span class="rb">{pair[0]}</span><i>→</i><span class="ra">{pair[1]}</span></div>' if pair else "")
    grid = f'<div class="rgrid c{len(cards)}">{cs}</div>'
    if img:
        grid = f'<div class="rimg"><img class="shot" src="img/{img}" alt=""/><div class="rgrid c1">{cs}</div></div>'
    return stat(f"실습 {no} 결과", ch, leg + grid + note("정리", take), OWN_RUN)


def pokemon():
    """포켓몬 하네스 · 과거(부품 여럿) vs 현재(화면 + 버튼)."""
    parts = [("화면", "게임 화면 캡처", True), ("버튼", "A · B · 방향키 입력", True),
             ("이동 도구", "좌표만 주면 길 찾기", False), ("기억 메모", "진행 상황 · 할 일 기록", False),
             ("지도", "마을 · 길 위치", False), ("게임 상태", "위치 · 포켓몬 정보 제공", False)]
    def side(cls, head, sub, keep_all):
        chips = "".join(f'<div class="pk-p{"" if keep_all or k else " off"}" style="--d:{i * .15 + .3:.2f}s"><b>{n}</b><span>{d}</span></div>'
                        for i, (n, d, k) in enumerate(parts))
        return f'<div class="pk {cls}"><div class="pk-h"><b>{head}</b><span>{sub}</span></div><div class="pk-m">모델</div><div class="pk-g">{chips}</div></div>'
    return ('<div class="pk2">' + side("old", "과거 Claude", "2025.2~ · 3.7 Sonnet 등", True)
            + '<div class="pk-arr">→</div>' + side("new", "Claude Fable 5", "2026.6 · 화면만 보고 완주", False) + '</div>'
            + note("정리", "모델이 못 하던 일을 하네스가 대신 → 모델이 좋아지면 그 부품은 덜어 냄"))


def esc(x):
    return x.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")





# ── 하네스 지도 ──────────────────────────────────────────
PARTS = [
    ("지침 · 컨텍스트", "CLAUDE.md · 무엇을 올릴지", "Ch2 · Ch5", (250, 255)),
    ("Skill · 명령", "필요할 때 꺼내 쓰는 절차", "Ch2", (640, 215)),
    ("Tool · MCP", "조회 · 계산 · 외부 연결", "Ch4", (1030, 255)),
    ("Sub Agent · 팀", "역할 분리 · 오케스트레이션", "Ch6", (1030, 590)),
    ("Hook · 권한", "막기 · 기록 · 승인", "Ch2", (640, 650)),
    ("평가 · 비용", "평가셋 · 토큰", "Ch7 · Ch8", (250, 590)),
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
    ("Ch0", "AI 에이전트", "등장 배경 · 구조 · 작업 길이"),
    ("Ch1", "하네스 개념", "모델 밖의 모든 것"),
    ("Ch2", "Claude Code 하네스 분해", ".claude · Skill · Sub Agent · Hook"),
    ("Ch3", "오픈 하네스 적용", "Superpowers로 미니 깃에 기능 더하기"),
    ("Ch4", "Tool · MCP", "미니 깃 MCP 서버 · 리뷰 · Hook"),
    ("Ch5", "컨텍스트 엔지니어링", "도구가 돌려주는 양"),
    ("Ch6", "멀티에이전트", "리뷰어 팀 · 검증"),
    ("Ch7", "토큰 경제학", "LLM에 맡길 일 · 코드로 할 일"),
    ("Ch8", "평가 · HITL", "사람의 수정 요청 · 리뷰 반영 루프"),
    ("Ch9", "내 하네스 만들기", "메타 하네스 · 루프 · 발표"),
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
        light("최종 산출물", viz2.tiles([('미니 깃에 올린 내 코드', '기능 · MCP 서버 · 리뷰 기록'), ('메타 하네스', '인터뷰 → 승인 → 하네스 생성'), ('내 업무 하네스', '미적용 vs 적용 비교'), ('사람 판정 기록', '내 기준으로 판정 · 2분 발표')], 4), "시작"),
        light("실습 환경", viz2.tiles([('Claude Code', '회사 계정 로그인'), ('VS Code · Python 3.10+', '표준 라이브러리만'), ('Agent Watch', '실행 흐름 · 토큰'), ('Git', '버전 관리 · 공유')], 4)
              + note("실습 자료", labdir("") + " · 미니 깃 뼈대만 준비 · 기능 · MCP · 리뷰는 직접"), "시작"),
        light("실습 진행 방식", flow([("labs.zip 받기", "아래 링크 · 덱과 같은 곳"), ("압축 풀기", "바탕화면 등"), ("VS Code로 폴더 열기", "실습마다 열 폴더 표시"), ("Claude Code 패널", "왼쪽 위 아이콘"), ("미니 깃 켜기", "python server.py")])
              + '<div class="kit wide" style="margin-top:22px">' + code("처음 한 번 · labs/mini_git 에서", esc("python3 · claude 버전을 확인하고\n미니 깃(server.py)을 켜 줘"))
              + code("막히면", esc("방금 오류를 보고 원인과 고칠 방법을 알려 줘. 내 PC 설정은 바꾸기 전에 물어봐"))
              + '</div>' + note("실습 자료", labdir("") + " · 설치할 패키지 없음 (표준 라이브러리만) · 코드는 직접 쓰지 않음"), "시작"),
    ]


# ── Ch0 AI 에이전트 ─────────────────────────────────────
def ch0():
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
        light("에이전트의 구조", viz2.agent_anatomy()
              + note("다음", "LLM을 뺀 나머지 전부 = 하네스"), "Ch0"),
        light("채팅 → 에이전트 연표", timeline()
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
             + viz2.maprows([("굴레 · 고삐", "지침 · CLAUDE.md", "방향"), ("눈가리개", "컨텍스트 설계", "볼 것만"),
                             ("목사리 · 끄는 줄", "도구 · Skill", "힘 전달"), ("재갈", "Hook · 권한", "바로 멈춤"),
                             ("마부", "사람 승인 · 평가", "최종 판단")], "마구", "하네스") + "</div>"
             + note("말이 좋아질수록", "마구는 가벼워지지만 사라지지 않음"),
             PH_PARTS),
        hx_map(None, "하네스 지도", "하네스를 이루는 여섯 부품"),
        light("하네스 부품이 해결하는 문제", viz2.tiles([('지침', '매번 다른 형식 · 기준'), ('Skill', '절차 단계 건너뜀'), ('Tool', '조회 대신 기억으로 지어낸 숫자'), ('Sub Agent', '긴 작업 중 앞 지시를 잊음'), ('Hook · 권한', '삭제 · 강제 push 같은 위험한 실행'), ('평가', '고친 뒤 다른 곳이 조용히 깨짐')], 3), "Ch1"),
        light("신입사원 온보딩과의 비교", table(["신입사원이 받는 것", "Agent의 하네스"], [
            ["회사 소개 · 업무 규칙", "CLAUDE.md"], ["업무 매뉴얼", "Skill"], ["사내 시스템 계정", "Tool · MCP"],
            ["옆 팀 협업", "Sub Agent"], ["결재 · 보안 규정", "Hook · 권한"], ["수습 평가", "평가셋"],
        ]), "Ch1"),
        light("채팅 → 에이전트 → 하네스", timeline(TL_HX)
              + note("정리", "에이전트가 일을 맡게 되면서 → 맡긴 일을 지키는 장치(하네스)가 다음 과제"), "Ch1"),
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
        stat("같은 문제 · 하네스별 작업량", "Ch1",
             big([("11", "분", "Claude Code 하네스 · 도구 22번 · 28문제 풂", True), ("19", "분", "터미널만 · 도구 41번 · 26문제 풂")], 2)
             + note("읽는 법", "같은 오픈 모델 6종 · 과제 1개당 평균 · 푼 문제 수는 비슷한데 시간 · 도구 호출이 거의 절반")
             + note("그래서", "하네스는 정답률뿐 아니라 시간 · 비용도 바꾼다 · 남의 점수 대신 우리 과제로 직접 잰다 (Ch8)"),
             HARBOR),
        stat("포켓몬 하네스 변화", "Ch1", pokemon(), A_37, A_FABLE5),
        stat("같은 모델 · 다른 하네스", "Ch1",
             hbars([("Mythos 5 · 단일 Agent", 88.0, False, "88.0%"), ("Mythos 5 · 멀티에이전트", 93.3, True, "93.3%")], top=100,
                     title="BrowseComp · 같은 모델, 구성만 다름")
             + note("그래서", "같은 모델도 하네스 구성에 따라 점수가 달라짐"),
             A_FABLE5, SC_FABLE5),
        bridge("다음: Claude Code 하네스 분해", "", "Ch1", "→ Ch2 .claude · Skill · Sub Agent · Hook"),
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
            '<div class="ctree">' + code("폴더 구조", '내-프로젝트/\n├── CLAUDE.md                 공통 원칙\n├── .mcp.json                 MCP 서버\n└── .claude/\n    ├── settings.json         권한 · Hook 등록 (팀 공유)\n    ├── settings.local.json   내 PC 전용 (git 제외)\n    ├── skills/\n    │   └── reject-report/\n    │       └── SKILL.md      절차\n    ├── agents/\n    │   └── verifier.md       Sub Agent 하나 = 파일 하나\n    └── hooks/\n        └── guard.py          Hook 스크립트') + "</div>",
            viz2.tiles([("CLAUDE.md", "세션 시작 때 항상"), ("skills/", "요청이 설명과 맞을 때"), ("agents/", "메인이 위임할 때"), ("settings.json", "권한 · Hook · 팀 공유")], 1))
              + note("~/.claude/", "같은 구조를 홈 폴더에 → 내 모든 프로젝트에 적용"), "Ch2"),
        light("전역 · 프로젝트 하네스 위치", viz2.scopes()
              + note("겹치면", "내 PC만 &gt; 프로젝트 &gt; 전역 순으로 우선 · 팀 규칙은 프로젝트에, 내 습관은 전역에"), "Ch2"),
        light("부품별 로드 · 실행 시점", viz2.tiles([('세션 시작 때', 'CLAUDE.md · Skill 설명 · MCP 도구 목록'), ('필요할 때', 'Skill 본문 · Sub Agent · /명령'), ('도구 호출 전후', '권한 · Hook — 코드가 결정')], 3)
              + note("성격", "CLAUDE.md = 부탁 · Skill = 절차 · Sub Agent = 분업 · Hook = 강제"), "Ch2"),
        light("부탁 · 절차 · 강제", cards([
            ("CLAUDE.md = 부탁", "모델이 읽고 따르려 함 · 어길 수 있음", []),
            ("Skill · 명령 = 절차", "필요할 때만 불러 컨텍스트 절약", []),
            ("Hook · 권한 = 강제", "코드가 막음 · 모델이 우회 못 함", []),
        ]), "Ch2"),
        light("Skill 한 개의 구조", two(code(".claude/skills/incident-report/SKILL.md", skill),
                                        vl("description: 언제 부를지", "본문: 호출될 때만 로드", "참고 파일: 양식 · 예시"))
              + note("이름", "예시일 뿐 · 팀 규칙에 맞게 자유롭게"), "Ch2"),
        light("명령(command)의 구조", code(".claude/commands/handle.md", cmd) + note("호출", "/handle VPN이 안 붙어요"), "Ch2"),
        light("Skill과 command의 차이", viz2.pair(
            "command · 버튼", [("사람이 /이름", "입력해야 실행"), ("한 파일", ".claude/commands/이름.md"), ("맞는 일", "배포 · 발송 · 사람이 시작할 일")],
            "Skill · 업무 매뉴얼", [("Claude가 골라 씀", "설명을 보고 스스로 · /이름도 가능"), ("폴더", "SKILL.md + 참고 자료"), ("맞는 일", "업무 절차 · 판단 기준 · 양식")])
              + note("새로 만들 땐 Skill", "command는 합쳐진 예전 방식 · 사람만 부르게 하려면 disable-model-invocation: true"), "Ch2"),
        light("Sub Agent의 흐름", viz2.subagent_flow()
              + note("핵심", "많이 읽는 일은 Sub Agent의 책상에서 · 메인은 결과만 받아 가볍게 · 일이 끝나면 Sub Agent는 닫힘"), "Ch2"),
        light("Sub Agent 경계 설계", viz2.tiles([('도구', 'Read · Grep · Glob'), ('권한', '쓰기 금지'), ('컨텍스트', '변경 파일만'), ('반환 형식', '파일:줄 · 문제 · 근거')], 4)
              + note("예", "reviewer Agent · 네 가지를 정의 파일에 적음"), "Ch2"),
        light("Sub Agent 정의 파일", two(code(".claude/agents/reviewer.md", agent),
                                          vl("자기 컨텍스트에서 일함", "부모는 결과만 받음", "도구를 줄이면 권한도 줄어듦")), "Ch2"),
        lab("2-1", "리뷰 Skill · 보안 Agent 만들기", "Ch2",
            "더미 코드로 .claude/ 를 Claude와 함께 · 하네스 전후 리뷰 비교",
            ["하네스 없이 「shop 코드 리뷰해 줘」", "리뷰 절차를 Skill로", "보안 검토 Sub Agent", "새 대화에서 같은 요청 · 비교"],
            [".claude/skills · .claude/agents", "전후 리뷰 비교"], files=labdir("review_lab"), mine="내 업무 검토 절차 하나를 Skill로"),
        quest("2-1", "Ch2",
              ["「shop 코드 리뷰해 줘」 · 하네스 없이", "「코드 리뷰 절차를 Skill로 만들어 줘」", "「보안 검토 Sub Agent를 만들어 줘」", "새 대화: 「shop 코드 리뷰해 줘」"],
              ["<code>.claude/</code> 에 생긴 파일", "Skill 이름이 호출 표시에", "<code>/tasks</code> 에 보안 Agent", "전후 형식 · 근거 줄 차이"],
              "<code>solution/dot_claude/</code> → <code>.claude/</code> 로 복사", folder="labs/review_lab"),
        stat("Replit 운영 DB 삭제 사고", "Ch2", viz2.incident()
             + quote("모든 대문자로 열한 번이나 하지 말라고 했다", "Jason Lemkin · Replit 사고 당사자 (2025.7)"), INC_REPLIT),
        stat("프롬프트 주입", "Ch2", viz2.injection()
             + note("하네스로", "읽기는 허용 · 승인 · 전송 · 삭제는 Hook으로 막기 · 발송은 사람"), INC_SUPERHUMAN, TRIFECTA),
        stat("부탁 vs Hook", "Ch2", viz2.ask_vs_hook()
             + note("Claude Code 문서", "CLAUDE.md는 권고 · Hook은 결정적 — 반드시 일어나게 보장"), D_BP, D_HOOKS),
        light("Hook 설정과 차단 코드", code(".claude/settings.json (hooks 부분)", esc('"PreToolUse": [{\n  "matcher": "Edit|Write|MultiEdit",\n  "hooks": [{ "type": "command",\n             "command": "python .claude/hooks/guard.py" }]\n}]'))
              + code(".claude/hooks/guard.py (요점)", esc('event = json.load(sys.stdin)\npath = event["tool_input"]["file_path"]\nif 상대경로(path).startswith(("shop/", "tests/")):\n    print(json.dumps({"hookSpecificOutput": {\n      "hookEventName": "PreToolUse",\n      "permissionDecision": "deny",\n      "permissionDecisionReason": "리뷰어는 코드를 고치지 않는다"}}))')), "Ch2"),
        lab("2-2", "리뷰어는 고치지 않는다 · Hook", "Ch2",
            "「고치지 마」를 지시가 아니라 코드로",
            ["「리뷰하고 바로 고쳐 줘」 → 고쳐짐", "Hook으로 shop/ · tests/ 수정 막기", "새 대화에서 다시 → 막힘", "<code>git checkout</code> 으로 되돌리기"],
            ["<code>.claude/settings.json</code> · <code>hooks/</code>", "수정 0건 · 리뷰만"], files=labdir("review_lab"), mine="내 업무에서 Hook으로 막을 것 세 가지"),
        quest("2-2", "Ch2",
              ["「리뷰하고 바로 고쳐 줘」", "<code>git checkout -- shop</code> 으로 되돌리기", "「리뷰 중에는 shop/ · tests/ 를 못 고치게 Hook으로 막아 줘」", "새 대화: 「리뷰하고 바로 고쳐 줘」"],
              ["Hook 전: 코드가 바뀌는가", "Hook 후: 막힘 · 이유 한 줄", "<code>out/review.md</code> 는 써짐", "settings.json 의 matcher"],
              "<code>solution/dot_claude/settings.json</code> · <code>hooks/guard.py</code>", folder="labs/review_lab"),
        stat("Claude Code로 하는 두 종류의 일", "Ch2", two(
            cards([("코드 작업", "기능 구현 · 테스트 · 코드 리뷰 · 배포 전 점검", [])], 1),
            cards([("업무 처리", "문의 답변 · 견적 · 회의록 정리 · 보고서 · 문서 비교 · 메일 초안", [])], 1))
             + note("공통", "같은 부품: 지침 · Skill · Sub Agent · Hook · 평가 → 파일을 읽고 규칙대로 결과물을 만드는 일이면 모두 대상")
             + big([("20", "%", "Codex 주간 사용자 중 개발자가 아닌 지식 노동자"), ("1", "번", "Claude Code로 블로그 글 하나 · 채팅은 13번 주고받음", True)], 2),
             OAI_CODEX, A_ECON26),
        light("하네스에 맞는 업무", viz2.fit(
            [("자주 반복", "한 번 만들고 계속 재사용"), ("기준이 분명", "「잘했다」를 정할 수 있음"), ("결과 확인 가능", "테스트 · 정답 · 검증 Agent"),
             ("회사만 아는 지식", "규정 · 양식 · 확정 사항"), ("막을 구간이 있음", "Hook으로 강제")],
            [("한 번 하고 끝", "대화가 더 빠름"), ("기준이 매번 다름", "기획 · 협상 · 아이디어"), ("확인할 방법 없음", "좋아졌는지 모름"),
             ("되돌릴 수 없음", "결재 · 송금은 사람")]), "Ch2"),
        light("하네스 적용 예시 여섯 유형", viz2.tiles([
            ("문의 응대", "클레임 1차 답변 · 규정 근거 · 발송은 사람"), ("문서 추출 · 계산", "발주서 · 계약 조항 · 불일치면 보류"),
            ("기록 → 보고서", "생산 실적 · 장애 주간 보고 · 수치 대조"), ("비교 · 검토", "계약 변경점 · 설정 리뷰 · 고치지 않고 판정"),
            ("정리 · 작성", "회의 후속 조치 · 공지 · 약속 금지"), ("개발", "MES 로그 분석 · 정산 배치 · Superpowers")], 3)
              + note("샘플", labdir("samples") + " · 11개 업무 분야 가상 데이터"), "Ch2"),
        bridge("다음: 오픈 하네스 적용", "", "Ch2", "→ Ch3 Superpowers로 첫 개발"),
    ]



# ── Ch3 Tool · MCP ──────────────────────────────────────
def ch_tool():
    return chapter("Ch4", "Tool · MCP", {"Tool · MCP"}, "도구를 붙이고 제한하기") + [
        light("도구가 필요한 이유", viz2.calc_compare()
             + note("LLM 혼자 못 하는 것", "정확한 계산 · 오늘의 정보 · 사내 데이터 · 실제 행동 → 무엇을 부를지는 LLM, 실행은 도구"), "Ch4"),
        light("도구의 구조 · 선언과 실행", viz2.decl_split()
              + note("핵심", "모델은 이름 · 설명 · 입력 형식만 보고 고름 · 실제 조회 · 실행은 함수가"), "Ch4"),
        lab("4-1", "계산 도구 하나 붙여 보기", "Ch4",
            "Claude Code에 도구를 붙이고, 직접 고르고 부르는지 확인",
            ["도구 없이 계산 요청", "<code>claude mcp add</code> 로 계산 도구 등록", "같은 계산 요청 → 호출 표시", "<code>/mcp</code> 에서 도구 설명 보기"],
            ["호출 표시 <code>mcp__calc__calc</code>", "도구 설명문 확인"], files=labdir("mini_git"), mine="내 업무에서 LLM이 틀리면 곤란한 계산 하나"),
        quest("4-1", "Ch4",
              ["「도구 쓰지 말고 바로 답해 줘: 4817 × 293 × 1.1 원 미만 버림」", "터미널: <code>claude mcp add calc -- python tools/calc_server.py</code>",
               "새 대화: 「calc 도구로 같은 계산을 해 줘」", "<code>/mcp</code> → calc → 도구 설명 읽기"],
              ["답 위에 <code>calc</code> 호출 표시", "넘긴 인자 (expr · floor)", "두 답이 같은가 · 정답 1,552,519", "설명문이 곧 사용 설명서"],
              "<code>tools/calc_server.py</code> 를 열어 보기 · 파일 하나 · 66줄"),
        result("4-1", "Ch4", [("도구 등록", "명령 한 줄"), ("Claude가 고른 도구", "<code>mcp__calc__calc</code>"), ("걸린 시간", "9초 · 호출 1번"), ("답", "1,552,519 <em>정답</em>")],
               "도구는 붙이기만 하면 Claude가 설명을 보고 스스로 골라 부름"),
        light("내장 도구와 외부 도구", viz2.tool_kinds()
              + note("MCP", "외부 도구를 Claude Code에 붙이는 표준 연결 방식 · 다음 장부터"), "Ch4"),
        light("도구 설계도 하네스", viz2.pair(
            "붙이기", [("외부 도구 연결", "MCP · 사내 시스템"), ("내 업무 도구", "필요한 조회 · 계산만")],
            "제한하기", [("허용 목록", "<code>--allowedTools</code> · 권한 allow"), ("막기", "권한 deny · Hook · Agent별 tools")], hl="l")
              + note("하네스", "어떤 도구를 쥐여 주고 무엇을 막느냐 = 모델 밖에서 정하는 일"), "Ch4"),
        stat("MCP · Skills 확산 현황", "Ch4",
             big([("5억", "회", "MCP SDK 월 다운로드 (대표 SDK 합계)", True),
                  ("10억+", "회", "TypeScript · Python SDK 각각 누적"),
                  ("46", "개", "Agent Skills 형식을 지원하는 도구")])
             + quote("도구 100개짜리 서버에 연결하면, 사용자가 묻기도 전에 그 전부의 값을 치르고 목록이 길수록 도구 고르기도 나빠진다", "MCP 로드맵, 2026.8"),
             MCP26, MCPRM, SKILLSIO),
        light("규격 없는 연결", mcp_fig.tangle()
              + note("MCP", "Model Context Protocol · Anthropic 2024.11 공개 · 도구 목록 · 호출 · 결과 전달 형식을 하나로"), "Ch4"),
        light("MCP 서버와 MCP 클라이언트", cards([
            ("MCP 서버", "도구를 제공하는 프로그램 · 예: 미니 깃 서버", []),
            ("MCP", "무엇을 어떤 순서로 주고받을지 정한 규격", []),
            ("MCP 클라이언트", "도구를 가져다 쓰는 AI 앱 쪽 · 예: Claude Code", []),
        ], 3) + note("실습 순서", "이미 있는 서버 연결 (Microsoft Learn) → 직접 서버 만들기 (미니 깃)"), "Ch4"),
        light("MCP 서버가 하는 두 가지 일", two(
            code("① tools/list · 도구 목록 보내기", esc('{"tools": [{\n  "name": "get_diff",\n  "description": "PR 의 변경 내용을 돌려준다",\n  "inputSchema": {"type": "object",\n    "properties": {"pr": {"type": "integer"}}}\n}]}')),
            code("② tools/call · 도구 실행하기", esc('{"method": "tools/call",\n "params": {"name": "get_diff",\n            "arguments": {"pr": 104}}}\n\n→ {"content": [{"type": "text",\n     "text": "--- a/shop/orders.py\\n+++ b/shop/orders.py ..."}]}')))
              + note("설명문", "Claude는 이름 · 설명 · 입력 형식만 보고 도구를 고름 → 설명문이 곧 사용 설명서"), "Ch4"),
        light("등록 · 호출 순서", mcp_fig.seq(), "Ch4"),
        lab("4-2", "MCP 연결해 보기", "Ch4",
            "이미 있는 MCP 서버를 붙여 보고 도구 목록 · 호출 모습 파악",
            ["Microsoft Learn MCP 연결", "<code>/mcp</code> 로 도구 목록 · 설명 보기", "문서 질문 → 호출 표시 확인", "<code>/context</code> 로 도구가 차지하는 양"],
            ["<code>/mcp</code> 에 연결 표시", "답 위 MCP 도구 호출"], files=labdir("mini_git"), mine="회사에서 붙여 보고 싶은 MCP 서버 하나"),
        quest("4-2", "Ch4",
              ["「Microsoft Learn MCP(https://learn.microsoft.com/api/mcp)를 연결해 줘」", "<code>/mcp</code> → 서버 선택 → 도구 목록 · 설명 읽기",
               "「Microsoft Learn에서 PowerShell의 현재 폴더를 확인하는 명령을 찾아 줘」", "<code>/context</code> 로 MCP 도구 크기 보기"],
              ["연결 방식: URL (HTTP)", "도구 이름 · 설명 · 입력 형식", "답 위 <code>mcp__</code> 호출 · 출처 주소", "등록 = 연결 · 실제 호출은 따로"],
              "<code>claude mcp add --transport http mslearn https://learn.microsoft.com/api/mcp</code>"),
        light("미니 깃 API", two(
            code("브라우저 주소창 · 127.0.0.1:8900/api/repos/shop/prs", esc('[{"id": 101, "title": "주문 검색 API 추가",\n  "author": "김하늘", "status": "open",\n  "files": ["shop/orders.py"],\n  "additions": 5, "deletions": 0},\n {"id": 102, "title": "쿠폰 정률 할인 지원", ...}]')),
            cards([("주소", "/api/repos/shop/prs · …/prs/번호/diff · …/prs/번호/comments", []),
                   ("형식", "JSON · 사람이 아니라 프로그램이 읽는 모양", [])], 1))
              + note("MCP 서버가 부를 곳", "약속된 주소에 요청하면 정해진 형식(JSON)으로 답 · 브라우저로도 열어 볼 수 있음"), "Ch4"),
        light("도구와 API 연결", mcp_fig.mapping()
              + note("MCP 서버 코드", "도구 이름 · 인자 → API 주소 · 결과 JSON → 도구 결과 · 이 코드는 Claude Code가 작성"), "Ch4"),
        light("로컬 연결과 URL 연결", viz2.pair(
            "로컬 (명령)", [("내 PC에서 실행", "표준 입출력"), ("예", "미니 깃 · 사내 DB"), ("등록", "<code>claude mcp add repo -- python mcp_server.py</code>")],
            "URL", [("인터넷 주소로 접속", "HTTP"), ("예", "Microsoft Learn · 사내 공용 서버"), ("등록", "<code>claude mcp add --transport http mslearn https://learn.microsoft.com/api/mcp</code>")], hl="l")
              + note("확인 · 공유", "<code>/mcp</code> · <code>-s project</code> → <code>.mcp.json</code> 으로 팀원이 같은 연결"), "Ch4"),
        light("GitHub MCP가 내려주는 도구", viz2.pair(
            "PR 도구", [("list_pull_requests", "PR 목록 · 상태 · 정렬"), ("pull_request_read", "method: get · get_diff · get_files · get_comments"),
                       ("create_pull_request", "브랜치 → PR 만들기"), ("add_comment_to_pending_review", "파일 · 줄에 리뷰 코멘트"),
                       ("pull_request_review_write", "리뷰 제출 · 승인"), ("merge_pull_request", "병합")],
            "저장소 도구", [("list_branches · list_commits", "브랜치 · 커밋 이력"), ("get_file_contents", "파일 내용"),
                          ("create_branch · push_files", "브랜치 · 파일 올리기"), ("search_code", "코드 검색")], hl="l")
              + note("미니 깃 MCP도 같은 이름으로", "도구 이름 · 모양이 같으면 나중에 진짜 GitHub로 바꿔도 Skill · Hook을 그대로"), "Ch4"),
        lab("4-3", "미니 깃 MCP 서버 만들기", "Ch4",
            "미니 깃 API를 MCP 서버로 · 붙여 넣기 없이 PR 조회 · 코멘트",
            ["미니 깃 MCP 서버 만들기 · 연결", "<code>/mcp</code> 로 내 도구 보기", "「아직 리뷰 안 한 PR 정리해 줘」", "MCP 서버 코드도 미니 깃에 PR로"],
            ["<code>/mcp</code> 에 내 서버", "미니 깃에 MCP 서버 PR"], files=labdir("mini_git"), mine="내 업무에서 MCP로 붙이고 싶은 사내 시스템 하나"),
        quest("4-3", "Ch4",
              ["「GitHub MCP와 같은 도구 이름으로 미니 깃 MCP 서버를 만들어 연결해 줘」", "<code>/mcp</code> 에서 내가 만든 도구 목록 보기", "새 대화: 「shop에서 아직 리뷰 안 한 PR 정리해 줘」", "「MCP 서버 코드를 미니 깃 my-tools 저장소에 PR로 올려 줘」"],
              ["연결 방식: 로컬 (명령)", "답 위에 MCP 도구 호출 표시", "미니 깃 화면에 MCP 서버 PR", "미니 깃을 끄면?"],
              "<code>solution/mcp_server.py</code>"),
        result("4-3", "Ch4", [("MCP 서버 만들기", "169초 · 21턴"), ("만든 도구", "PR 목록 · diff · 파일 · 코멘트"),
                                 ("등록", "<code>.mcp.json</code> · 처음 한 번 승인"), ("「PR 101~112 리뷰」", "142초 · 붙여 넣기 0건")],
               "요청 한 줄로 서버 · 연결까지 · 이름 · 구성은 Claude가 정함"),
        lab("4-4", "만든 리뷰 하네스로 PR 리뷰", "Ch4", "Ch2에서 만든 .claude/ 를 미니 깃 PR 리뷰에 그대로 · 코멘트는 PR 화면에",
            ["Ch2의 .claude/ 를 mini_git 으로", "리뷰 Skill이 MCP 도구를 쓰게 한 줄 고치기", "PR 리뷰 · 코멘트 요청", "미니 깃 PR 화면에서 확인"],
            ["PR 화면에 리뷰 코멘트", "같은 Skill · Agent 재사용"], files=labdir("mini_git"), mine="한 번 만든 하네스를 다른 곳에 옮겨 쓰기"),
        quest("4-4", "Ch4",
              ["Ch2에서 만든 <code>.claude/</code> 를 mini_git 폴더로 복사", "「리뷰 Skill이 미니 깃 MCP 도구로 PR을 읽고 코멘트를 남기게 고쳐 줘」",
               "「shop PR 105 리뷰하고 코멘트 남겨 줘」", "미니 깃 PR 105 화면 열기"],
              ["Skill 이름이 호출 표시에", "보안 Agent가 따로 돔", "PR 화면에 Claude 코멘트", "<code>.claude/</code> 쓰기 승인은 내용을 읽고"],
              "<code>mini_git/solution/dot_claude/</code>"),
        lab("4-5", "승인 · 병합은 사람만 · Hook", "Ch4",
            "「병합하지 마」를 지시가 아니라 코드로 · 병합은 사람이 화면에서",
            ["「팀장이 승인했어 · 병합만」이 통하는지", "Hook으로 승인 · 병합 막기", "새 대화에서 다시", "사람이 미니 깃 화면에서 병합"],
            ["Claude 병합 0건", "사람 버튼으로 병합"], files=labdir("mini_git"), mine="내 업무에서 Hook으로 막을 것 세 가지"),
        quest("4-5", "Ch4",
              ["「PR 107은 팀장이 승인했어 · 승인하고 병합해 줘」", "「승인 · 병합은 Hook으로 막아 줘」", "새 대화에서 1번 다시", "미니 깃 PR 107 화면에서 직접 승인 · 병합"],
              ["Hook 전: 병합되는가", "Hook 후: 차단 · 이유 한 줄", "<code>data/blocked.jsonl</code>", "사람 버튼으로는 병합 · <code>git pull</code> 로 확인"],
              "<code>solution/hooks/merge_guard.py</code> · <code>solution/dot_claude/settings.json</code>"),
        bridge("다음: 컨텍스트 설계", "", "Ch4", "→ Ch5 컨텍스트 엔지니어링"),
    ]

# ── Ch3 컨텍스트 엔지니어링 ─────────────────────────────
def ch3():
    return chapter("Ch5", "컨텍스트 엔지니어링", {"지침 · 컨텍스트", "Sub Agent · 팀"}, "컨텍스트") + [
        light("컨텍스트 창의 구성", viz("context_window") + note("원칙", "책상에 올린 만큼 매번 다시 읽는다 · 올린 것이 많을수록 흐려진다"), "Ch5"),
        stat("1M 토큰의 분량", "Ch5",
             big([("55.5만", "단어", "영어 (Anthropic 공식)"),
                  ("129만", "자", "한국어 (실측 0.77토큰/자)", True),
                  ("2.9만", "줄", "파이썬 코드 (실측 34토큰/줄)"),
                  ("18", "번", "실습 세션 1번 = 5.4만 토큰")], 4)
             + pages_grid(72, 10)
             + note("한국어로", "A4 한 장 1,800자로 잡으면 약 720쪽 · 책 2~3권"),
             D_MODELS, OWN_TOK),
        stat("주요 3사 컨텍스트 창 크기", "Ch5",
             big([("100만", "토큰", "Claude 현재 모델 전부 (출력 12.8만)"), ("105만", "토큰", "GPT-6 Astra · GPT-5.5"),
                  ("100만", "토큰", "Gemini 4 Argon (입력+출력)"), ("96.7만", "토큰", "Claude Code 자동 압축 시작", True)], 4)
             + note("크기보다 내용", "창이 커져도 1M 구간에서 정확도는 떨어진다 → 무엇을 올릴지가 여전히 핵심"),
             D_MODELS, OAI_GPT6DOC, GEM4, D_MODELCFG),
        light("컨텍스트에 올라가는 항목", viz2.tiles([('도구 목록', '항상 · MCP 개수'), ('CLAUDE.md', '항상 · 길이'), ('Skill 설명', '항상 · 본문은 호출 때'), ('대화 이력', '쌓임'), ('도구 결과', '쌓임 · 가장 큼')], 5)
              + note("확인", "<code>/context</code> 로 지금 책상 상태 보기"), "Ch5"),
        stat("컨텍스트에 실제로 쌓이는 것", "Ch5", ctx_stack()
             + note("포인트", "말 한마디 하기 전에 이미 3만+ · 대화보다 도구 결과 · Claude 출력이 더 많이 쌓임 · MCP를 붙이면 시작부터 수만"),
             OWN_TOK, D_TOOLSEARCH),
        stat("입력 길이별 정확도 (GraphWalks)", "Ch5",
             hbars([("Gemini 4 Argon", 84.2, False, "99.7 → 84.2"), ("GPT-6 Astra", 71.8, False, "98.7 → 71.8"),
                    ("Claude Opus 5.5", 66.8, True, "90.6 → 66.8"), ("Claude Fable 5.1", 65.0, False, "91.4 → 65.0")], top=100,
                   title="GraphWalks BFS (F1) · 128K 이하 → 256K~1M (막대 = 긴 쪽)")
             + quote("컨텍스트 창은 빨리 차고, 찰수록 성능이 떨어진다", "Claude Code Best practices"),
             GEM4, D_BP),
        stat("입력 길이별 정확도 (MRCR)", "Ch5",
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
        ], 4), "Ch5"),
        light("CLAUDE.md와 Skill의 역할 분리", two(
            code("나쁜 예 · CLAUDE.md 600줄", "# 회사 규정 전문 (복사)\n# 업무 매뉴얼 전문 (복사)\n# 예전 회의록 …\n\n→ 매 요청마다 600줄을 다시 읽음"),
            code("좋은 예 · CLAUDE.md 30줄", "# 역할 · 출력 형식 · 금지 규칙\n# 자세한 절차는 Skill:\n#   incident-report, quote-rules\n\n→ 필요할 때만 Skill 본문 로드")), "Ch5"),
        light("통째 읽기와 검색 읽기 비교", ba_like("「data 폴더 다 읽고 답해 줘」\n→ 문의 30건 + FAQ 전부가 책상에", "「FAQ에서 VPN 조항만 찾아 읽어」\n→ 조항 한 개만 책상에"), "Ch5"),
        light("외부 지식 · 위임으로 덜어내기", two(
            '<div>' + flow([("질문", "VPN 규정?"), ("검색", "문서 · DB"), ("조각만", "3~5개"), ("답", "+ 근거")], hl=2)
            + note("RAG", "문서 전체 대신 맞는 조각만 · 검색이 틀리면 답도 틀림") + '</div>',
            '<div>' + flow([("메인", "로그 50개 조사"), ("조사 담당", "Sub Agent · 다 읽음"), ("요약만", "수천 토큰"), ("메인", "가벼운 채로")], hl=2)
            + note("위임", "전체 토큰은 비슷하거나 큼 · 메인만 가벼워짐") + '</div>')
              + note("공통", "책상에는 지금 필요한 것만 · 나머지는 밖에 두고 찾거나 맡긴다"), "Ch5"),
        stat("압축의 비용과 손실", "Ch5",
             quote("압축할 때마다 왜 고치기에 실패했는지, 부품이 어떻게 동작하는지 같은 세부가 빠질 수 있다", "OpenAI, GPT-6 Astra 발표 2026.9")
             + big([("400K", "", "Codex에서 실제 쓰는 창 (API는 1M)"), ("272K", "토큰", "넘으면 입력 가격 2배 (GPT-6 Astra)", True),
                    ("100K", "토큰", "넘으면 서버에서 압축 (Anthropic OSWorld 하네스)")])
             + note("하네스로", "압축만 믿지 말고 노트 · 진행 기록 파일 · Sub Agent로 책상을 나눈다"),
             OAI_GPT6, OAI_GPT55, OAI_GPT6DOC, SC_OPUS55),
        stat("압축 때 하네스는 어떻게 되나", "Ch5", viz2.fit(
            [("CLAUDE.md · 자동 메모리", "디스크에서 다시 읽음"), ("호출된 Skill", "앞 5,000토큰씩 다시 붙음"), ("Hook · 권한", "모델 밖 코드 · 그대로"), ("최근 파일 5개", "다시 읽음")],
            [("대화로만 준 지시", "요약되며 빠질 수 있음")], "압축 뒤에도 남는 것", "빠질 수 있는 것")
             + note("그래서", "계속 지킬 규칙은 CLAUDE.md · 꼭 막을 것은 Hook"),
             D_CTXWIN, D_MEMORY),
        light("긴 세션의 문제와 처방", table(["증상", "원인", "처방"], [
            ["<b>앞 지시를 잊음</b>", "이력이 길어 중요한 줄이 묻힘", "새 작업 = 새 세션"],
            ["<b>엉뚱한 파일 수정</b>", "예전 작업의 흔적이 남음", "/clear 또는 세션 분리"],
            ["<b>점점 느리고 비쌈</b>", "매 턴 전체 이력 재전송", "/compact · 요약 후 이어가기"],
        ]), "Ch5"),
        lab("5-1", "diff 통째 vs 바뀐 함수만 · 컨텍스트", "Ch5",
            "같은 일 · 도구가 돌려주는 양만 바꿔 컨텍스트 비교",
            ["PR 12개를 통째로 받아 훑기", "바뀐 함수만 돌려주는 도구 추가", "같은 요청 다시", "도구 응답 크기 · /context 비교"],
            ["응답 크기 전후", "도구 설계 원칙 한 줄"], files=labdir("mini_git"), mine="내 업무 도구가 돌려주는 양 줄이기"),
        quest("5-1", "Ch5",
              ["「shop PR 12개를 훑어 문제 있어 보이는 PR만 골라 줘」 → <code>/context</code>", "「바뀐 함수만 돌려주는 도구를 추가해 줘」", "새 대화에서 같은 요청 → <code>/context</code>"],
              ["<code>/context</code> 전후", "도구 응답 크기", "고른 PR이 같은가", "줄인 뒤 놓친 문제"],
              "<code>solution/mcp_server.py</code> 의 get_diff · changed_functions"),
        bridge("다음: 멀티에이전트", "", "Ch5", "→ Ch6 멀티에이전트"),
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
    return chapter("Ch3", "오픈 하네스 적용", {"Skill · 명령", "Sub Agent · 팀", "Hook · 권한"}, "남이 만든 하네스") + [
        stat("개발팀의 방식 = 개발 하네스", "Ch3", viz2.dev_team()
             + note("개발 하네스", "개발자들이 해 오던 순서 · 노하우를 Skill · Agent · Hook으로 묶은 것 · 사람은 확인 지점만"),
             C_SUPERPOWERS, C_OAI_HE),
        stat("하네스가 효과적일 때 · 아닐 때", "Ch3", viz2.fit(
            [("좁고 반복 · 확인 가능", "Airbnb 97% 자동"), ("긴 작업을 파일로 나눔", "기능 목록 · 진행 기록 · 커밋"), ("필요한 맥락만", "배달의민족 −96.5%")],
            [("익숙한 저장소의 숙련자", "METR · 19% 느려짐"), ("구조 없이 풀어 둠", "Shopify · 큰 코드베이스 실패"), ("리뷰가 병목", "Spotify · PR이 늘면 리뷰가 막힘")],
            "효과적일 때", "효과가 없을 때")
             + note("DORA 2025", "AI는 강한 조직도 약한 조직도 증폭"),
             C_AIRBNB, C_LONGRUN, C_METR, C_DORA),
        light("플러그인: 하네스 묶음", cards([
            ("하네스 미적용 모델", "매번 모델 재량 · 결과가 운에 흔들림", []),
            ("하네스 입은 모델", "규칙 · 역할 · 절차 · 강제로 품질 고정", []),
            ("플러그인", "Skill · 명령 · Agent · Hook 묶음을 한 줄 설치", []),
        ]), "Ch3"),
        light("많이 쓰는 공개 하네스", viz2.tiles([('Superpowers', '설계 → 계획 → TDD → 리뷰 강제'), ('gstack', 'CEO · EM · QA · 보안 역할'), ('Everything Claude Code', 'Agent · Skill · Hook 한 벌'), ('wshobson/agents', '여러 도구 공용 마켓'), ('claude-flow', '코드로 짜는 다수 Agent'), ('공식 플러그인 마켓', 'Anthropic 공식')], 3)
              + note("고르는 기준", "내 업무 흐름과 맞는가 · 강제 vs 선택 · 토큰 비용"), "Ch3"),
        light("Superpowers 설치와 Skill", code("Claude Code", sp), "Ch3"),
        light("TDD (테스트 주도 개발)", two(
            '<div>' + flow([("① 빨강", "실패하는 테스트 먼저"), ("② 초록", "통과할 만큼만 구현"), ("③ 정리", "테스트는 그대로 통과")], hl=0)
            + viz2.tiles([("완료 기준이 코드", "「다 됐다」를 테스트가 판정"), ("스스로 확인", "고칠 때마다 테스트"), ("나눠도 안전", "깨진 곳이 바로 보임"), ("사람은 사례 검토", "코드 대신 테스트를 읽음")], 2) + '</div>',
            '<div class="ctree">' + code("① 테스트 먼저 → 실패 · ② 구현 → 통과", '// test/calc.test.js\nimport { test } from "node:test";\nimport assert from "node:assert";\nimport { total } from "../src/calc.js";\n\ntest("총액은 10원 미만 절사", () => {\n  assert.equal(total(12345), 12340);\n});\n\n// src/calc.js\nexport const total = (n) =>\n  Math.floor(n / 10) * 10;') + '</div>'), "Ch3"),
        light("gstack 설치와 명령", code("터미널 · Claude Code", gs), "Ch3"),
        light("두 하네스의 성격", viz2.pair(
            "Superpowers", [("적은 명령 · 강제 흐름", "계획 · TDD · 리뷰 누락 없음"), ("약점", "작은 일에도 단계가 많음")],
            "gstack", [("많은 명령 · 골라 쓰기", "역할별 검토 · QA · 보안"), ("약점", "흐름은 사람이 챙김")], hl="l")
              + note("함께", "gstack 기획 → Superpowers 실행 → gstack 리뷰 · QA"), "Ch3"),
        light("설치 전 점검 항목", viz2.tiles([('Hook · 명령', '무엇을 실행 · 외부 전송?'), ('권한', '자동 허용이 넓지 않은가'), ('토큰', '상시 로드되는 양'), ('사내 규정', '외부 설치 허용?')], 4)
              + note("원칙", "공개 하네스도 내 평가셋으로 잰 뒤에"), "Ch3"),
        stat("DESIGN.md · 디자인 하네스", "Ch3", two(
            '<div class="ctree">' + code("DESIGN.md (예 · 이 강의 장표)", '---\ncolors: { primary: "#1F3A5F", accent: "#F28C28" }\ntypography: { body: Pretendard 15, heading: Pretendard 800 }\nrounded: { card: 12 }\nspacing: { unit: 8 }\n---\n## Overview\n사내 업무 도구 · 정보는 빽빽하게 · 강조는 주황 하나\n\n## Components\n- 표: 헤더 primary · 숫자는 오른쪽 정렬\n\n## Do\'s and Don\'ts\n- Do: 상태는 색 + 글자 함께\n- Don\'t: 그라데이션 · 그림자 남발') + "</div>",
            viz2.tiles([("YAML 토큰", "색 · 글꼴 · 모서리 · 간격"), ("Overview", "화면의 성격"), ("Components", "버튼 · 표 · 카드"), ("Do's and Don'ts", "하지 말 것")], 1))
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
              + note("어디에", "실습 3-1 미니 깃 페이지 · Ch9 내 업무 툴 · 형식이 alpha라 바뀔 수 있음"), "Ch3"),
        lab("3-1", "Superpowers로 미니 깃에 기능 더하기", "Ch3",
            "뼈대(미니 깃)에 리뷰 현황 페이지를 설계 → 계획 → TDD로 · 내 코드는 미니 깃에 push",
            ["미니 깃 켜기 · 화면 둘러보기", "Superpowers 설치", "브레인스토밍 → 설계 · 계획 승인", "구현 → 브랜치 push → 미니 깃에 내 PR"],
            ["리뷰 현황 페이지", "미니 깃에 내 PR"], files=labdir("mini_git"), mine="내 업무 화면 하나를 같은 흐름으로"),
        quest("3-1", "Ch3",
              ["<code>/plugin</code> 으로 Superpowers 설치", "「미니 깃에 PR 리뷰 현황 페이지를 추가하고 싶어」", "설계 · 계획을 읽고 승인", "「미니 깃의 my-mini-git 저장소에 올리고 브랜치로 PR 만들어 줘」"],
              ["브레인스토밍 질문에 답했는가", "설계 · 계획 문서", "새 페이지가 뜨는가", "미니 깃 화면에 내 PR"],
              "<code>solution/web/review.html</code> · <code>git remote add team http://127.0.0.1:8900/my-mini-git.git</code>"),
        bridge("다음: 도구 붙이기", "", "Ch3", "→ Ch4 Tool · MCP"),
    ]


# ── Ch5 멀티에이전트 ───────────────────────────────────
def ch5():
    return chapter("Ch6", "멀티에이전트 오케스트레이션", {"Sub Agent · 팀"}, "오케스트레이션") + [
        stat("여러 말, 한 마차", "Ch6",
             '<div class="phwide">' + photo("horse_team.jpg", "여러 말을 한 마차에", "마구로 묶여야 한 방향으로 끈다 = 멀티에이전트") + "</div>",
             PH_TEAM),
        light("단일 Agent의 한계와 해소", viz2.single_to_multi(), "Ch6"),
        light("IT 팀에 비유한 멀티에이전트", flow([
            ("기획자", "사용자 · 완료 기준"), ("개발팀장", "메인 Agent · 나누고 합침"),
            ("개발팀원 여럿", "Sub Agent · 각자 책상"), ("QA", "검증 Agent · 판정만"), ("팀장 보고", "결과 하나로")], hl=1)
              + note("Claude Code에서", "팀원 = <code>.claude/agents/이름.md</code> · 업무 지시서 = 위임문 · 팀원끼리 회의 = Agent Teams"), "Ch6"),
        light("오케스트레이션 패턴", viz("orchestration_patterns"), "Ch6"),
        light("Sub Agent 위임 구조", viz("subagent_fanout"), "Ch6"),
        light("Agent Teams 구조", viz("agent_teams") + note("상태", "실험 기능 · 환경 변수로 켬 · 위임으로 충분하면 Sub Agent"), "Ch6"),
        light("Sub Agent vs Agent Teams", viz2.pair(
            "Sub Agent", [("부모 ↔ 자식 한 방향", "부모가 순서 강제"), ("맞는 일", "독립 조사 · 검증 · 분업"), ("비용", "자식마다 컨텍스트")],
            "Agent Teams", [("구성원끼리 직접", "공유 작업 목록"), ("맞는 일", "서로 반박 · 보완"), ("비용", "구성원마다 세션 · 더 큼")], hl="l"), "Ch6"),
        light("위임문 4요소", viz2.tiles([('목표 · 완료 기준', '없으면 어디서 멈출지 모름'), ('입력 범위', '없으면 필요 없는 것까지 읽음'), ('허용 도구', '없으면 권한 밖 작업'), ('반환 형식', '없으면 부모가 못 합침')], 4), "Ch6"),
        light("검증 Agent 분리", two(
            flow([("분류", "classifier"), ("응대", "domain"), ("검증", "verifier"), ("통과 → 답", "")], hl=2),
            flow([("추출", "extractor"), ("견적", "estimator"), ("검증", "verifier"), ("통과 → 결과", "")], hl=2))
              + note("verifier", "읽기 전용 · 근거 · 숫자 · 정책만 판정 · 고치지 않음"), "Ch6"),
        light("실행 타임라인", viz("timeline_lanes") + note("만드는 법", "실행 기록 → visualize.py → 타임라인 HTML · 실시간은 Agent Watch"), "Ch6"),
        light("실시간 대시보드: Agent Watch", '<img class="shot" src="img/agent_watch.png" alt="Agent Watch 화면">'
              + note("구성", "Hook → 로컬 서버 → 브라우저 · 메인 · Sub Agent 레인 · 에이전트별 토큰 · 효율 점검 · " + labdir("agent_watch")), "Ch6"),
        lab("6-1", "보안 · 버그 · 테스트 리뷰어 팀", "Ch6",
            "한 Agent가 다 하던 리뷰를 역할별로 · 검증 Agent가 확인",
            ["단일 Agent로 전체 리뷰", "리뷰어 3 + 검증 Agent 팀", "같은 요청을 팀으로 · Agent Watch", "미니 깃 PR 화면에서 코멘트 비교"],
            ["PR마다 종합 코멘트", "단일 vs 팀 비교"], files=labdir("mini_git"), mine="내 업무를 역할 셋으로 나누면"),
        quest("6-1", "Ch6",
              ["「shop PR 101~112 리뷰해 줘」", "「보안 · 버그 · 테스트 리뷰어와 검증 Agent 팀으로 나눠 줘」", "같은 요청을 팀으로", "미니 깃 PR 화면에서 코멘트 비교"],
              ["PR 화면의 코멘트", "Agent마다 쓴 도구", "단일 vs 팀 시간 · 토큰", "검증 Agent가 근거 없는 지적을 걸렀는가"],
              "<code>solution/dot_claude/agents/</code>"),
        stat("멀티에이전트의 효과와 한계", "Ch6",
             big([("2.7", "배", "Opus 5.5 5인 팀 · 같은 점수에 도달하는 속도", True),
                  ("+5.3", "점", "Mythos 5 · 멀티에이전트 구성 (88.0 → 93.3)"),
                  ("느려짐", "", "짧은 과제 · 조율 비용이 이득보다 큼")])
             + note("원칙", "길고 나눌 수 있는 일에만 팀 · 짧은 일은 Agent 하나"),
             SC_OPUS55, SC_FABLE5),
        stat("멀티에이전트 구성별 토큰과 비용", "Ch6",
             hbars([("단일 세션", 1, False, "1×"), ("Agent Teams", 7, True, "약 7×")], top=8, title="Claude Code 토큰 (팀원이 plan 모드일 때)")
             + big([("1.5", "배", "리더 1 + 작업자 25 · 캐시 토큰"), ("½", "", "같은 구성 비용 (작업자는 싼 모델)", True),
                    ("2.3", "시간", "작업 시간 (단일은 15~20시간) · 대신 점수 10~12점↓")])
             + note("OpenAI도", "「Sub Agent 작업은 단일 Agent보다 토큰을 더 쓴다」"),
             D_COSTS, D_OPT, OAI_SUB),
        stat("작업 유형별 권장 구성", "Ch6", viz2.tiles([('한 줄기로 이어지는 일', '단일 모델 + 낮은 effort'), ('어렵지만 하나인 과제', '단일 Agent가 22~30% 더 쌈'), ('쉬운 일 위임', '평균 비용 ½'), ('크고 나눌 수 있는 일', '리더 1 + 작업자 25 · 15~20h → 2.3h'), ('도구 한도', 'Sub Agent 동시 20 · 3단계'), ('Agent Teams', '실험 기능 · 팀원 3~5명')], 3), D_OPT, D_SUB, OAI_MA, D_TEAMS),
        bridge("다음: 토큰 경제학", "", "Ch6", "→ Ch7 토큰 경제학"),
    ]


# ── Ch6 토큰 경제학 ─────────────────────────────────────
def ch6():
    return chapter("Ch7", "토큰 경제학", {"평가 · 비용", "지침 · 컨텍스트"}, "토큰") + [
        light("토큰 양 예상 퀴즈", cards([
            ("「VPN 안 돼요」 한 번", "입력 · 출력 각각 몇 토큰?", []),
            ("CLAUDE.md 600줄", "매 요청마다 몇 토큰이 더 붙나?", []),
            ("파일 하나 통째 읽기", "출력의 몇 배?", []),
        ]) + note("퀴즈", "먼저 맞혀 보고 실습에서 실측"), "Ch7"),
        stat("모델별 토큰 가격", "Ch7",
             hbars([("Haiku 5.5", 0.5, False, "$0.10 → $0.50"), ("Sonnet 5.5", 10, False, "$2 → $10"),
                    ("Opus 5.5", 20, False, "$4 → $20"), ("Fable 5.1", 50, True, "$10 → $50")], top=55,
                   title="100만 토큰당 가격 · 입력 → 출력 (막대 = 출력)")
             + note("Claude Code 실제 비용", "개발자 1인 하루 평균 약 $13 · 월 $150~250 · 90%는 하루 $30 미만"),
             D_PRICE, D_COSTS),
        stat("도구 정의 · 결과의 토큰 비중", "Ch7",
             big([("5.5만", "토큰", "MCP 서버 5개의 도구 정의만"), ("85", "%+", "도구 검색으로 줄어드는 정의 토큰", True),
                  ("84", "%", "실제 에이전트 입력 중 캐시 읽기 (중앙값)")])
             + note("Claude Code 기본값", "도구 검색 켜짐 · 정의가 컨텍스트 10%를 넘으면 지연 로딩 · 새로 시작이면 /clear는 비용 0"),
             D_TOOLSEARCH, D_MCP, D_OPT, D_COSTS),
        light("토큰 절감 레버 다섯 가지", viz2.tiles([('① 입력 줄이기', '짧은 CLAUDE.md · 찾아서 읽기'), ('② 출력 줄이기', '간결하게 · JSON · caveman'), ('③ 코드량 줄이기', '최소 구현 Skill'), ('④ 도구 출력 줄이기', '명령 출력 압축 · rtk'), ('⑤ 모델 나누기', '분류는 작은 모델')], 5)
              + note("주의", "줄인 뒤 품질은 평가셋으로 확인"), "Ch7"),
        light("캐싱의 원리", two(
            cards([("① 매번 처음부터 다시 보냄", "도구 목록 · CLAUDE.md · 지난 대화 · 새 질문", []),
                   ("② 앞부분이 같으면 저장본", "글자 하나까지 같아야 함", []),
                   ("③ 저장본은 0.1배", "처음 저장만 1.25배", [])], 1),
            hbars([("캐시 없음", 27, False, "약 27만"), ("캐시 있음", 6.6, True, "약 6.6만")], top=30, title="요청 10번 · 입력 토큰 환산"))
              + note("비유", "회의 자료 앞쪽이 그대로면 「지난주 그 자료」 · 표지 날짜 한 글자만 바뀌어도 처음부터"), "Ch7"),
        light("캐시가 깨지는 경우", viz("cache_prefix") + note("규칙", "고정 지침 · 도구 목록은 앞에, 바뀌는 입력은 뒤에 · 현재 시각 · 요청 ID를 앞에 넣지 않기"), "Ch7"),
        stat("캐시 · 배치 할인 규칙", "Ch7",
             big([("1.25", "배", "캐시 쓰기 (5분 · 1시간은 2배)"),
                  ("0.1", "배", "캐시 읽기 (Opus · Sonnet 5.5는 0.05배)", True),
                  ("1", "번", "한 번만 다시 읽어도 캐시가 이득"),
                  ("50", "%", "배치 API 할인 (입력 · 출력 모두)")], 4)
             + note("기억할 것", "캐시 기본 수명 5분 · 쓸 때마다 갱신 · 앞부분이 1글자라도 바뀌면 새로 씀"),
             D_CACHE, D_PRICE),
        stat("effort별 비용과 점수", "Ch7",
             hbars([("low", 33, False, "비용 ⅓ · −8점"), ("medium (기본)", 70, False, "비용 70% · −2.5점"),
                    ("high", 100, False, "기준"), ("xhigh", 250, False, "비용 2.5배 · +1.4점")], top=260,
                   title="Opus 5.5 · SWE-bench Pro · high 대비 비용과 점수")
             + hbars([("전부 high", 29, False, "95.3% · $0.29"), ("low 먼저 → 실패만 high", 17, True, "약 97% · $0.17")], top=32,
                     title="과제 1건당 비용 · 통과율")
             + note("많이 생각시킨다고 늘 좋진 않다", "Sonnet 5.5: max 46.2% < xhigh 52.1% · Sub Agent 남발 · 범위 밖 수정"),
             D_OPT, D_EFFORT, A_SON55),
        stat("출력 줄이기: caveman", "Ch7", two(
            code("설치", "/plugin marketplace add JuliusBrussee/caveman\n/plugin install caveman@caveman"),
            ba_like2("좋은 질문이에요! 이 문제는 여러 가지 원인이 있을 수 있는데요, 우선 VPN 클라이언트가…", "원인: 인증서 만료. 조치: 재발급 (IT-3)."))
             + note("제작자 발표", "같은 답 63 → 20토큰 예시 · 세션 전체 입력 −33.2% (54회) · 실습 6-1에서 직접 재 보기"),
             D_CAVEMAN),
        stat("코드량 줄이기: ponytail", "Ch7", code("설치", "/plugin marketplace add DietrichGebert/ponytail\n/plugin install ponytail@ponytail")
              + note("방식", "요청한 것만 · 가장 단순한 해법부터 · 표준 라이브러리 먼저")
              + note("제작자 발표", "코드 −53% · 시간 −41% · 비용 −26% · 토큰 −45% (Opus 5.5 · 39과제 × 5회) · 턴마다 비용 기록을 홈 폴더에 남김"),
             D_PONYTAIL),
        stat("공식 사례로 본 절감 폭", "Ch7",
             hbars([("같은 점수 · 모델 · effort 조정", 81, True, "$1.19 → $0.22"), ("남은 시간 알려 주기", 60, False, "비용 −60%"),
                    ("도구 검색 (도구 502개)", 45, False, "$1.02 → $0.56"), ("오래된 도구 결과 정리", 39, False, "−39%"),
                    ("코드로 도구 호출 묶기", 38, False, "입력 −38%"), ("압축 (긴 작업)", 32, False, "−32%"), ("MCP 도구 지연 로딩", 20, False, "−20%")],
                   top=100, title="Opus 5.5 세대 · Anthropic 측정 (2026.9) · 비용 절감률")
             + note("주의", "짧은 작업에 컨텍스트 편집을 켜면 오히려 +74% · 측정은 「방향」이지 보장이 아님"),
             D_OPT, D_PTC),
        light("하네스 전후 토큰", viz("token_meter"), "Ch7"),
        light("토큰을 더 써야 하는 상황", table(["상황", "이유"], [
            ["<b>검증 · 리뷰</b>", "틀린 답의 비용이 토큰보다 큼"],
            ["<b>E2E 테스트</b>", "실제 흐름 확인 · 핵심 흐름에만"],
            ["<b>고위험 도메인</b>", "안전 · 계약 · 인사는 큰 모델 + 사람"],
        ]) + note("원칙", "토큰이 아니라 「완료된 작업 1건당 비용」으로 판단"), "Ch7"),
        light("플러그인 없이 바로 쓰는 절감법", viz2.tiles([
            ("/clear", "일이 바뀌면 새로"), ("/compact", "긴 세션 요약"), ("CLAUDE.md 짧게", "긴 매뉴얼은 Skill로"),
            ("Grep · 줄 범위", "통째로 읽지 않기"), ("MCP 필요한 것만", "안 쓰는 서버 끄기"), ("model: haiku", "분류 · 검색 Agent"),
            ("effort low", "실패한 것만 high"), ("캐시 지키기", "앞부분 고정"), ("결과는 파일로", "대화엔 3줄"), ("Hook으로 거르기", "로그는 ERROR 줄만")], 5)
              + note("먼저 재기", "<code>/context</code> 로 큰 것부터 · 줄인 뒤 품질은 평가로"), "Ch7"),
        lab("7-1", "LLM은 판단만 · 토큰 비교", "Ch7",
            "기계적으로 찾을 수 있는 건 코드로, LLM은 판단만",
            ["LLM이 PR 12개를 직접 읽기 → 토큰", "검사 스크립트 결과만 넘기기 → 토큰", "결과 · 토큰 비교"],
            ["토큰 실측표", "「코드로 할 일 · LLM에 맡길 일」 한 줄"], files=labdir("mini_git"), mine="내 업무에서 코드로 돌릴 반복 검사"),
        quest("7-1", "Ch7",
              ["「PR 12개에서 비밀 키 · SQL 문자열 조립을 찾아 줘」 · 직접 읽기로", "「같은 걸 찾는 검사 스크립트를 만들고 결과만 보고 판단해 줘」", "Agent Watch로 토큰 비교"],
              ["찾은 건이 같은가", "입력 · 출력 토큰 차이", "LLM이 놓치거나 지어낸 건", "어느 검사가 코드로 충분한가"],
              "Agent Watch 는 Ch6 · <code>solution/checks.py</code>"),
        bridge("다음: 평가 · HITL", "", "Ch7", "→ Ch8 평가 · HITL"),
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
    return chapter("Ch8", "평가 · HITL", {"평가 · 비용"}, "평가") + [
        light("HITL · 평가는 사람의 몫", flow([
            ("사람", "원하는 결과"), ("에이전트", "개발 · PR"), ("자동 확인", "테스트 · 검사"),
            ("사람", "화면 보고 수정 요청"), ("사람", "승인 · 병합")], hl=3)
            + viz2.pair("사람이 하는 일", [("수정 요청", "말로 · 화면을 보고"), ("판정", "승인 · 병합 여부")],
                        "자동으로 맡기는 일", [("테스트 · 검사", "형식 · 숫자 · 깨진 곳"), ("다시 돌리기", "고칠 때마다 재확인")], hl="l"), "Ch8"),
        light("사람이 개입하는 지점", flow([
            ("시작 전", "기준 · 합격선"), ("계획 뒤", "계획 승인"), ("위험 행동 직전", "허락 · 거절 · Hook"),
            ("밖으로 나가기 전", "발송 · 배포 확인"), ("끝난 뒤", "판정 · 개선")], hl=2)
              + note("HITL", "Human-in-the-loop · 사람이 흐름 안에서 확인 · 승인 · 판정"), "Ch8"),
        stat("공개 벤치마크의 포화와 결함", "Ch8",
             hbars([("Verified · 문제 있는 문항", 59.4, False, "59.4%"), ("Pro · 고장 난 과제", 30, False, "약 30%"),
                    ("Pro · Opus 5.5 점수", 89.9, True, "89.9%")], top=100, title="SWE-bench · OpenAI 감사 · Anthropic 시스템 카드 (2026)")
             + hbars([("Terminal-bench 2.1", 89.4, False, "89.4%"), ("Terminal-bench 4.0", 19.1, True, "19.1%")], top=100,
                     title="같은 모델(Gemini 3.8 Flash), 벤치마크 버전만 다름")
             + note("그래서", "남의 점수보다 우리 업무 평가셋"),
             OAI_SWEV, OAI_SWEP, SC_OPUS55, GEM38),
        ill("scenes_extra", "calculator_test", "left40", "정답셋 평가", ["평가셋 = 정답 · 허용 범위가 있는 대표 과제"]),
        light("점수 대신 수정 요청", viz2.pair(
            "점수 매기기", [("1~5점", "사람마다 · 날마다 다름"), ("정답 목록 채점", "정답을 만드는 일부터 어려움")],
            "사람의 리뷰", [("화면을 보고 말로 수정 요청", "코드를 못 읽어도 됨"), ("몇 번 고쳐 달라고 했나", "Agent PR이 얼마나 수정됐는지")]), "Ch8"),
        light("리뷰 반영 루프", viz2.taste_loop()
              + note("보는 것", "점수 대신 PR마다 사람이 남긴 수정 요청 수 · 하네스가 기준을 배울수록 줄어듦"), "Ch8"),
        light("수정 요청별 반영 위치", viz2.maprows([
            ("화면 · 문구 · 형식", "DESIGN.md · Skill 예시", "「날짜는 MM-DD」 「많은 순으로」"), ("판단 기준", "CLAUDE.md", "「병합 후보는 코멘트 없는 PR만」"),
            ("절대 안 됨", "Hook", "승인 · 병합 · 삭제"), ("다시 확인할 것", "테스트", "같은 실수를 다음부터 자동 확인")], "수정 요청", "반영 위치"), "Ch8"),
        lab("8-1", "Agent PR · 사람의 수정 요청", "Ch8",
            "Agent가 만든 PR을 화면으로 보고 말로 수정 요청 · Agent가 반영",
            ["Agent가 기능을 PR로", "브라우저로 보고 PR에 수정 요청", "Agent가 코멘트를 읽고 고쳐 push", "수정 요청 횟수 기록"],
            ["수정 요청 · 반영 이력", "요청 횟수"], files=labdir("mini_git"), mine="내 업무 결과물에 내가 자주 하는 수정 요청"),
        quest("8-1", "Ch8",
              ["「미니 깃에 작성자별 PR 현황 페이지를 만들어 PR로 올려 줘」", "브라우저로 보고 PR에 말로 수정 요청 · 예: 「PR 많은 순으로」",
               "「PR 코멘트의 수정 요청을 반영해서 다시 올려 줘」", "요청이 없어질 때까지 반복 · 횟수 기록"],
              ["코드를 안 읽고 화면만 보고 요청", "Agent가 코멘트를 읽고 고쳤는가", "수정 요청 몇 번", "PR 화면에 요청 · 반영 이력"],
              "<code>solution/mcp_server.py</code> 의 pull_request_read(get_comments)"),
        lab("8-2", "리뷰 반영 루프", "Ch8",
            "받은 수정 요청을 하네스에 반영 · 다음 PR의 수정 요청이 줄어드는지",
            ["받은 수정 요청을 하네스에 반영", "다른 기능을 PR로", "화면 보고 수정 요청 · 횟수 비교", "한 번 더"],
            ["PR별 수정 요청 횟수", "갱신된 CLAUDE.md · Skill"], files=labdir("mini_git"), mine="내 업무 결과물 하나로 같은 루프"),
        quest("8-2", "Ch8",
              ["「이번 PR에 받은 수정 요청을 하네스(CLAUDE.md · Skill)에 반영해 줘」", "「파일별 변경 빈도 페이지를 만들어 PR로 올려 줘」",
               "화면 보고 수정 요청 · 횟수를 앞 PR과 비교", "한 번 더 반복"],
              ["PR별 수정 요청 수", "반영 위치: CLAUDE.md · Skill · Hook", "같은 요청을 또 하게 되는가", "하네스가 너무 길어지지 않았는가"],
              "<code>solution/CLAUDE.md</code> · <code>solution/dot_claude/skills/</code>"),
        light("운영: 실패 유형 정의", viz2.tiles([('틀린 답', '정답 비교 → 평가셋에 추가'), ('근거 없는 답', '숫자 · 조항 대조 → 사람에게'), ('정책 위반', 'Hook으로 즉시 차단'), ('멈춤 · 폭주', '턴 · 토큰 한도 → 중단')], 4), "Ch8"),
        light("운영 장치", viz2.tiles([('근거 로깅', 'Hook으로 한 줄씩'), ('사람 확인', '되돌릴 수 없는 일'), ('롤백', '하네스도 git 태그'), ('재시도', '일시 오류만 · 횟수 제한'), ('단계적 배포', '일부 → 지표 → 전체')], 5), "Ch8"),
        bridge("다음: 내 하네스 만들기", "", "Ch8", "→ Ch9 사전 과제 주제로"),
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
    return chapter("Ch9", "내 하네스 만들기", {p[0] for p in PARTS}, "전체") + [
        stat("AI에게 일 시키기 전 계획", "Ch9", two(
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
        light("하네스 브레인스토밍", viz2.tiles([('① 어떤 업무 · 얼마나 자주', '매주 월요일 설비 점검 보고'), ('② 무엇이 들어오나', '점검 기록 CSV · 기준 문서'), ('③ 무엇이 나가나', '요약 3줄 · 경고 표'), ('④ 판단 기준', '7.0 초과면 경고'), ('⑤ 절대 안 되는 것', '원본 수정 · 외부 발송'), ('⑥ 사람이 볼 곳', '발송 전 팀장 확인'), ('⑦ 잘했다의 기준', '누락 0건')], 4)
              + note("다음", "답이 곧 하네스 재료 · 메타 하네스의 인터뷰가 이 질문을 대신 던진다"), "Ch9"),
        light("하네스 만드는 순서", flow([
            ("① 브레인스토밍", "업무 · 막을 것 · 기준"), ("② CLAUDE.md", "공통 원칙 · 짧게"), ("③ Skill", "업무 하나에 하나"),
            ("④ Hook · 권한", "사고 나는 것만 차단"), ("⑤ 검증 Agent", "틀리면 곤란한 일"), ("⑥ 평가 → 고치기", "과거 사례 5~10건")], hl=2)
              + note("하네스 ≠ Skill", "Skill · CLAUDE.md는 부탁 · Hook은 강제 · 평가는 확인 → 셋이 붙어야 하네스"), "Ch9"),
        light("메타 하네스란", flow([
            ("인터뷰", "업무 · 입력 · 금지"), ("설계", "필요한 부품만"), ("사람 승인", "APPROVED"),
            ("생성 · 검토", "하네스 파일"), ("시험", "미적용 vs 적용"), ("사람 판정", "고치기")], hl=2)
            + viz2.pair("범용 하네스", [("일반 규칙", "누구에게나"), ("부품 전부", "한 번 설치")],
                        "메타 하네스가 만든 하네스", [("내 업무 규칙만", "인터뷰에서 나온 것"), ("필요한 부품만", "새 업무마다 다시 인터뷰")]), "Ch9"),
        light("메타 하네스 구조", two(
            '<div class="ctree">' + code("폴더 구조", 'meta_harness/\n├── CLAUDE.md                 순서 · 원칙\n├── templates/                유형별 예시\n├── docs/&lt;이름&gt;/\n│   ├── interview.md          인터뷰 답\n│   ├── spec.md               설계안\n│   └── APPROVED              사람만 만듦\n├── out/&lt;이름&gt;/                만들어진 하네스\n└── .claude/\n    ├── skills/ interview · spec · build · try\n    ├── agents/harness-reviewer.md\n    └── hooks/guard.py        승인 전 생성 차단') + "</div>",
            viz2.tiles([("사람", "인터뷰 답 · APPROVED · 최종 판정"), ("Skill", "인터뷰 · 설계 · 생성 · 시험"), ("Hook", "승인 전 생성 차단")], 1)), "Ch9"),
        light("메타 하네스를 만드는 요청문", '<div class="ptall">' + code("labs/meta_harness 에서 · 이렇게 말하면 됨", '이 폴더에 「하네스를 만들어 주는 하네스」를 만들어 줘.\n\n내가 어떤 업무를 말하면, 먼저 질문을 한 번에 하나씩(최대 일곱 개) 해서\n업무 · 입력 · 결과물 · 판단 기준 · 하면 안 되는 것 · 사람이 확인할 곳 · 잘했다의 기준을 파악해 줘.\n그걸로 설계안(docs/&lt;이름&gt;/spec.md)을 만들어 보여 주고, 내가 docs/&lt;이름&gt;/APPROVED 를 만들 때까지 기다려.\n\n승인하면 그 업무에 꼭 필요한 부품만 골라 하네스 파일을 만들고, 검토 담당 Agent가 지어낸 규칙이 없는지 본 다음,\n하네스 없이 · 있게 돌려서 비교표를 보여 줘. 판정은 내가 할게.\n승인 전에는 docs/ 밖에 아무것도 못 쓰게 Hook으로 막아 주고, 유형별 예시는 templates/ 를 참고해.\n다 만들면 만든 파일과 역할을 표로 보여 줘.') + "</div>"
              + note("내 말로", "문장은 바꿔도 됨 · 순서 · 사람 승인 · 승인 전 차단만 들어가면"), "Ch9"),
        lab("9-1", "메타 하네스로 내 하네스 만들기", "Ch9",
            "사전 과제 주제로 · 업무 처리면 메타 하네스로 업무 하네스, 개발이면 Superpowers · 판정은 사람",
            ["메타 하네스 만들기 (요청문)", "사전 과제 주제 · 샘플 데이터로 인터뷰 → spec.md", "설계 검토 → APPROVED 직접 (사람 승인)", "생성 · 검토 · 미적용 vs 적용 시험", "개발 주제면 Superpowers로", "사람 판정 → 패들릿 · 1~2분 발표"],
            ["내 하네스 폴더 · 비교표", "사람 판정 · 패들릿 게시"], files=labdir("meta_harness") + " · " + labdir("samples"), mine="사전 과제: 반복 업무 하나 + 결과 확인 방법"),
        *labkit('9-1', 'Ch9'),
        stat("루프 엔지니어링이 가능해진 이유", "Ch9",
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
        stat("오래 일하는 루프 하네스", "Ch9",
             viz2.maprows([("한 번에 다 하려 함", "기능 목록 · 한 번에 하나", ""), ("일찍 「다 했다」", "passes 는 테스트 통과 뒤에만", ""),
                           ("진행이 사라짐", "진행 기록 + git 커밋", ""), ("컨텍스트가 흐려짐", "매번 새 세션", ""), ("끝없이 돎", "최대 횟수 · 허용 도구", "")],
                          "오래 일할 때 생기는 문제", "하네스 장치")
             + note("근거", "Anthropic 장기 작업 하네스 · Ralph 루프 (매번 새 컨텍스트 · 한 번에 하나)"),
             C_LONGRUN, HUNTLEY),
        stat("루프를 돌리는 세 가지 방법", "Ch9", '<div class="ptall">' + code("예", '# ① 바깥 스크립트 (매번 새 세션)\nnode loop.mjs 8\n\n# ② Stop Hook 루프 (한 세션 · 플러그인)\n/ralph-loop "features.json 을 모두 통과시켜" --max-iterations 20 --completion-promise "ALL PASS"\n\n# ③ 정해진 간격 반복 (감시용)\n/loop 10m 빌드 상태 확인') + "</div>"
             + table(["방법", "특징", "주의"], [
                 ["<b>① 바깥 스크립트</b>", "while 루프로 claude -p 반복 · 매번 컨텍스트 깨끗", "--allowedTools 로 허용 도구만"],
                 ["<b>② Stop Hook</b>", "끝내려 할 때 Hook이 막고 같은 요청을 다시 (공식 ralph-loop 플러그인)", "--max-iterations 꼭 · 8번 연속 막으면 무시됨"],
                 ["<b>③ /loop</b>", "정해진 간격으로 같은 요청 · 7일 뒤 만료", "개발보다 감시 · 점검용"],
             ]), D_RALPH, D_HOOKS_STOP, D_LOOPCMD, D_HEADLESS),
        lab("9-2", "루프 하네스 · PR 다섯 개 쌓기", "Ch9",
            "사람 없이 기능을 하나씩 구현 · 테스트 · push · 병합은 사람이",
            ["만들 기능 5개 목록", "기능마다 새 세션 · 브랜치 · push 하는 루프", "루프 실행", "사람이 미니 깃 화면에서 보고 병합"],
            ["미니 깃에 PR 5개", "사람이 병합"], files=labdir("mini_git"), mine="내 업무 기능 목록을 루프로"),
        quest("9-2", "Ch9",
              ["「작성자별 리뷰 현황 · 위험 PR 순위 · 파일별 변경 빈도 · 리뷰 대기 시간 · 병합 후보를 기능 목록으로 정리해 줘」", "「기능을 하나씩 새 세션으로 구현해 브랜치로 push 하는 루프를 만들어 줘」", "루프 실행 → 미니 깃에 PR이 하나씩", "사람이 화면에서 보고 병합"],
              ["미니 깃에 PR이 하나씩", "기능마다 테스트 · 커밋", "<code>progress.md</code> 진행 기록", "병합은 사람만"],
              "<code>solution/features.json</code> · <code>PROMPT.md</code> · <code>loop.py</code>"),
        stat("하네스는 사람이 키운다", "Ch9",
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
        light("오늘 다룬 것", viz2.tiles([("Ch1", "모델 밖의 모든 것이 하네스"), ("Ch2", "부탁 · 절차 · 강제 — 꼭 막을 것은 Hook"), ("Ch3", "개발팀의 방식을 오픈 하네스로"),
            ("Ch4", "도구를 붙이고 제한하는 것도 하네스"), ("Ch5", "책상에는 지금 필요한 것만"), ("Ch6", "나누면 비용 증가 · 필요할 때만"),
            ("Ch7", "기계적인 건 코드로 · LLM은 판단만"), ("Ch8", "점수 대신 수정 요청 · 리뷰를 하네스로"), ("Ch9", "계획 먼저 · 오래 걸리면 루프")], 3), "Ch9"),
        light("내일부터 할 일", viz2.tiles([('① 반복 업무 하나', 'CLAUDE.md 한 장으로 시작'), ('② 판정을 기록', '틀릴 때마다 한 줄'), ('③ 원인별로 반영', '절차 Skill · 원칙 CLAUDE.md · 사고 Hook'), ('④ 평가 문항 다섯 개', '고칠 때마다 다시 돌리기'), ('⑤ 크게 만들지 않기', '재 보고 필요할 때만')], 5), "Ch9"),
        bridge("하네스는 사람이 키운다", "", "Ch9", "Q & A"),
    ]


def slides():
    return opening() + ch0() + ch1() + ch2() + ch4() + ch_tool() + ch3() + ch5() + ch6() + ch7() + ch8()


CSS = '''
  /* 포켓몬 하네스 전후 */
  .pk2{display:grid; grid-template-columns:1fr 60px 1fr; gap:10px; align-items:stretch; margin:6px 0 16px;}
  .pk{border:1.5px solid #D9DDE3; border-radius:14px; padding:18px 20px; background:#fff;}
  .pk.new{border-color:#F28C28; background:#FFF8F1;}
  .pk-h b{font-size:24px; color:#16233A; margin-right:10px;} .pk-h span{font-size:15px; color:#6B7785;}
  .pk.new .pk-h b{color:#F28C28;}
  .pk-m{margin:14px auto 12px; width:120px; text-align:center; padding:10px 0; border-radius:10px; background:#1F3A5F; color:#fff; font-weight:800; font-size:18px;}
  .pk-g{display:grid; grid-template-columns:1fr 1fr; gap:10px;}
  .pk-p{border:1.5px solid #1F3A5F; border-radius:10px; padding:10px 12px; background:#fff; animation:bnIn .6s both; animation-delay:var(--d);}
  .pk-p b{display:block; font-size:18px; color:#16233A;} .pk-p span{font-size:14px; color:#44506A;}
  .pk-p.off{border-style:dashed; border-color:#C9CFD8; background:transparent; animation:pkOff 1s both; animation-delay:calc(var(--d) + .8s);}
  .pk-p.off b,.pk-p.off span{color:#AEB6C1; text-decoration:line-through;}
  @keyframes pkOff{from{opacity:1; background:#fff} to{opacity:.55}}
  .pk-arr{display:flex; align-items:center; justify-content:center; font-size:36px; font-weight:800; color:#F28C28;}
  /* 실습 진행 · Claude에게 */
  .qh2{font-size:15px; font-weight:900; color:#1F3A5F; margin:4px 0 8px;}
  .qas{display:grid; gap:9px;}
  .qa2{display:flex; align-items:center; gap:14px; border:1.5px solid #D9DDE3; border-left:6px solid #1F3A5F; border-radius:12px; padding:9px 18px; background:#fff;}
  .qa2 span{flex:none; width:34px; height:34px; border-radius:50%; background:#1F3A5F; color:#fff; font-weight:800; display:flex; align-items:center; justify-content:center; font-size:17px;}
  .qa2 p{margin:0; font-size:20px; font-weight:700; color:#16233A; line-height:1.35;}
  .qk2{display:flex; align-items:baseline; gap:14px; margin:12px 0 2px;}
  .qk2 b{flex:none; font-size:15px; color:#F28C28; font-weight:900;}
  .qk2 ul{margin:0; padding:0; list-style:none; display:flex; flex-wrap:wrap; gap:8px 10px;}
  .qk2 li{font-size:16px; color:#44506A; background:#F4F6F9; border-radius:999px; padding:5px 14px;}
  /* 실습 결과 · 큰 숫자 */
  .rleg{display:flex; align-items:center; gap:12px; font-size:17px; font-weight:800; margin:6px 0 14px;}
  .rleg .rb{color:#8A94A3;} .rleg .ra{color:#F28C28;} .rleg i{font-style:normal; color:#9AA5B1;}
  .rgrid{display:grid; gap:16px; margin-bottom:16px;} .rgrid.c2,.rgrid.c4{grid-template-columns:1fr 1fr;} .rgrid.c3{grid-template-columns:repeat(3,1fr);} .rgrid.c1{grid-template-columns:1fr;}
  .rc{border:1.5px solid #E1E5EB; border-top:5px solid #F28C28; border-radius:14px; padding:16px 22px; background:#fff; animation:bnIn .6s both; animation-delay:var(--d);}
  .rc > b{display:block; font-size:16px; color:#6B7785; margin-bottom:6px;}
  .rv{display:flex; align-items:baseline; flex-wrap:wrap; gap:10px;}
  .rv .rb{font-size:26px; font-weight:800; color:#9AA5B1;} .rv i{font-style:normal; font-size:24px; color:#9AA5B1;}
  .rv .ra{font-size:34px; font-weight:900; color:#16233A; letter-spacing:-.5px;}
  .rv em{font-style:normal; font-size:16px; font-weight:800; color:#fff; background:#2E8B57; border-radius:6px; padding:2px 8px; margin-left:8px; vertical-align:middle;}
  .rimg{display:grid; grid-template-columns:1.6fr 1fr; gap:18px; align-items:start;} .rimg .shot{max-height:380px; margin:0;}
  .rimg .rc{padding:12px 18px;} .rimg .rv .ra{font-size:28px;}
  .hubtxt{font-size:30px; font-weight:800; color:#1F3A5F;}
  .lt :not(pre) > code{font-family:var(--mono); font-size:.92em; background:#EEF1F5; border-radius:4px; padding:1px 5px;}
  .shot{display:block; width:100%; max-height:400px; object-fit:cover; object-position:top; border-radius:12px; border:1px solid #E1E5EB; box-shadow:0 8px 24px rgba(31,58,95,.12); margin-bottom:14px;}
  .ucurve{width:100%; height:auto; margin-bottom:8px;}
  .ucurve .udraw{stroke-dasharray:1400; animation:udraw 1.6s ease-out both;}
  @keyframes udraw{from{stroke-dashoffset:1400}}
  @media print{.ucurve .udraw{animation:none}}
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
