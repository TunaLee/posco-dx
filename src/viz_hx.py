"""하네스 · 멀티에이전트 · 컨텍스트 · 토큰 — 움직이는 도해.

함수마다 인라인 <svg> 하나를 돌려준다. 밝은 내용 장의 본문(약 1160×470)에 그대로 넣는다.
- 색: 남색 · 회색 · 주황 · 흰색만. 주황 = 움직이는 것 · 강조.
- 움직임: CSS keyframes (6–12초 반복). 인쇄 · 동작 줄이기 설정에서는 멈추고,
  속성값(기본값)이 그대로 보인다 → 기본값을 「대표 장면」으로 둔다.
- id · 클래스 · keyframes 이름은 함수마다 접두어를 따로 쓴다 (숨은 장의 url(#id) 참조 방지).
"""

N, G, O, W = "#1F3A5F", "#D9DDE3", "#F28C28", "#FFFFFF"
S = "#44506A"  # 보조 글자 (덱 .bs 와 같은 색)


class _D:
    """도해 하나: 접두어 · 반복 길이 · keyframes 모음."""

    def __init__(self, p, dur):
        self.p, self.dur, self.kfs, self.n = p, dur, [], 0

    def a(self, stops, ease="linear", extra=""):
        """stops: [(퍼센트, 'css 선언'), ...] → style 속성 문자열."""
        self.n += 1
        name = f"hx{self.p}{self.n}"
        body = "".join(f"{p:g}%{{{d}}}" for p, d in stops)
        self.kfs.append(f"@keyframes {name}{{{body}}}")
        return f'style="animation:{name} {self.dur}s {ease} infinite both;{extra}"'

    def id(self, s):
        return f"hx{self.p}{s}"

    def markers(self):
        def m(i, c):
            return (f'<marker id="{self.id(i)}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
                    f'orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="{c}"/></marker>')
        return m("ah", N) + m("aho", O) + m("ahg", "#9AA3B0")

    def svg(self, w, h, body, css=""):
        r = f".hx-{self.p}"
        base = (f"{r}{{width:100%;height:auto;max-height:470px;display:block;margin:0 auto;overflow:visible}}"
                f"{r} text{{font-family:var(--serif);dominant-baseline:middle}}"
                f"{r} .tt{{font-size:19px;font-weight:800;fill:{N}}}"
                f"{r} .ts{{font-size:15px;fill:{S}}}"
                f"{r} .to{{font-size:15px;font-weight:700;fill:{O}}}"
                f"{r} .tw{{font-size:15px;font-weight:700;fill:{W}}}"
                f"{r} .tn{{font-size:15px;font-weight:700;fill:{N}}}"
                f"@media print{{{r} *{{animation:none!important}}{r} .mv{{display:none}}}}"
                f"@media (prefers-reduced-motion:reduce){{{r} *{{animation:none!important}}{r} .mv{{display:none}}}}")
        css = css.replace("&", r)
        return (f'<svg class="hxv hx-{self.p}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
                f'<style>{base}{css}{"".join(self.kfs)}</style><defs>{self.markers()}</defs>{body}</svg>')


def _t(x, y, s, cls="ts", anchor="middle", extra=""):
    return f'<text x="{x:g}" y="{y:g}" text-anchor="{anchor}" class="{cls}" {extra}>{s}</text>'


def _box(x, y, w, h, title, cls="tt", sub="", fill=W, stroke=N, sw=3, rx=14, extra=""):
    s = f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
    if sub:
        s += _t(x + w / 2, y + h / 2 - 11, title, cls) + _t(x + w / 2, y + h / 2 + 14, sub, "ts")
    else:
        s += _t(x + w / 2, y + h / 2 + 1, title, cls)
    return s


def _tr(x, y):
    return f"transform:translate({x:g}px,{y:g}px)"


def _move(d, pts, color=O, r=9, shape=None):
    """pts: [(퍼센트, x, y, 보임 0/1), ...] 를 따라 움직이는 점(또는 shape)."""
    stops = [(p, f"{_tr(x, y)};opacity:{v}") for p, x, y, v in pts]
    inner = shape or f'<circle r="{r}" fill="{color}"/>'
    return f'<g class="mv" {d.a(stops)}>{inner}</g>'


# ════════════════════════════════════════════════════════════
# 1. 컨텍스트 창 = 책상
# ════════════════════════════════════════════════════════════
def context_window():
    d = _D("cw", 12)
    X0, Y, H, BW = 60, 110, 84, 1040
    fixed = [("시스템", 1, .06), ("도구 목록", .72, .10), ("CLAUDE.md", .5, .05), ("Skill 설명", .3, .04)]
    clip = d.id("clip")
    s = f'<clipPath id="{clip}"><rect x="{X0}" y="{Y}" width="{BW}" height="{H}" rx="12"/></clipPath>'
    s += f'<rect x="{X0}" y="{Y}" width="{BW}" height="{H}" rx="12" fill="{G}" fill-opacity=".3"/>'
    s += f'<g clip-path="url(#{clip})">'
    x = X0
    for _, op, f in fixed:
        s += f'<rect x="{x:g}" y="{Y}" width="{f*BW:g}" height="{H}" fill="{N}" fill-opacity="{op}" stroke="{W}" stroke-width="1.5"/>'
        x += f * BW
    XF = x
    # 상태: (시각%, 요약, 대화, 도구 결과) — 너비 비율
    st, conv, res = [(0, 0, 0, 0)], 0, 0
    pre = [4, 11, 18, 25, 32, 39, 46, 53]
    post = [75, 82]
    for t in pre:
        st.append((t, 0, conv, res))
        conv, res = conv + .025, res + .044
        st.append((t + 3, 0, conv, res))
    st += [(60, 0, conv, res), (68, .05, 0, 0)]
    conv = res = 0
    for t in post:
        st.append((t, .05, conv, res))
        conv, res = conv + .025, res + .044
        st.append((t + 3, .05, conv, res))
    st += [(95, .05, conv, res), (100, 0, 0, 0)]
    # 인쇄 장면: 압축 직전 (80% 근처)
    pc, pr = .025 * 8, .044 * 8

    def seg(kind, fill, op, bx, bw):
        stops = []
        for t, sm, cv, rs in st:
            xx, ww = {"sum": (XF, sm), "conv": (XF + sm * BW, cv), "res": (XF + (sm + cv) * BW, rs)}[kind]
            ww = ww * BW
            stops.append((t, f"x:{xx:g}px;width:{ww:g}px"))
        return (f'<rect x="{bx:g}" y="{Y}" width="{bw:g}" height="{H}" fill="{fill}" fill-opacity="{op}" '
                f'stroke="{W}" stroke-width="1.5" {d.a(stops)}/>')

    s += seg("sum", O, .35, XF, 0)
    s += seg("conv", G, 1, XF, pc * BW)
    s += seg("res", O, 1, XF + pc * BW, pr * BW)
    s += "</g>"
    s += f'<rect x="{X0}" y="{Y}" width="{BW}" height="{H}" rx="12" fill="none" stroke="{N}" stroke-width="3"/>'
    s += _t(X0, 88, "컨텍스트 창", "tt", "start") + _t(X0 + 124, 89, "= 책상 위 공간", "ts", "start")
    s += _t(X0 + BW, 88, "한도", "tt", "end")
    x80 = X0 + .8 * BW
    s += f'<line x1="{x80:g}" y1="{Y-8}" x2="{x80:g}" y2="{Y+H+8}" stroke="{N}" stroke-width="2" stroke-dasharray="5 5"/>'
    s += _t(x80, Y + H + 24, "80%", "tn")
    # /compact 알림
    call = (f'<rect x="{x80-72:g}" y="18" width="144" height="40" rx="20" fill="{O}"/>'
            + _t(x80, 39, "/compact", "tw", extra='style="font-size:18px"')
            + f'<line x1="{x80:g}" y1="58" x2="{x80:g}" y2="{Y-12}" stroke="{O}" stroke-width="3"/>'
            + _t(x80 + 84, 39, "대화 → 요약", "to", "start"))
    s += f'<g {d.a([(0, "opacity:0"), (54, "opacity:0"), (57, "opacity:1"), (70, "opacity:1"), (74, "opacity:0"), (100, "opacity:0")])}>{call}</g>'
    # 턴 표시
    TY = 270
    s += _t(X0, TY, "턴", "tt", "start")
    turns = pre + post
    for i, t in enumerate(turns):
        cx = 130 + i * 92 + (60 if i >= 8 else 0)
        base = O if i < 8 else G
        s += (f'<circle cx="{cx}" cy="{TY}" r="12" fill="{base}" '
              + d.a([(0, f"fill:{G}"), (t, f"fill:{G}"), (t + 1, f"fill:{O}"), (95, f"fill:{O}"), (100, f"fill:{G}")]) + "/>")
        s += _t(cx, TY + 30, str(i + 1), "ts", extra='style="font-size:14px"')
    mx = 130 + 7 * 92 + 76
    s += f'<line x1="{mx}" y1="{TY-20}" x2="{mx}" y2="{TY+20}" stroke="{O}" stroke-width="3"/>'
    s += _t(mx, TY + 30, "압축", "to", extra='style="font-size:14px"')
    # 범례
    leg = [("시스템", N, 1), ("도구 목록", N, .72), ("CLAUDE.md", N, .5), ("Skill 설명", N, .3),
           ("대화", G, 1), ("도구 결과", O, 1), ("요약", O, .35)]
    LY = 360
    for i, (name, c, op) in enumerate(leg):
        lx = X0 + i * 150
        s += f'<rect x="{lx}" y="{LY-11}" width="22" height="22" rx="4" fill="{c}" fill-opacity="{op}"/>'
        s += _t(lx + 30, LY + 1, name, "ts", "start")
    return d.svg(1160, 390, s)


# ════════════════════════════════════════════════════════════
# 2. Sub Agent 위임
# ════════════════════════════════════════════════════════════
def subagent_fanout():
    d = _D("sa", 10)
    s = ""
    MX, MY = 340, 230
    s += _box(40, 130, 300, 200, "", sub="")
    s += _t(190, 176, "메인 에이전트", "tt") + _t(190, 203, "Supervisor", "ts")
    s += _t(70, 256, "컨텍스트", "ts", "start")
    s += f'<rect x="70" y="268" width="240" height="22" rx="5" fill="{W}" stroke="{G}" stroke-width="2"/>'
    s += (f'<rect x="70" y="268" width="80" height="22" rx="5" fill="{N}" '
          + d.a([(0, "transform:scaleX(.5)"), (80, "transform:scaleX(.5)"), (86, "transform:scaleX(1)"),
                 (95, "transform:scaleX(1)"), (100, "transform:scaleX(.5)")],
                extra="transform-box:fill-box;transform-origin:0 50%") + "/>")
    subs = [20, 175, 330]
    for i, sy in enumerate(subs):
        ty = sy + 60
        s += f'<line x1="{MX}" y1="{MY}" x2="820" y2="{ty}" stroke="{G}" stroke-width="3" stroke-dasharray="7 6"/>'
    for i, sy in enumerate(subs):
        s += f'<rect x="820" y="{sy}" width="300" height="120" rx="14" fill="{W}" stroke="{N}" stroke-width="3"/>'
        s += _t(970, sy + 32, f"Sub Agent {i+1}", "tt")
        s += _t(850, sy + 60, "자기 컨텍스트", "ts", "start", 'style="font-size:14px"')
        s += f'<rect x="850" y="{sy+74}" width="240" height="22" rx="5" fill="{W}" stroke="{G}" stroke-width="2"/>'
        s += (f'<rect x="850" y="{sy+74}" width="228" height="22" rx="5" fill="{O}" '
              + d.a([(0, "transform:scaleX(0)"), (22 + i * 2, "transform:scaleX(0)"), (52 + i * 3, "transform:scaleX(1)"),
                     (92, "transform:scaleX(1)"), (100, "transform:scaleX(0)")],
                    "ease-in-out", "transform-box:fill-box;transform-origin:0 50%") + "/>")
    pkt = (f'<rect x="-18" y="-13" width="36" height="26" rx="4" fill="{O}"/>'
           f'<line x1="-10" y1="-4" x2="10" y2="-4" stroke="{W}" stroke-width="2.5"/>'
           f'<line x1="-10" y1="4" x2="5" y2="4" stroke="{W}" stroke-width="2.5"/>')
    for i, sy in enumerate(subs):
        ty, a = sy + 60, i * 2
        s += _move(d, [(0, MX, MY, 0), (4 + a, MX, MY, 0), (5 + a, MX + 12, MY, 1), (20 + a, 805, ty, 1),
                       (22 + a, 812, ty, 0), (100, 812, ty, 0)], shape=pkt)
        b = i * 3
        s += _move(d, [(0, 815, ty, 0), (58 + b, 815, ty, 0), (59 + b, 805, ty, 1), (76 + b, MX + 14, MY, 1),
                       (78 + b, MX + 8, MY, 0), (100, MX, MY, 0)], r=8)
    # 단계 캡션
    caps = [("① 위임", 0, 22), ("② 각자 조사", 22, 58), ("③ 결과만 반환", 58, 90)]
    for i, (c, a, b) in enumerate(caps):
        stops = [(0, f"fill:{N}")] if a > 0 else []
        stops += [(max(a, 0.1) if a else 0, f"fill:{O}"), (b, f"fill:{O}"), (b + 1, f"fill:{N}"), (100, f"fill:{N}")]
        if a > 0:
            stops.insert(1, (a - 1, f"fill:{N}"))
        s += _t(40, 380 + i * 32, c, "tt", "start", d.a(stops))
    s += _t(560, 440, "메인에는 짧은 요약만 쌓인다", "ts")
    return d.svg(1160, 460, s)


# ════════════════════════════════════════════════════════════
# 3. Agent Teams — 동료끼리 직접 메시지 + 공유 작업 목록
# ════════════════════════════════════════════════════════════
def agent_teams():
    d = _D("at", 12)
    s = ""
    peers = {"A": (40, 40), "B": (40, 350), "C": (930, 40), "D": (930, 350)}
    PW, PH = 190, 80
    ctr = {k: (x + PW / 2, y + PH / 2) for k, (x, y) in peers.items()}
    # 경로 선 (동료 ↔ 동료)
    ln = f'stroke="{G}" stroke-width="3"'
    s += f'<line x1="230" y1="80" x2="930" y2="80" {ln}/><line x1="230" y1="390" x2="930" y2="390" {ln}/>'
    s += f'<line x1="135" y1="120" x2="135" y2="350" {ln}/><line x1="1025" y1="120" x2="1025" y2="350" {ln}/>'
    # 동료 → 작업 목록 (점선)
    dl = f'stroke="{N}" stroke-width="2" stroke-dasharray="4 6" opacity=".45"'
    s += (f'<line x1="230" y1="112" x2="380" y2="160" {dl}/><line x1="930" y1="112" x2="780" y2="160" {dl}/>'
          f'<line x1="230" y1="358" x2="380" y2="330" {dl}/><line x1="930" y1="358" x2="780" y2="330" {dl}/>')
    # 메일박스
    s += f'<rect x="550" y="62" width="60" height="38" rx="6" fill="{W}" stroke="{N}" stroke-width="3"/>'
    s += f'<path d="M552 64 L580 84 L608 64" fill="none" stroke="{N}" stroke-width="2.5"/>'
    s += _t(580, 40, "메일박스", "tn")
    # 작업 목록
    s += f'<rect x="380" y="128" width="400" height="236" rx="14" fill="{W}" stroke="{N}" stroke-width="3"/>'
    s += _t(580, 152, "공유 작업 목록", "tt", extra='style="font-size:17px"')
    cols = [("할 일", 395), ("진행", 525), ("완료", 655)]
    for name, cx in cols:
        s += f'<rect x="{cx}" y="170" width="120" height="182" rx="8" fill="{G}" fill-opacity=".4"/>'
        s += _t(cx + 60, 188, name, "ts")
    # 카드: (행 y, 진행 시작, 완료 시작, 인쇄 상태 열, 맡은 동료)
    cards = [(220, 8, 30, 2, "A"), (257, 30, 55, 2, "C"), (294, 52, 80, 1, "D"), (331, 82, 200, 0, "B")]
    sty = {0: (W, N), 1: (O, W), 2: (N, W)}
    for i, (cy, a, b, pcol, who) in enumerate(cards):
        def col_at(c):
            return f"{_tr(c * 130, 0)}"

        stops_g = [(0, col_at(0)), (a, col_at(0)), (a + 2, col_at(1))]
        stops_r = [(0, f"fill:{W}"), (a, f"fill:{W}"), (a + 2, f"fill:{O}")]
        stops_t = [(0, f"fill:{N}"), (a, f"fill:{N}"), (a + 2, f"fill:{W}")]
        if b < 100:
            stops_g += [(b, col_at(1)), (b + 2, col_at(2)), (96, col_at(2))]
            stops_r += [(b, f"fill:{O}"), (b + 2, f"fill:{N}"), (96, f"fill:{N}")]
            stops_t += [(b, f"fill:{W}"), (b + 2, f"fill:{W}"), (96, f"fill:{W}")]
        else:
            stops_g += [(96, col_at(1))]
            stops_r += [(96, f"fill:{O}")]
            stops_t += [(96, f"fill:{W}")]
        stops_g += [(100, col_at(0))]
        stops_r += [(100, f"fill:{W}")]
        stops_t += [(100, f"fill:{N}")]
        f_, tc = sty[pcol]
        s += (f'<g transform="translate({pcol*130},0)" {d.a(stops_g, "ease-in-out")}>'
              f'<rect x="405" y="{cy-15}" width="100" height="30" rx="6" fill="{f_}" stroke="{N}" stroke-width="2" {d.a(stops_r)}/>'
              + _t(455, cy + 1, f"작업 {i+1}", "tn", extra=d.a(stops_t, extra=f"font-size:14px;fill:{tc}"))
              + "</g>")
    # 동료 상자 — 맡은 작업이 진행 중이면 주황 테두리
    work = {who: (a, min(b, 96)) for (_, a, b, _, who) in cards}
    for k, (x, y) in peers.items():
        a, b = work[k]
        busy_print = k == "D"
        st_ = [(0, f"stroke:{N}"), (a, f"stroke:{N}"), (a + 2, f"stroke:{O}"), (b, f"stroke:{O}"), (b + 2, f"stroke:{N}"), (100, f"stroke:{N}")]
        s += (f'<rect x="{x}" y="{y}" width="{PW}" height="{PH}" rx="14" fill="{W}" stroke="{O if busy_print else N}" '
              f'stroke-width="3.5" {d.a(st_)}/>')
        s += _t(x + PW / 2, y + PH / 2 - 10, f"에이전트 {k}", "tt")
        s += _t(x + PW / 2, y + PH / 2 + 16, "팀원", "ts", extra='style="font-size:14px"')
    # 편지: 동료 → 동료
    env = (f'<rect x="-17" y="-12" width="34" height="24" rx="3" fill="{O}"/>'
           f'<path d="M-15 -10 L0 2 L15 -10" fill="none" stroke="{W}" stroke-width="2.2"/>')
    routes = [
        [(5, 245, 80), (13, 580, 80), (16, 580, 80), (24, 915, 80)],      # A → C (메일박스 경유)
        [(30, 1025, 135), (40, 1025, 335)],                                # C → D
        [(48, 915, 390), (62, 245, 390)],                                  # D → B
        [(68, 135, 335), (78, 135, 135)],                                  # B → A
        [(84, 915, 80), (92, 580, 80)],                                    # C → 메일박스
    ]
    for r in routes:
        p0, x0, y0 = r[0]
        p1, x1, y1 = r[-1]
        pts = [(0, x0, y0, 0), (p0 - .5, x0, y0, 0), (p0, x0, y0, 1)] + [(p, x, y, 1) for p, x, y in r[1:]]
        pts += [(p1 + 1.5, x1, y1, 0), (100, x1, y1, 0)]
        s += _move(d, pts, shape=env)
    s += _t(580, 450, "Agent Teams (실험 기능)", "ts", extra=f'style="font-size:14px;fill:{N};opacity:.6"')
    return d.svg(1160, 466, s)


# ════════════════════════════════════════════════════════════
# 4. 오케스트레이션 패턴 4가지
# ════════════════════════════════════════════════════════════
def orchestration_patterns():
    d = _D("op", 8)
    s = ""
    CW, CH = 570, 225
    cells = [(0, 0, "순차"), (590, 0, "병렬 분배 · 수집"), (0, 245, "감독 · 검증 루프"), (590, 245, "평가 · 개선 루프")]
    for cx, cy, t in cells:
        s += f'<rect x="{cx+1.5}" y="{cy+1.5}" width="{CW-3}" height="{CH-3}" rx="14" fill="{W}" stroke="{G}" stroke-width="2.5"/>'
        s += _t(cx + 22, cy + 30, t, "tt", "start", 'style="font-size:18px"')

    top = []  # 상자는 점 위에 그린다 → 점이 상자 안에 들어가면 상자 테두리가 주황으로 켜진다

    def node(x, y, w, h, label, win=()):
        st = ""
        if win:
            stops = [(0, f"stroke:{N}")]
            for a, b in win:
                stops += [(a, f"stroke:{N}"), (a + 1, f"stroke:{O}"), (b, f"stroke:{O}"), (b + 1, f"stroke:{N}")]
            stops += [(100, f"stroke:{N}")]
            st = d.a(stops)
        top.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{W}" stroke="{N}" stroke-width="3" {st}/>'
                   + _t(x + w / 2, y + h / 2 + 1, label, "tn", extra='style="font-size:16px"'))
        return ""

    def arr(x1, y1, x2, y2, c=N, dash=""):
        m = d.id("aho" if c == O else "ah")
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="2.5"{dd} marker-end="url(#{m})"/>'

    # ① 순차
    cx, cy = 0, 0
    ys = cy + 100
    xs = [cx + 45, cx + 230, cx + 415]
    for x, l, w in zip(xs, "ABC", [(3, 15), (32, 49), (66, 87)]):
        s += node(x, ys, 110, 54, l, [w])
    s += arr(xs[0] + 112, ys + 27, xs[1] - 4, ys + 27) + arr(xs[1] + 112, ys + 27, xs[2] - 4, ys + 27)
    c = [x + 55 for x in xs]
    yc = ys + 27
    s += _move(d, [(0, c[0], yc, 0), (4, c[0], yc, 1), (14, c[0], yc, 1), (34, c[1], yc, 1), (48, c[1], yc, 1),
                   (68, c[2], yc, 1), (86, c[2], yc, 1), (92, c[2], yc, 0), (100, c[2], yc, 0)], r=10)
    s += _t(cx + CW / 2, cy + 190, "앞 단계 결과가 다음 단계 입력", "ts")

    # ② 병렬 분배 · 수집
    cx, cy = 590, 0
    src = (cx + 30, cy + 98, 100, 50)
    col = (cx + 440, cy + 98, 100, 50)
    wy = [cy + 52, cy + 104, cy + 156]
    s += node(*src, "분배", [(5, 13)]) + node(*col, "수집", [(62, 89)])
    for i, y in enumerate(wy):
        s += node(cx + 225, y, 120, 38, f"작업 {i+1}", [(31, 41 + i * 6)])
        s += arr(src[0] + 102, cy + 123, cx + 221, y + 19) + arr(cx + 347, y + 19, col[0] - 4, cy + 109 + i * 14)
    sx, sy_ = src[0] + 50, cy + 123
    ex = col[0] + 50
    for i, y in enumerate(wy):
        wx, wyc = cx + 285, y + 19
        s += _move(d, [(0, sx, sy_, 0), (6, sx, sy_, 1), (12, sx, sy_, 1), (34, wx, wyc, 1), (40 + i * 6, wx, wyc, 1),
                       (64 + i * 4, ex, sy_, 1), (88, ex, sy_, 1), (93, ex, sy_, 0), (100, ex, sy_, 0)], r=9)

    # ③ 감독 · 검증 루프
    cx, cy = 0, 245
    ny = cy + 72
    nx = [cx + 30, cx + 210, cx + 390]
    for x, l, w in zip(nx, ["감독", "작업", "검증"], [[(2, 9)], [(16, 25), (57, 63)], [(32, 41), (70, 77)]]):
        s += node(x, ny, 100, 54, l, w)
    s += arr(nx[0] + 102, ny + 27, nx[1] - 4, ny + 27) + arr(nx[1] + 102, ny + 27, nx[2] - 4, ny + 27)
    by = cy + 172
    s += (f'<path d="M{nx[2]+50} {ny+56} L{nx[2]+50} {by} L{nx[1]+50} {by} L{nx[1]+50} {ny+60}" fill="none" '
          f'stroke="{O}" stroke-width="2.5" stroke-dasharray="6 5" marker-end="url(#{d.id("aho")})"/>')
    s += _t((nx[1] + nx[2]) / 2 + 50, by + 22, "실패 → 다시", "to")
    s += arr(nx[2] + 102, ny + 27, cx + 525, ny + 27)
    pas = _t(cx + 534, ny - 6, "통과", "to")
    s += f'<g {d.a([(0, "opacity:0"), (80, "opacity:0"), (83, "opacity:1"), (96, "opacity:1"), (100, "opacity:0")])}>{pas}</g>'
    a, b, c3 = nx[0] + 50, nx[1] + 50, nx[2] + 50
    yc = ny + 27
    s += _move(d, [(0, a, yc, 0), (3, a, yc, 1), (8, a, yc, 1), (18, b, yc, 1), (24, b, yc, 1), (34, c3, yc, 1),
                   (40, c3, yc, 1), (44, c3, by, 1), (54, b, by, 1), (58, b, yc, 1), (62, b, yc, 1), (72, c3, yc, 1),
                   (76, c3, yc, 1), (82, cx + 530, yc, 1), (90, cx + 530, yc, 1), (94, cx + 530, yc, 0), (100, cx + 530, yc, 0)], r=10)

    # ④ 평가 · 개선 루프
    cx, cy = 590, 245
    gx, ex_, ny = cx + 50, cx + 370, cy + 78
    s += node(gx, ny, 140, 60, "생성") + node(ex_, ny, 140, 60, "평가")
    s += arr(gx + 142, ny + 18, ex_ - 4, ny + 18) + arr(ex_ - 2, ny + 44, gx + 146, ny + 44)
    s += _t((gx + ex_ + 140) / 2, ny + 4, "초안", "ts") + _t((gx + ex_ + 140) / 2, ny + 62, "피드백", "ts")
    pas = _t(ex_ + 70, ny + 92, "통과 ✓", "to", extra='style="font-size:17px"')
    s += f'<g {d.a([(0, "opacity:0"), (80, "opacity:0"), (83, "opacity:1"), (96, "opacity:1"), (100, "opacity:0")])}>{pas}</g>'
    s += _t(gx + 70, ny + 92, "기준을 넘을 때까지", "ts")
    L, R = gx + 156, ex_ - 16
    t1, t2 = ny + 18, ny + 44
    pts = [(0, L, t1, 0), (3, L, t1, 1)]
    p = 3
    for k in range(3):
        pts += [(p + 10, R, t1, 1), (p + 14, R, t1, 1)]
        p += 14
        if k < 2:
            pts += [(p + 1, R, t2, 1), (p + 10, L, t2, 1), (p + 14, L, t2, 1), (p + 15, L, t1, 1)]
            p += 15
    pts += [(90, R, t1, 1), (94, R, t1, 0), (100, R, t1, 0)]
    s += _move(d, pts, r=10)
    return d.svg(1160, 470, s + "".join(top))


# ════════════════════════════════════════════════════════════
# 5. 타임라인 — 병렬 Sub Agent 작업과 검증 · 재실행
# ════════════════════════════════════════════════════════════
def timeline_lanes():
    d = _D("tl", 12)
    lanes = ["메인", "분류", "응대 A", "응대 B", "검증"]
    L0, LH, TX0, TX1 = 40, 76, 150, 1130
    TW = TX1 - TX0
    P = .86  # 재생선이 끝까지 가는 비율

    def tx(u):
        return TX0 + TW * u / 100

    def tp(u):
        return u * P

    s = _t(TX0, 18, "시간 →", "ts", "start")
    for i, name in enumerate(lanes):
        y = L0 + i * LH
        if i % 2 == 0:
            s += f'<rect x="0" y="{y}" width="1160" height="{LH}" fill="{G}" fill-opacity=".28"/>'
        s += _t(128, y + LH / 2, name, "tt", "end", 'style="font-size:18px"')
    s += f'<line x1="{TX0-6}" y1="{L0}" x2="{TX0-6}" y2="{L0+5*LH}" stroke="{N}" stroke-width="2"/>'

    def fade_in(u):
        return [(0, "opacity:0"), (tp(u), "opacity:0"), (tp(u) + 1, "opacity:1"), (96, "opacity:1"), (100, "opacity:0")]

    def bar(lane, a, b, label, kind="n"):
        y = L0 + lane * LH + 18
        x, w = tx(a), tx(b) - tx(a)
        fill, stroke, cls = {"n": (N, N, "tw"), "o": (O, O, "tw"), "r": (W, O, "to")}[kind]
        grow = [(0, "transform:scaleX(0);opacity:1"), (tp(a), "transform:scaleX(0);opacity:1"),
                (tp(b), "transform:scaleX(1);opacity:1"), (96, "transform:scaleX(1);opacity:1"), (100, "transform:scaleX(1);opacity:0")]
        r = (f'<rect x="{x:g}" y="{y}" width="{w:g}" height="40" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="3" '
             + d.a(grow, extra="transform-box:fill-box;transform-origin:0 50%") + "/>")
        return r + _t(x + w / 2, y + 21, label, cls, extra=d.a(fade_in(b)))

    def down(u, l1, l2, c=N):
        y1, y2 = L0 + l1 * LH + 60, L0 + l2 * LH + 16
        if l2 < l1:
            y1, y2 = L0 + l1 * LH + 16, L0 + l2 * LH + 60
        m = d.id("aho" if c == O else "ah")
        return (f'<line x1="{tx(u):g}" y1="{y1}" x2="{tx(u):g}" y2="{y2}" stroke="{c}" stroke-width="2.5" '
                f'stroke-dasharray="5 4" marker-end="url(#{m})" {d.a(fade_in(u))}/>')

    s += bar(0, 0, 10, "요청 분석") + bar(0, 88, 100, "취합")
    s += down(10.5, 0, 1)
    s += bar(1, 11, 26, "분류")
    s += down(27, 0, 2) + down(28.5, 0, 3)
    s += bar(2, 29, 62, "응대 A") + bar(3, 30, 50, "응대 B")
    s += bar(4, 51, 58, "B 실패", "o")
    s += down(58.5, 4, 3, O)
    s += bar(3, 59, 78, "재실행", "r")
    s += bar(4, 63, 70, "A 통과") + bar(4, 79, 86, "B 통과")
    s += down(87, 4, 0)
    # 재생선
    ph = (f'<line x1="0" y1="{L0-6}" x2="0" y2="{L0+5*LH+6}" stroke="{O}" stroke-width="3"/>'
          f'<circle cx="0" cy="{L0-6}" r="6" fill="{O}"/>')
    s += (f'<g class="mv" {d.a([(0, f"{_tr(TX0, 0)};opacity:1"), (P * 100, f"{_tr(TX1, 0)};opacity:1"), (92, f"{_tr(TX1, 0)};opacity:1"), (96, f"{_tr(TX1, 0)};opacity:0"), (100, f"{_tr(TX0, 0)};opacity:0")])}>{ph}</g>')
    return d.svg(1160, 430, s)


# ════════════════════════════════════════════════════════════
# 6. 프롬프트 캐시 — 접두부가 같아야 적중
# ════════════════════════════════════════════════════════════
def cache_prefix():
    d = _D("cp", 12)
    s = ""
    WD = {"도구 목록": 120, "시스템": 120, "CLAUDE.md": 120}

    def blocks(n, stamp=None):
        sysl = f"시스템 {stamp}" if stamp else "시스템"
        out = [("도구 목록", 120), (sysl, 120), ("CLAUDE.md", 120)]
        out += [(f"대화 {k}", 90) for k in range(1, n)]
        out += [(f"질문 {n}", 90)]
        return out

    # (헤더, 행들) 행 = (블록, 종류 문자열 h=적중 g=새로 b=깨짐, 결과 글, 글 클래스)
    secs = [
        ("접두부를 그대로 둘 때", 22, [
            (blocks(1), "gggg", "처음 · 캐시에 저장", "ts"),
            (blocks(2), "hhhhg", "적중 4칸", "tn"),
            (blocks(3), "hhhhhg", "적중 5칸", "tn"),
        ]),
        ("시스템에 현재 시각을 넣을 때", 232, [
            (blocks(1, "12:01"), "gggg", "처음 · 캐시에 저장", "ts"),
            (blocks(2, "12:02"), "hbbbg", "적중 1칸 · 나머지 깨짐", "to"),
            (blocks(3, "12:03"), "hbbbbg", "적중 1칸 · 나머지 깨짐", "to"),
        ]),
    ]
    starts = [2, 13, 24, 45, 56, 67]
    col = {"h": (N, W), "g": (G, N), "b": (O, W)}
    ri = 0
    for head, hy, rows in secs:
        s += _t(20, hy, head, "tt", "start", 'style="font-size:18px"')
        for k, (bl, kinds, res, rcls) in enumerate(rows):
            y = hy + 20 + k * 46
            t0 = starts[ri]
            ri += 1
            s += _t(20, y + 19, f"요청 {k+1}", "ts", "start")
            x = 100
            for j, ((label, w), kd) in enumerate(zip(bl, kinds)):
                fill, tc = col[kd]
                ta, tc_ = t0 + j * .8, t0 + 6 + j * .6
                op = [(0, "opacity:0"), (ta, "opacity:0"), (ta + 1, "opacity:1"), (95, "opacity:1"), (99, "opacity:0"), (100, "opacity:0")]
                rf = [(0, f"fill:{G}"), (tc_, f"fill:{G}"), (tc_ + 1.5, f"fill:{fill}"), (100, f"fill:{fill}")]
                tf = [(0, f"fill:{N}"), (tc_, f"fill:{N}"), (tc_ + 1.5, f"fill:{tc}"), (100, f"fill:{tc}")]
                s += (f'<g {d.a(op)}><rect x="{x}" y="{y}" width="{w}" height="38" rx="6" fill="{fill}" {d.a(rf)}/>'
                      + _t(x + w / 2, y + 20, label, "tn", extra=d.a(tf, extra=f"fill:{tc}")) + "</g>")
                x += w + 6
            s += _t(790, y + 20, res, rcls, "start", d.a([(0, "opacity:0"), (t0 + 10, "opacity:0"), (t0 + 11.5, "opacity:1"), (95, "opacity:1"), (99, "opacity:0"), (100, "opacity:0")]))
        if hy == 22:
            s += f'<line x1="20" y1="{hy+170}" x2="1140" y2="{hy+170}" stroke="{G}" stroke-width="2"/>'
    LY = 418
    for i, (name, c) in enumerate([("캐시 적중", N), ("새로 처리", G), ("캐시 깨짐", O)]):
        lx = 100 + i * 170
        s += f'<rect x="{lx}" y="{LY-11}" width="22" height="22" rx="4" fill="{c}"/>' + _t(lx + 30, LY + 1, name, "ts", "start")
    return d.svg(1160, 440, s)


# ════════════════════════════════════════════════════════════
# 7. 토큰 계량기 — 하네스 미적용 vs 하네스 + 레버
# ════════════════════════════════════════════════════════════
def token_meter():
    d = _D("tm", 9)
    BASE, TOP = 390, 40
    s = ""
    bars = [("하네스 미적용", 250, [("입력(캐시)", G, 18), ("입력(새)", N, 200), ("출력", O, 112)], 0),
            ("하네스 + 레버", 610, [("입력(캐시)", G, 150), ("입력(새)", N, 46), ("출력", O, 44)], 36)]
    for name, x, segs, t0 in bars:
        y = BASE
        lab = ""
        for lname, c, h in segs:
            y -= h
            s += f'<rect x="{x}" y="{y}" width="180" height="{h}" fill="{c}" stroke="{W}" stroke-width="2"/>'
            ly = y + h / 2
            lab += f'<line x1="{x+186}" y1="{ly:g}" x2="{x+204}" y2="{ly:g}" stroke="{G}" stroke-width="2"/>'
            lab += _t(x + 210, ly, lname, "tn" if c != O else "to", "start")
        # 덮개: 위에서부터 걷힌다
        s += (f'<rect class="mv" x="{x-4}" y="{TOP-4}" width="188" height="{BASE-TOP+4}" fill="{W}" '
              + d.a([(0, "transform:scaleY(1)"), (t0 + 2, "transform:scaleY(1)"), (t0 + 30, "transform:scaleY(0)"),
                     (92, "transform:scaleY(0)"), (100, "transform:scaleY(1)")], "ease-in-out",
                    "transform-box:fill-box;transform-origin:50% 0") + "/>")
        s += f'<g {d.a([(0, "opacity:0"), (t0 + 30, "opacity:0"), (t0 + 34, "opacity:1"), (92, "opacity:1"), (97, "opacity:0"), (100, "opacity:0")])}>{lab}</g>'
        s += _t(x + 90, BASE + 30, name, "tt")
    s += f'<line x1="200" y1="{BASE}" x2="900" y2="{BASE}" stroke="{N}" stroke-width="3"/>'
    s += f'<rect x="1010" y="24" width="110" height="32" rx="16" fill="none" stroke="{G}" stroke-width="2"/>' + _t(1065, 41, "예시 비율", "ts")
    notes = [("같은 작업", "tt"), ("캐시 비중 ↑", "to"), ("새 입력 ↓", "tn"), ("출력 ↓", "to")]
    nt = "".join(_t(970, 150 + i * 36, n, c, "start") for i, (n, c) in enumerate(notes))
    s += f'<g {d.a([(0, "opacity:0"), (68, "opacity:0"), (72, "opacity:1"), (92, "opacity:1"), (97, "opacity:0"), (100, "opacity:0")])}>{nt}</g>'
    return d.svg(1160, 440, s)


# ════════════════════════════════════════════════════════════
# 8. 토큰 레버 — 거름망을 지날 때마다 줄어드는 더미
# ════════════════════════════════════════════════════════════
def token_levers():
    d = _D("tv", 10)
    BASE = 400
    gates = ["출력 줄이기", "명령 출력 압축", "필요한 것만 읽기", "Sub Agent 분리", "오래된 결과 정리"]
    gx = [205, 395, 585, 775, 965]
    px = [110, 300, 490, 680, 870, 1070]
    counts = [18, 14, 11, 8, 6, 4]
    s = ""
    # 지나가는 흐름 (요청)
    T0, T1 = 4, 70

    def at(x):
        return T0 + (T1 - T0) * (x - px[0]) / (px[-1] - px[0])

    s += f'<line x1="60" y1="{BASE}" x2="1130" y2="{BASE}" stroke="{N}" stroke-width="3"/>'
    for i, (g, x) in enumerate(zip(gates, gx)):
        t = at(x)
        s += (f'<rect x="{x-12}" y="110" width="24" height="{BASE-110}" rx="6" fill="{N}" '
              + d.a([(0, f"fill:{N}"), (t - 1.5, f"fill:{N}"), (t, f"fill:{O}"), (t + 4, f"fill:{O}"), (t + 7, f"fill:{N}"), (100, f"fill:{N}")]) + "/>")
        s += _t(x, 90, g, "tn")
        s += f'<circle cx="{x}" cy="58" r="14" fill="{W}" stroke="{N}" stroke-width="2.5"/>' + _t(x, 59, str(i + 1), "tn", extra='style="font-size:14px"')
    for k, (x, n) in enumerate(zip(px, counts)):
        chips = "".join(f'<rect x="{x-32}" y="{BASE-6-(j+1)*15}" width="64" height="11" rx="3" fill="{O}" fill-opacity="{.95 - .02*j:g}"/>'
                        for j in range(n))
        if k == 0:
            s += f"<g>{chips}</g>"
        else:
            t = at(x)
            s += (f'<g {d.a([(0, "opacity:0;transform:translateY(-14px)"), (t - 2, "opacity:0;transform:translateY(-14px)"), (t + 2, "opacity:1;transform:translateY(0)"), (94, "opacity:1;transform:translateY(0)"), (99, "opacity:0;transform:translateY(0)"), (100, "opacity:0;transform:translateY(-14px)")], "ease-out")}>{chips}</g>')
    s += _t(px[0], BASE + 24, "처음", "ts") + _t(px[-1], BASE + 24, "남은 양", "to")
    # 흐르는 요청 표시
    pill = (f'<rect x="-30" y="-14" width="60" height="28" rx="14" fill="{O}"/>' + _t(0, 1, "요청", "tw", extra='style="font-size:14px"'))
    s += _move(d, [(0, px[0], 452, 0), (T0 - 2, px[0], 452, 0), (T0, px[0], 452, 1), (T1, px[-1], 452, 1),
                   (T1 + 4, px[-1], 452, 0), (100, px[-1], 452, 0)], shape=pill)
    return d.svg(1160, 470, s)


ALL = [context_window, subagent_fanout, agent_teams, orchestration_patterns,
       timeline_lanes, cache_prefix, token_meter, token_levers]
