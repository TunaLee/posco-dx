"""원리 애니메이션 — 타임라인 SVG (samsung-ds vizanim 의 _D 헬퍼를 posco-dx 색으로 옮김).

함수마다 인라인 <svg> 하나를 돌려준다. 본문 폭 1160 기준.
- 움직임: CSS keyframes · 「몇 % 시점에 무엇이」를 stops 로 적는다. 장면 설명은 once=True (한 번 재생 → 마지막 장면에 멈춤).
- 인쇄 · 동작 줄이기 설정에서는 멈추고 속성 기본값이 보인다 → 기본값을 마지막 장면으로 둔다.
- id · keyframes 이름은 함수마다 접두어를 따로 (숨은 장의 같은 id 충돌 방지).
"""
import math

N, G, O, W, S = "#16233A", "#D9DDE3", "#F28C28", "#FFFFFF", "#6B7785"
K, R, OK, BG = "#1F3A5F", "#C62828", "#2E7D32", "#F4F6F9"


class _D:
    """도해 하나: 접두어 · 길이(초) · keyframes 모음."""

    def __init__(self, p, dur, once=True):
        self.p, self.dur, self.kfs, self.n = p, dur, [], 0
        self.rep = "1 both" if once else "infinite both"

    def a(self, stops, ease="linear", extra=""):
        self.n += 1
        name = f"an{self.p}{self.n}"
        body = "".join(f"{p:g}%{{{d}}}" for p, d in stops)
        self.kfs.append(f"@keyframes {name}{{{body}}}")
        return f'style="animation:{name} {self.dur}s {ease} {self.rep};{extra}"'

    def show(self, t, end=None):
        """t% 에 나타나서 끝까지 (end 를 주면 그때 사라짐)."""
        st = [(0, "opacity:0"), (t, "opacity:0"), (t + 3, "opacity:1")]
        st += [(end, "opacity:1"), (end + 3, "opacity:0"), (100, "opacity:0")] if end else [(100, "opacity:1")]
        return self.a(st)

    def id(self, s):
        return f"an{self.p}{s}"

    def markers(self):
        def m(i, c):
            return (f'<marker id="{self.id(i)}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
                    f'orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="{c}"/></marker>')
        return m("k", K) + m("o", O) + m("r", R) + m("g", OK)

    def svg(self, w, h, body):
        r = f".an-{self.p}"
        base = (f"{r}{{width:100%;height:auto;max-height:470px;display:block;margin:0 auto;overflow:visible}}"
                f"{r} text{{dominant-baseline:middle}}"
                f"{r} .tt{{font-size:19px;font-weight:800;fill:{N}}}"
                f"{r} .ts{{font-size:15px;fill:{S}}}"
                f"{r} .to{{font-size:15px;font-weight:800;fill:#EF6C00}}"
                f"{r} .tw{{font-size:15px;font-weight:800;fill:{W}}}"
                f"{r} .tn{{font-size:15px;font-weight:700;fill:{N}}}"
                f"{r} .tm{{font-size:14px;font-weight:700;fill:{N};font-family:var(--mono,monospace)}}"
                f"@media print{{{r} *{{animation:none!important}}}}"
                f"@media (prefers-reduced-motion:reduce){{{r} *{{animation:none!important}}}}")
        return (f'<svg class="an an-{self.p}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
                f'<style>{base}{"".join(self.kfs)}</style><defs>{self.markers()}</defs>{body}</svg>')


def _t(x, y, s, cls="ts", anchor="middle", extra=""):
    return f'<text x="{x:g}" y="{y:g}" text-anchor="{anchor}" class="{cls}" {extra}>{s}</text>'


def _box(x, y, w, h, title, sub="", fill=W, stroke=K, sw=2.5, rx=14, cls="tt", extra=""):
    s = f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
    if sub:
        return s + _t(x + w / 2, y + h / 2 - 11, title, cls) + _t(x + w / 2, y + h / 2 + 14, sub, "ts")
    return s + _t(x + w / 2, y + h / 2 + 1, title, cls)


def _dot(d, pts, color=O, r=10, label=""):
    """pts: [(퍼센트, x, y, 보임 0/1)] 을 따라 움직이는 점."""
    stops = [(p, f"transform:translate({x:g}px,{y:g}px);opacity:{v}") for p, x, y, v in pts]
    lab = _t(0, -20, label, "to", extra='style="font-size:13px"') if label else ""
    return f'<g {d.a(stops)}><circle r="{r}" fill="{color}"/>{lab}</g>'


# ── 1 에이전트 루프 ─────────────────────────────────
def agent_loop():
    """모델은 다음 행동을 글로 씀 → 하네스가 실제로 실행 → 결과를 붙여 다시 모델로.
    도구 호출이 없으면 끝. 아래 줄: 회차마다 처음부터 다시 읽는 컨텍스트가 길어짐. 18초 · 한 번."""
    d = _D("lp", 18)
    s = ""
    # 사용자 요청
    s += (f'<g {d.show(1)}><rect x="40" y="16" width="300" height="50" rx="25" fill="{N}"/>'
          + _t(190, 41, "「11/10 회의록 정리해 줘」", "tw", extra='style="font-size:17px"') + "</g>")
    s += f'<path d="M190 66 V96" stroke="{N}" stroke-width="3" marker-end="url(#{d.id("k")})"/>'
    # 모델
    s += f'<rect x="40" y="100" width="300" height="190" rx="18" fill="{W}" stroke="{K}" stroke-width="3"/>'
    s += _t(190, 140, "Claude 모델", "tt", extra='style="font-size:22px"') + _t(190, 170, "다음 행동을 글로 씀", "ts")
    # 하네스
    s += f'<rect x="560" y="100" width="300" height="190" rx="18" fill="{K}"/>'
    s += _t(710, 140, "Claude Code", "tw", extra='style="font-size:22px"') + _t(710, 170, "하네스 · 실제로 실행", "tw", extra='style="font-weight:500;fill:#C9D3E0"')
    chips = {}
    for i, n in enumerate(("Glob", "Read", "Write")):
        x = 585 + i * 88
        chips[n] = x
        s += f'<rect x="{x}" y="215" width="76" height="40" rx="10" fill="#2C4C75"/>' + _t(x + 38, 236, n, "tw", extra='style="font-family:var(--mono,monospace)"')
    # 내 폴더
    s += f'<rect x="900" y="100" width="240" height="190" rx="18" fill="{BG}" stroke="{G}" stroke-width="2"/>' + _t(920, 124, "내 폴더", "tn", "start")
    files = [("원본/11-03_주간회의", 156), ("원본/11-05_프로모션", 186), ("원본/11-10_주간회의", 216)]
    for n, y in files:
        s += f'<rect x="916" y="{y - 13}" width="208" height="26" rx="6" fill="{W}" stroke="{G}"/>' + _t(928, y, n, "tm", "start", 'style="font-size:13px"')
    s += (f'<g {d.show(62)}><rect x="916" y="{259}" width="208" height="26" rx="6" fill="#E8F5E9" stroke="{OK}" stroke-width="2"/>'
          + _t(928, 272, "out/11-10_정리.md", "tm", "start", f'style="font-size:13px;fill:{OK}"') + "</g>")
    s += f'<path d="M864 195 H896" stroke="{G}" stroke-width="3"/>'
    # 화살표 두 줄
    dim = d.a([(0, "opacity:1"), (73, "opacity:1"), (76, "opacity:.15"), (100, "opacity:.15")])
    s += (f'<g {dim}><path d="M344 150 H552" stroke="{O}" stroke-width="3.5" marker-end="url(#{d.id("o")})"/>'
          f'<path d="M556 248 H348" stroke="{OK}" stroke-width="3.5" marker-end="url(#{d.id("g")})"/></g>')

    rounds = [(6, "Glob 원본/*.md", "Glob", [156, 186, 216], "파일 3개"),
              (28, "Read 11-10_주간회의.md", "Read", [216], "본문 · 할 일 5건"),
              (50, "Write out/11-10_정리.md", "Write", [], "저장 완료")]
    for i, (T, call, tool, hl, res) in enumerate(rounds):
        end = T + 21
        s += f'<g {d.show(T, end)}>' + _t(190, 236, f"{i + 1}회차", "to", extra='style="font-size:24px"') + "</g>"
        s += f'<g {d.show(T + 2, end)}>' + _t(450, 128, call, "tm", extra='style="font-size:14.5px"') + "</g>"
        s += _dot(d, [(0, 344, 150, 0), (T + 2, 344, 150, 0), (T + 2.5, 344, 150, 1), (T + 8, 552, 150, 1), (T + 8.5, 552, 150, 0), (100, 552, 150, 0)], color=O, r=9)
        x = chips[tool]
        s += f'<rect x="{x}" y="215" width="76" height="40" rx="10" fill="{O}" {d.show(T + 8, T + 13)}/>'
        s += f'<g {d.show(T + 8, T + 13)}>' + _t(x + 38, 236, tool, "tw", extra='style="font-family:var(--mono,monospace)"') + "</g>"
        for y in hl:
            s += f'<rect x="914" y="{y - 15}" width="212" height="30" rx="7" fill="none" stroke="{O}" stroke-width="3" {d.show(T + 9, T + 14)}/>'
        s += _dot(d, [(0, 552, 248, 0), (T + 12, 552, 248, 0), (T + 12.5, 552, 248, 1), (T + 18, 348, 248, 1), (T + 18.5, 348, 248, 0), (100, 348, 248, 0)], color=OK, r=9)
        s += f'<g {d.show(T + 13, end)}>' + _t(450, 272, res, "tn", extra=f'style="font-size:15px;fill:{OK}"') + "</g>"
    # 끝 · 도구 호출 없음
    s += f'<g {d.show(72)}>' + _t(190, 236, "4회차", "to", extra='style="font-size:24px"') + "</g>"
    s += f'<g {d.show(75)}>' + _t(450, 128, "도구 호출 없음", "to", extra='style="font-size:15px"') + "</g>"

    # 컨텍스트 줄
    s += _t(40, 330, "컨텍스트 · 회차마다 처음부터 다시 읽음", "tn", "start")
    blocks = [(1, "요청", 70, N), (8, "호출", 64, O), (22, "결과", 64, OK), (30, "호출", 64, O), (44, "결과 · 회의록 본문", 250, OK),
              (52, "호출", 64, O), (66, "결과", 64, OK), (80, "답", 70, K)]
    x = 40
    for t, lab, w, col in blocks:
        s += (f'<g {d.show(t)}><rect x="{x}" y="350" width="{w - 4}" height="40" rx="8" fill="{col}"/>'
              + _t(x + (w - 4) / 2, 371, lab, "tw", extra='style="font-size:14px"') + "</g>")
        x += w
    # 답
    s += (f'<g {d.show(82)}><rect x="40" y="410" width="560" height="46" rx="12" fill="{W}" stroke="{N}" stroke-width="2"/>'
          + _t(60, 433, "답 · 할 일 5건 · 담당 · 기한 표 → out/11-10_정리.md", "tn", "start", 'style="font-size:16px"')
          + _t(620, 433, "도구 호출이 없으면 루프 끝", "to", "start", 'style="font-size:17px"') + "</g>")
    return d.svg(1160, 470, s)


# ── 2 컨텍스트가 쌓이는 모습 ─────────────────────────
def context_fill():
    """한 번에 읽는 양(컨텍스트)에 무엇이 · 언제 올라가는지. 항상 → 쌓임 → 호출될 때. 12초 · 한 번."""
    d = _D("cf", 12)
    X0, Y, H, BW = 40, 70, 70, 1080
    items = [("시스템 · 내장 도구", .10, K, 1, 3, "항상"), ("MCP 도구 목록", .08, K, .7, 10, "항상 · 연결한 만큼"),
             ("CLAUDE.md", .05, K, .45, 17, "항상 · 길이만큼"), ("Skill 설명", .04, O, .45, 24, "항상 · 설명만"),
             ("대화", .12, G, 1, 36, "쌓임"), ("도구 결과", .30, O, 1, 50, "쌓임 · 가장 큼"), ("Skill 본문", .07, O, .75, 68, "호출될 때만")]
    s = f'<rect x="{X0}" y="{Y}" width="{BW}" height="{H}" rx="12" fill="{BG}" stroke="{N}" stroke-width="3"/>'
    s += _t(X0, 40, "컨텍스트 · 한 번에 읽는 양", "tt", "start") + _t(X0 + BW, 40, "한도", "tt", "end")
    x = X0
    for i, (name, f, col, op, t, when) in enumerate(items):
        w = f * BW
        s += (f'<rect x="{x:g}" y="{Y}" height="{H}" fill="{col}" fill-opacity="{op}" stroke="{W}" stroke-width="2" '
              + d.a([(0, "width:0px"), (t, "width:0px"), (t + 6, f"width:{w:g}px"), (100, f"width:{w:g}px")]) + "/>")
        ly = 190 + i * 32
        s += (f'<g {d.show(t)}><rect x="{X0}" y="{ly - 11}" width="22" height="22" rx="4" fill="{col}" fill-opacity="{op}"/>'
              + _t(X0 + 34, ly, name, "tn", "start") + _t(X0 + 230, ly, when, "to" if "호출" in when or "가장" in when else "ts", "start") + "</g>")
        x += w
    s += f'<g {d.show(80)}>' + _t(700, 260, "설명은 늘 올라가 있고", "tn", "start") + _t(700, 292, "본문 · 결과는 쓸 때만 올라감", "tn", "start") + _t(700, 336, "→ CLAUDE.md 는 짧게 · 절차는 Skill 로", "to", "start") + "</g>"
    return d.svg(1160, 420, s)


# ── 3 Skill이 불리는 순간 ─────────────────────────────
def skill_trigger():
    """요청 문장과 Skill 설명을 비교 → 맞는 Skill 본문만 열림. 10초 · 한 번."""
    d = _D("sk", 10)
    s = (f'<g {d.show(2)}><rect x="20" y="150" width="250" height="60" rx="14" fill="{N}"/>' + _t(145, 181, "「11/10 회의록 정리해 줘」", "tw") + "</g>")
    cards = [("weekly-report", "주간 보고서를 쓸 때"), ("meeting-notes", "회의록을 할 일 · 결정으로 정리할 때"), ("mail-draft", "고객 메일 답장 초안을 쓸 때")]
    s += _t(470, 40, "Skill 설명 · 항상 올라가 있음", "tn")
    for i, (n, desc) in enumerate(cards):
        y = 70 + i * 100
        s += f'<rect x="320" y="{y}" width="300" height="80" rx="12" fill="{W}" stroke="{G}" stroke-width="2"/>'
        s += _t(340, y + 26, n, "tm", "start") + _t(340, y + 54, desc, "ts", "start", 'style="font-size:13.5px"')
    # 훑는 표시
    s += (f'<rect x="314" width="312" height="92" rx="14" fill="none" stroke="{O}" stroke-width="4" '
          + d.a([(0, "y:64px;opacity:0"), (12, "y:64px;opacity:0"), (14, "y:64px;opacity:1"), (24, "y:64px;opacity:1"),
                 (32, "y:164px;opacity:1"), (100, "y:164px;opacity:1")]) + "/>")
    s += f'<g {d.show(34)}>' + _t(470, 380, "요청과 설명이 맞음 → meeting-notes", "to") + f'<path d="M630 210 H700" stroke="{O}" stroke-width="3" marker-end="url(#{d.id("o")})"/></g>'
    # 본문 열림
    s += (f'<rect x="710" y="60" width="430" rx="14" fill="#FFF8F1" stroke="{O}" stroke-width="2.5" '
          + d.a([(0, "height:0px;opacity:0"), (40, "height:0px;opacity:1"), (55, "height:300px;opacity:1"), (100, "height:300px;opacity:1")]) + "/>")
    body = ["SKILL.md 본문", "1. 원본/ 에서 회의록 고르기", "2. 결정 · 할 일 · 열린 질문", "3. 담당 · 기한 · 근거 한 줄", "4. 지난 할 일 완료 여부", "5. out/ 에 저장 · 대화엔 3줄"]
    for i, line in enumerate(body):
        s += f'<g {d.show(52 + i * 5)}>' + _t(734, 96 + i * 42, line, "tt" if i == 0 else "tn", "start") + "</g>"
    s += f'<g {d.show(88)}>' + _t(925, 392, "나머지 Skill 본문은 열리지 않음", "ts") + "</g>"
    return d.svg(1160, 410, s)


# ── 4 Hook이 끼어드는 시점 ───────────────────────────
def hook_gate():
    """원본/ 수정 요청은 Hook 이 가로채 거부 · out/ 쓰기는 통과. 10초 · 한 번 · 끝 장면에 두 결과가 남음."""
    d = _D("hk", 10)
    s = _box(20, 110, 180, 210, "Claude", "도구 호출")
    s += f'<rect x="520" y="60" width="26" height="320" rx="8" fill="{K}"/>' + _t(533, 402, "Hook", "tt")
    s += (f'<rect x="510" y="60" width="46" height="320" rx="10" fill="none" stroke="{R}" stroke-width="5" '
          + d.a([(0, "opacity:0"), (26, "opacity:0"), (28, "opacity:1"), (42, "opacity:1"), (45, "opacity:0"), (100, "opacity:0")]) + "/>")
    s += (f'<rect x="510" y="60" width="46" height="320" rx="10" fill="none" stroke="{OK}" stroke-width="5" '
          + d.a([(0, "opacity:0"), (64, "opacity:0"), (66, "opacity:1"), (74, "opacity:1"), (77, "opacity:0"), (100, "opacity:0")]) + "/>")
    s += _box(900, 105, 240, 110, "원본/", "회의록 3개", fill=BG, stroke=G)
    s += _box(900, 235, 240, 110, "out/", "정리 결과", fill=BG, stroke=G)
    for y, x2 in ((160, 500), (290, 500)):
        s += f'<path d="M200 {y} H{x2}" stroke="{G}" stroke-width="3" stroke-dasharray="6 6"/><path d="M560 {y} H890" stroke="{G}" stroke-width="3" stroke-dasharray="6 6"/>'
    s += _dot(d, [(0, 210, 160, 0), (6, 210, 160, 1), (26, 500, 160, 1), (34, 500, 160, 1), (44, 210, 160, 1), (46, 210, 160, 0), (100, 210, 160, 0)],
              color=R, r=12, label="Edit 원본/11-03")
    s += (f'<g {d.show(30)}><circle cx="500" cy="160" r="15" fill="{W}" stroke="{R}" stroke-width="3"/>'
          f'<path d="M493 153 L507 167 M507 153 L493 167" stroke="{R}" stroke-width="3.5"/>'
          + _t(350, 120, "거부 · 이유를 Claude에게", "tt", extra=f'style="fill:{R};font-size:17px"') + "</g>")
    s += f'<g {d.show(46)}>' + _t(350, 225, "이유를 읽고 out/ 으로", "ts") + "</g>"
    s += _dot(d, [(0, 210, 290, 0), (52, 210, 290, 0), (54, 210, 290, 1), (66, 533, 290, 1), (80, 890, 290, 1), (82, 890, 290, 0), (100, 890, 290, 0)],
              color=OK, r=12, label="Write out/11-03_정리")
    s += f'<g {d.show(82)}>' + _t(725, 330, "통과 · 저장됨", "tt", extra=f'style="fill:{OK};font-size:17px"') + "</g>"
    return d.svg(1160, 420, s)


# ── 5 MCP 호출 순서 ──────────────────────────────────
def mcp_call():
    """연결 때 도구 목록 → 질문 → 모델이 도구 고름 → MCP 서버 → 노션 → 결과 → 답. 12초 · 한 번."""
    d = _D("mc", 12)
    xs = [(110, "사용자", ""), (400, "Claude Code", "MCP 클라이언트"), (720, "노션 MCP 서버", "mcp.notion.com"), (1030, "노션", "내 페이지")]
    s = ""
    for x, h, sub in xs:
        s += _box(x - 100, 20, 200, 74, h, sub, fill=K if h == "Claude Code" else W, stroke=K,
                  cls="tw" if h == "Claude Code" else "tt")
        s += f'<line x1="{x}" y1="94" x2="{x}" y2="410" stroke="{G}" stroke-width="2" stroke-dasharray="6 6"/>'
    steps = [(4, 400, 720, 130, "① 도구 목록 주세요", K), (12, 720, 400, 165, "notion-search · notion-fetch …", K),
             (26, 110, 400, 210, "② 「주간 회의 페이지 찾아서 할 일만」", K), (36, 400, 400, 250, "③ 모델이 notion-search 고름", O),
             (46, 400, 720, 290, "④ 호출", O), (54, 720, 1030, 290, "노션 API", O), (62, 1030, 720, 330, "페이지 내용", OK),
             (70, 720, 400, 330, "결과", OK), (82, 400, 110, 375, "⑤ 할 일 표로 답", OK)]
    for t, a, b, y, lab, col in steps:
        mk = {K: "k", O: "o", OK: "g"}[col]
        if a == b:
            s += f'<g {d.show(t)}><rect x="{a - 150}" y="{y - 17}" width="300" height="34" rx="10" fill="#FFF8F1" stroke="{O}" stroke-width="2"/>' + _t(a, y + 1, lab, "to") + "</g>"
            continue
        dirn = 1 if b > a else -1
        s += (f'<g {d.show(t + 4)}><line x1="{a + dirn * 6}" y1="{y}" x2="{b - dirn * 10}" y2="{y}" stroke="{col}" stroke-width="3" marker-end="url(#{d.id(mk)})"/>'
              + _t((a + b) / 2, y - 14, lab, "tn" if col == K else ("to" if col == O else "tn"), extra=f'style="fill:{col};font-size:14px"') + "</g>")
        s += _dot(d, [(0, a, y, 0), (t, a, y, 0), (t + .5, a, y, 1), (t + 5, b, y, 1), (t + 6, b, y, 0), (100, b, y, 0)], color=col, r=8)
    return d.svg(1160, 420, s)
