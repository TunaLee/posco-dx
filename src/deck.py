"""이론 덱 전체 구성. 실습 · 따라하기 장은 별도 덱에 있다.

장 종류
  ill      그림 장 — 장면(SVG) + 빈 구역에 제목과 3줄 이내 본문
  ba       프롬프트 장 — Before / After 두 칸
  diagram  도식 장 — 카드 · 흐름
  dark     표지 · 간지 · 생태계 지도
"""
import importlib
from pathlib import Path

import explain
import intro
from intro import ICON, NAMES, coord, icon

N, G, O = "#1F3A5F", "#D9DDE3", "#F28C28"


# ── 장면 ────────────────────────────────────────────────
def scene(mod, fn):
    """장면 함수를 찾고, 아직 없으면 회색 자리 표시를 돌려준다."""
    try:
        return getattr(importlib.import_module(mod), fn)()
    except (ImportError, AttributeError):
        return (f'<rect x="560" y="200" width="660" height="460" rx="18" fill="{G}"/>'
                f'<text x="890" y="440" text-anchor="middle" font-size="22" fill="{N}">이미지 준비 중 · {fn}</text>')


PRINCIPLES = {1: "근거를 쥐여 준다", 2: "계획을 보여 줄 때 개입한다"}


def badge(n):
    return f'<div class="pbadge"><span class="pn">원칙 {"①②"[n-1]}</span>{PRINCIPLES[n]}</div>' if n else ""


# ── 장 만들기 ────────────────────────────────────────────
def ill(mod, fn, zone, title, lines=(), principle=0, extra=""):
    pos = "left" if zone == "left40" else "top"
    body = "".join(f"<li>{l}</li>" for l in lines)
    return f'''<section class="slide ill" data-title="{title}">
  <svg class="scene" viewBox="0 0 1280 720" aria-hidden="true">{scene(mod, fn)}</svg>
  {coord()}{badge(principle)}
  <div class="cap {pos}{' z25' if zone == 'top25' else ''}"><h2>{title}</h2>{'<div class="bar"></div>' if pos == 'left' else ''}{f'<ul>{body}</ul>' if body else ''}</div>
  {extra}
</section>'''


def light(title, body, ch, principle=0):
    return f'''<section class="slide lt" data-title="{title}">
  {coord()}{badge(principle)}
  <div class="eyebrow"><span class="tag">{ch}</span></div>
  <h2 class="s-title sm">{title}</h2>
  <div class="rule"></div>
  <div class="body"><div class="mid">{body}</div></div>
</section>'''


def ba(title, ch, before, after, note="", principle=0):
    def esc(t):
        return t.replace("\n", "<br/>")
    nb = f'<div class="banote">{note}</div>' if note else ""
    return light(title, f'''<div class="ba">
  <div class="b"><div class="lab">Before</div><div class="q">{esc(before)}</div></div>
  <div class="arr">→</div>
  <div class="a"><div class="lab">After</div><div class="q">{esc(after)}</div></div>
</div>{nb}''', ch, principle)


def cards(items, cols=3):
    """items: (머리, 본문, 아이콘 목록)"""
    out = []
    for h, p, ics in items:
        ic = "".join(icon(n) for n in ics)
        out.append(f'<div class="kcard">{f"<div class=icons>{ic}</div>" if ic else ""}<h4>{h}</h4>{f"<p>{p}</p>" if p else ""}</div>')
    return f'<div class="kcards c{cols}">{"".join(out)}</div>'


def flow(steps, hl=None):
    out = []
    for i, (h, p) in enumerate(steps):
        cls = " hl" if hl is not None and i == hl else ""
        out.append(f'<div class="fs{cls}"><b>{h}</b>{f"<span>{p}</span>" if p else ""}</div>')
    return '<div class="flow">' + '<div class="fa">→</div>'.join(out) + "</div>"


# ── 캡처 장 ──────────────────────────────────────────────
# 캡처 파일은 docs/grounding/assets/capture/<이름>.png. 없으면 회색 자리에 「캡처: …」를 적는다.
CAPDIR = Path(__file__).resolve().parent.parent / "docs" / "assets" / "capture"


def cap(name, label):
    for ext in ("png", "jpg", "webp"):
        if (CAPDIR / f"{name}.{ext}").exists():
            return f'<figure class="capfig"><img src="assets/capture/{name}.{ext}" alt="{label}"/><figcaption>{label}</figcaption></figure>'
    return f'<figure class="capfig empty"><div class="ph">캡처: {label}<span>{name}.png</span></div><figcaption>{label}</figcaption></figure>'


def capture(title, ch, shots, lines=()):
    """shots: [(파일 이름, 화면 이름)] 1~2개."""
    body = "".join(cap(n, l) for n, l in shots)
    side = "".join(f"<li>{x}</li>" for x in lines)
    return light(title, f'<div class="caps n{len(shots)}">{body}</div>' + (f'<ul class="capnote">{side}</ul>' if side else ""), ch)


def lab(no, title, ch, goal, steps, done, minutes=None, files=""):
    """실습 장 — 목표 · 단계 · 완료 기준 · 시간 네 칸 고정."""
    st = "".join(f"<li>{x}</li>" for x in steps)
    dn = "".join(f"<li>{x}</li>" for x in done)
    return f'''<section class="slide lt labs" data-title="[실습 {no}] {title}">
  {coord()}
  <div class="eyebrow"><span class="tag">{ch}</span><span class="labtag">실습 {no}</span></div>
  <h2 class="s-title sm">{title}</h2>
  <div class="rule"></div>
  <div class="body"><div class="labgrid">
    <div class="lc goal"><div class="lh">목표</div><p>{goal}</p>{f'<div class="lf">사용 파일 · {files}</div>' if files else ''}</div>
    <div class="lc steps"><div class="lh">단계</div><ol>{st}</ol></div>
    <div class="lc done"><div class="lh">완료 기준</div><ul>{dn}</ul></div>
  </div></div>
</section>'''


def bridge(title, question, ch, nxt):
    return f'''<section class="slide dk bridge" data-title="{title}">
  {coord()}
  <div class="kick">{ch} 정리</div>
  <h2>{title}</h2>
  {f'<div class="q">{question}</div>' if question else ''}
  <div class="nxt">{nxt}</div>
</section>'''


# ── 생태계 지도 ───────────────────────────────────────────
# 역할, 도구, 아이콘, 처음 쓰는 장. 위치는 그림 ⑨와 같은 시계 방향.
ROLES = [
    ("리서치 담당", "Deep Research", ["gemini"], "Ch1", (250, 255)),
    ("검토자", "NotebookLM", ["notebooklm"], "Ch1", (640, 215)),
    ("데이터 창고", "Sheets · Forms", ["sheets", "forms"], "Ch2", (1030, 255)),
    ("작업대", "Canvas", ["docs"], "Ch3", (1030, 590)),
    ("자동화 담당", "Apps Script · Studio", ["appsscript"], "Ch4", (640, 650)),
    ("전담 비서", "Skills", ["gemini"], "Ch5", (250, 590)),
]
ACTIVE = {
    "Ch1": {"리서치 담당", "검토자"}, "Ch2": {"데이터 창고"}, "Ch3": {"작업대"},
    "Ch4": {"작업대", "자동화 담당"}, "Ch5": {"전담 비서"},
    "적용": {r[0] for r in ROLES},
}
ORDER = ["Ch1", "Ch2", "Ch3", "Ch4", "Ch5", "적용"]


def eco(ch=None, title=None):
    hub = (640, 430)

    def state(role, first):
        if ch is None:
            return "all"
        if role in ACTIVE[ch]:
            return "on"
        return "done" if ORDER.index(first) < ORDER.index(ch) else "dim"

    lines, cards_ = [], []
    for role, tool, ics, first, (x, y) in ROLES:
        st = state(role, first)
        line = {
            "all": f'stroke="{O}" stroke-width="2.5" stroke-dasharray="6 7" opacity=".7"',
            "done": 'stroke="#fff" stroke-width="2.5" opacity=".45"',
            "dim": 'stroke="#fff" stroke-width="2" stroke-dasharray="4 8" opacity=".12"',
            "on": f'stroke="{O}" stroke-width="5" opacity=".35"',
        }[st]
        lines.append(f'<line x1="{hub[0]}" y1="{hub[1]}" x2="{x}" y2="{y}" {line}/>')
        if st == "on":
            lines.append(f'<line class="flow" x1="{hub[0]}" y1="{hub[1]}" x2="{x}" y2="{y}" stroke="{O}" stroke-width="5" stroke-linecap="round" stroke-dasharray="14 12"/>')
        cards_.append(f'''<div class="node {st}" style="left:{x-170}px; top:{y-44}px">
  <div class="nh"><span class="chip">{first}</span><b>{role}</b></div>
  <div class="icons">{"".join(icon(n) for n in ics)}<span class="nm">{tool}</span></div>
</div>''')
    if ch is None:
        kick, h2, dt = "구글 생태계", title or "도구 지도", "생태계 지도"
    else:
        kick, h2, dt = f"구글 생태계 · {ch}", title, f"[{ch}] 생태계 지도"
    return f'''<section class="slide dk eco{' focus' if ch else ''}" data-title="{dt}">
  {coord()}
  <div class="kick">{kick}</div>
  <h2>{h2}</h2>
  <svg class="ecosvg" viewBox="0 0 1280 720">{"".join(lines)}</svg>
  {"".join(cards_)}
  <div class="hub" style="left:{hub[0]-74}px; top:{hub[1]-74}px"><img src="{ICON.format("gemini")}" alt="Gemini"/></div>
</section>'''


def divider(ch, title, sub):
    num = ch[2:].zfill(2) if ch.startswith("Ch") else (ch if ch.isdigit() else {"최종": "06", "적용": "07"}.get(ch, "06"))
    return f'''<section class="slide dk divider" data-title="[{ch}] {title}">
  <div class="ghost">{num}</div>
  <div class="kick">{ch}</div>
  <h2 class="big">{title}</h2>
  {f'<div class="sub">{sub}</div>' if sub else ''}
</section>'''


def chapter(ch, title, sub, map_title):
    return [divider(ch, title, sub), eco(ch, map_title)]


# ── 오프닝 ───────────────────────────────────────────────
def cover():
    strip = "".join(icon(n, "tile") for n in ["gemini", "notebooklm", "sheets", "docs", "appsscript", "gmail", "drive", "calendar"])
    return f'''<section class="slide dk cover-dk active" data-title="표지">
  <div class="glow"></div>
  <div class="kick">생성형 AI 중급 과정 · 국내영업</div>
  <h1>AI로 일하는 방식<br/>바꾸기</h1>
  <div class="strip">{strip}</div>
</section>'''


def o02():
    left = "".join(f"<span>{t}</span>" for t in ["질문하기", "요약하기", "초안 쓰기"])
    right = "".join(f"<span>{t}</span>" for t in ["조사 · 검증", "데이터 정리", "문서와 화면", "자동화", "전담 비서"])
    return light("초급과 중급의 차이", f'''<div class="lvl">
  <div class="col"><div class="h">초급</div><div class="chips2">{left}</div></div>
  <div class="arr">→</div>
  <div class="col hl"><div class="h">중급</div><div class="chips2">{right}</div></div>
</div>''', "오프닝")


AGENDA = [
    ("Ch1", "근거 있는 답", "출처 달린 조사 보고서", ["gemini", "notebooklm"]),
    ("Ch2", "하네스와 Skills", "메일 Skill · 응대 Skill", ["gemini"]),
    ("Ch3", "데이터 정리 · 분석", "정제본 시트 · 8월 집계", ["sheets"]),
    ("Ch4", "Canvas 대시보드", "대시보드 시제품", ["docs"]),
    ("Ch5", "연결 · 배포", "웹앱 대시보드", ["appsscript"]),
    ("최종", "핸즈온", "점포 점검 대시보드 웹앱", ["sheets", "gemini", "appsscript"]),
]


def agenda():
    rows = "".join(f'''<div class="ch"><span class="chip">{c}</span><div class="tx"><b>{t}</b><span>{d}</span></div>
<div class="icons">{"".join(icon(n) for n in ics)}</div></div>''' for c, t, d, ics in AGENDA)
    day2 = ''
    return f'''<section class="slide dk" data-title="목차">
  {coord()}
  <h2>목차</h2>
  <div class="days one">
    <div class="daycol">{rows}{day2}</div>
  </div>
</section>'''


def o_work():
    rows = [("파일마다 매출 취합", "Sheets 자동 집계"),
            ("달성률 손 계산", "수식 자동 계산"),
            ("문의마다 새로 쓰는 회신", "응대 Skill 초안"),
            ("매주 새로 쓰는 보고", "초안 자동 생성")]
    trs = "".join(f'<div class="wb"><span class="w0">{a}</span><span class="wa">→</span><span class="w1">{b}</span></div>' for a, b in rows)
    return light("반복 업무의 변화", f'<div class="wbh"><span>지금</span><span></span><span>이후</span></div>{trs}', "오프닝")


def o05():
    return light("가상 시나리오", f'''<div class="scen">
  <div class="who">가상 영업관리 DB · <b>2026년 4~9월 · 180행</b></div>
  <div class="who"><b>A편의점 본부</b> · 4분기 신제품 입점 제안</div>
  {flow([("조사", "Ch1"), ("숫자 정리", "Ch2"), ("제안서 · ROI", "Ch3"), ("대시보드 · 주간 보고", "Ch4"), ("응대 Skill", "Ch5")])}
</div>''', "오프닝")


def o06():
    return light("약속 세 가지", cards([
        ("실제 데이터 넣지 않기", "", []),
        ("막히면 바로 손들기", "", []),
        ("먼저 끝나면 옆 사람 돕기", "", []),
    ]), "오프닝")


# ── Ch1 ─────────────────────────────────────────────────
CH1_ILL = [
    ("s1", "left40", "AI 답, 그대로 써도 될까요?", 0),
    ("s2", "top25", "AI는 모를 때도 문장을 완성한다", 0),
    ("s3", "top20", "AI가 모르는 두 가지: 최신 정보, 우리 회사", 0),
    ("s4", "top20", "근거를 찾아오게 하거나, 근거 안에 가두거나", 0),
    ("s5", "left40", "Deep Research는 계획부터 세운다", 2),
    ("s6", "top20", "노트북은 오픈북 시험이다", 1),
    ("s7", "top20", "같은 질문, 세 가지 답", 0),
    ("s8", "left40", "AI 답의 품질은 근거의 품질이다", 1),
]


def ch1():
    out = chapter("Ch1", "근거 있는 답을 받는 법", "", "Deep Research · NotebookLM")
    for (fn, zone, title, pr), ex in zip(CH1_ILL, explain.SLIDES):
        out.append(ill("scenes_ch1", fn, zone, title, principle=pr))
        out.append(ex())
    out.append(light("원칙 두 가지", cards([
        ("원칙 ① 근거를 쥐여 준다", "볼 자료를 정해 준다", ["notebooklm"]),
        ("원칙 ② 계획을 보여 줄 때 개입한다", "실행 전에 계획을 고친다", ["gemini"]),
    ], 2), "Ch1"))
    return out


# ── Ch2 ─────────────────────────────────────────────────
def ch2():
    m = "scenes_ch2"
    cols = ["월", "지역", "채널", "거래처", "제품", "목표매출_원", "실제매출_원", "달성률"]
    row = ["2026-09", "수도권", "대형마트", "가상거래처-01", "제품명", "5,000,000", "4,650,000", "93%"]
    db = ('<table class="dbt"><thead><tr>' + "".join(f"<th>{c}</th>" for c in cols) + "</tr></thead><tbody><tr>"
          + "".join(f"<td>{c}</td>" for c in row) + "</tr>"
          + "<tr class=more>" + "".join("<td>⋮</td>" for _ in cols) + "</tr></tbody></table>")
    return chapter("Ch2", "숫자를 믿을 수 있게 정리하기", "", "Sheets · Forms") + [
        ill(m, "tables", "top20", "AI가 잘 읽는 표",
            ["한 행에 한 건", "헤더는 한 줄", "병합 셀 없음"]),
        light("매출원본", f'''{db}
<div class="dbnote"><span>180행</span> 2026년 4~9월 · 지역 5 · 채널 3 · 가상 거래처 30</div>''', "Ch2"),
        ill("scenes_extra", "forms_inlet", "top20", "Forms로 입력 양식 통일",
            ["메모 · 메신저: 제각각", "Forms: 응답 1건 = 1행"]),
        ba("데이터 설명 후 단계별 요청", "Ch2",
           "이 데이터 분석해 줘",
           "이 시트는 2026년 4~9월 지역 · 채널 · 거래처별 월 매출이야.\n열은 월, 지역, 채널, 거래처, 제품, 목표매출_원, 실제매출_원, 달성률이야.\n1단계로 달성률 90% 미만 행만 골라 미달 금액 순으로 정렬해 줘.\n확인하고 다음 단계를 요청할게.",
           "맥락 · 한 단계 · 확인"),
        ill(m, "navigation", "left40", "Sheets Gemini: 계획 먼저 확인",
            ["요청 → 계획 확인 → 실행"], principle=2),
        ill(m, "gauges", "top20", "값 대신 수식",
            ["값: 그대로", "수식: 다시 계산"]),
        ill(m, "two_sheets", "left40", "합계 두 개 직접 대조",
            ["총 목표 · 총 실적 SUM 대조"]),
        ill("scenes_extra", "fact_hypothesis", "left40", "사실과 가설 구분",
            ["사실: 시트의 숫자", "가설: 원인 추정"], principle=1),
        bridge("다음: 정리한 숫자로 제안서 쓰기", "", "Ch2", "→ Ch3"),
    ]


# ── Ch3 ─────────────────────────────────────────────────
def ch3():
    m = "scenes_ch3"
    return chapter("Ch3", "근거 있는 제안서를 빠르게", "", "Canvas") + [
        ill(m, "chat_vs_workbench", "top20", "채팅은 대화, Canvas는 작업대",
            ["채팅: 흘러가는 답", "Canvas: 한 장을 두고 수정"]),
        ill(m, "mural", "top20", "전체 재생성 대신 부분 수정",
            []),
        ill(m, "briefing", "left40", "신입에게 업무를 맡기듯",
            ["역할 · 맥락 · 작업 · 형식"]),
        ba("제안서 요청", "Ch3",
           "편의점에 낼 제안서 써 줘",
           "너는 식품회사 국내영업 담당자야.\nA편의점 본부 바이어에게 신제품 입점을 제안하려고 해.\n첨부한 검증 완료 보고서와 실적 시트 숫자를 근거로 1페이지 제안서를 써 줘.\n순서는 제안 배경, 제품 강점, 기대 효과(표), 지원 조건이고 과장 표현은 쓰지 마."),
        ill(m, "audience", "top20", "상대에 따라 강조점 조정",
            ["신규: 신뢰 · 초기 지원", "기존: 실적 · 확대 효과", "이탈 위험: 문제 해결 · 조건"]),
        ba("판촉 ROI 계산기 요청", "Ch3",
           "판촉 ROI 계산기 만들어 줘",
           "영업기획 담당자를 위한 판촉 ROI 계산기를 만들어 줘.\n입력: 행사 전 매출, 행사 후 매출, 매출총이익률, 판촉비\n출력: 증분매출, 증분이익, ROI = (증분이익 − 판촉비) ÷ 판촉비\n계산식은 화면 아래에 적고, 판촉비가 0원이어도 멈추지 않게 해 줘.",
           "입력 · 출력 · 계산식 · 예외"),
        ill("scenes_extra", "calculator_test", "left40", "정답을 아는 값으로 검증",
            ["5,000만 → 6,500만 · 30% · 300만", "→ ROI 50%", "추정치 ≠ 효과 증명"], principle=1),
        ill(m, "photo", "left40", "공유된 Canvas는 그 순간의 사진",
            []),
    ]


# ── Ch4 ─────────────────────────────────────────────────
def ch4():
    m = "scenes_ch4"
    sc = '<div class="capbox">캡처: Sheets canvas 화면</div>'
    return chapter("Ch4", "한 번 만들면 계속 돌아가게", "", "Canvas · Apps Script · Studio") + [
        ill(m, "photo_window", "top20", "사진과 창문",
            ["사진: 그때 숫자", "창문: 지금 숫자"]),
        ill(m, "hang_window", "left40", "Apps Script로 시트와 연결",
            ["Canvas 대시보드 + 시트 연결", "주소 하나로 공유"]),
        ill(m, "menu_board", "left40", "틀은 그대로, 데이터만 교체",
            ["render(rows) 하나로 요청"]),
        ba("대시보드 요청", "Ch4",
           "실적 대시보드 만들어 줘",
           "'매출원본' 시트의 지역, 채널, 목표매출_원, 실제매출_원으로\n총 목표 · 총 실적 · 달성률 카드와 채널별 목표 대비 실적 막대그래프가 있는 대시보드를 만들어 줘.\n화면은 render(rows) 함수 하나로 그리고,\n데이터는 나중에 시트에서 받을 수 있게 분리해 줘."),
        light("Sheets canvas", f'''<div class="twocol">
  <div class="vl"><p>시트 안 실시간 대시보드</p><p>현재 영어 설정 계정만</p></div>
  {sc}
</div>''', "Ch4"),
        ill(m, "alarm", "left40", "자동화 = 언제 + 무엇을",
            ["언제: 월요일 8시 · 메일 도착", "무엇을: 읽기 · 요약 · 보내기"]),
        ill(m, "two_tools", "top20", "Apps Script와 Studio 비교",
            ["Apps Script: 코드 · 정확한 계산", "Studio: 말로 만들고 수정"]),
        ba("자동화 요청", "Ch4",
           "매주 실적 메일 자동으로 보내 줘",
           "'매출원본' 시트를 읽어서\n매주 월요일 오전 8시에\n지난주 지역별 목표 · 실적 · 달성률을 표로 만들어\n내 메일로 보내 줘."),
        ill(m, "domino", "top20", "Studio: 말로 만드는 자동화",
            ["단계 검토: 사람"], principle=2),
        ill(m, "envelope_fly", "left40", "테스트도 실제로 발송됨",
            ["실습 수신자: 본인"]),
        ill("scenes_extra", "draft_review", "top20", "초안까지 자동, 발송은 사람",
            ["초안 → 숫자 검증 → 수신인 → 발송"], principle=2),
        bridge("다음: 반복 지시 저장하기", "", "Ch4", "→ Ch5"),
    ]


# ── Ch5 ─────────────────────────────────────────────────
def ch5():
    m = "scenes_ch5"
    bot = f'''<div class="ba">
  <div class="b"><div class="lab">2023~2024 · 봇</div><div class="q">GPTs · Gems<br/>역할마다 따로 만든 대화 상대<br/>쓰려면 그 봇으로 이동</div></div>
  <div class="arr">→</div>
  <div class="a"><div class="lab">2025~2026 · 스킬</div><div class="q">Skills<br/>필요할 때 꺼내 쓰는 업무 지침 묶음<br/>한 대화에서 <b>/이름</b>으로 호출 · 여러 개 조합</div></div>
</div>'''
    trend = f'''<div class="tline t4">
  <div class="tl"><b>2025.10</b><span>Claude · Agent Skills</span></div>
  <div class="tl"><b>2025.12</b><span>Agent Skills 공개 표준</span></div>
  <div class="tl"><b>2026</b><span>ChatGPT · Skills (업무용 플랜)</span></div>
  <div class="tl hl"><b>2026.10</b><span>Gemini · Skills</span></div>
</div>
<div class="homework"><b>공통</b> 이름 · 설명 · 지침 · 참고 자료 한 묶음</div>'''
    move = f'''<div class="tline">
  <div class="tl"><b>2026.10.13</b><span>Gemini 앱에 Skills 출시</span></div>
  <div class="tl"><b>2026.11.17</b><span>Gem은 설정 메뉴로 이동</span></div>
  <div class="tl hl"><b>2027.3.1</b><span>Workspace 계정 Gem 종료</span></div>
</div>
<div class="homework"><b>이전</b> 기존 Gem → Skill 비활성 초안 · 검토 후 활성화</div>'''
    skillmd = ("---\n"
               "name: 거래처 응대\n"
               "description: 편의점 거래처 문의에 1차 회신 초안을 쓴다\n"
               "---\n"
               "역할: 편의점 거래처 응대 도우미\n"
               "출력: 회신 초안 5문장 이내 + 근거 조항 번호\n"
               "규칙: 원인 확인 전 보상 약속 금지\n"
               "참고: 05 카탈로그 · 06 기준표 · 07 응대가이드")
    harness = '''<div class="hn">
  <div class="hn-out"><div class="hn-lab">하네스</div>
    <div class="hn-row"><span class="hl">지침 = Skill</span><span>참고 자료</span></div>
    <div class="hn-core">모델</div>
    <div class="hn-row"><span>도구 연결</span><span>사람 확인</span></div>
  </div>
</div>'''
    return chapter("Ch5", "반복되는 지시를 저장하는 Skills", "", "Skills") + [
        light("봇에서 스킬로", bot, "Ch5"),
        light("AI 도구 모두 Skills로", trend, "Ch5"),
        light("Gem에서 Skills로", move, "Ch5"),
        light("Skill의 구조", f'<div class="twocol">{explain.prompt("Skill 한 개", skillmd)}<div class="vl"><p>이름 · 설명: 언제 쓸지</p><p>지침: 어떻게 할지</p><p>참고 자료: 무엇을 근거로</p></div></div>', "Ch5"),
        light("모델과 하네스", harness, "Ch5"),
        ill(m, "secretary", "left40", "Skill: 저장해 두는 업무 지침",
            ["/이름으로 호출", "여러 Skill 조합"]),
        ill(m, "conveyor", "top20", "지침은 매번 자동 적용",
            ["지침 품질 = 결과 품질"]),
        ill("scenes_ch1", "s6", "top20", "참조 파일은 참고 교재",
            ["수치는 사용자가 준 것만"], principle=1),
        ba("Skill 지침 작성", "Ch5",
           "너는 거래처 응대 도우미야",
           "역할: 편의점 거래처 응대 도우미\n입력: 거래처 문의 내용\n출력: 1차 회신 초안 5문장 이내 + 근거 조항 번호\n규칙: 원인 확인 전 보상 약속 금지, 기준표에 없는 조건은 [확인 필요]\n참조: 05 제품카탈로그 · 06 단가 기준표 · 07 응대가이드"),
        capture("Skill 만들기", "Ch5", [("skill-01-create", "Skill 만들기"), ("skill-02-instructions", "지침 입력")]),
        capture("참조 파일 추가", "Ch5", [("skill-03-files", "참조 파일")], ["PDF · 문서 · 이미지"]),
        lab("5-1", "첫 Skill: /응대", "Ch5",
            "거래처 문의에 1차 회신 초안을 쓰는 Skill",
            ["지침 작성 (역할 · 입력 · 출력 · 규칙)", "참조 파일 05 · 06 · 07 추가", "저장", "새 대화에서 /응대 호출"],
            ["A편의점 결품 문의 → R-6 절차대로 회신", "금지 표현 없음 · 5문장 이내"],
            25, "05 · 06 · 07"),
        ill(m, "interview", "top20", "세 가지 입력으로 테스트",
            ["정상: A편의점 결품 문의", "기준표 밖: 북부대리점 행사 물량", "기준 위반: A마트 매대 3주"]),
        capture("/로 불러 테스트", "Ch5", [("skill-04-run", "/응대 · 결품 문의 테스트")]),
        ba("지침 한 줄 추가 전후", "Ch5",
           "문의: 신제품 A 결품, 보상 가능한가요?\n\n→ 불편을 드려 죄송합니다. 보상해 드리겠습니다.",
           "지침 추가: 원인 확인 전 보상 약속 금지\n\n→ 물류팀 확인 결과를 받은 뒤\n   2영업일 안에 다시 연락드리겠습니다."),
        lab("5-2", "세 가지 입력으로 고치기", "Ch5",
            "틀린 답을 찾아 지침 한 줄씩 보완",
            ["세 가지 입력을 /응대로 차례로 테스트", "기준과 다른 답 표시", "지침에 규칙 한 줄 추가", "같은 입력으로 다시 테스트"],
            ["세 답 모두 근거 조항 번호 표기", "북부대리점 → [확인 필요]", "A마트 → 최대 2주 안내 (P-5)"],
            15, "02 · 06 · 07"),
        light("Skill 조합", f'''<div class="combo"><span>/응대</span><b>+</b><span>/회신 형식</span><b>=</b><span class="hl">기준 지킨 회신 초안</span></div>''', "Ch5"),
        light("영업관리 Skill 예시", cards([
            ("응대", "거래처 문의 1차 회신", ["gemini"]),
            ("매출 분석", "실적 미달 거래처 정리", ["sheets"]),
            ("주간 보고", "정해진 양식의 회의 보고문", ["docs"]),
            ("판촉 기획", "목표 · 예상 성과 · 위험 요인", ["gemini"]),
        ], 4), "Ch5"),
        lab("5-3", "나만의 반복 업무 Skill", "Ch5",
            "매주 하는 일 하나를 /한 줄로",
            ["예시 셋 중 하나 또는 내 업무 선택", "잘 된 대화에서 「이 대화를 Skill로 만들어 줘」", "지침 · 참조 파일 다듬기", "새 대화에서 /이름 + /응대 등 조합"],
            ["새 대화에서 /이름 한 줄로 같은 형식 결과", "숫자는 04 시트와 일치"],
            25, "04 · 03"),
        ill(m, "agent_morning", "top20", "Studio + 지침 = 에이전트",
            ["문의 → 답장 초안 → 담당자 알림", "자동 발송 없음"]),
        light("결과물의 연결", f'''{flow([("조사", "Ch1"), ("숫자", "Ch2"), ("제안서", "Ch3"), ("대시보드 · 메일", "Ch4"), ("Skill", "Ch5")])}
<div class="homework"><b>숙제</b> 내 업무에서 만들 것 하나</div>''', "Ch5"),
    ]


# ── 적용 ───────────────────────────────────────────────
def apply_():
    return chapter("적용", "내 업무에 적용하기", "", "전체 도구") + [
        light("두 가지 원칙", cards([
            ("원칙 ① 근거를 쥐여 준다", "Ch1 오픈북 · Ch5 참조 파일", ["notebooklm", "gemini"]),
            ("원칙 ② 계획을 보여 줄 때 개입한다", "Ch1 Deep Research · Ch2 Sheets · Ch4 Studio", ["gemini", "sheets", "appsscript"]),
        ], 2), "적용"),
        ill("scenes_ch5", "construction", "top20", "작게 끝내기",
            ["Before: 팀 전체 영업 관리 시스템", "After: 내 방문 메모 정리 흐름"]),
        light("트랙 선택", cards([
            ("문서 · 제안", "Canvas + Skill<br/>예: 판촉 성과 비교 도구", ["docs", "gemini"]),
            ("대시보드", "Sheets + Forms + Canvas<br/>예: 이슈 통합 관리 화면", ["sheets", "forms", "docs"]),
            ("자동화", "Apps Script · Studio + Skill<br/>예: 지역별 미달 알림 초안", ["appsscript", "gemini"]),
        ]), "적용"),
        light("평가 기준", f'''<div class="score">
  <div class="sc"><b>30</b><span>실제 업무 적합성</span></div><div class="sc"><b>30</b><span>계산 · 분석 정확도</span></div>
  <div class="sc"><b>25</b><span>실행 완성도</span></div><div class="sc"><b>15</b><span>사용성 · 확장성</span></div>
</div>
<div class="homework"><b>완료</b> 분석 1 + 계산 1 + 자동화 시연 1</div>''', "적용"),
        light("발표 2분", flow([("문제", ""), ("데모", ""), ("전후 비교", "")], hl=1), "적용"),
        bridge("작은 자동화부터 2주 시범 운영", "", "적용", "운영 계정 · 데이터 정책 → 2주 파일럿 → 개선"),
    ]


# ── 오프닝 이어 붙이기 ─────────────────────────────────────
# 그림 ⑨ 이름표 자리 (scenes_ch2.office_map 의 label 위치와 같다)
TAGS = [((400, 344), "리서치 · Deep Research"), ((880, 344), "검토자 · NotebookLM"), ((1112, 500), "데이터 창고 · Sheets · Forms"),
        ((880, 654), "작업대 · Canvas"), ((420, 654), "자동화 · Apps Script · Studio"), ((168, 500), "전담 비서 · Skills")]


def tags():
    return "".join(f'<div class="tagl" style="left:{x-107}px; top:{y}px">{t}</div>' for (x, y), t in TAGS)


def opening():
    return [
        cover(),
        intro.speaker(),
        intro.codered(),
        intro.meme(),
        o02(),
        o_work(),
        ill("scenes_ch2", "desk_outputs", "top25", "결과물 다섯 가지"),
        agenda(),
        ill("scenes_ch2", "office_map", "top20", "도구별 역할", extra=tags()),
        eco(None),
        o05(),
        o06(),
    ]


def slides():
    return opening() + ch1() + ch2() + ch3() + ch4() + ch5() + apply_()


CSS = '''
  /* ── 그림 장 ── */
  .slide.ill{padding:0; background:#fff; border:none;}
  .slide.ill svg.scene{position:absolute; inset:0; width:1280px; height:720px;}
  .ill .cap{position:absolute; z-index:2; color:#1F3A5F;}
  .ill .cap h2{margin:0; font-weight:800; letter-spacing:-.03em; word-break:keep-all;}
  .ill .cap ul{list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:8px;}
  .ill .cap li{position:relative; padding-left:16px; color:#1F3A5F; word-break:keep-all;}
  .ill .cap li::before{content:""; position:absolute; left:0; top:.62em; width:7px; height:7px; border-radius:50%; background:#F28C28;}
  .ill .cap.left{left:72px; top:0; bottom:0; width:410px; display:flex; flex-direction:column; justify-content:center;}
  .ill .cap.left h2{font-size:40px; line-height:1.22;}
  .ill .cap.left .bar{width:56px; height:5px; border-radius:3px; background:#F28C28; margin:22px 0 20px;}
  .ill .cap.left li{font-size:19px; line-height:1.5;}
  .ill .cap.top{left:72px; right:150px; top:34px; display:grid; grid-template-columns:1.35fr 1fr; gap:36px; align-items:start;}
  .ill .cap.top h2{font-size:31px; line-height:1.25;}
  .ill .cap.top ul{padding-top:4px; gap:5px;}
  .ill .cap.top li{font-size:16px; line-height:1.45;}
  .ill .cap.top.z25 h2{font-size:34px;}
  .ill .coord{z-index:3;}
  .ill .tagl{position:absolute; z-index:2; width:214px; height:24px; line-height:24px; text-align:center; font-size:12.5px; font-weight:700; color:#1F3A5F; letter-spacing:-.02em;}
  .pbadge{position:absolute; right:40px; top:56px; z-index:3; display:flex; align-items:center; gap:8px; font-size:12.5px; font-weight:700; color:#1F3A5F; background:#FFF3E6; border:1px solid #F7C99A; border-radius:999px; padding:5px 12px 5px 6px;}
  .pbadge .pn{background:#F28C28; color:#fff; border-radius:999px; padding:2px 8px; font-size:11.5px;}
  .slide.dk .pbadge{top:56px;}

  /* ── 밝은 본문 장 ── */
  .slide.lt .eyebrow .tag{font-family:var(--serif);}
  .ba{display:grid; grid-template-columns:1fr 56px 1.5fr; align-items:stretch;}
  .ba .b, .ba .a{border-radius:16px; padding:24px 26px; display:flex; flex-direction:column; gap:14px;}
  .ba .b{background:#EEF1F5; border:1px solid #DDE2E9;}
  .ba .a{background:#fff; border:2px solid #F28C28; box-shadow:0 18px 40px -26px rgba(242,140,40,.6);}
  .ba .lab{font-family:var(--mono); font-size:13px; font-weight:700; letter-spacing:.08em; color:#8A94A6; text-transform:uppercase;}
  .ba .a .lab{color:#F28C28;}
  .ba .q{font-size:18.5px; line-height:1.65; color:#16233A; word-break:keep-all;}
  .ba .b .q{color:#44506A;}
  .ba .arr{display:grid; place-items:center; font-size:30px; color:#F28C28; font-weight:800;}
  .banote{margin-top:4px; font-size:15px; color:#44506A;}
  .banote::before{content:"구성  "; font-weight:800; color:#F28C28;}
  .kcards{display:grid; gap:18px;} .kcards.c2{grid-template-columns:1fr 1fr;} .kcards.c3{grid-template-columns:repeat(3,1fr);} .kcards.c4{grid-template-columns:repeat(4,1fr);}
  .kcard{background:#fff; border:1px solid #E1E5EB; border-top:4px solid #1F3A5F; border-radius:10px; padding:24px 24px 26px; display:flex; flex-direction:column; gap:10px;}
  .kcard h4{margin:0; font-size:22px; font-weight:800; color:#16233A; word-break:keep-all;}
  .kcard p{margin:0; font-size:16.5px; line-height:1.55; color:#44506A; word-break:keep-all;}
  .kcard .icons{display:flex; gap:8px; margin-bottom:4px;}
  .kcard .ic, .lt .ic{width:38px; height:38px; border-radius:10px; background:#F6F8FA; border:1px solid #E1E5EB; display:inline-grid; place-items:center;}
  .kcard .ic img{width:24px; height:24px;}
  .flow{display:flex; align-items:stretch; gap:0;}
  .flow .fs{flex:1; background:#fff; border:1px solid #E1E5EB; border-top:4px solid #1F3A5F; border-radius:10px; padding:18px 14px; text-align:center; display:flex; flex-direction:column; gap:6px; justify-content:center;}
  .flow .fs b{font-size:19px; color:#16233A;} .flow .fs span{font-size:14px; color:#8A94A6;}
  .flow .fs.hl{border-top-color:#F28C28; box-shadow:0 18px 40px -26px rgba(242,140,40,.6);}
  .flow .fa{display:grid; place-items:center; padding:0 8px; color:#F28C28; font-weight:800; font-size:22px;}
  .lvl{display:grid; grid-template-columns:1fr 70px 1.4fr; align-items:stretch;}
  .lvl .col{background:#EEF1F5; border-radius:16px; padding:26px 28px; display:flex; flex-direction:column; gap:8px;}
  .lvl .col.hl{background:#fff; border:2px solid #F28C28;}
  .lvl .h{font-size:24px; font-weight:800; color:#16233A;} .lvl .sub{font-size:15px; color:#8A94A6; margin-bottom:10px;}
  .lvl .arr{display:grid; place-items:center; font-size:34px; color:#F28C28; font-weight:800;}
  .chips2{display:flex; flex-wrap:wrap; gap:10px;}
  .chips2 span{font-size:17px; font-weight:700; color:#1F3A5F; background:#fff; border:1px solid #D9DDE3; border-radius:999px; padding:8px 16px;}
  .lvl .col.hl .chips2 span{background:#FFF3E6; border-color:#F7C99A;}
  .scen{display:flex; flex-direction:column; gap:28px;}
  .scen .who{font-size:21px; color:#16233A; background:#EEF1F5; border-radius:12px; padding:18px 22px;}
  .scen .who b{color:#F28C28;}
  .homework{margin-top:30px; font-size:20px; color:#16233A; border-left:4px solid #F28C28; padding:8px 0 8px 18px;}
  .homework b{color:#F28C28; margin-right:12px;}
  .capbox{background:#D9DDE3; border-radius:14px; height:300px; display:grid; place-items:center; font-size:18px; font-weight:700; color:#1F3A5F;}
  .wbh, .wb{display:grid; grid-template-columns:1fr 50px 1fr; align-items:center;}
  .wbh{font-size:14px; font-weight:800; color:#8A94A6; margin-bottom:6px;} .wbh span:last-child{color:#F28C28;}
  .wb{padding:15px 0; border-bottom:1px solid #E1E5EB;} .wb .w0{font-size:19px; color:#8A94A6;} .wb .w1{font-size:20px; font-weight:800; color:#16233A;} .wb .wa{color:#F28C28; font-weight:800; font-size:20px; text-align:center;}
  .dbt{width:100%; border-collapse:collapse; font-size:16px;} .dbt th{background:#1F3A5F; color:#fff; padding:12px 10px; font-weight:700; text-align:left;}
  .dbt td{padding:12px 10px; border-bottom:1px solid #E1E5EB; color:#16233A;} .dbt tr.more td{color:#8A94A6; text-align:center;}
  .dbnote{margin-top:18px; font-size:18px; color:#44506A;} .dbnote span{background:#F28C28; color:#fff; font-weight:800; border-radius:6px; padding:3px 10px; margin-right:10px;}
  .score{display:grid; grid-template-columns:repeat(4,1fr); gap:16px;} .sc{background:#fff; border:1px solid #E1E5EB; border-top:4px solid #1F3A5F; border-radius:10px; padding:22px; display:flex; flex-direction:column; gap:6px;}
  .sc b{font-size:40px; color:#F28C28;} .sc span{font-size:17px; font-weight:700; color:#16233A;}
  .days.one{grid-template-columns:1fr; max-width:760px;}
  .caps{display:grid; gap:20px;} .caps.n1{grid-template-columns:1fr; justify-items:center;} .caps.n2{grid-template-columns:1fr 1fr;}
  .capfig{margin:0; display:flex; flex-direction:column; gap:8px; align-items:center; width:100%;}
  .capfig img{max-width:100%; max-height:420px; border-radius:10px; border:1px solid #E1E5EB; box-shadow:0 18px 40px -26px rgba(22,35,58,.5);}
  .caps.n2 .capfig img{max-height:380px;}
  .capfig figcaption{font-size:14px; color:#8A94A6;}
  .capfig .ph{width:100%; max-width:820px; aspect-ratio:16/9; max-height:420px; background:#D9DDE3; border-radius:12px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px; font-size:20px; font-weight:800; color:#1F3A5F;}
  .caps.n2 .ph{max-height:330px;}
  .capfig .ph span{font-family:var(--mono); font-size:13px; font-weight:400; color:#44506A;}
  .capfig.empty figcaption{display:none;}
  .capnote{list-style:none; margin:18px 0 0; padding:0; display:flex; gap:28px; justify-content:center;}
  .capnote li{font-size:16px; color:#44506A;} .capnote li::before{content:"· "; color:#F28C28; font-weight:800;}
  .tline{display:grid; grid-template-columns:repeat(3,1fr); gap:0; border-top:4px solid #D9DDE3; margin-top:10px;}
  .tline .tl{padding:22px 18px 0 0; display:flex; flex-direction:column; gap:8px; position:relative;}
  .tline .tl::before{content:""; position:absolute; top:-12px; left:0; width:20px; height:20px; border-radius:50%; background:#1F3A5F;}
  .tline .tl b{font-size:26px; color:#16233A;} .tline .tl span{font-size:18px; color:#44506A;}
  .tline .tl.hl::before{background:#F28C28;} .tline .tl.hl b{color:#F28C28;}
  .combo{display:flex; align-items:center; justify-content:center; gap:22px; font-size:30px; font-weight:800; color:#16233A;}
  .combo span{background:#EEF1F5; border-radius:14px; padding:22px 28px; font-family:var(--mono);} .combo span.hl{background:#FFF3E6; border:2px solid #F28C28; font-family:var(--serif);}
  .combo b{color:#F28C28;}
  .tline.t4{grid-template-columns:repeat(4,1fr);}
  .labtag{background:#F28C28; color:#fff; font-size:12px; font-weight:800; border-radius:6px; padding:3px 9px; letter-spacing:0;}
  .labgrid{margin-top:14px; display:grid; grid-template-columns:1fr; grid-template-rows:auto 1fr; gap:16px; height:100%; padding-bottom:10px;}
  .labgrid .lc{background:#fff; border:1px solid #E1E5EB; border-radius:12px; padding:18px 22px;}
  .labgrid .lh{font-size:13px; font-weight:800; color:#F28C28; margin-bottom:8px;}
  .labgrid .goal p{margin:0; font-size:22px; font-weight:800; color:#16233A;}
  .labgrid .lf{margin-top:8px; font-size:15px; color:#8A94A6;} .labgrid .lf .dl{font-size:15px; text-decoration:underline;}
  .labgrid .time{grid-row:1 / span 2; grid-column:2; background:#1F3A5F; border:none; color:#fff; display:flex; flex-direction:column; justify-content:center; align-items:center;}
  .labgrid .time .lh{color:#F5B06A;} .labgrid .time b{font-size:64px; line-height:1;} .labgrid .time span{font-size:18px; opacity:.8;}
  .labgrid .steps, .labgrid .done{grid-column:1;}
  .labgrid .lc ol, .labgrid .lc ul{margin:0; padding-left:22px; display:flex; flex-direction:column; gap:6px; font-size:17px; color:#16233A;}
  .labgrid{grid-template-rows:auto auto auto;} .labgrid .time{grid-row:1 / span 3;}
  .hn{display:flex; justify-content:center;}
  .hn-out{position:relative; border:3px solid #1F3A5F; border-radius:22px; padding:44px 50px 30px; display:flex; flex-direction:column; align-items:center; gap:18px; min-width:620px;}
  .hn-lab{position:absolute; top:-16px; left:30px; background:#fff; padding:0 12px; font-size:20px; font-weight:800; color:#1F3A5F;}
  .hn-row{display:flex; gap:18px;} .hn-row span{background:#EEF1F5; border-radius:10px; padding:12px 22px; font-size:18px; font-weight:700; color:#16233A;}
  .hn-row span.hl{background:#FFF3E6; border:2px solid #F28C28; color:#F28C28;}
  .hn-core{width:150px; height:150px; border-radius:50%; background:#1F3A5F; color:#fff; display:grid; place-items:center; font-size:26px; font-weight:800;}
  .vl p{font-size:20px; color:#16233A; margin:0 0 12px; padding-left:16px; border-left:4px solid #F28C28;}

  /* ── 어두운 정리 장 ── */
  .bridge{justify-content:center;}
  .bridge h2{font-size:44px; max-width:24ch; word-break:keep-all;}
  .dk h2, .s-title{word-break:keep-all;}
  .bridge .q{margin-top:30px; font-size:22px; color:rgba(255,255,255,.85); border-left:4px solid #F28C28; padding:6px 0 6px 18px;}
  .bridge .nxt{margin-top:26px; font-size:16px; color:#F28C28; font-weight:700;}
  .divider .sub{font-size:20px; color:rgba(255,255,255,.7); margin-top:16px;}
  .eco .node{width:340px;}
  .eco .nm{font-size:13px;}
'''
