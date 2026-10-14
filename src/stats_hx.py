"""통계 시각화 부품 — 큰 숫자 카드 · 가로 막대 · 고리 · 출처 줄.

모두 HTML/CSS (+ 작은 SVG). 화면에서는 자라나는 애니메이션, 인쇄(PDF)에서는 완성된 모습.
"""
from deck import light


def src(*items):
    """출처 줄. items: (이름, url) — 슬라이드 왼쪽 아래."""
    links = " · ".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in items)
    return f'<div class="src">출처 · {links}</div>'


def big(items, cols=None):
    """큰 숫자 카드. items: (값, 단위, 설명[, 강조]) — 강조면 주황."""
    cards = []
    for i, it in enumerate(items):
        v, unit, label = it[:3]
        hl = len(it) > 3 and it[3]
        cards.append(f'<div class="bn{" hl" if hl else ""}" style="--d:{i * .12:.2f}s">'
                     f'<div class="bv">{v}<small>{unit}</small></div><div class="bl">{label}</div></div>')
    return f'<div class="bns c{cols or len(items)}">{"".join(cards)}</div>'


def hbars(rows, unit="", top=None, title=""):
    """가로 막대. rows: (이름, 값[, 강조, 표시 문자열])."""
    mx = top or max(r[1] for r in rows) or 1
    out = []
    for i, r in enumerate(rows):
        name, v = r[0], r[1]
        hl = len(r) > 2 and r[2]
        shown = r[3] if len(r) > 3 else f"{v:g}{unit}"
        out.append(f'<div class="hb{" hl" if hl else ""}" style="--d:{i * .1:.2f}s">'
                   f'<span class="hn">{name}</span><span class="ht"><span class="hf" style="width:{100 * v / mx:.1f}%"></span></span>'
                   f'<span class="hv">{shown}</span></div>')
    t = f'<div class="hbt">{title}</div>' if title else ""
    return f'<div class="hbars">{t}{"".join(out)}</div>'


def ring(pct, label, hl=True, size=170):
    """고리 그래프 하나. pct: 0~100."""
    r = 62
    c = 2 * 3.14159 * r
    off = c * (1 - pct / 100)
    col = "#F28C28" if hl else "#1F3A5F"
    return (f'<div class="ring" style="width:{size}px"><svg viewBox="0 0 160 160">'
            f'<circle cx="80" cy="80" r="{r}" fill="none" stroke="#EEF1F5" stroke-width="16"/>'
            f'<circle class="rg" cx="80" cy="80" r="{r}" fill="none" stroke="{col}" stroke-width="16" stroke-linecap="round" '
            f'stroke-dasharray="{c:.1f}" stroke-dashoffset="{off:.1f}" style="--c:{c:.1f}" transform="rotate(-90 80 80)"/>'
            f'<text x="80" y="88" text-anchor="middle" class="rv">{pct:g}%</text></svg><div class="rl">{label}</div></div>')


def rings(items):
    return '<div class="rings">' + "".join(ring(*it) for it in items) + "</div>"


def passk(p=0.75, kmax=10):
    """pass@k(한 번이라도 성공) vs pass^k(매번 성공) — 1회 성공률 p에서 계산한 곡선."""
    W, H, X0, Y0 = 1120, 330, 90, 290
    X = lambda k: X0 + (W - X0 - 40) * (k - 1) / (kmax - 1)
    Y = lambda v: Y0 - v * 250
    at = [1 - (1 - p) ** k for k in range(1, kmax + 1)]
    al = [p ** k for k in range(1, kmax + 1)]
    path = lambda vs: "M" + " L".join(f"{X(k):.0f} {Y(v):.0f}" for k, v in zip(range(1, kmax + 1), vs))
    g = "".join(f'<line x1="{X0}" x2="{W - 40}" y1="{Y(v):.0f}" y2="{Y(v):.0f}" stroke="#EEF1F5" stroke-width="2"/>'
                f'<text x="{X0 - 12}" y="{Y(v) + 5:.0f}" text-anchor="end" font-size="15" fill="#8A94A3">{int(v * 100)}%</text>'
                for v in (0, .25, .5, .75, 1))
    g += "".join(f'<text x="{X(k):.0f}" y="{Y0 + 26}" text-anchor="middle" font-size="15" fill="#8A94A3">{k}</text>' for k in range(1, kmax + 1))
    g += f'<path d="{path(at)}" fill="none" stroke="#1F3A5F" stroke-width="6" stroke-linecap="round" class="pk"/>'
    g += f'<path d="{path(al)}" fill="none" stroke="#F28C28" stroke-width="6" stroke-linecap="round" class="pk"/>'
    g += f'<circle cx="{X(3):.0f}" cy="{Y(al[2]):.0f}" r="9" fill="#F28C28"/><text x="{X(3) + 16:.0f}" y="{Y(al[2]) - 12:.0f}" font-size="19" font-weight="800" fill="#E07A12">3번 모두 성공 {al[2] * 100:.0f}%</text>'
    g += f'<text x="{X(kmax):.0f}" y="{Y(at[-1]) - 14:.0f}" text-anchor="end" font-size="18" font-weight="800" fill="#1F3A5F">한 번이라도 성공 (pass@k)</text>'
    g += f'<text x="{X(kmax):.0f}" y="{Y(al[-1]) - 14:.0f}" text-anchor="end" font-size="18" font-weight="800" fill="#E07A12">매번 성공 (pass^k)</text>'
    g += f'<text x="{(X0 + W - 40) / 2:.0f}" y="{Y0 + 50}" text-anchor="middle" font-size="15" fill="#8A94A3">시도 횟수 k · 1회 성공률 {int(p * 100)}%</text>'
    return f'<svg class="pkc" viewBox="0 0 {W} {H + 50}">{g}</svg>'


def quote(text, who):
    return f'<div class="qt"><p>{text}</p><span>{who}</span></div>'


def stat(title, ch, body, *sources):
    return light(title, body + (src(*sources) if sources else ""), ch)


CSS = r"""
  .slide .src{position:absolute; right:60px; top:62px; font-size:12px; color:#8A94A3; max-width:640px; text-align:right; line-height:1.5; z-index:3;}
  .slide .src a{color:#6B7785; text-decoration:none; border-bottom:1px dotted #B5BDC8;}
  .slide.dk .src, .slide.dk .src a{color:#AEB8C6;}

  .bns{display:grid; gap:18px; margin:6px 0 18px;}
  .bns.c1{grid-template-columns:1fr} .bns.c2{grid-template-columns:repeat(2,1fr)} .bns.c3{grid-template-columns:repeat(3,1fr)} .bns.c4{grid-template-columns:repeat(4,1fr)}
  .bn{background:#fff; border:1px solid #E1E5EB; border-top:5px solid #1F3A5F; border-radius:14px; padding:22px 24px 20px;
      animation:bnIn .7s cubic-bezier(.2,.8,.2,1) both; animation-delay:var(--d);}
  .bn.hl{border-top-color:#F28C28; background:#FFF8F1;}
  .bn .bv{font-size:56px; line-height:1; font-weight:800; color:#1F3A5F; letter-spacing:-1px; font-variant-numeric:tabular-nums;}
  .bn.hl .bv{color:#E07A12;}
  .bn .bv small{font-size:24px; font-weight:700; margin-left:4px; letter-spacing:0;}
  .bn .bl{margin-top:12px; font-size:18px; color:#3B4756; line-height:1.4; font-weight:600;}
  @keyframes bnIn{from{opacity:0; transform:translateY(18px)} to{opacity:1; transform:none}}

  .hbars{display:grid; gap:12px; margin:4px 0 16px;}
  .hbt{font-size:15px; color:#6B7785; font-weight:700; margin-bottom:2px;}
  .hb{display:grid; grid-template-columns:280px 1fr 200px; align-items:center; gap:14px; font-size:18px;}
  .hb .hn{font-weight:700; color:#1F3A5F; text-align:right;}
  .hb .ht{height:30px; background:#EEF1F5; border-radius:8px; overflow:hidden;}
  .hb .hf{display:block; height:100%; background:#9AA5B1; border-radius:8px; transform-origin:left;
          animation:hbGrow 1s cubic-bezier(.2,.8,.2,1) both; animation-delay:var(--d);}
  .hb.hl .hf{background:#F28C28;} .hb.hl .hv{color:#E07A12;}
  .hb .hv{font-weight:800; color:#1F3A5F; font-size:20px; font-variant-numeric:tabular-nums;}
  @keyframes hbGrow{from{transform:scaleX(0)} to{transform:scaleX(1)}}

  .rings{display:flex; gap:44px; justify-content:center; margin:6px 0 16px;}
  .ring{text-align:center;}
  .ring svg{width:100%; height:auto;}
  .ring .rg{animation:rgFill 1.4s cubic-bezier(.2,.8,.2,1) both;}
  .ring .rv{font-size:30px; font-weight:800; fill:#1F3A5F;}
  .ring .rl{font-size:16px; color:#3B4756; font-weight:600; margin-top:6px; line-height:1.35;}
  @keyframes rgFill{from{stroke-dashoffset:var(--c)}}

  .qt{border-left:5px solid #F28C28; background:#FFF8F1; padding:16px 22px; border-radius:0 12px 12px 0; margin:6px 0 16px;}
  .qt p{margin:0; font-size:21px; color:#1F3A5F; font-weight:700; line-height:1.45;}
  .qt span{display:block; margin-top:8px; font-size:14px; color:#6B7785;}

  .pkc{width:100%; height:auto; margin-bottom:6px;}
  .pkc .pk{stroke-dasharray:1400; animation:pkd 1.6s ease-out both;}
  @keyframes pkd{from{stroke-dashoffset:1400}}
  @media print{.bn,.hb .hf,.ring .rg,.pkc .pk{animation:none!important}}
"""
