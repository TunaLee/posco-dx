"""Ch2 MCP 설명 그림 — 규격 없는 연결 · 등록 · 호출 순서 · 도구와 API 연결."""
K, O, G, M = "#1F3A5F", "#F28C28", "#C9CFD8", "#6B7785"


def tangle():
    """AI 앱 3개 × 사내 시스템 3개 — 규격 없이 각자 연결 vs MCP로 한 번씩."""
    apps = ["Claude Code", "ChatGPT", "사내 챗봇"]
    systems = ["시험실 LIMS", "MES", "ERP"]

    def side(x0, hub):
        s = []
        ys = [70, 170, 270]
        for i, a in enumerate(apps):
            s.append(f'<rect x="{x0}" y="{ys[i]-24}" width="150" height="48" rx="10" fill="#fff" stroke="{K}" stroke-width="2"/>'
                     f'<text x="{x0+75}" y="{ys[i]+6}" text-anchor="middle" class="mf-t">{a}</text>')
        for j, b in enumerate(systems):
            s.append(f'<rect x="{x0+330}" y="{ys[j]-24}" width="150" height="48" rx="10" fill="#fff" stroke="{K}" stroke-width="2"/>'
                     f'<text x="{x0+405}" y="{ys[j]+6}" text-anchor="middle" class="mf-t">{b}</text>')
        if not hub:
            k = 0
            for i in range(3):
                for j in range(3):
                    s.append(f'<line x1="{x0+150}" y1="{ys[i]}" x2="{x0+330}" y2="{ys[j]}" stroke="#D9534F" stroke-width="2" '
                             f'class="mf-ln" style="--d:{k * .08:.2f}s"/>')
                    k += 1
            s.append(f'<text x="{x0+240}" y="335" text-anchor="middle" class="mf-c" fill="#D9534F">연결 코드 3 × 3 = 9개</text>')
        else:
            hx = x0 + 240
            s.append(f'<rect x="{hx-42}" y="140" width="84" height="60" rx="12" fill="{O}"/>'
                     f'<text x="{hx}" y="177" text-anchor="middle" class="mf-t" style="fill:#fff">MCP</text>')
            for i in range(3):
                s.append(f'<line x1="{x0+150}" y1="{ys[i]}" x2="{hx-42}" y2="170" stroke="{K}" stroke-width="2.4" class="mf-ln" style="--d:{i * .1:.2f}s"/>')
                s.append(f'<line x1="{hx+42}" y1="170" x2="{x0+330}" y2="{ys[i]}" stroke="{K}" stroke-width="2.4" class="mf-ln" style="--d:{.3 + i * .1:.2f}s"/>')
            s.append(f'<text x="{hx}" y="335" text-anchor="middle" class="mf-c" fill="{O}">MCP 서버 3개 · 어느 앱에서나</text>')
        return "".join(s)

    return (f'<svg viewBox="0 0 1180 350" class="mf">'
            f'<text x="295" y="20" text-anchor="middle" class="mf-h" fill="#D9534F">규격이 없으면</text>{side(50, False)}'
            f'<text x="885" y="20" text-anchor="middle" class="mf-h" fill="{O}">MCP로</text>{side(640, True)}</svg>')


def seq():
    """등록부터 답까지 — Claude Code(MCP 클라이언트)가 서버와 주고받는 순서. 줄마다 차례로 나타남."""
    X = {"L": 150, "A": 520, "S": 850, "P": 1070}
    s = [f'<defs><marker id="mfa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         f'<path d="M0 0 L10 5 L0 10 Z" fill="{K}"/></marker>'
         f'<marker id="mfo" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         f'<path d="M0 0 L10 5 L0 10 Z" fill="{O}"/></marker></defs>']
    heads = [("L", "Claude (모델)", "도구 고르기 · 답"), ("A", "Claude Code", "MCP 클라이언트"),
             ("S", "lims MCP 서버", "내가 만든 프로그램"), ("P", "시뮬레이터 API", ":8800")]
    for k, t, d in heads:
        x = X[k]; w = 200 if k == "P" else 250
        fill, tc = (K, "#fff") if k == "A" else ("#fff", K)
        s.append(f'<rect x="{x-w/2}" y="6" width="{w}" height="56" rx="12" fill="{fill}" stroke="{K}" stroke-width="2"/>'
                 f'<text x="{x}" y="31" text-anchor="middle" class="mf-t" style="fill:{tc}">{t}</text>'
                 f'<text x="{x}" y="51" text-anchor="middle" class="mf-s" style="fill:{"#C9CFD8" if k == "A" else M}">{d}</text>'
                 f'<line x1="{x}" y1="62" x2="{x}" y2="440" stroke="{G}" stroke-width="2" stroke-dasharray="6 6"/>')
    rows = [
        ("1", "A", "A", "claude mcp add 로 등록한 서버를 실행", False),
        ("2", "A", "S", "tools/list", False),
        ("", "S", "A", "도구 이름 · 설명 · 입력 형식", False),
        ("3", "A", "L", "질문 + 도구 목록", False),
        ("", "L", "A", "recent_results(limit=50)", True),
        ("4", "A", "S", "tools/call", True),
        ("", "S", "P", "GET /api/results", True),
        ("", "P", "S", "JSON", True),
        ("5", "S", "A", "도구 결과", True),
        ("", "A", "L", "결과를 읽고 답", True),
    ]
    y = 98
    for i, (no, a, b, txt, hot) in enumerate(rows):
        c, mk = (O, "mfo") if hot else (K, "mfa")
        g = [f'<g class="mf-row" style="--d:{i * .45:.2f}s">']
        if no:
            g.append(f'<circle cx="30" cy="{y-4}" r="14" fill="{O}"/><text x="30" y="{y+1}" text-anchor="middle" class="mf-n">{no}</text>')
        if a == b:
            x = X[a]
            g.append(f'<rect x="{x-230}" y="{y-20}" width="460" height="32" rx="8" fill="#F4F6F9" stroke="{G}"/>'
                     f'<text x="{x}" y="{y+2}" text-anchor="middle" class="mf-s" fill="{K}">{txt}</text>')
        else:
            x1, x2 = X[a], X[b]; d = 1 if x2 > x1 else -1
            g.append(f'<line x1="{x1 + d*6}" y1="{y}" x2="{x2 - d*8}" y2="{y}" stroke="{c}" stroke-width="2.6" marker-end="url(#{mk})"/>'
                     f'<text x="{(x1+x2)/2}" y="{y-8}" text-anchor="middle" class="mf-l" fill="{c}">{txt}</text>')
        g.append("</g>")
        s.append("".join(g))
        y += 35
    return f'<svg viewBox="0 0 1180 450" class="mf">{"".join(s)}</svg>'


def mapping():
    """Claude가 고르는 도구 → MCP 서버가 부르는 API."""
    return ('<div class="mfm">'
            '<div class="mfm-c"><div class="mfm-h">Claude가 고르는 도구</div><code>recent_results(</code>'
            '<div class="mfm-k">limit <small>정수 · 최근 몇 건</small></div>'
            '<div class="mfm-k">grade <small>문자열 · 강종 필터 · 선택</small></div><code>)</code></div>'
            '<div class="mfm-m"><span>MCP 서버 코드</span><b>도구 이름 · 인자 → 주소</b><span>결과 JSON → 도구 결과</span></div>'
            '<div class="mfm-c on"><div class="mfm-h">시뮬레이터 API</div><code>GET 127.0.0.1:8800/api/results</code>'
            '<div class="mfm-k">?limit= <small>건수</small></div>'
            '<div class="mfm-k">&amp;grade= <small>강종</small></div><code>→ JSON</code></div>'
            '</div>')


CSS = """
  /* MCP 그림 */
  .mf{width:100%; height:auto; display:block; margin:4px 0 10px;}
  .mf-t{font-size:17px; font-weight:800; fill:#16233A;} .mf-s{font-size:14px; font-weight:600;}
  .mf-h{font-size:18px; font-weight:900;} .mf-c{font-size:16px; font-weight:800;}
  .mf-l{font-size:14.5px; font-weight:800; font-family:var(--mono, monospace);} .mf-n{font-size:14px; font-weight:900; fill:#fff;}
  .mf-ln{stroke-dasharray:500; animation:mfDraw .8s ease-out both; animation-delay:var(--d);}
  @keyframes mfDraw{from{stroke-dashoffset:500}}
  .mf-row{animation:mfIn .4s ease-out both; animation-delay:var(--d);}
  @keyframes mfIn{from{opacity:0; transform:translateY(6px)}}
  @media print{.mf-ln,.mf-row{animation:none}}
  .mfm{display:grid; grid-template-columns:1fr 260px 1fr; gap:18px; align-items:center; margin:10px 0 18px;}
  .mfm-c{border:2px solid #1F3A5F; border-radius:14px; padding:18px 22px; background:#fff;} .mfm-c.on{border-color:#F28C28; background:#FFF8F1;}
  .mfm-h{font-size:15px; font-weight:900; color:#6B7785; margin-bottom:8px;}
  .mfm-c code{display:block; font-size:19px; font-weight:800; color:#16233A; background:none; padding:0;}
  .mfm-k{font-size:19px; font-weight:700; color:#1F3A5F; padding:4px 0 4px 18px; font-family:var(--mono, monospace);} .mfm-k small{font-family:inherit; font-size:13px; color:#8A94A3; margin-left:8px;}
  .mfm-m{display:flex; flex-direction:column; align-items:center; gap:8px; text-align:center; font-size:14px; color:#6B7785;}
  .mfm-m b{font-size:16px; color:#fff; background:#1F3A5F; border-radius:999px; padding:8px 16px;}
"""
