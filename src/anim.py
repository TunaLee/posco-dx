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


# ── 0 배경 · 아는 것과 하는 것 ───────────────────────
def chat_vs_agent():
    """같은 요청 · 채팅은 방법만 답하고 일은 사람 손 · 에이전트는 직접 읽고 쓰고 저장. 12초 · 한 번.
    참고: IBM Technology 「What is OpenClaw?」 00:00~01:35 · Claude Code 문서 「How Claude Code works」."""
    d = _D("cv", 12)
    s = ""
    rows = [(30, "채팅", 2, [("파일 열기", R), ("복사 · 붙여 넣기", R), ("표 만들기", R), ("저장", R)],
             "「회의록을 열어 할 일을 표로 정리하세요」", "일은 사람 손으로", R),
            (260, "에이전트", 50, [("Glob 찾기", K), ("Read 읽기", K), ("표 작성", K), ("Write 저장", K)],
             "도구로 직접 처리", "out/11-10_정리.md", OK)]
    for y, name, t, steps, reply, end, col in rows:
        s += _t(20, y + 14, name, "tt", "start", 'style="font-size:22px"')
        s += (f'<g {d.show(t)}><rect x="20" y="{y + 40}" width="290" height="50" rx="25" fill="{N}"/>'
              + _t(165, y + 65, "「11/10 회의록 정리해 줘」", "tw", extra='style="font-size:16px"') + "</g>")
        s += (f'<g {d.show(t + 6)}><path d="M314 {y + 65} H350" stroke="{G}" stroke-width="3" marker-end="url(#{d.id("k")})"/>'
              f'<rect x="356" y="{y + 40}" width="380" height="50" rx="12" fill="{W}" stroke="{K}" stroke-width="2"/>'
              + _t(546, y + 65, reply, "tn", extra='style="font-size:15px"') + "</g>")
        who = "사람" if name == "채팅" else "하네스"
        s += f'<g {d.show(t + 12)}>' + _t(20, y + 128, who, "tn", "start", f'style="fill:{col if name == "채팅" else K}"') + "</g>"
        for i, (st, c) in enumerate(steps):
            x = 90 + i * 162
            s += (f'<g {d.show(t + 14 + i * 5)}><rect x="{x}" y="{y + 108}" width="148" height="40" rx="10" fill="{W}" stroke="{c}" stroke-width="2.5"/>'
                  + _t(x + 74, y + 129, st, "tn", extra=f'style="fill:{c}"') + "</g>")
        s += (f'<g {d.show(t + 36)}><rect x="760" y="{y + 100}" width="380" height="56" rx="14" fill="{"#FDECEA" if col == R else "#E8F5E9"}" stroke="{col}" stroke-width="2.5"/>'
              + _t(950, y + 129, end, "tt", extra=f'style="fill:{col};font-size:19px"') + "</g>")
    s += f'<line x1="20" y1="232" x2="1140" y2="232" stroke="{G}" stroke-width="2" stroke-dasharray="6 6"/>'
    return d.svg(1160, 430, s)


# ── 1 에이전트 루프 ─────────────────────────────────
def agent_loop():
    """컨텍스트 조립(하네스) → 모델 판단 → 도구 필요? → 도구 실행(하네스) → 결과를 붙여 다시 조립 · 아니오면 답.
    상자를 하나씩 그려 고리를 닫고(0~24%), 점이 세 바퀴(Glob · Read · Write) 돈 뒤 고리 밖으로. 20초 · 한 번.
    참고: Claude Code 「How Claude Code works」 · IBM 「What is OpenClaw?」 · IBM 「AI Model vs Agentic Harness」 · Nate Herk 「Agent Loops Clearly Explained」."""
    d = _D("lp", 20)
    s = ""
    MO = "#FFF3E6"
    # 상자 · 화살표 차례로 그림
    s += f'<g {d.show(1)}><rect x="20" y="70" width="150" height="56" rx="28" fill="{N}"/>' + _t(95, 98, "요청", "tw", extra='style="font-size:18px"') + "</g>"
    s += f'<g {d.show(3)}><path d="M174 98 H226" stroke="{N}" stroke-width="3.5" marker-end="url(#{d.id("k")})"/></g>'
    s += (f'<g {d.show(4)}><rect x="232" y="30" width="290" height="140" rx="16" fill="{K}"/>'
          + _t(377, 62, "컨텍스트 조립", "tw", extra='style="font-size:21px"') + _t(377, 88, "하네스 · 요청 + 지금까지의 결과", "tw", extra='style="font-weight:500;fill:#C9D3E0;font-size:14px"') + "</g>")
    s += f'<g {d.show(7)}><path d="M526 100 H636" stroke="{K}" stroke-width="3.5" marker-end="url(#{d.id("k")})"/>' + _t(581, 84, "전체를 보냄", "ts", extra='style="font-size:13px"') + "</g>"
    s += (f'<g {d.show(8)}><rect x="642" y="30" width="260" height="140" rx="16" fill="{MO}" stroke="{O}" stroke-width="3"/>'
          + _t(772, 82, "모델 판단", "tt", extra='style="font-size:22px"') + _t(772, 112, "다음 행동 고르기", "ts") + "</g>")
    s += f'<g {d.show(11)}><path d="M772 174 V214" stroke="{O}" stroke-width="3.5" marker-end="url(#{d.id("o")})"/></g>'
    s += (f'<g {d.show(12)}><path d="M772 220 L852 262 L772 304 L692 262 Z" fill="{W}" stroke="{O}" stroke-width="3"/>'
          + _t(772, 263, "도구 필요?", "tn", extra='style="font-size:16px"') + "</g>")
    s += (f'<g {d.show(15)}><path d="M772 308 V372 H526" fill="none" stroke="{O}" stroke-width="3.5" marker-end="url(#{d.id("o")})"/>'
          + _t(786, 334, "예 · 도구 호출", "to", "start") + "</g>")
    s += (f'<g {d.show(16)}><rect x="232" y="320" width="290" height="110" rx="16" fill="{K}"/>'
          + _t(377, 346, "도구 실행", "tw", extra='style="font-size:21px"') + _t(377, 368, "하네스", "tw", extra='style="font-weight:500;fill:#C9D3E0;font-size:14px"') + "</g>")
    chips = {}
    for i, n in enumerate(("Glob", "Read", "Write")):
        x = 256 + i * 82
        chips[n] = x
        s += f'<g {d.show(17)}><rect x="{x}" y="388" width="74" height="30" rx="8" fill="#2C4C75"/>' + _t(x + 37, 404, n, "tw", extra='style="font-family:var(--mono,monospace);font-size:14px"') + "</g>"
    # 고리를 닫는 화살표 (마지막에)
    s += (f'<g {d.show(21)}><path d="M300 316 V174" stroke="{OK}" stroke-width="4" marker-end="url(#{d.id("g")})"/>'
          + _t(186, 245, "결과를 붙임", "tn", extra=f'style="fill:{OK};font-size:16px"') + "</g>")
    s += (f'<g {d.show(19)}><path d="M856 262 H930" stroke="{N}" stroke-width="3.5" marker-end="url(#{d.id("k")})"/>' + _t(893, 246, "아니오", "tn")
          + f'<rect x="936" y="226" width="200" height="72" rx="14" fill="{W}" stroke="{N}" stroke-width="2.5"/>' + _t(1036, 262, "답 → 사용자", "tt") + "</g>")
    # 컨텍스트 칩 (요청 + 결과)
    s += f'<g {d.show(5)}><rect x="250" y="116" width="58" height="34" rx="8" fill="{N}"/>' + _t(279, 133, "요청", "tw", extra='style="font-size:14px"') + "</g>"

    C, M, DM, DN, EX = (377, 100), (772, 100), (772, 262), (772, 372), (377, 372)
    T = [26, 41, 56]
    pts = [(0, *C, 0), (T[0] - .5, *C, 0)]
    for i, (t0, tool) in enumerate(zip(T, ("Glob", "Read", "Write"))):
        pts += [(t0, *C, 1), (t0 + 3, *M, 1), (t0 + 6, *DM, 1), (t0 + 8, *DN, 1), (t0 + 11, *EX, 1), (t0 + 14, 300, 372, 1), (t0 + 15, 300, 120, 1)]
        s += f'<path d="M772 220 L852 262 L772 304 L692 262 Z" fill="{O}" fill-opacity=".25" {d.show(t0 + 5, t0 + 8)}/>'
        x = chips[tool]
        s += f'<g {d.show(t0 + 10, t0 + 14)}><rect x="{x}" y="388" width="74" height="30" rx="8" fill="{O}"/>' + _t(x + 37, 404, tool, "tw", extra='style="font-family:var(--mono,monospace);font-size:14px"') + "</g>"
        cx = 316 + i * 64
        s += f'<g {d.show(t0 + 14)}><rect x="{cx}" y="116" width="58" height="34" rx="8" fill="{OK}"/>' + _t(cx + 29, 133, f"결과{i + 1}", "tw", extra='style="font-size:14px"') + "</g>"
    pts += [(71, *C, 1), (74, *M, 1), (77, *DM, 1), (81, 930, 262, 1), (82, 930, 262, 0), (100, 930, 262, 0)]
    s += _dot(d, pts, color=O, r=11)
    s += f'<path d="M772 220 L852 262 L772 304 L692 262 Z" fill="{N}" fill-opacity=".12" {d.show(76)}/>'
    s += f'<g {d.show(82)}><rect x="936" y="226" width="200" height="72" rx="14" fill="#E8F5E9" stroke="{OK}" stroke-width="3"/>' + _t(1036, 262, "답 → 사용자", "tt", extra=f'style="fill:{OK}"') + "</g>"
    # 범례
    s += (f'<g {d.show(86)}><rect x="642" y="400" width="22" height="22" rx="5" fill="{MO}" stroke="{O}" stroke-width="2.5"/>' + _t(672, 412, "모델 · 판단", "tn", "start")
          + f'<rect x="800" y="400" width="22" height="22" rx="5" fill="{K}"/>' + _t(830, 412, "하네스 · 조립 · 실행", "tn", "start") + "</g>")
    return d.svg(1160, 440, s)


def _path_dot(d, xy, t0, t1, color=O, r=9, label=""):
    """꺾은선 xy 를 t0% → t1% 동안 따라가는 점 (앞뒤로는 숨김)."""
    segs = [math.dist(a, b) for a, b in zip(xy, xy[1:])]
    tot = sum(segs) or 1
    pts, acc = [(0, *xy[0], 0), (max(t0 - .3, 0), *xy[0], 0), (t0, *xy[0], 1)], 0
    for (x, y), L in zip(xy[1:], segs):
        acc += L
        pts.append((t0 + (t1 - t0) * acc / tot, x, y, 1))
    pts += [(t1 + .5, *xy[-1], 0), (100, *xy[-1], 0)]
    return _dot(d, pts, color, r, label)


def _flow(d, t, xy, col, mk, lab="", lx=0, ly=0, anchor="middle", span=5, r=8, dash=False):
    """t% 에 화살표가 나타나고 점이 span 동안 따라감."""
    path = "M" + " L".join(f"{x:g} {y:g}" for x, y in xy)
    tc = "#EF6C00" if col == O else col
    da = 'stroke-dasharray="7 6" ' if dash else ""
    s = (f'<g {d.show(t)}><path d="{path}" fill="none" stroke="{col}" stroke-width="3" '
         f'{da}marker-end="url(#{d.id(mk)})"/>')
    if lab:
        s += _t(lx, ly, lab, "tn", anchor, f'style="fill:{tc};font-size:14.5px"')
    return s + "</g>" + _path_dot(d, xy, t, t + span, col, r)


# ── 2 컨텍스트가 차는 모습 ───────────────────────────
def context_fill():
    """같은 크기 그릇이 입력 전부터 차 있고 → 작업하며 쌓이고 → 한도 근처에서 자동 요약. 16초 · 한 번.
    참고: Claude Code 「Explore the context window」 · NetworkChuck 「Why LLMs get dumb」 · IBM 「What is a Context Window?」."""
    d = _D("cx", 16)
    X0, Y, H, BW = 40, 80, 80, 1080
    FL = "#8FA3BF"
    start = [("시스템 프롬프트", .06, N, 1, 3), ("CLAUDE.md", .04, K, 1, 7), ("MCP 도구 이름", .015, K, .5, 11), ("Skill 설명", .015, O, .6, 14)]
    work = [("요청", .03, S, .6, 24), ("회의록 11-03", .11, FL, 1, 30), ("회의록 11-10", .11, FL, 1, 36), ("회의록 11-05", .11, FL, 1, 42),
            ("Skill 본문", .05, O, 1, 50), ("도구 결과", .10, "#5C7FA8", 1, 56), ("대화 · 답", .21, S, .45, 62)]
    s = f'<rect x="{X0}" y="{Y}" width="{BW}" height="{H}" rx="12" fill="{BG}" stroke="{N}" stroke-width="3"/>'
    s += _t(X0, 40, "컨텍스트 · 한 번에 읽는 양", "tt", "start") + _t(X0 + BW, 40, "한도", "tt", "end")
    x, pct, marks = X0, 0, []
    for name, f, col, op, t in start:
        w = f * BW
        s += (f'<rect x="{x:g}" y="{Y}" height="{H}" fill="{col}" fill-opacity="{op}" stroke="{W}" stroke-width="2" '
              + d.a([(0, "width:0px"), (t, "width:0px"), (t + 4, f"width:{w:g}px"), (100, f"width:{w:g}px")]) + "/>")
        x += w
        pct += f
        marks.append((t + 3, pct))
    sx = x
    s += f'<g {d.show(16)}><path d="M{X0} 176 H{sx:g}" stroke="{N}" stroke-width="2"/>' + _t((X0 + sx) / 2, 194, "입력 전에 이미", "tn", extra='style="font-size:14px"') + "</g>"
    for name, f, col, op, t in work:
        w = f * BW
        s += (f'<rect x="{x:g}" y="{Y}" height="{H}" fill="{col}" fill-opacity="{op}" stroke="{W}" stroke-width="2" '
              + d.a([(0, "width:0px;opacity:1"), (t, "width:0px;opacity:1"), (t + 4, f"width:{w:g}px;opacity:1"), (76, f"width:{w:g}px;opacity:1"),
                     (82, "width:0px;opacity:0"), (100, "width:0px;opacity:0")]) + "/>")
        if f >= .1:
            s += f'<g {d.show(t + 3, 76)}>' + _t(x + w / 2, Y + H / 2, name, "tw", extra='style="font-size:14px"') + "</g>"
        x += w
        pct += f
        marks.append((t + 3, pct))
    # 자동 요약
    ax = X0 + .885 * BW
    s += f'<g {d.show(70)}><path d="M{ax:g} {Y - 14} V{Y + H + 14}" stroke="{R}" stroke-width="3" stroke-dasharray="6 5"/>' + _t(ax, Y + H + 30, "자동 요약", "tn", extra=f'style="fill:{R};font-size:14px"') + "</g>"
    sw = .07 * BW
    s += (f'<rect x="{sx:g}" y="{Y}" height="{H}" fill="{OK}" stroke="{W}" stroke-width="2" '
          + d.a([(0, "width:0px"), (80, "width:0px"), (85, f"width:{sw:g}px"), (100, f"width:{sw:g}px")]) + "/>")
    s += f'<g {d.show(84)}>' + _t(sx + sw / 2, Y + H / 2, "요약", "tw", extra='style="font-size:14px"') + "</g>"
    marks.append((80, sum(f for _, f, *_ in start) + .07))
    # 퍼센트 (다음 값이 나올 때 바뀜)
    for i, (t, p) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else None
        if end and end <= t:
            continue
        s += f'<g {d.show(t, end if end else None)}>' + _t(600, 40, f"{round(p * 100)}%", "tt", extra=f'style="font-size:24px;fill:{R if p > .8 else N}"') + "</g>"
    # 범례
    leg = [("시스템 프롬프트 · CLAUDE.md", N, 1, "입력 전 · 항상", 4), ("MCP 도구 이름 · Skill 설명", K, .5, "입력 전 · 이름 · 설명만", 12),
           ("요청 · 대화 · 답", S, .5, "쌓임", 24), ("읽은 파일 · 도구 결과", FL, 1, "쌓임 · 가장 큼", 31),
           ("Skill 본문", O, 1, "호출될 때만", 50), ("요약", OK, 1, "한도 가까우면 자동으로", 84)]
    for i, (name, col, op, when, t) in enumerate(leg):
        ly = 232 + i * 34
        s += (f'<g {d.show(t)}><rect x="{X0}" y="{ly - 11}" width="22" height="22" rx="4" fill="{col}" fill-opacity="{op}"/>'
              + _t(X0 + 34, ly, name, "tn", "start") + _t(X0 + 290, ly, when, "to" if t in (31, 50, 84) else "ts", "start") + "</g>")
    s += (f'<g {d.show(88)}>' + _t(700, 262, "요약 뒤에도 다시 올라가는 것", "tn", "start")
          + _t(700, 292, "시스템 프롬프트 · CLAUDE.md · Skill 설명", "ts", "start")
          + _t(700, 336, "→ CLAUDE.md 는 짧게 · 절차는 Skill 로", "to", "start") + "</g>")
    return d.svg(1160, 440, s)


# ── 3 Skill 이 열리는 단계 ────────────────────────────
def skill_trigger():
    """① 시작할 때 설명 줄만 → ② 요청과 맞으면 본문 → ③ 본문이 가리킬 때 부속 파일 · 스크립트는 실행 결과만. 14초 · 한 번.
    참고: Claude Code Skills 문서 · Claude 「What are skills?」 · IBM 「What AI Agent Skills Are and How They Work」."""
    d = _D("sk", 14)
    BAND = "#FFF3E6"
    cards = [("weekly-report", "주간 보고서를 쓸 때"), ("meeting-notes", "회의록을 할 일 · 결정으로 정리할 때"), ("mail-draft", "고객 메일 답장 초안을 쓸 때")]
    s = _t(230, 20, "Skill 폴더 · 디스크", "tn")
    s += f'<rect x="560" y="10" width="580" height="410" rx="16" fill="{BG}" stroke="{N}" stroke-width="3"/>' + _t(850, 34, "컨텍스트", "tt")
    for i, (n, desc) in enumerate(cards):
        y = 40 + i * 125
        s += f'<rect x="30" y="{y}" width="400" height="105" rx="12" fill="{W}" stroke="{G}" stroke-width="2"/>'
        s += f'<rect x="31" y="{y + 1}" width="398" height="32" rx="11" fill="{BAND}"/>' + _t(46, y + 18, f"{n} · {desc}", "tm", "start", 'style="font-size:13px"')
        dim = "" if i == 1 else d.a([(0, "opacity:1"), (84, "opacity:1"), (88, "opacity:.35"), (100, "opacity:.35")])
        s += f'<g {dim}>' + "".join(f'<rect x="46" y="{y + 44 + k * 14}" width="{300 - k * 60}" height="7" rx="3" fill="{G}"/>' for k in range(3)) + "</g>"
        if i == 1:
            s += _t(46, y + 92, "부속: 양식.md · check.py", "ts", "start", 'style="font-size:13px"')
        # ① 설명 줄이 컨텍스트로
        cy = 78 + i * 26
        t = 4 + i * 3
        dx, dy = 30 - 600, y - cy
        s += (f'<g {d.a([(0, f"transform:translate({dx}px,{dy}px);opacity:0"), (t, f"transform:translate({dx}px,{dy}px);opacity:0"), (t + 1, f"transform:translate({dx}px,{dy}px);opacity:1"), (t + 7, "transform:translate(0px,0px);opacity:1"), (100, "transform:translate(0px,0px);opacity:1")], "ease-out")}>'
              f'<rect x="600" y="{cy}" width="400" height="22" rx="6" fill="{BAND}"/>' + _t(612, cy + 11, f"{n} · {desc}", "tm", "start", 'style="font-size:12.5px"') + "</g>")
    s += f'<g {d.show(3)}>' + _t(580, 66, "① 시작할 때 — 이름 · 설명만", "tn", "start", 'style="font-size:14px"') + "</g>"
    # 요청 → 맞는 설명 고름
    s += f'<g {d.show(22)}><rect x="600" y="160" width="300" height="32" rx="16" fill="{N}"/>' + _t(750, 176, "「11/10 회의록 정리해 줘」", "tw", extra='style="font-size:14px"') + "</g>"
    s += f'<rect x="596" y="100" width="408" height="30" rx="8" fill="none" stroke="{O}" stroke-width="3" {d.show(30)}/>'
    s += f'<rect x="27" y="162" width="406" height="111" rx="14" fill="none" stroke="{O}" stroke-width="3.5" {d.show(32)}/>'
    s += f'<g {d.show(32)}>' + _t(1012, 115, "← 요청과 맞음", "to", "start", 'style="font-size:13.5px"') + "</g>"
    # ② 본문
    s += _flow(d, 38, [(434, 230), (556, 270)], O, "o")
    s += f'<g {d.show(38)}>' + _t(580, 214, "② 요청과 맞으면 — 본문", "tn", "start", 'style="font-size:14px"') + "</g>"
    s += (f'<rect x="600" y="226" width="520" rx="12" fill="#FFF8F1" stroke="{O}" stroke-width="2.5" '
          + d.a([(0, "height:0px;opacity:0"), (40, "height:0px;opacity:1"), (48, "height:104px;opacity:1"), (100, "height:104px;opacity:1")]) + "/>")
    for k, line in enumerate(["SKILL.md 본문 · meeting-notes", "1. 결정 · 할 일 · 열린 질문으로 나누기", "2. 형식은 양식.md · 다 쓰면 check.py 로 확인"]):
        s += f'<g {d.show(46 + k * 3)}>' + _t(616, 248 + k * 30, line, "tn" if k else "tt", "start", 'style="font-size:15px"' if k else 'style="font-size:16px"') + "</g>"
    # ③ 부속 파일 · 스크립트
    s += f'<g {d.show(58)}>' + _t(580, 350, "③ 본문이 가리킬 때만 — 부속", "tn", "start", 'style="font-size:14px"') + "</g>"
    s += (f'<g {d.show(60)}><rect x="600" y="364" width="240" height="38" rx="10" fill="{W}" stroke="{O}" stroke-width="2.5"/>'
          + _t(720, 383, "양식.md · 읽어서 올림", "tn", extra='style="font-size:14px"') + "</g>")
    s += (f'<g {d.show(70)}><rect x="856" y="364" width="264" height="38" rx="10" fill="{W}" stroke="{K}" stroke-width="2.5" stroke-dasharray="6 4"/>'
          + _t(988, 383, "check.py · 실행 결과만", "tn", extra='style="font-size:14px"') + "</g>")
    s += f'<g {d.show(86)}>' + _t(230, 418, "나머지 Skill 본문은 열리지 않음", "ts") + "</g>"
    return d.svg(1160, 430, s)


# ── 4 Hook 이 끼어드는 시점 ───────────────────────────
def hook_gate():
    """이벤트 시간축 중 「실행 직전(PreToolUse)」에 관문 → 원본/ 수정은 exit 2 로 막고 이유를 Claude 에게 · out/ 쓰기는 통과. 14초 · 한 번.
    참고: Claude Code Hooks 문서 · Claude 「Hooks in Claude Code」 · Agentic Lab 「Claude Code Hooks, Explained Simply」."""
    d = _D("hk", 14)
    MO = "#FFF3E6"
    ev = [("요청 제출", "UserPromptSubmit"), ("실행 직전", "PreToolUse"), ("도구 실행", ""), ("실행 직후", "PostToolUse"), ("응답 끝", "Stop")]
    s = f'<path d="M40 48 H1100" stroke="{G}" stroke-width="3"/>'
    for i, (k, e) in enumerate(ev):
        x = 30 + i * 218
        op = "" if i == 1 else d.a([(0, "opacity:1"), (6, "opacity:1"), (9, "opacity:.4"), (100, "opacity:.4")])
        s += (f'<rect x="{x}" y="20" width="196" height="58" rx="12" fill="{W}" stroke="{G if i != 1 else K}" stroke-width="2"/>'
              f'<g {op}>' + _t(x + 98, 40 if e else 49, k, "tn", extra='style="font-size:16px"') + (_t(x + 98, 62, e, "tm", extra=f'style="font-size:12.5px;fill:{S}"') if e else "") + "</g>")
    s += f'<rect x="248" y="20" width="196" height="58" rx="12" fill="none" stroke="{O}" stroke-width="4" {d.show(6)}/>'
    s += f'<path d="M346 80 V94 H400 V108" fill="none" stroke="{O}" stroke-width="3" stroke-dasharray="5 4" {d.show(8)}/>'
    # 무대
    s += _box(20, 150, 200, 190, "Claude", "도구 호출", fill=MO, stroke=O)
    s += f'<rect x="387" y="110" width="26" height="300" rx="8" fill="{K}"/>' + _t(400, 428, "Hook · guard.py", "tn")
    s += _box(500, 240, 190, 90, "도구 실행", "")
    s += _box(790, 140, 200, 80, "원본/", "회의록 3개", fill=BG, stroke=G)
    s += _box(790, 245, 200, 80, "out/", "정리 결과", fill=BG, stroke=G)
    for y, segs in ((190, ((220, 383), (417, 786))), (285, ((220, 383), (417, 496), (690, 786)))):
        for a, b in segs:
            s += f'<path d="M{a} {y} H{b}" stroke="{G}" stroke-width="3" stroke-dasharray="6 6"/>'
    # 1) 원본 수정 → 막힘
    s += f'<g {d.show(8)}>' + _t(230, 172, "Edit 원본/11-03.md", "tm", "start", f'style="fill:{R};font-size:12.5px"') + "</g>"
    s += _path_dot(d, [(232, 190), (375, 190)], 10, 20, R, 11)
    s += (f'<rect x="381" y="110" width="38" height="300" rx="10" fill="none" stroke="{R}" stroke-width="5" '
          + d.a([(0, "opacity:0"), (20, "opacity:0"), (21, "opacity:1"), (30, "opacity:1"), (33, "opacity:0"), (100, "opacity:0")]) + "/>")
    s += (f'<g {d.show(22)}><circle cx="400" cy="190" r="16" fill="{W}" stroke="{R}" stroke-width="3"/>'
          f'<path d="M393 183 L407 197 M407 183 L393 197" stroke="{R}" stroke-width="3.5"/>'
          + _t(430, 166, "exit 2 · 막음", "tn", "start", f'style="fill:{R};font-size:15px"') + "</g>")
    ret = [(381, 214), (330, 238), (226, 236)]
    s += f'<path d="M381 214 Q330 246 226 236" fill="none" stroke="{R}" stroke-width="3" marker-end="url(#{d.id("r")})" {d.show(28)}/>'
    s += _path_dot(d, ret, 28, 34, R, 8)
    s += f'<g {d.show(32)}>' + _t(120, 368, "이유가 Claude에게", "tn", extra=f'style="fill:{R};font-size:15px"') + _t(120, 392, "「원본/은 수정 금지 · out/ 에 쓰기」", "ts", extra='style="font-size:13.5px"') + "</g>"
    # 2) out/ 쓰기 → 통과
    s += f'<g {d.show(44)}>' + _t(230, 267, "Write out/정리.md", "tm", "start", f'style="fill:{OK};font-size:12.5px"') + "</g>"
    s += _path_dot(d, [(232, 285), (375, 285)], 46, 56, OK, 11)
    s += (f'<rect x="381" y="110" width="38" height="300" rx="10" fill="none" stroke="{OK}" stroke-width="5" '
          + d.a([(0, "opacity:0"), (56, "opacity:0"), (57, "opacity:1"), (64, "opacity:1"), (67, "opacity:0"), (100, "opacity:0")]) + "/>")
    s += f'<g {d.show(57)}>' + _t(430, 262, "exit 0 · 통과", "tn", "start", f'style="fill:{OK};font-size:15px"') + "</g>"
    s += _path_dot(d, [(400, 285), (595, 285), (786, 285)], 60, 74, OK, 11)
    s += f'<g {d.show(76)}><rect x="790" y="245" width="200" height="80" rx="14" fill="#E8F5E9" stroke="{OK}" stroke-width="3"/>' + _t(890, 274, "out/", "tt", extra=f'style="fill:{OK}"') + _t(890, 300, "저장됨", "ts", extra=f'style="fill:{OK}"') + "</g>"
    s += f'<g {d.show(86)}>' + _t(500, 380, "도구 호출마다 매번 같은 검사", "tn", "start") + _t(500, 406, "권한 모드보다 먼저 실행", "ts", "start") + "</g>"
    return d.svg(1160, 440, s)


# ── 5 MCP 호출 순서 ──────────────────────────────────
def mcp_call():
    """호스트(Claude Code)만 모델 · 서버와 통신. 연결 때 도구 이름 → 요청 → 모델이 도구를 고름 → 호스트가 서버로 호출 → 결과 → 답. 16초 · 한 번.
    참고: modelcontextprotocol.io 「Architecture overview」 · IBM 「What is MCP?」 · ByteByteGo 「Why Everyone's Talking About MCP?」."""
    d = _D("mc", 16)
    MO = "#FFF3E6"
    s = f'<g {d.show(1)}><rect x="20" y="40" width="150" height="56" rx="28" fill="{N}"/>' + _t(95, 68, "사용자", "tw", extra='style="font-size:18px"') + "</g>"
    s += (f'<g {d.show(2)}><rect x="230" y="20" width="300" height="150" rx="16" fill="{K}"/>' + _t(380, 48, "Claude Code", "tw", extra='style="font-size:21px"')
          + _t(380, 74, "호스트 · MCP 클라이언트", "tw", extra='style="font-weight:500;fill:#C9D3E0;font-size:14px"') + "</g>")
    s += f'<g {d.show(4)}><rect x="790" y="20" width="260" height="150" rx="16" fill="{MO}" stroke="{O}" stroke-width="3"/>' + _t(920, 72, "모델", "tt", extra='style="font-size:22px"') + _t(920, 102, "도구를 고르기만", "ts") + "</g>"
    s += f'<g {d.show(6)}>' + _box(230, 300, 300, 100, "노션 MCP 서버", "mcp.notion.com") + "</g>"
    s += f'<g {d.show(8)}>' + _box(790, 300, 260, 100, "노션", "내 페이지", fill=BG, stroke=G) + "</g>"
    # ① 연결할 때 도구 이름
    s += _flow(d, 10, [(262, 174), (262, 294)], K, "k", span=4)
    s += _flow(d, 14, [(292, 296), (292, 176)], K, "k", "① 연결할 때 · 도구 이름 목록", 250, 236, "end", span=4)
    for x, w, n in ((246, 136, "notion-search"), (390, 124, "notion-fetch")):
        s += f'<g {d.show(18)}><rect x="{x}" y="118" width="{w}" height="30" rx="8" fill="#2C4C75"/>' + _t(x + w / 2, 133, n, "tw", extra='style="font-family:var(--mono,monospace);font-size:13px"') + "</g>"
    # ② 요청 ~ ⑦ 답
    s += f'<g {d.show(22, 80)}>' + _t(95, 116, "「회의 페이지에서 할 일만」", "ts", extra='style="font-size:13.5px"') + "</g>"
    s += _flow(d, 22, [(174, 68), (226, 68)], N, "k", "②", 200, 52, span=3)
    s += _flow(d, 30, [(534, 48), (784, 48)], K, "k", "③ 요청 + 도구 이름", 659, 32)
    s += _flow(d, 40, [(786, 92), (536, 92)], O, "o", "④ notion-search 호출", 659, 76)
    s += _flow(d, 50, [(450, 174), (450, 294)], O, "o", "⑤ 호출 전달", 438, 222, "end", span=4)
    s += _flow(d, 57, [(534, 334), (784, 334)], O, "o", "노션 API", 659, 318, span=4)
    s += _flow(d, 63, [(786, 372), (536, 372)], OK, "g", "페이지 내용", 659, 390, span=4)
    s += _flow(d, 69, [(500, 296), (500, 176)], OK, "g", "⑥ 결과", 512, 262, "start", span=4)
    s += _flow(d, 75, [(534, 140), (784, 140)], OK, "g", "결과를 붙여 다시", 659, 124, span=4)
    s += _flow(d, 84, [(226, 156), (150, 156), (150, 100)], OK, "g", "⑦ 답", 120, 176, span=4)
    # 모델과 서버 사이엔 선이 없음
    s += (f'<g {d.show(90)}><path d="M800 174 L540 296" stroke="{S}" stroke-width="2.5" stroke-dasharray="6 6"/>'
          f'<circle cx="670" cy="235" r="14" fill="{W}" stroke="{S}" stroke-width="2.5"/><path d="M664 229 L676 241 M676 229 L664 241" stroke="{S}" stroke-width="3"/>'
          + _t(692, 235, "모델 ↔ 서버 직접 연결 없음", "tn", "start", 'style="font-size:14.5px"') + "</g>")
    return d.svg(1160, 420, s)
