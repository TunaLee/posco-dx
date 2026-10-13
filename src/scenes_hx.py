"""하네스 장면: 흔들리는 답 vs 한결같은 답 · 문의 라우팅 · 사양서 추출 · 회귀 테스트 게이트."""
import math

from art import *  # noqa


def _hand(x, y, r=10):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{G}" stroke="{N}" stroke-width="3"/>'


def _phand(x, y, s=1):
    return f'<circle cx="{x}" cy="{y}" r="{12*s}" fill="{W}" stroke="{N}" stroke-width="3"/>'


def _arrow(x1, y1, x2, y2, cx=None, cy=None, color=N, op=.55, w=4):
    """점선 화살표. cx, cy 를 주면 휘어진다."""
    if cx is None:
        a = math.atan2(y2 - y1, x2 - x1)
        d = f"M{x1} {y1} L{x2} {y2}"
    else:
        a = math.atan2(y2 - cy, x2 - cx)
        d = f"M{x1} {y1} Q{cx} {cy} {x2} {y2}"
    l, k = 13, .55
    p1 = (x2 - l * math.cos(a - k), y2 - l * math.sin(a - k))
    p2 = (x2 - l * math.cos(a + k), y2 - l * math.sin(a + k))
    return (f'<g stroke="{color}" stroke-opacity="{op}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="{d}" stroke-dasharray="8 9"/>'
            f'<path d="M{p1[0]:.1f} {p1[1]:.1f} L{x2} {y2} L{p2[0]:.1f} {p2[1]:.1f}"/></g>')


def _shape(kind, x, y, r, fill=N):
    """작은 표식 도형. (x, y) = 가운데."""
    if kind == "sq":
        return f'<rect x="{x-r}" y="{y-r}" width="{2*r}" height="{2*r}" rx="{r*.2:.1f}" fill="{fill}"/>'
    if kind == "ci":
        return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>'
    if kind == "tr":
        return f'<path d="M{x} {y-r*1.1:.1f} L{x+r*1.15:.1f} {y+r*.85:.1f} L{x-r*1.15:.1f} {y+r*.85:.1f} Z" fill="{fill}" stroke="{fill}" stroke-width="2" stroke-linejoin="round"/>'
    if kind == "di":
        return f'<path d="M{x} {y-r*1.2:.1f} L{x+r*1.2:.1f} {y} L{x} {y+r*1.2:.1f} L{x-r*1.2:.1f} {y} Z" fill="{fill}"/>'
    if kind == "wv":
        return (f'<path d="M{x-r*1.3:.1f} {y} Q{x-r*.65:.1f} {y-r} {x} {y} Q{x+r*.65:.1f} {y+r} {x+r*1.3:.1f} {y}" '
                f'stroke="{fill}" stroke-width="{r*.45:.1f}" fill="none" stroke-linecap="round"/>')
    return ""


def _envelope(x, y, w=64, h=42, rot=0, fill=W, tag=None):
    """봉투. (x, y) = 가운데."""
    out = (f'<g transform="translate({x},{y}) rotate({rot})">'
           f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="4" fill="{fill}" stroke="{N}" stroke-width="3"/>'
           f'<path d="M{-w/2+3} {-h/2+3} L0 {h*.08:.1f} L{w/2-3} {-h/2+3}" stroke="{N}" stroke-width="3" fill="none" stroke-linejoin="round"/>')
    if tag:
        out += (f'<circle cx="{w/2-4}" cy="{h/2-4}" r="11" fill="{W}" stroke="{N}" stroke-width="2.5"/>'
                + _shape(tag, w / 2 - 4, h / 2 - 4, 5))
    return out + "</g>"


# ── ① 하네스 없는 Agent vs 있는 Agent ────────────────────────
def _qcard(x, y, rot=0):
    """질문 카드(회색). (x, y) = 왼쪽 위, 96x56."""
    return (f'<g transform="rotate({rot} {x+48} {y+28})">'
            f'<rect x="{x}" y="{y}" width="96" height="56" rx="6" fill="{G}" stroke="{N}" stroke-width="3"/>'
            + lines(x + 16, x + 80, [y + 20], W, 6) + lines(x + 16, x + 58, [y + 36], W, 6) + "</g>")


def _acard(x, y, kind, rot=0):
    """답 카드(흰색) + 도형. (x, y) = 왼쪽 위, 96x72."""
    return (f'<g transform="rotate({rot} {x+48} {y+36})">'
            f'<rect x="{x}" y="{y}" width="96" height="72" rx="6" fill="{W}" stroke="{N}" stroke-width="3.5"/>'
            + _shape(kind, x + 30, y + 36, 14)
            + lines(x + 56, x + 80, [y + 28, y + 44], G, 5) + "</g>")


def wobbly_vs_steady():
    fy = 668
    # 왼쪽: 하네스 없음
    qs_l = _qcard(46, 352, -3) + _qcard(52, 436, 2) + _qcard(44, 520, -1)
    rs = 1.05
    bx = 330
    bot_l = robot(bx, fy, rs, rarm(-44, -86, -78, -150, -96, -100) + rarm(44, -86, 80, -150, 98, -100), mouth="wavy")
    qm = (f'<path d="M{bx-16} {fy-266} Q{bx-16} {fy-290} {bx+2} {fy-290} Q{bx+20} {fy-290} {bx+20} {fy-272} '
          f'Q{bx+20} {fy-258} {bx+4} {fy-252} L{bx+4} {fy-240}" stroke="{N}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
          f'<circle cx="{bx+4}" cy="{fy-224}" r="5" fill="{N}"/>')
    ans_l = _acard(470, 268, "tr", -14) + _acard(500, 392, "ci", 10) + _acard(452, 506, "wv", -6)
    arr_l = (_arrow(156, 384, 232, 440) + _arrow(162, 466, 232, 470) + _arrow(156, 548, 232, 500)
             + _arrow(426, 448, 470, 340, 450, 410)
             + _arrow(430, 470, 488, 424) + _arrow(426, 494, 446, 540, 440, 520))
    left = f'''
{floor(320, 670, 290)}
{qs_l}{arr_l}{bot_l}{qm}{ans_l}'''

    # 오른쪽: 하네스 있음 (배낭 · 서류가방 · 케이블)
    bx, rs = 940, 1.05
    pack = (f'<g transform="translate({bx},{fy}) scale({rs})">'
            f'<rect x="-96" y="-128" width="92" height="104" rx="20" fill="{O}" stroke="{N}" stroke-width="4"/>'
            f'<rect x="-88" y="-146" width="62" height="26" rx="4" fill="{W}" stroke="{N}" stroke-width="3" transform="rotate(-8 -57 -133)"/>'
            f'<path d="M-82 -138 L-34 -145" stroke="{G}" stroke-width="4" stroke-linecap="round"/>'
            f'<path d="M-96 -96 Q-60 -88 -40 -96" stroke="{N}" stroke-width="3.5" fill="none"/>'
            f'</g>')
    straps = (f'<path d="M-36 -96 L-30 -38 M36 -96 L30 -38" stroke="{N}" stroke-width="7" stroke-linecap="round"/>'
              f'<rect x="-46" y="-46" width="92" height="12" rx="5" fill="{N}"/>'
              f'<rect x="40" y="-50" width="18" height="20" rx="4" fill="{G}" stroke="{N}" stroke-width="3"/>')
    hx, hy = -84, -64
    case = (f'<path d="M{hx-14} {hy+6} L{hx-14} {hy-4} Q{hx} {hy-14} {hx+14} {hy-4} L{hx+14} {hy+6}" stroke="{N}" stroke-width="5" fill="none"/>'
            f'<rect x="{hx-36}" y="{hy+6}" width="72" height="48" rx="7" fill="{G}" stroke="{N}" stroke-width="4"/>'
            f'<line x1="{hx-36}" y1="{hy+22}" x2="{hx+36}" y2="{hy+22}" stroke="{N}" stroke-width="3"/>'
            f'<rect x="{hx-7}" y="{hy+17}" width="14" height="10" rx="2" fill="{W}" stroke="{N}" stroke-width="2.5"/>')
    arms = rarm(-44, -86, hx, hy - 6, -70, -96) + case + rarm(44, -86, 70, -40, 66, -66)
    bot_r = robot(bx, fy, rs, straps + arms, mouth="smile")
    jx, jy = bx + 58 * rs, fy - 40 * rs
    cable = (f'<path d="M{jx} {jy} C{jx+40} {jy+6} {jx+30} {fy-4} {jx+70} {fy-6}" stroke="{N}" stroke-width="7" fill="none" stroke-linecap="round"/>'
             f'<rect x="{jx+66}" y="{fy-18}" width="26" height="18" rx="4" fill="{N}"/>')
    qs_r = _qcard(682, 352) + _qcard(682, 436) + _qcard(682, 520)
    ans_r = "".join(_acard(1130, y, "ci") for y in (334, 426, 518))
    arr_r = "".join(_arrow(792, y, 842, y) for y in (380, 464, 548)) + "".join(_arrow(1056, y, 1114, y) for y in (370, 462, 554))
    right = f'''
{floor(960, 670, 300)}
{qs_r}{arr_r}{pack}{cable}{bot_r}{ans_r}'''
    return left + f'<line x1="640" y1="190" x2="640" y2="690" stroke="{G}" stroke-width="3"/>' + right


# ── ② 문의 라우팅 ─────────────────────────────────────────
def router_desk():
    fy = 668
    kinds = ["sq", "ci", "tr", "di"]
    bw, gap, x0 = 150, 24, 580
    top, win0, win1, ledge = 70, 150, 286, 300
    booths = []
    for i, k in enumerate(kinds):
        x = x0 + i * (bw + gap)
        cx = x + bw / 2
        sub = robot(cx, win1 + 64, .58, rarm(-44, -86, -66, -40) + rarm(44, -86, 66, -40), mouth="smile")
        booths.append(
            f'<rect x="{x}" y="{top}" width="{bw}" height="{ledge+50-top}" rx="8" fill="{G}" stroke="{N}" stroke-width="4"/>'
            f'<rect x="{x+16}" y="{win0}" width="{bw-32}" height="{win1-win0}" rx="4" fill="{W}" stroke="{N}" stroke-width="3"/>'
            f'<g clip-path="url(#rdwin{i})">{sub}</g>'
            f'<clipPath id="rdwin{i}"><rect x="{x+16}" y="{win0}" width="{bw-32}" height="{win1-win0}" rx="4"/></clipPath>'
            f'<rect x="{x-8}" y="{ledge-14}" width="{bw+16}" height="16" rx="5" fill="{N}"/>'
            f'<circle cx="{cx}" cy="{top+40}" r="24" fill="{W}" stroke="{N}" stroke-width="3.5"/>'
            + _shape(k, cx, top + 40, 11))
    booth_svg = "".join(booths)
    # 책상 + 들어온 봉투 더미
    dx0, dx1, dt = 600, 1010, 566
    desk = (f'<path d="M{dx0+30} {dt} L{dx1-30} {dt} L{dx1} {dt+50} L{dx0} {dt+50} Z" fill="{G}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>'
            f'<rect x="{dx0-6}" y="{dt+50}" width="{dx1-dx0+12}" height="16" rx="4" fill="{N}"/>'
            f'<rect x="{dx0+20}" y="{dt+66}" width="14" height="{fy-dt-66}" fill="{N}"/>'
            f'<rect x="{dx1-34}" y="{dt+66}" width="14" height="{fy-dt-66}" fill="{N}"/>')
    tx = 900
    tray = (f'<path d="M{tx} {dt+4} L{tx+96} {dt+4} L{tx+104} {dt+34} L{tx-6} {dt+34} Z" fill="{N}"/>'
            + _envelope(tx + 48, dt - 6, 76, 40, -4) + _envelope(tx + 50, dt - 22, 76, 40, 5) + _envelope(tx + 46, dt - 36, 76, 40, -2))
    # Supervisor: 왼손으로 답장을 누르고, 오른손 돋보기로 확인
    bx, rs = 760, 1.2
    ex, ey = 680, 590
    env = _envelope(ex, ey, 92, 56, -6, O)
    lh = (636, 596)
    lens = (690, 568)
    rh = (794, 608)
    L = lambda p: ((p[0] - bx) / rs, (p[1] - fy) / rs)
    bot = robot(bx, fy, rs, mouth="flat")
    sup_arms = (f'<g transform="translate({bx},{fy}) scale({rs})">'
                + rarm(-44, -86, *L(lh), -90, -70, hand=False) + rarm(44, -86, *L(rh), hand=False) + "</g>")
    mag = (f'<line x1="{lens[0]+22}" y1="{lens[1]+22}" x2="{rh[0]}" y2="{rh[1]}" stroke="{N}" stroke-width="10" stroke-linecap="round"/>'
           f'<circle cx="{lens[0]}" cy="{lens[1]}" r="30" fill="{W}" fill-opacity=".45" stroke="{N}" stroke-width="7"/>'
           f'<path d="M{lens[0]-17} {lens[1]-12} A20 20 0 0 1 {lens[0]-4} {lens[1]-20}" stroke="{W}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    # 분류해 보내는 봉투들 + 돌아온 답장 경로
    fly = []
    for i, k in enumerate(kinds):
        cx = x0 + i * (bw + gap) + bw / 2
        sx, sy = tx + 48, dt - 64
        mx, my = (sx + cx) / 2 + 30, 420
        if i > 0:
            fly.append(_arrow(sx, sy, cx, ledge + 40, mx, my - 30))
        t = .55
        px = (1 - t) ** 2 * sx + 2 * (1 - t) * t * mx + t * t * cx
        py = (1 - t) ** 2 * sy + 2 * (1 - t) * t * (my - 30) + t * t * (ledge + 40)
        if i > 0:
            fly.append(_envelope(round(px), round(py), 52, 34, (-10, 6, -6, 8)[i], W, k))
    back = _arrow(616, ledge + 44, 640, ey - 40, 590, 470)
    return f'''
{floor(900, 670, 360)}
{booth_svg}
{"".join(fly)}{back}
{bot}{desk}{tray}{env}{sup_arms}{mag}{_hand(*lh)}{_hand(*rh)}'''


# ── ③ 사양서 추출 ────────────────────────────────────────
def spec_extract():
    fy = 668
    # 도면 (이젤에 세운 큰 종이)
    gx0, gy0, gw, gh = 560, 230, 300, 300
    grid = "".join(f'<line x1="{gx0+12}" y1="{y}" x2="{gx0+gw-12}" y2="{y}" stroke="{G}" stroke-width="2"/>' for y in range(gy0 + 30, gy0 + gh - 8, 26)) + \
        "".join(f'<line x1="{x}" y1="{gy0+12}" x2="{x}" y2="{gy0+gh-12}" stroke="{G}" stroke-width="2"/>' for x in range(gx0 + 30, gx0 + gw - 8, 26))
    fx, fyc = gx0 + 92, gy0 + 100
    flange = (f'<circle cx="{fx}" cy="{fyc}" r="56" fill="none" stroke="{N}" stroke-width="4"/>'
              f'<circle cx="{fx}" cy="{fyc}" r="22" fill="none" stroke="{N}" stroke-width="4"/>'
              + "".join(f'<circle cx="{fx+40*math.cos(a):.1f}" cy="{fyc+40*math.sin(a):.1f}" r="6" fill="none" stroke="{N}" stroke-width="3"/>'
                        for a in [i * math.pi / 3 for i in range(6)])
              + f'<path d="M{fx-70} {fyc} L{fx+70} {fyc} M{fx} {fyc-70} L{fx} {fyc+70}" stroke="{N}" stroke-width="1.5" stroke-dasharray="10 4 2 4"/>')
    hx, hy = gx0 + 226, gy0 + 66
    bolt = (f'<path d="M{hx-26} {hy} L{hx-13} {hy-22} L{hx+13} {hy-22} L{hx+26} {hy} L{hx+13} {hy+22} L{hx-13} {hy+22} Z" fill="none" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>'
            f'<circle cx="{hx}" cy="{hy}" r="10" fill="none" stroke="{N}" stroke-width="3"/>'
            f'<rect x="{hx-12}" y="{hy+38}" width="24" height="76" fill="none" stroke="{N}" stroke-width="4"/>'
            f'<rect x="{hx-20}" y="{hy+26}" width="40" height="12" fill="none" stroke="{N}" stroke-width="3.5"/>'
            + "".join(f'<line x1="{hx-12}" y1="{y}" x2="{hx+12}" y2="{y-6}" stroke="{N}" stroke-width="2"/>' for y in range(hy + 72, hy + 114, 9)))
    py0 = gy0 + 220
    pipe = (f'<rect x="{gx0+40}" y="{py0}" width="160" height="40" fill="none" stroke="{N}" stroke-width="4"/>'
            f'<rect x="{gx0+28}" y="{py0-10}" width="14" height="60" rx="2" fill="none" stroke="{N}" stroke-width="3.5"/>'
            f'<rect x="{gx0+198}" y="{py0-10}" width="14" height="60" rx="2" fill="none" stroke="{N}" stroke-width="3.5"/>'
            f'<line x1="{gx0+46}" y1="{py0+20}" x2="{gx0+194}" y2="{py0+20}" stroke="{N}" stroke-width="1.5" stroke-dasharray="10 4 2 4"/>')
    drawing = (f'<rect x="{gx0+60}" y="{gy0+gh}" width="14" height="{fy-gy0-gh}" fill="{N}"/>'
               f'<rect x="{gx0+gw-74}" y="{gy0+gh}" width="14" height="{fy-gy0-gh}" fill="{N}"/>'
               f'<rect x="{gx0-8}" y="{gy0+gh-6}" width="{gw+16}" height="16" rx="5" fill="{N}"/>'
               f'<rect x="{gx0}" y="{gy0}" width="{gw}" height="{gh}" rx="6" fill="{W}" stroke="{N}" stroke-width="5"/>'
               + grid + flange + bolt + pipe)
    # 표 (보드)
    tx0, ty0, cols, rows, cw, ch = 952, 300, 4, 6, 58, 40
    tw, th = cols * cw, rows * ch
    hl = 3
    cells = []
    for r in range(rows):
        for c in range(cols):
            x, y = tx0 + c * cw, ty0 + r * ch
            cells.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" fill="{G if r == 0 else W}" stroke="{N}" stroke-width="2.5"/>')
            if 0 < r < 5:
                col = O if r == hl else G
                cells.append(f'<line x1="{x+12}" y1="{y+ch/2}" x2="{x+cw-12-(c % 2)*12}" y2="{y+ch/2}" stroke="{col}" stroke-width="6" stroke-linecap="round"/>')
    ry = ty0 + hl * ch
    cells.append(f'<rect x="{tx0}" y="{ry}" width="{tw}" height="{ch}" fill="{O}" fill-opacity=".14" stroke="{O}" stroke-width="5"/>')
    table = (f'<rect x="{tx0+tw/2-7}" y="{ty0+th+20}" width="14" height="{fy-ty0-th-20}" fill="{N}"/>'
             f'<rect x="{tx0+tw/2-44}" y="{fy-12}" width="88" height="12" rx="5" fill="{N}"/>'
             f'<rect x="{tx0-16}" y="{ty0-16}" width="{tw+32}" height="{th+36}" rx="10" fill="{W}" stroke="{N}" stroke-width="5"/>'
             + "".join(cells))
    # 로봇: 왼손 돋보기 → 도면, 오른손 펜 → 표
    bx, rs = 900, 1.05
    lens = (gx0 + 150, py0 + 18)
    lh = (lens[0] + 50, lens[1] + 56)
    pen = (tx0 + 30, ty0 + 4 * ch + 20)
    L = lambda p: ((p[0] - bx) / rs, (p[1] - fy) / rs)
    bot = robot(bx, fy, rs, rarm(-44, -86, *L(lh), -90, -110, hand=False) + rarm(44, -86, *L(pen), 60, -150, hand=False), mouth="smile")
    mag = (f'<line x1="{lens[0]+24}" y1="{lens[1]+24}" x2="{lh[0]}" y2="{lh[1]}" stroke="{N}" stroke-width="10" stroke-linecap="round"/>'
           f'<circle cx="{lens[0]}" cy="{lens[1]}" r="34" fill="{W}" fill-opacity=".45" stroke="{N}" stroke-width="7"/>'
           f'<path d="M{lens[0]-20} {lens[1]-14} A24 24 0 0 1 {lens[0]-5} {lens[1]-24}" stroke="{W}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    penl = f'<line x1="{pen[0]}" y1="{pen[1]}" x2="{pen[0]+10}" y2="{pen[1]-30}" stroke="{N}" stroke-width="6" stroke-linecap="round"/>'
    arrow = _arrow(gx0 + gw - 30, gy0 - 20, tx0 + 30, ty0 - 34, (gx0 + gw + tx0) / 2, gy0 - 100)
    # 회사원: 계산기 들고 주황 줄 확인
    s = .78
    px, wy = 1216, fy - 152 * s
    calc_c = (1236, 498)
    hold = (calc_c[0] - 4, calc_c[1] + 30)
    point = (tx0 + tw + 4, ry + ch / 2)
    Lp = lambda p: ((p[0] - px) / s, (p[1] - wy) / s)
    man = person(px, wy, s, legs=True)
    arm_r = f'<g transform="translate({px},{wy}) scale({s})">' + parm(54, -140, *Lp(hold), 90, -40, hand=False) + "</g>"
    arm_l = f'<g transform="translate({px},{wy}) scale({s})">' + parm(-54, -140, *Lp(point), -100, -120, hand=False) + "</g>"
    calc = (f'<g transform="rotate(8 {calc_c[0]} {calc_c[1]})">'
            f'<rect x="{calc_c[0]-26}" y="{calc_c[1]-38}" width="52" height="76" rx="6" fill="{N}"/>'
            f'<rect x="{calc_c[0]-18}" y="{calc_c[1]-30}" width="36" height="14" rx="2" fill="{W}"/>'
            + "".join(f'<circle cx="{calc_c[0]-12+i*12}" cy="{calc_c[1]-2+j*12}" r="3.6" fill="{G}"/>' for i in range(3) for j in range(3))
            + "</g>")
    return f'''
{floor(900, 670, 370)}
{drawing}{table}{arrow}
{bot}{mag}{penl}{_hand(*lh)}{_hand(*pen)}
{man}{arm_r}{calc}{_phand(*hold, s)}{arm_l}{_phand(*point, s)}'''


# ── ④ 회귀 테스트 게이트 ───────────────────────────────────
def _crate(x, y, w=66, h=58, fill=G, rot=0):
    """상자. (x, y) = 왼쪽 위."""
    return (f'<g transform="rotate({rot} {x+w/2} {y+h/2})">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{fill}" stroke="{N}" stroke-width="3.5"/>'
            f'<line x1="{x+w*.5-8}" y1="{y}" x2="{x+w*.5-8}" y2="{y+h*.35}" stroke="{N}" stroke-width="3"/>'
            f'<line x1="{x+w*.5+8}" y1="{y}" x2="{x+w*.5+8}" y2="{y+h*.35}" stroke="{N}" stroke-width="3"/>'
            "</g>")


def regression_gate():
    fy = 668
    bt = 540  # 벨트 윗면
    bx0, bx1 = 30, 1110
    rollers = "".join(f'<circle cx="{x}" cy="{bt+14}" r="7" fill="{W}" stroke="{N}" stroke-width="2.5"/>' for x in range(bx0 + 18, bx1 - 8, 38))
    belt = ("".join(f'<rect x="{x}" y="{bt+28}" width="12" height="{fy-bt-28}" fill="{N}"/>' for x in (bx0 + 30, 400, 760, bx1 - 50))
            + f'<rect x="{bx0}" y="{bt}" width="{bx1-bx0}" height="28" rx="14" fill="{G}" stroke="{N}" stroke-width="4"/>' + rollers)
    # 게이트
    gx0, gx1, gtop = 470, 640, 330
    gate_back = (f'<path d="M{gx0} {fy} L{gx0} {gtop+60} Q{gx0} {gtop} {(gx0+gx1)/2} {gtop} Q{gx1} {gtop} {gx1} {gtop+60} L{gx1} {fy} '
                 f'L{gx1-28} {fy} L{gx1-28} {gtop+64} Q{gx1-28} {gtop+28} {(gx0+gx1)/2} {gtop+28} Q{gx0+28} {gtop+28} {gx0+28} {gtop+64} L{gx0+28} {fy} Z" '
                 f'fill="{G}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>')
    lx = (gx0 + gx1) / 2
    lights = (f'<rect x="{lx-4}" y="{gtop-24}" width="8" height="26" fill="{N}"/>'
              f'<rect x="{lx-66}" y="{gtop-74}" width="132" height="54" rx="27" fill="{N}"/>'
              f'<circle cx="{lx-38}" cy="{gtop-47}" r="15" fill="{O}" stroke="{W}" stroke-width="3"/>'
              f'<circle cx="{lx}" cy="{gtop-47}" r="15" fill="{G}" fill-opacity=".45"/>'
              f'<circle cx="{lx+38}" cy="{gtop-47}" r="15" fill="{G}" fill-opacity=".45"/>')
    scan = f'<path d="M{gx0+34} {gtop+70} L{gx1-34} {gtop+70}" stroke="{N}" stroke-opacity=".35" stroke-width="4" stroke-dasharray="6 8"/>'
    # 상자들
    boxes_in = _crate(70, bt - 58) + _crate(180, bt - 58, fill=W) + _crate(290, bt - 58)
    boxes_out = _crate(660, bt - 58, fill=W) + _crate(940, bt - 58) + _crate(1036, bt - 58, fill=W)
    # 옆 레일 (게이트 앞에서 아래로 빠짐)
    rail = (f'<path d="M376 {bt+30} L300 {fy-6}" stroke="{N}" stroke-width="8" stroke-linecap="round"/>'
            f'<path d="M446 {bt+30} L370 {fy-6}" stroke="{N}" stroke-width="8" stroke-linecap="round"/>'
            f'<path d="M376 {bt+30} L446 {bt+30} L370 {fy-6} L300 {fy-6} Z" fill="{G}"/>'
            + "".join(f'<line x1="{376-76*t+4:.0f}" y1="{bt+30+(fy-6-bt-30)*t:.0f}" x2="{446-76*t-4:.0f}" y2="{bt+30+(fy-6-bt-30)*t:.0f}" stroke="{N}" stroke-width="3"/>' for t in (.2, .45, .7, .95)))
    stop = _crate(330, bt + 8, 70, 62, O, 22)
    divert = _arrow(400, bt - 40, 316, bt + 6, 350, bt - 50)
    # 로봇: 게이트 오른쪽에서 클립보드로 점수 확인
    bx, rs, rfy = 790, 1.0, 704
    cbx, cby, cw, chh = 856, 544, 76, 96
    hold = (cbx + 4, cby + 74)
    bars = "".join(f'<rect x="{cbx+16}" y="{cby+26+i*24}" width="{w}" height="14" rx="3" fill="{c}" stroke="{N}" stroke-width="2.5"/>'
                   for i, (w, c) in enumerate(((40, N), (34, N), (44, N))))
    clip = (f'<g transform="rotate(-8 {cbx+cw/2} {cby+chh/2})">'
            f'<rect x="{cbx}" y="{cby}" width="{cw}" height="{chh}" rx="7" fill="{N}"/>'
            f'<rect x="{cbx+8}" y="{cby+12}" width="{cw-16}" height="{chh-20}" rx="2" fill="{W}"/>'
            f'<rect x="{cbx+cw/2-18}" y="{cby-6}" width="36" height="16" rx="4" fill="{G}" stroke="{N}" stroke-width="2.5"/>'
            + bars + "</g>")
    L = lambda p: ((p[0] - bx) / rs, (p[1] - rfy) / rs)
    bot = floor(bx + 40, rfy + 2, 120) + robot(bx, rfy, rs, "", mouth="smile")
    arm2 = (f'<g transform="translate({bx},{rfy}) scale({rs})">' + rarm(-44, -86, -66, -40)
            + rarm(44, -86, *L(hold), 70, -50, hand=False) + "</g>")
    # 회사원: 오른쪽 끝에서 통과한 상자를 받는다
    s = .78
    px, wy = 1200, fy - 152 * s
    got = (1100, 444)
    Lp = lambda p: ((p[0] - px) / s, (p[1] - wy) / s)
    lhp, rhp = (got[0] - 2, got[1] + 40), (got[0] + 68, got[1] + 40)
    man = person(px, wy, s, extra_back=parm(54, -140, *Lp(rhp), 90, -60, hand=False), legs=True)
    arm_l = f'<g transform="translate({px},{wy}) scale({s})">' + parm(-54, -140, *Lp(lhp), -100, -60, hand=False) + "</g>"
    held = _crate(got[0], got[1], 66, 58, W)
    pass_arrow = _arrow(860, bt - 100, 1000, bt - 100)
    return f'''
{floor(640, 670, 610)}
{gate_back}{lights}{scan}
{rail}{belt}
{boxes_in}{boxes_out}{divert}{stop}
{bot}{clip}{arm2}{_hand(*hold)}
{man}{held}{arm_l}{_phand(*lhp, s)}{_phand(*rhp, s)}'''
