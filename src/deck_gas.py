"""짧은 강의: Skill 정제 + Apps Script 웹앱 대시보드.

출력: docs/gas-dashboard/index.html  (python3 src/build.py gas)
기존 덱의 부품 · 장면을 그대로 쓴다.
"""
from pathlib import Path

import deck
import explain
from deck import ba, bridge, capture, cards, divider, flow, ill, lab, light
from intro import ICON, coord, icon

N, G, O, W = "#1F3A5F", "#D9DDE3", "#F28C28", "#FFFFFF"
deck.CAPDIR = Path(__file__).resolve().parent.parent / "docs" / "assets" / "capture"
code = explain.prompt


# ── 도식 ────────────────────────────────────────────────
def box(x, y, w, h, title, sub="", fill=W, stroke=N, tcolor=N, rx=14):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
    s += f'<text x="{x+w/2}" y="{y+(h/2 if not sub else h/2-8)}" text-anchor="middle" dominant-baseline="middle" class="bt" fill="{tcolor}">{title}</text>'
    if sub:
        s += f'<text x="{x+w/2}" y="{y+h/2+16}" text-anchor="middle" dominant-baseline="middle" class="bs">{sub}</text>'
    return s


_P = ["a"]  # 그림마다 화살표 머리 id 를 다르게 쓴다 (숨은 장의 id 를 참조하면 안 보인다)


def arrow(x1, y1, x2, y2, color=N, dash="", w=3, mid="ah"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}"{d} marker-end="url(#{_P[0]}{mid})"/>'


def markers(prefix):
    _P[0] = prefix
    return _MARKERS.replace('id="ah"', f'id="{prefix}ah"').replace('id="aho"', f'id="{prefix}aho"')


_MARKERS = (f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
           f'<path d="M0 0 L10 5 L0 10 Z" fill="{N}"/></marker>'
           f'<marker id="aho" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
           f'<path d="M0 0 L10 5 L0 10 Z" fill="{O}"/></marker></defs>')


def browser(x, y, w, h, inner):
    """브라우저 창: 위 막대 + 안쪽 내용."""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{W}" stroke="{N}" stroke-width="3"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="12" fill="{G}"/><rect x="{x}" y="{y+14}" width="{w}" height="12" fill="{G}"/>'
            + "".join(f'<circle cx="{x+16+i*14}" cy="{y+13}" r="4" fill="{N}"/>' for i in range(3))
            + inner)


def bars(x, y, hs, color=N, bw=22, gap=12):
    base = y
    return "".join(f'<rect x="{x+i*(bw+gap)}" y="{base-h}" width="{bw}" height="{h}" rx="3" fill="{color}"/>' for i, h in enumerate(hs))


def db(x, y, w=120, h=130, label="시트"):
    """데이터베이스 원통."""
    ry = 16
    return (f'<path d="M{x} {y+ry} L{x} {y+h-ry} A{w/2} {ry} 0 0 0 {x+w} {y+h-ry} L{x+w} {y+ry}" fill="{G}" stroke="{N}" stroke-width="3"/>'
            f'<ellipse cx="{x+w/2}" cy="{y+ry}" rx="{w/2}" ry="{ry}" fill="{W}" stroke="{N}" stroke-width="3"/>'
            f'<path d="M{x} {y+h*0.45} A{w/2} {ry} 0 0 0 {x+w} {y+h*0.45}" fill="none" stroke="{N}" stroke-width="2"/>'
            f'<path d="M{x} {y+h*0.7} A{w/2} {ry} 0 0 0 {x+w} {y+h*0.7}" fill="none" stroke="{N}" stroke-width="2"/>'
            f'<text x="{x+w/2}" y="{y+h+30}" text-anchor="middle" class="bt" fill="{N}">{label}</text>')


def static_web():
    mk = markers("st")
    page = browser(760, 70, 330, 250, bars(800, 290, [90, 140, 70, 170, 120], G))
    file_ = (f'<path d="M140 90 L250 90 L290 130 L290 300 L140 300 Z" fill="{W}" stroke="{N}" stroke-width="3"/>'
             f'<path d="M250 90 L250 130 L290 130" fill="none" stroke="{N}" stroke-width="3"/>'
             + "".join(f'<rect x="160" y="{150+i*26}" width="{100 - (i%2)*30}" height="9" rx="4" fill="{G}"/>' for i in range(5))
             + f'<text x="215" y="340" text-anchor="middle" class="bt" fill="{N}">완성된 HTML 파일</text>'
             + f'<text x="215" y="366" text-anchor="middle" class="bs">숫자가 파일 안에 고정</text>')
    flowline = (arrow(310, 195, 740, 195, N, w=4)
                + f'<text x="525" y="178" text-anchor="middle" class="bs">그대로 전달</text>')
    return f'''<svg viewBox="0 0 1180 400" class="websvg">{mk}{file_}{flowline}{page}
<text x="925" y="352" text-anchor="middle" class="bt" fill="{N}">브라우저</text>
<text x="925" y="378" text-anchor="middle" class="bs">숫자를 바꾸려면 파일을 다시 만들어 올림</text></svg>'''


def dynamic_web():
    # 브라우저(왼쪽) · Apps Script 서버(가운데) · 시트(오른쪽). 위 줄은 요청, 아래 줄은 데이터가 흐른다.
    mk = markers("dy")
    page = browser(40, 80, 300, 230, bars(80, 280, [80, 120, 150, 100, 170], O))
    server = box(470, 120, 220, 150, "Apps Script", "틀(HTML) + 데이터", fill="#EEF1F5")
    sheet = db(880, 110)
    req = (arrow(345, 130, 465, 130, N, "7 6") + f'<text x="405" y="112" text-anchor="middle" class="bs">① 요청</text>'
           + arrow(695, 150, 875, 150, N, "7 6") + f'<text x="785" y="132" text-anchor="middle" class="bs">② 조회</text>')
    res = (arrow(875, 250, 695, 250, O, w=4, mid="aho") + f'<text x="785" y="282" text-anchor="middle" class="bso">③ 최신 데이터</text>'
           + arrow(465, 270, 345, 270, O, w=4, mid="aho") + f'<text x="405" y="302" text-anchor="middle" class="bso">④ 화면 그리기</text>')
    # 흐르는 데이터 점
    dots = "".join(
        f'<circle r="8" fill="{O}"><animateMotion dur="2.4s" begin="{d}s" repeatCount="indefinite" path="M875 250 L695 250 L580 260 L465 270 L345 270"/></circle>'
        for d in (0, .8, 1.6))
    return f'''<svg viewBox="0 0 1180 400" class="websvg">{mk}{page}{server}{sheet}{req}{res}{dots}
<text x="190" y="350" text-anchor="middle" class="bt" fill="{N}">브라우저</text>
<text x="190" y="376" text-anchor="middle" class="bs">열 때마다 지금 숫자</text></svg>'''


def pipeline():
    """전체 구조 — 입력 A · B → 시트 마스터 → 웹앱 대시보드."""
    s = markers("pl")
    s += box(40, 30, 300, 92, "입력 A · 대량 엑셀 원본", "오탈자 · 중복 · 공백")
    s += box(840, 30, 300, 92, "입력 B · 웹 화면 건별 입력", "드롭다운 · 자동완성")
    s += box(40, 170, 300, 92, "정제 Skill", "교정 · 중복 제거 · 검증", fill="#FFF3E6", stroke=O)
    s += box(840, 170, 300, 92, "GAS  addSalesRecord", "검증 · 금액 계산 · 저장", fill="#EEF1F5")
    s += db(530, 250, 120, 110, "")
    s += f'<text x="590" y="395" text-anchor="middle" class="bt" fill="{N}">시트 마스터 · 클린 데이터</text>'
    s += box(440, 440, 300, 80, "GAS 웹앱 대시보드", "KPI · 차트 · 새로고침", fill=N, stroke=N, tcolor=W)
    s += arrow(190, 124, 190, 166) + arrow(990, 124, 990, 166)
    s += arrow(340, 216, 525, 290) + arrow(840, 216, 655, 290)
    s += arrow(590, 405, 590, 436, O, w=4, mid="aho")
    s = s.replace('class="bs">KPI', 'class="bsw">KPI')
    return f'<svg viewBox="0 0 1180 530" class="websvg pipe2">{s}</svg>'


def lock(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<path d="M-12 0 V-10 A12 12 0 0 1 12 -10 V0" fill="none" stroke="{O}" stroke-width="5"/>'
            f'<rect x="-18" y="0" width="36" height="28" rx="6" fill="{O}"/><circle cx="0" cy="12" r="4" fill="{W}"/></g>')


def proxy():
    """원본 시트는 잠가 두고, 웹앱(실행: 나)이 대신 접근한다."""
    s = markers("px")
    # 보안 영역
    s += f'<rect x="30" y="20" width="560" height="420" rx="22" fill="#F6F8FA" stroke="{N}" stroke-width="2.5" stroke-dasharray="9 7"/>'
    s += f'<text x="58" y="56" class="bt" fill="{N}">Drive 보안 영역</text>'
    s += db(110, 120, 130, 140, "")
    s += lock(175, 104, 1.1)
    s += f'<text x="175" y="300" text-anchor="middle" class="bt" fill="{N}">원본 시트</text>'
    s += f'<text x="175" y="326" text-anchor="middle" class="bs">공유: 제한됨 · 나만</text>'
    s += box(360, 150, 190, 120, "Apps Script", "실행: 나 (소유자)", fill="#EEF1F5")
    s += arrow(355, 190, 245, 190) + arrow(245, 230, 355, 230)
    s += f'<text x="300" y="176" text-anchor="middle" class="bs">읽기</text><text x="300" y="256" text-anchor="middle" class="bs">쓰기</text>'
    s += f'<text x="455" y="300" text-anchor="middle" class="bs">소유자 권한을 대신 사용</text>'
    # 팀원
    s += arrow(555, 210, 740, 210, O, w=4, mid="aho") + f'<text x="648" y="192" text-anchor="middle" class="bso">웹앱 URL</text>'
    for i, y in enumerate((60, 190, 320)):
        s += browser(760, y, 220, 110, bars(790, y + 95, [30, 50, 40, 60], O if i == 1 else G, bw=16, gap=10))
    s += f'<text x="1080" y="190" class="bt" fill="{N}">팀원</text>'
    s += f'<text x="1080" y="218" class="bs">시트 링크 모름</text><text x="1080" y="242" class="bs">시트 권한 없음</text><text x="1080" y="266" class="bs">보기 · 입력 가능</text>'
    return f'<svg viewBox="0 0 1240 460" class="websvg">{s}</svg>'


def save_flow():
    return flow([("등록 버튼", "웹 화면"), ("google.script.run", "브라우저 → 서버"),
                 ("addSalesRecord", "검증 · 금액 계산"), ("appendRow", "시트에 한 행 추가")], hl=3)


# ── 도구 ↔ 직무 지도 (본 강의 생태계 지도와 같은 방식) ─────────────
TEAM = [
    ("drive", "Drive", "데이터 보관 담당", "파일 보관 · 공유 권한", (250, 255)),
    ("sheets", "Sheets", "데이터 엔지니어 · 분석가", "정리 · 저장 · 집계", (640, 215)),
    ("gemini", "Skill", "데이터 품질 담당", "정제 · 판단", (1030, 255)),
    ("docs", "Canvas", "프론트엔드 · 백엔드 개발자", "화면 · 시제품", (1030, 590)),
    ("appsscript", "Apps Script", "Ops 엔지니어", "연결 · 배포 · 권한", (640, 650)),
    ("google", "웹앱 URL", "서비스 운영", "팀 공유 · 입력", (250, 590)),
]


def team_map(active=None, kick="도구 지도", title="구글 도구로 꾸리는 작은 개발팀", roles=None):
    hub = (640, 430)
    lines, cards_ = [], []
    for ic, tool, role, job, (x, y) in (roles or TEAM):
        st = "all" if active is None else ("on" if tool in active else "dim")
        line = {"all": f'stroke="{O}" stroke-width="2.5" stroke-dasharray="6 7" opacity=".7"',
                "dim": 'stroke="#fff" stroke-width="2" stroke-dasharray="4 8" opacity=".12"',
                "on": f'stroke="{O}" stroke-width="5" opacity=".35"'}[st]
        lines.append(f'<line x1="{hub[0]}" y1="{hub[1]}" x2="{x}" y2="{y}" {line}/>')
        if st != "dim":
            lines.append(f'<line class="flow" x1="{hub[0]}" y1="{hub[1]}" x2="{x}" y2="{y}" stroke="{O}" stroke-width="{5 if st == "on" else 3}" stroke-linecap="round" stroke-dasharray="14 12"/>')
        cards_.append(f'''<div class="node {st}" style="left:{x-170}px; top:{y-46}px">
  <div class="nh">{icon(ic)}<b>{tool}</b></div>
  <div class="tj"><span class="chip">{role}</span><span class="nm">{job}</span></div>
</div>''')
    return f'''<section class="slide dk eco{' focus' if active else ''}" data-title="{title}">
  {coord()}
  <div class="kick">{kick}</div>
  <h2>{title}</h2>
  <svg class="ecosvg" viewBox="0 0 1280 720">{"".join(lines)}</svg>
  {"".join(cards_)}
  <div class="hub" style="left:{hub[0]-74}px; top:{hub[1]-74}px"><img src="{ICON.format("gemini")}" alt="Gemini"/></div>
</section>'''


def team_table():
    rows = [("Drive", "원본 · 결과 파일 보관, 공유 범위 지정", "데이터 보관 담당"),
            ("Sheets", "정리된 데이터 저장, 수식 · 피벗 집계", "데이터 엔지니어 · 분석가"),
            ("Skill", "처음 보는 오류도 판단해 정제", "데이터 품질 담당"),
            ("Canvas", "대시보드 화면 · 동작 코드", "프론트엔드 · 백엔드 개발자"),
            ("Apps Script", "시트 ↔ 화면 연결, 배포, 권한", "Ops 엔지니어"),
            ("웹앱 URL", "팀원이 보고 입력하는 창구", "서비스 운영")]
    trs = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td><span class=\"rolechip\">{c}</span></td></tr>" for a, b, c in rows)
    return f'<table class="dbt"><thead><tr><th>도구</th><th>실제로 하는 일</th><th>회사라면</th></tr></thead><tbody>{trs}</tbody></table>'


def table(head, rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="dbt"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def note(label, text):
    return f'<div class="dbnote"><span>{label}</span> {text}</div>'


# ── 장 ──────────────────────────────────────────────────
def cover():
    strip = "".join(icon(n, "tile") for n in ["gemini", "sheets", "appsscript", "drive"])
    return f'''<section class="slide dk cover-dk active" data-title="표지">
  <div class="glow"></div>
  <div class="kick">실습 · 영업 데이터 파이프라인</div>
  <h1>Skill과 Apps Script로<br/>만드는 실적 대시보드</h1>
  <div class="strip">{strip}</div>
</section>'''


def slides():
    skill_md = ("---\n"
                "name: (내가 정한 이름)\n"
                "description: 판매 데이터 파일이 오면 마스터 구조로 정리\n"
                "---\n"
                "목표: 어떤 형식의 파일이든 마스터와 같은 구조로\n"
                "1. 열의 의미부터 파악 (이름 · 순서가 달라도)\n"
                "2. 거래처 · 제품은 참조 마스터에서 가장 가까운 값으로\n"
                "3. 같은 거래로 보이는 행은 하나로\n"
                "4. 수량 · 단가 · 금액이 안 맞으면 고치지 말고 표시\n"
                "5. 확신이 낮은 교정은 리포트에 따로\n"
                "참조: 거래처 마스터 · 05 제품카탈로그")
    gas_code = ("function doGet() {\n"
                "  return HtmlService.createHtmlOutputFromFile('Index');\n"
                "}\n"
                "function getCleanedSalesData() {   // 시트 → 화면\n"
                "  return SpreadsheetApp.getActive()\n"
                "    .getSheetByName('판매실적_마스터').getDataRange().getValues();\n"
                "}\n"
                "function addSalesRecord(r) {       // 화면 → 시트\n"
                "  // 검증 · 매출액 = 납품수량 × 단가\n"
                "  sheet.appendRow([...]);\n"
                "}")
    return [
        cover(),
        light("전체 구조", pipeline(), "개요"),
        team_map(),
        light("도구와 직무", team_table(), "개요"),
        light("원본은 잠그고, 웹앱이 대신 접근", proxy(), "개요"),
        light("단계별 역할", f'''<table class="dbt">
<thead><tr><th>단계</th><th>하는 일</th><th>도구</th></tr></thead><tbody>
<tr><td><b>정리</b></td><td>오탈자 · 중복 · 공백 정리</td><td>정제 Skill</td></tr>
<tr><td><b>입력</b></td><td>건별 거래를 바로 기록</td><td>웹 화면 + GAS addSalesRecord</td></tr>
<tr><td><b>저장</b></td><td>깨끗한 데이터 한 곳</td><td>시트 마스터</td></tr>
<tr><td><b>보여주기</b></td><td>지금 숫자를 화면에</td><td>GAS 웹앱 대시보드</td></tr>
</tbody></table>''', "개요"),

        divider("01", "정적 웹과 동적 웹", ""),
        team_map({"Canvas", "Apps Script"}, "도구 지도 · 01", "화면을 만드는 쪽"),
        ill("scenes_ch4", "photo_window", "top20", "사진과 창문", ["사진: 그때 숫자", "창문: 지금 숫자"]),
        light("정적 웹: 완성된 파일을 그대로", static_web(), "01"),
        light("동적 웹: 열 때마다 데이터를 가져와 그림", dynamic_web(), "01"),
        ill("scenes_ch4", "menu_board", "left40", "틀은 그대로, 데이터만 교체", ["화면 틀: Index.html", "데이터: 시트에서"]),

        divider("02", "Skill로 원본 정리", ""),
        team_map({"Drive", "Sheets", "Skill"}, "도구 지도 · 02", "데이터를 다루는 쪽"),
        light("모델과 하네스", '''<div class="hn">
  <div class="hn-out"><div class="hn-lab">하네스</div>
    <div class="hn-row"><span class="hl">지침 = Skill</span><span>참고 자료</span></div>
    <div class="hn-core">모델</div>
    <div class="hn-row"><span>도구 연결</span><span>사람 확인</span></div>
  </div>
</div>''', "02"),
        ill("scenes_ch5", "secretary", "left40", "Skill: 저장해 두는 업무 지침", ["/이름으로 호출", "필요할 때 꺼내 씀"]),
        light("원본의 흔한 오류", f'''<table class="dbt">
<thead><tr><th>오류</th><th>원본</th><th>정리 후</th></tr></thead><tbody>
<tr><td><b>띄어쓰기</b></td><td>B 편의점</td><td>B편의점</td></tr>
<tr><td><b>오탈자</b></td><td>B편의졈</td><td>B편의점</td></tr>
<tr><td><b>중복 행</b></td><td>같은 기준월 · 거래처 · SKU 2줄</td><td>1줄</td></tr>
<tr><td><b>계산 불일치</b></td><td>매출액 ≠ 납품수량 × 단가</td><td>표시 후 확인</td></tr>
</tbody></table>
<div class="dbnote"><span>01 원본</span> 4,381행 → 정리 후 4,368행</div>''', "02"),
        ill("scenes_ch5", "conveyor", "top20", "규칙이 아니라 판단으로 정리", ["처음 보는 오탈자도 마스터에 맞춰 교정", "열 이름 · 순서가 달라도 처리"]),
        ba("정해진 규칙 vs Skill", "02",
           "수식 · 스크립트\n\n정해 둔 규칙만 처리\n'B 편의점' → 규칙에 있으면 교정\n'B편의젬' → 규칙에 없으면 그대로\n열 순서가 바뀌면 오류",
           "Skill\n\n마스터와 비교해 판단\n'B편의젬' · 'ㅂ편의점'도 B편의점으로\n열 이름 · 순서가 달라도 읽음\n애매한 건 정제 리포트에 표시"),
        ba("지침은 규칙 목록이 아니라 판단 기준", "02",
           "'B 편의점'을 'B편의점'으로 바꿔 줘.\nC열과 D열을 기준으로 중복을 지워 줘.\n2~4381행만 처리해 줘.\n\n→ 다음 달 파일에서는 안 맞음",
           "목표: 어떤 파일이든 마스터 구조로\n열 의미부터 파악하고, 거래처는 마스터에서 가장 가까운 값으로.\n안 맞는 숫자는 고치지 말고 표시, 애매한 건 리포트에.\n\n→ 파일이 바뀌어도 그대로 사용"),
        light("정제 Skill 지침", f'<div class="twocol">{code("Skill", skill_md)}<div class="vl"><p>목표</p><p>판단 기준</p><p>모를 때의 처리</p><p>참조 마스터</p></div></div>', "02"),
        light("외부 AI와 시트 안 Apps Script", f'''<table class="dbt">
<thead><tr><th>작업</th><th>외부 AI (대화창)</th><th>시트 안 Apps Script</th></tr></thead><tbody>
<tr><td><b>읽기</b></td><td>가능</td><td>가능</td></tr>
<tr><td><b>새 파일 만들기</b></td><td>가능</td><td>가능</td></tr>
<tr><td><b>기존 셀 수정</b></td><td>권한 거부</td><td>가능</td></tr>
<tr><td><b>행 삭제 · 일괄 치환 · 행 추가</b></td><td>권한 거부</td><td>가능</td></tr>
</tbody></table>
<div class="dbnote"><span>이유</span> Apps Script는 시트 소유자 권한으로 실행</div>''', "02"),
        light("정제 방식 두 가지", cards([
            ("A · 안전 분리형", "원본은 그대로<br/>정제본을 새 시트로 생성<br/>언제: 백업 · 변경 기록이 중요할 때", ["drive"]),
            ("B · 내부 직접 조작형", "Skill이 Apps Script 코드 생성<br/>시트에 커스텀 메뉴 · 버튼<br/>언제: 팀원이 버튼으로 품질 검사", ["appsscript"]),
        ], 2), "02"),
        lab("1", "방식 A · 정제본 만들기", "02",
            "원본은 두고 정제본 시트를 새로",
            ["정제 Skill 만들기 (이름은 자유)", "01 원본을 Drive에 올리고 대화에 첨부", "/내 Skill 이름으로 호출", "정제 리포트 확인 → 정제본 시트 생성"],
            ["정제본 4,368행 · 원본 4,381행 그대로", "편의점 8월 매출 14.21억 원"],
            20, "01 · 04(대조용)"),
        lab("2", "방식 B · 시트 안 정제 메뉴", "02",
            "버튼 한 번으로 시트 안에서 정제",
            ["Skill에 「이 시트용 정제 Apps Script 만들어 줘」", "확장 프로그램 → Apps Script에 붙여넣기 · 저장", "시트 새로고침(F5) → 커스텀 메뉴 확인", "메뉴 실행 → 권한 승인(처음 한 번)"],
            ["메뉴 한 번으로 중복 · 띄어쓰기 정리", "실행 전 사본으로 백업"],
            15, "01 사본"),

        divider("03", "웹 화면에서 바로 입력", ""),
        team_map({"웹앱 URL", "Apps Script", "Sheets"}, "도구 지도 · 03", "입력이 시트로 가는 길"),
        ill("scenes_extra", "forms_inlet", "top20", "입구부터 반듯하게", ["드롭다운 · 자동완성", "오탈자 원천 차단"]),
        light("등록 버튼에서 시트까지", save_flow(), "03"),

        divider("04", "Apps Script 웹앱 대시보드", ""),
        team_map({"Canvas", "Apps Script", "웹앱 URL"}, "도구 지도 · 04", "만들고, 연결하고, 배포"),
        ill("scenes_ch4", "hang_window", "left40", "Apps Script로 시트와 연결", ["Code.gs: 시트 ↔ 화면", "Index.html: 화면 틀", "URL 하나로 공유"]),
        light("Code.gs의 세 함수", code("Code.gs", gas_code), "04"),
        light("처음부터 끝까지 다섯 단계", flow([("환경 준비", ".XLSX → Google 시트"), ("코드 받기", "Skill이 Code.gs · Index.html 생성"),
                                ("코드 넣기", "Apps Script 붙여넣기 · 메뉴"), ("웹앱 배포", "실행: 나"), ("운영", "정제 → 누적 → 새로고침")], hl=3), "04"),
        light("② 코드 받기", code("Skill에 요청", "이 시트의 열 구조를 먼저 읽고\n시트 안 정제 메뉴와 대시보드를 만드는\nCode.gs · Index.html 코드를 만들어 줘.\n시트 이름 · 열 이름은 실제 시트에 맞춰서."), "04"),
        light("코드 넣기 · 배포 · 승인", table(["단계", "누르는 곳", "확인"], [
            ["<b>코드 넣기</b>", "확장 프로그램 → Apps Script → 파일 추가(+) → HTML", "파일 이름 Index (대소문자 그대로)"],
            ["<b>웹앱 배포</b>", "배포 → 새 배포 → 톱니바퀴 → 웹 앱", "실행: 나 · 액세스: 내 조직"],
            ["<b>권한 승인</b>", "액세스 승인 → 계정 선택", "경고 창: 고급 → 이동 → 허용"],
        ]) + note(".XLSX 파일", "Apps Script 메뉴가 안 보이면 파일 → Google 스프레드시트로 저장"), "04"),
        lab("3", "웹앱 대시보드", "04",
            "시트와 연결된 대시보드 주소 받기",
            ["판매실적_마스터에서 Apps Script 열기", "Code.gs · Index.html 붙여넣기", "웹앱 배포 → 권한 승인", "웹 화면에서 한 건 등록"],
            ["옆 사람이 URL로 접속", "등록한 한 건이 시트와 화면에 반영"],
            30, "판매실적_마스터 · 09(화면 틀)"),
        light("⑤ 운영: 매달 반복", flow([("새 원본 도착", ""), ("정제 Skill 실행", "검출 · 정제"), ("마스터에 누적", "append"), ("팀원 새로고침", "URL 그대로")], hl=1), "04"),
        bridge("Skill은 정리, Apps Script는 연결", "", "전체", "원본 → Skill → 시트 마스터 → 웹앱"),
    ]


CSS = '''
  .websvg{width:100%; height:auto; max-height:430px;}
  .eco .tj{display:flex; align-items:center; gap:10px;}
  .eco .tj .chip{font-family:var(--serif); font-size:13px;}
  .eco .nh .ic{width:30px; height:30px;} .eco .nh .ic img{width:20px; height:20px;}
  .rolechip{background:#FFF3E6; color:#F28C28; font-weight:800; border-radius:6px; padding:3px 10px; font-size:15px;}
  .websvg.pipe2{max-height:470px;}
  .websvg .bt{font-family:var(--serif); font-size:20px; font-weight:800;}
  .websvg .bs{font-family:var(--serif); font-size:15px; fill:#44506A;}
  .websvg .bso{font-family:var(--serif); font-size:15px; fill:#F28C28; font-weight:700;}
  .websvg .bsw{font-family:var(--serif); font-size:15px; fill:#D9DDE3;}
'''
