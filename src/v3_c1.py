"""3-1 하네스 엔지니어링 (30분).

에이전트 다시 보기 → 프롬프트 · 컨텍스트 · 하네스 → 하네스 개념(마구 비유 · 정의 · 부품) → 같은 모델 · 다른 하네스.
"""
import anim
import viz2
from anim import _D, _t, BG, K, N, O, S, W
from deck import ba, divider, flow, light
from hx import code, esc, note
from v3kit import pick

T = "3-1"


# ── 그림: 모델 + 하네스 = 에이전트 ─────────────────────
def anatomy():
    """가운데 모델 · 둘레에 하네스 부품이 하나씩 붙고 · 바깥 테두리가 에이전트. 10초 · 한 번.
    참고: Claude Code 「How Claude Code works」(모델을 감싼 층 = agentic harness) · IBM 「AI Model vs Agentic Harness」(모델 ⊂ 하네스 ⊂ 에이전트)."""
    d = _D("c1a", 10)
    s = (f'<g {d.show(78)}><rect x="16" y="8" width="1128" height="414" rx="22" fill="none" stroke="{N}" stroke-width="3" stroke-dasharray="9 7"/>'
         + _t(40, 34, "에이전트 = 모델 + 하네스", "tt", "start", 'style="font-size:21px"') + "</g>")
    s += (f'<g {d.show(12)}><rect x="60" y="56" width="1040" height="346" rx="18" fill="#EEF2F7" stroke="{K}" stroke-width="2.5"/>'
          + _t(1080, 80, "하네스 · 모델을 감싼 나머지 전부", "tn", "end", f'style="fill:{K}"') + "</g>")
    parts = [(110, 110, "내장 도구", "Claude Code 기본 · 읽기 · 쓰기 · 실행"), (110, 210, "지시", "CLAUDE.md · 3-4"), (110, 310, "절차", "Skill · 3-5"),
             (820, 110, "외부 도구", "MCP · 3-3"), (820, 210, "통제", "권한 · Hook · 3-6"), (820, 310, "검증", "검토 Agent · 3-7")]
    for i, (x, y, h, sub) in enumerate(parts):
        t = 22 + i * 8
        cx = x + 230 if x < 500 else x
        s += (f'<g {d.show(t)}><path d="M{cx} {y + 33} L{580 if x < 500 else 580} 230" stroke="{G_}" stroke-width="2" stroke-dasharray="5 5"/>'
              f'<rect x="{x}" y="{y}" width="230" height="66" rx="12" fill="{W}" stroke="{K}" stroke-width="2.2"/>'
              + _t(x + 115, y + 23, h, "tn", extra='style="font-size:17px"') + _t(x + 115, y + 47, sub, "ts", extra='style="font-size:13.5px"') + "</g>")
    s += (f'<g {d.show(2)}><rect x="470" y="180" width="220" height="100" rx="16" fill="#FFF3E6" stroke="{O}" stroke-width="3"/>'
          + _t(580, 218, "모델", "tt", extra='style="font-size:22px"') + _t(580, 250, "판단 · 작성", "ts") + "</g>")
    return d.svg(1160, 430, s)


G_ = "#D9DDE3"


# ── 부품 한 장 ─────────────────────────────────────────
def part(title, without, piece, example, ch, file, text):
    """없으면 생기는 일 → 부품 → 회의록 예 · 실제 파일 조각 · 다루는 차시."""
    body = flow([("없으면", without), (piece[0], piece[1]), ("회의록 예", example)], hl=1)
    body += code(file, esc(text)) + note("다루는 차시", ch)
    return light(title, body, T)


def slides():
    sl = [divider("01", "하네스 엔지니어링", "")]

    # A. 에이전트 다시 보기
    sl += [
        light("채팅과 에이전트", anim.chat_vs_agent()
              + note("참고", "IBM Technology 「What is OpenClaw?」 · Claude Code 문서 「How Claude Code works」 — 도구가 없으면 글로만 답함"), T),
        light("신입 인턴 비유", viz2.maprows([
            ("팀장의 지시", "사용자 요청", ""), ("다음 할 일을 머리로 정함", "모델 판단", "무엇을 먼저 볼지 · 어떤 도구를 쓸지"),
            ("컴퓨터 · 파일로 직접 처리", "하네스가 도구 실행", "찾기 · 읽기 · 저장"), ("결과를 보고 다음 할 일", "결과가 컨텍스트에 붙음", "다음 판단의 재료"),
            ("다 됐으면 보고", "도구 호출 없음 → 답", "루프 끝")], "인턴", "에이전트"), T),
        light("에이전트 루프", anim.agent_loop()
              + note("참고", "Claude Code 「How Claude Code works」 · IBM Technology 「What is OpenClaw?」 · Nate Herk 「Agent Loops Clearly Explained」"), T),
        light("Claude Code 내장 도구", viz2.tiles([
            ("파일", "읽기 · 수정 · 새로 만들기"), ("검색", "이름 · 내용으로 파일 찾기"), ("실행", "명령 · 서버 · 테스트 · git"),
            ("웹", "검색 · 문서 가져오기"), ("그 밖", "Sub Agent 호출 · 사용자에게 질문")], 5)
              + note("Claude Code 문서", "도구가 없으면 글로만 답함 · 도구 결과가 다음 판단의 재료"), T),
        pick("대화형 작업과 위임형 작업", T),
        pick("에이전트 등장 배경", T),
        pick("AI가 맡을 수 있는 작업 길이 (METR)", T),
    ]

    # B. 프롬프트 → 컨텍스트 → 하네스
    prompt = ("너는 회의록 정리 담당이다.\n"
              "아래 회의록에서 할 일만 뽑아\n"
              "담당 · 기한 · 할 일 표로 정리해 줘.\n\n"
              "(회의록 본문을 여기에 붙여 넣기)")
    sl += [
        light("프롬프트 엔지니어링", code("채팅창에 보내는 요청 한 번", esc(prompt))
              + note("손대는 곳", "질문 문장 · 역할 · 형식 · 효과는 이번 답 한 번"), T),
        light("프롬프트만의 한계", viz2.tiles([
            ("매번 붙여 넣기", "회의록을 열어 복사 · 대화창에 붙임"), ("매번 같은 설명", "형식 · 규칙을 대화마다 다시"),
            ("손이 없음", "파일 저장 · 폴더 정리는 사람이")], 3)
              + note("그래서", "보여 줄 자료를 미리 골라 둠 → 컨텍스트 엔지니어링"), T),
        light("컨텍스트 엔지니어링", viz2.pair(
            "보여 줄 것", [("원본 회의록", "11/3 · 11/5 · 11/10"), ("규칙 메모", "「기한이 없으면 기한 미정」"), ("지난 결과", "11/3 할 일 표")],
            "뺄 것", [("관계없는 회의록", "다른 팀 · 지난달"), ("긴 메일 묶음", "할 일과 무관한 공지")], hl="l")
              + note("손대는 곳", "모델이 읽는 자료 · 무엇을 넣고 무엇을 뺄지"), T),
        light("컨텍스트만의 한계", viz2.tiles([
            ("지키는지 모름", "규칙을 보여 줘도 놓칠 수 있음"), ("위험한 실행", "원본 수정 · 슬랙 발송을 못 막음"),
            ("확인 없음", "빠진 할 일을 아무도 모름")], 3)
              + note("그래서", "도구 · 통제 · 확인까지 일하는 환경 전체를 설계 → 하네스 엔지니어링"), T),
        light("하네스 엔지니어링", flow([("프롬프트", "요청 한 번"), ("컨텍스트", "보여 줄 자료"), ("하네스", "도구 · 권한 · 절차 · 확인까지")], hl=2)
              + viz2.tiles([("도구", "회의록을 직접 읽고 저장"), ("통제", "원본 수정 · 발송은 막음"), ("확인", "원본과 대조 후 내보냄")], 3), T),
        pick("채팅 → 에이전트 → 하네스", T),
        pick("프롬프트 · 컨텍스트 · 하네스 선택 기준", T),
    ]

    # C. 하네스 개념 — 배경 → 비유 → 정의 → 부품
    sl += [
        pick("Harness = 마구(馬具)", T),
        pick("마구와 하네스 부품", T, drop_notes=True),
        light("모델과 하네스", anatomy()
              + note("참고", "Claude Code 「How Claude Code works」 · IBM Technology 「AI Model vs Agentic Harness」 · 부품은 업무마다 골라 씀"), T),
        light("Claude Code = 기본 하네스", viz2.pair(
            "처음부터 있는 것", [("내장 도구", "파일 · 검색 · 실행 · 웹"), ("컨텍스트 관리", "한도 근처에서 자동 요약"), ("권한 모드", "수정 · 명령 전 확인")],
            "내가 더하는 것", [("CLAUDE.md · Skill", "지시 · 절차"), ("MCP", "노션 · 슬랙 · 드라이브"), ("Hook · Sub Agent", "강제 규칙 · 검토")])
              + note("Claude Code 문서", "Skill · MCP · Hook · Sub Agent = 기본 루프 위에 얹는 층"), T),
        pick("신입사원 온보딩과의 비교", T, repl=[("평가셋", "검토 Agent")]),
        part("지시 · CLAUDE.md", "기한을 지어냄 · 형식이 매번 다름", ("CLAUDE.md", "대화마다 먼저 읽는 규칙"),
             "「기한이 없으면 기한 미정 · 지어내지 않는다」", "3-4",
             "CLAUDE.md", "- 원본: `원본/` · 읽기만 한다. 결과는 `out/` 에 파일로\n- 할 일은 담당자 · 기한 · 근거(원문 한 줄)를 함께 · 기한이 없으면 「기한 미정」"),
        part("외부 도구 · MCP", "노션 회의록을 사람이 복사", ("MCP", "노션 · 슬랙을 표준 방식으로 연결"),
             "노션 회의록 페이지를 직접 찾아 읽음", "3-3",
             "연결하면 Claude가 받는 도구 이름 예", "notion-search    페이지 찾기\nnotion-fetch     페이지 읽기"),
        part("절차 · Skill", "단계를 건너뜀 · 매번 같은 설명", ("Skill", "필요할 때 꺼내 쓰는 업무 절차"),
             "결정 · 할 일 · 열린 질문 → out/ 저장", "3-5",
             ".claude/skills/meeting-notes/SKILL.md", "---\nname: meeting-notes\ndescription: 회의록을 할 일 · 결정 · 공유 초안으로 정리할 때.\n---\n2. 세 가지로 나눈다 — 결정 · 할 일 · 열린 질문"),
        part("통제 · 권한과 Hook", "원본을 고침 · 슬랙에 바로 보냄", ("권한 · Hook", "막을 일은 코드로 매번 확인"),
             "원본/ 수정은 거부 · 이유를 Claude에게", "3-6",
             "Hook이 Claude에게 돌려주는 이유", "원본/2026-11-03_주간회의.md — 원본 회의록은 고치지 않는다 · 결과는 out/ 에"),
        part("검증 · 검토 Agent", "빠진 할 일 · 지어낸 기한을 모름", ("검토 Agent", "따로 일하는 검토 담당"),
             "정리 결과를 원본과 한 줄씩 대조", "3-7",
             ".claude/agents/notes-checker.md", "description: 회의록 정리 결과를 원본과 대조해\n  빠진 할 일 · 틀린 담당자 · 지어낸 기한을 찾는다.\ntools: Read, Grep, Glob"),
    ]

    # D. 같은 모델, 다른 하네스
    before = ("· 인증 방식 변경 검토 — 준호\n· 보안팀 미팅 — 11/14\n· 메일 서버 수정\n\n"
              "기한을 지어냄 · 담당 빠짐 · 근거 없음")
    after = ("결정 1 · 할 일 2 · 기한 미정 1\n"
             "· 보안팀 미팅 잡기 — 준호 · 기한 미정\n  근거: 「언제까지인지 정하지 않음」\n"
             "· 메일 발송 서버 수정 배포 — 11/12\n  근거: 「11/12 수정 배포 예정」")
    sl += [
        pick("같은 모델의 하네스별 점수", T),
        pick("같은 문제 · 하네스별 작업량", T, repl=[("남의 점수 대신 우리 과제로 직접 잰다 (Ch8)", "남의 점수 대신 내 업무로 직접 확인")]),
        pick("포켓몬 하네스 변화", T),
        pick("같은 모델 · 다른 하네스", T),
        ba("회의록 정리 · 하네스 전후 예", T, before, after, note="원본 · 11/10 주간회의 · 같은 모델 · 하네스만 다름"),
        light("하네스를 붙이는 순서", flow([("3-2 설계", "업무 쪼개기 · 설계서"), ("3-3 MCP", "노션 연결"), ("3-4 CLAUDE.md", "공통 규칙"),
                                     ("3-5 Skill", "정리 절차"), ("3-6 Hook", "원본 보호"), ("3-7 검토", "검토 Agent")], hl=0)
              + note("실습 폴더", "<code>labs/meeting_agent</code> · 하네스 없이 시작해 차시마다 하나씩"), T),
    ]
    return sl
