"""vibe3 공통 도구 — pick · brief · how_to_ask · CSS. 차시 모듈(v3_c1 … v3_c8)이 가져다 쓴다.

바이브코딩 온라인 강의 3장 — 하네스 엔지니어링 & 내 업무 에이전트 (180분).

posco-dx 덱의 장 · 그림을 그대로 꺼내 쓰고(pick), 회의록 업무에 맞춰야 하는 장만 같은 그림 함수로 새로 만든다.
공통 업무: 회의록 → 할 일 정리 → 공유 초안 (labs/meeting_agent)
"""
import re
from pathlib import Path

import anim
import hx
import mcp_fig
import viz2
from deck import divider, flow, lab, light
from hx import code, esc, labdir, note
from stats_hx import stat

F = labdir("meeting_agent")
FOLDER = "labs/meeting_agent"
SOL = Path(__file__).resolve().parent.parent / "labs" / "meeting_agent" / "solution"
_ALL = {}


def pick(title, tag, repl=(), drop_notes=False):
    """posco-dx 덱의 장을 제목으로 꺼내 차시 표시만 바꾼다 · repl 로 문구 교체 · drop_notes 로 하단 메모 삭제."""
    if not _ALL:
        for s in hx.slides():
            m = re.search(r'data-title="([^"]*)"', s)
            if m:
                _ALL.setdefault(m.group(1), s)
    s = _ALL[title]
    s = re.sub(r'(<span class="tag">)[^<]*(</span>)', rf'\g<1>{tag}\2', s, count=1)
    for a, b in repl:
        assert a in s, (title, a)
        s = s.replace(a, b)
    if drop_notes:
        s = re.sub(r'<div class="dbnote">.*?</div>', "", s, flags=re.S)
    return s


def brief(no, ch, steps, slots, keys, checks, stuck):
    """실습 진행 — 완성 요청문 대신 「요청에 들어갈 것」 · 키워드 · 확인. 요청 문장은 수강생이 쓴다."""
    st = "".join(f"<li>{x}</li>" for x in steps)
    sl = "".join(f'<div class="bs"><b>{k}</b><span>{v}</span></div>' for k, v in slots)
    kw = "".join(f"<code>{x}</code>" for x in keys)
    ck = "".join(f"<li>{x}</li>" for x in checks)
    head = (f'<div class="kithead"><span>VS Code로 열 폴더</span><code>{FOLDER}</code>'
            f'<em>요청 문장은 내가 쓴다 · 규칙도 내가 정한다</em></div>')
    body = (f'<div class="bf"><div class="bf-l"><div class="bh">요청에 들어갈 것</div>{sl}</div>'
            f'<div class="bf-r"><div class="bh">순서</div><ol>{st}</ol><div class="bh">키워드</div><div class="bk">{kw}</div></div></div>'
            f'<div class="qk2"><b>확인</b><ul>{ck}</ul></div>' + note("막히면", stuck))
    return light(f"실습 {no} 진행", head + body, ch)


def how_to_ask(ch="3-2"):
    """요청 쓰는 법 — 한 줄 요청 vs 네 칸을 채운 요청."""
    weak = ('<div class="ha weak"><div class="bh">한 줄 요청</div><p class="hq">「회의록 정리해 줘」</p>'
            '<ul><li>어느 회의록 → 추측</li><li>어떤 형식 · 어디에 저장 → 추측</li><li>기한 없는 할 일 → 지어냄</li></ul></div>')
    rows = [("목표", "11/10 회의의 할 일만"), ("입력", "원본/2026-11-10_주간회의.md"),
            ("산출물", "담당 · 기한 표 → out/"), ("하지 말 것", "원본 수정 · 없는 기한 채우기")]
    good = ('<div class="ha good"><div class="bh">네 칸을 채운 요청</div>'
            + "".join(f'<div class="bs"><b>{k}</b><span>{v}</span></div>' for k, v in rows) + "</div>")
    return light("요청 쓰는 법", f'<div class="hw">{weak}<div class="hw-a">→</div>{good}</div>'
                 + note("빈 칸", "Claude가 추측으로 채움 · 판단 기준은 사람이 정해서 넣기"), ch)


CSS = """
  /* vibe3 · 카드 · 흐름 · 전후 비교를 크게 (빈 화면 줄이기) */
  .lt .v2tile{padding:24px 26px; min-height:132px; justify-content:center; gap:10px;}
  .lt .v2tile b{font-size:25px;} .lt .v2tile span{font-size:18px; line-height:1.5;}
  .lt .v2tiles{gap:20px;}
  .lt .v2tiles.c1{gap:12px;} .lt .v2tiles.c1 .v2tile{min-height:0; padding:12px 20px; gap:4px;}
  .lt .v2tiles.c1 .v2tile b{font-size:20px;} .lt .v2tiles.c1 .v2tile span{font-size:15px;}
  .lt .flow .fs{padding:30px 16px; min-height:150px; gap:10px;}
  .lt .flow .fs b{font-size:24px;} .lt .flow .fs span{font-size:17px; line-height:1.45;}
  .lt .fa{font-size:28px; padding:0 10px;}
  .lt .ba .b, .lt .ba .a{min-height:210px; justify-content:center; padding:30px 32px;}
  .lt .ba .q{font-size:23px;}
  .lt .dbnote{font-size:17px;}
  .v3logo{display:flex; align-items:center; gap:14px; margin:0 0 16px;} .v3logo img{height:52px; width:auto;} .v3logo b{font-size:24px; color:#16233A;}
  .phmap.v3ph{grid-template-columns:400px 1fr;} .phmap.v3ph .ph img{height:330px; object-fit:cover;}
  /* vibe3 · 요청 쓰기 */
  .bf{display:grid; grid-template-columns:1.25fr 1fr; gap:18px; margin-bottom:12px;}
  .bh{font-size:14px; font-weight:900; color:#6B7785; letter-spacing:.02em; margin:0 0 8px;}
  .bs{display:grid; grid-template-columns:120px 1fr; align-items:center; gap:12px; border:1.5px solid #D9DDE3; border-left:6px solid #F28C28;
      border-radius:12px; padding:9px 16px; background:#fff; margin-bottom:8px;}
  .bs b{font-size:18px; color:#16233A;} .bs span{font-size:17px; color:#3A4657; line-height:1.35;}
  .bf-r ol{margin:0 0 14px; padding-left:24px; font-size:17px; color:#16233A; line-height:1.6; font-weight:600;}
  .bk{display:flex; flex-wrap:wrap; gap:8px;}
  .bk code{font-size:15px; background:#F4F6F9; border:1.5px solid #D9DDE3; border-radius:999px; padding:5px 13px; color:#1F3A5F; font-weight:700;}
  .hw{display:grid; grid-template-columns:1fr 60px 1.2fr; align-items:center; gap:10px; margin:6px 0 16px;}
  .hw-a{font-size:40px; color:#F28C28; text-align:center; font-weight:900;}
  .ha{border-radius:16px; padding:20px 24px; background:#fff; border:2px solid #D9DDE3;} .ha.good{border-color:#F28C28; background:#FFF8F1;}
  .hq{font-size:26px; font-weight:800; color:#16233A; margin:4px 0 14px;}
  .ha.weak ul{margin:0; padding-left:20px; font-size:17px; color:#C62828; line-height:1.7; font-weight:600;}
  .an{margin:2px 0 8px;}
"""


def phmap(img, cap, credit, url, body):
    """비유 장 — 왼쪽 실물 사진 + 오른쪽 대응표 · 출처는 오른쪽 위 (Commons · 라이선스 확인)."""
    from hx import photo
    from stats_hx import src
    return f'<div class="phmap v3ph">{photo(img, cap)}{body}</div>' + src((credit, url))


def logo(img, name, url):
    """서비스 장 머리 — 공식 로고(참조용 · Commons 퍼블릭 도메인) + 이름 · 출처는 오른쪽 위."""
    from stats_hx import src
    return f'<div class="v3logo"><img src="img/{img}" alt="{name} 로고"/><b>{name}</b></div>' + src((f"로고 · {name} · 퍼블릭 도메인 (Commons)", url))


def cover():
    return '''<section class="slide dk cover-dk active" data-title="표지">
  <div class="glow"></div>
  <div class="kick">바이브코딩 · 3</div>
  <h1>하네스 엔지니어링<br/>· 내 업무 에이전트</h1>
</section>'''


AGENDA = [("3-1", "하네스 엔지니어링", "모델을 감싸는 환경"), ("3-2", "업무 분석 · 에이전트 설계", "입력 → 판단 → 처리 → 산출물"),
          ("3-3", "MCP 연결", "노션 · 슬랙 · 드라이브"), ("3-4", "CLAUDE.md", "공통 원칙 · 위치"),
          ("3-5", "Skill 제작", "반복 업무를 지시서로"), ("3-6", "통제 · 안전장치", "권한 · Hook · 가드레일"),
          ("3-7", "검증 루프", "작업자와 검토자 분리"), ("3-8", "운영하며 키우기", "수정 요청 → 하네스")]


def agenda():
    rows = "".join(f'<div class="ch"><span class="chip">{c}</span><div class="tx"><b>{t}</b><span>{d}</span></div></div>' for c, t, d in AGENDA)
    return f'''<section class="slide dk" data-title="목차">
  <div class="coord"><b></b> / <span class="tot"></span></div>
  <h2>목차</h2>
  <div class="days two"><div class="daycol">{rows}</div></div>
</section>'''


