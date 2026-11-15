"""vibe3 3-8 마무리 · 운영하며 키우기 (10분).

앞 차시(3-3 ~ 3-7)가 만든 파일을 모아 완성 에이전트로 보여 주고, 결과 → 사람의 수정 요청 → 하네스 반영 루프로 닫는다.
파일 내용은 labs/meeting_agent/solution 에서 그대로 읽는다.
"""
import anim
import viz2
from anim import BG, G, K, N, O, OK, S, W, _D, _path_dot, _t
from deck import divider, flow, light
from hx import code, esc, note
from v3kit import pick

T = "3-8"


def run_anim():
    """요청 한 줄이 하네스 부품을 차례로 지나는 모습. 12초 · 한 번. 접두어 fin."""
    d = _D("fin", 12)
    MO = "#FFF3E6"
    steps = [("규칙 읽기", "원본은 읽기만", "CLAUDE.md", "3-4"), ("절차 고르기", "meeting-notes", "Skill", "3-5"),
             ("회의록 읽기", "notion-fetch", "노션 MCP", "3-3"), ("결과 저장", "out/ · Hook 통과", "Hook", "3-6"),
             ("검토", "원본과 대조", "검토 Agent", "3-7"), ("확인 · 발송", "슬랙 초안 → 사람", "사람", "")]
    s = (f'<g {d.show(1)}><rect x="330" y="8" width="500" height="44" rx="22" fill="{N}"/>'
         + _t(580, 31, "「11/10 회의록 정리하고 검토까지 해 줘」", "tw", extra='style="font-size:16px"') + "</g>")
    xs = [8 + i * 192 for i in range(6)]
    for i, (h, sub, part, ch) in enumerate(steps):
        x = xs[i]
        t0 = 8 + i * 13
        hu = i == 5
        s += (f'<g {d.show(3 + i * 2)}><rect x="{x}" y="86" width="168" height="34" rx="10" fill="{O if hu else K}"/>'
              + _t(x + 84, 104, part, "tw", extra='style="font-size:14.5px"') + "</g>")
        s += (f'<g {d.show(3 + i * 2)}><rect x="{x}" y="136" width="168" height="120" rx="14" fill="{W}" stroke="{G}" stroke-width="2.5"/>'
              + _t(x + 84, 182, h, "tt", extra='style="font-size:18px"') + _t(x + 84, 212, sub, "ts", extra='style="font-size:13.5px"') + "</g>")
        if ch:
            s += f'<g {d.show(3 + i * 2)}>' + _t(x + 84, 276, ch, "tn", extra=f'style="fill:{S};font-size:13px"') + "</g>"
        # 점이 닿으면 칸이 켜짐
        s += (f'<rect x="{x}" y="136" width="168" height="120" rx="14" fill="{MO}" fill-opacity=".6" stroke="{O}" stroke-width="3.5" '
              + d.a([(0, "opacity:0"), (t0 + 13, "opacity:0"), (t0 + 15, "opacity:1"), (100, "opacity:1")]) + "/>")
        s += f'<g {d.show(t0 + 15)}>' + _t(x + 84, 182, h, "tt", extra='style="font-size:18px"') + _t(x + 84, 212, sub, "ts", extra='style="font-size:13.5px"') + "</g>"
        if i < 5:
            s += f'<path d="M{x + 170} 196 H{x + 188}" stroke="{G}" stroke-width="3" marker-end="url(#{d.id("k")})" {d.show(4 + i * 2)}/>'
    s += _path_dot(d, [(580, 52), (580, 66), (92, 66), (92, 196)], 14, 20, O, 10)
    s += _path_dot(d, [(92, 196), (xs[5] + 84, 196)], 20, 88, O, 10)
    s += (f'<g {d.show(90)}><rect x="250" y="310" width="660" height="56" rx="14" fill="#E8F5E9" stroke="{OK}" stroke-width="3"/>'
          + _t(580, 339, "out/2026-11-10_정리.md · 슬랙 초안 3줄 · 발송은 사람", "tt", extra=f'style="fill:{OK};font-size:18px"') + "</g>")
    return d.svg(1160, 380, s)


def _ba(title, ch, before, after, nlabel, ntext):
    """Before → After 두 칸 + 일반 메모 (deck.ba 의 메모는 「구성」 라벨이 고정이라 따로)."""
    b, a = before.replace("\n", "<br/>"), after.replace("\n", "<br/>")
    return light(title, f'<div class="ba"><div class="b"><div class="lab">Before</div><div class="q">{b}</div></div>'
                 f'<div class="arr">→</div><div class="a"><div class="lab">After</div><div class="q">{a}</div></div></div>'
                 + note(nlabel, ntext), ch)


def slides():
    t = T
    tree = ("meeting_agent/\n"
            "├── CLAUDE.md                          공통 원칙   3-4\n"
            "├── .claude/\n"
            "│   ├── skills/meeting-notes/SKILL.md  정리 절차   3-5\n"
            "│   ├── settings.json · hooks/guard.py 원본 보호   3-6\n"
            "│   └── agents/notes-checker.md        검토        3-7\n"
            "├── 원본/                              회의록 3개\n"
            "└── out/                               정리 결과\n"
            "\n+ 연결: 노션 MCP                       회의록 읽기 3-3")
    out_md = ("# 11/10 주간 회의 정리\n"
              "결정 2 · 할 일 2 · 기한 미정 1\n"
              "| 할 일 | 담당 | 기한 | 상태 | 근거 |\n"
              "| 보안팀 미팅 잡기 | 이준호 | 기한 미정 | 진행 | 「준호님이 보안팀 미팅 잡기로」 |\n"
              "| 메일 서버 설정 수정 배포 | 정우 | 11/12 | 진행 | 「11/12 수정 배포 예정」 |\n"
              "지난 할 일(11/3) — 이탈 수치 정리 완료 · 메일 건 진행 · 배너 확인 필요\n"
              "슬랙 초안\n"
              "· 「첫 달 무료」 법무 검토 완료 · 그대로 사용\n"
              "· 휴대폰 인증 42% 이탈 → 보안팀 의견 먼저\n"
              "· 메일 발송 서버 문제 11/12 수정 배포")
    return [divider("08", "운영하며 키우기", "")] + [
        light("완성 에이전트 구성", '<div class="ctree">' + code("meeting_agent 하네스", esc(tree)) + "</div>"
              + note("같은 모델", "모델은 그대로 · 바뀐 것은 모델을 감싼 파일과 연결"), t),
        light("파일별 핵심 한 줄", viz2.maprows([
            ("CLAUDE.md", "원본은 읽기만 · 기한이 없으면 「기한 미정」", "3-4 · 지시"),
            ("skills/meeting-notes", "결정 · 할 일 · 열린 질문 → 표 · 슬랙 초안 세 줄", "3-5 · 절차"),
            ("settings.json · guard.py", "Edit · Write 직전 · 원본/ 이면 거부", "3-6 · 통제"),
            ("agents/notes-checker", "원본과 대조 · 읽기 도구만 · 고치지 않음", "3-7 · 검증"),
            ("노션 MCP", "찾기 · 읽기 도구만 · 쓰기 도구는 deny", "3-3 · 도구")], "파일", "하는 일"), t),
        light("요청 한 줄이 지나는 길", run_anim()
              + note("부품마다 한 가지", "규칙 · 절차 · 연결 · 막기 · 검토는 파일이 · 판단은 모델이 · 발송은 사람이"), t),
        light("완성 에이전트 결과 예 · 11/10", code("out/2026-11-10_정리.md · 예", esc(out_md))
              + note("근거", "표의 줄마다 원본 회의록 문장 · 기한이 없던 보안팀 미팅은 「기한 미정」"), t),
        light("사람의 하네스 갱신", flow([("Agent", "회의록 정리"), ("사람", "결과 보고 수정 요청"), ("하네스 갱신", "CLAUDE.md · Skill · Hook"),
                                        ("다음 실행", "같은 요청이 안 나옴"), ("사람", "새로운 문제만 봄")], hl=2), t),
        light("수정 요청 반영 루프", viz2.taste_loop(steps=[("① Agent가 정리", "회의록 → 할 일 표"), ("② 사람이 수정 요청", "결과를 보고 말로"),
                                                    ("③ Agent가 고침", "다시 정리"), ("④ 하네스에 반영", "CLAUDE.md · Skill · Hook")], unit="회의")
              + note("보는 것", "회의별 수정 요청 수 · 줄어드는지 확인"), t),
        light("수정 요청별 반영 위치", viz2.maprows([
            ("형식 · 문구", "Skill 예시", "「담당자를 맨 앞 열로」"), ("판단 기준", "CLAUDE.md", "「기한이 없으면 기한 미정」"),
            ("절대 안 됨", "Hook", "원본 수정 · 외부 발송"), ("다시 확인할 것", "검토 Agent", "빠진 할 일 대조")], "수정 요청", "반영 위치"), t),
        _ba("수정 요청 반영 예", t,
           "매주 같은 말 「담당자를 맨 앞 열로 해 줘」\n결과를 받을 때마다 다시 요청",
           "「방금 말한 것 Skill에 반영해 줘」 한 번\nSKILL.md 형식 줄이 | 담당 | 할 일 | 기한 | … 으로 바뀜",
           "효과", "다음 회의록부터 같은 요청이 안 나옴 · 사람은 새로 틀린 것만 봄"),
        light("하네스 변경 기록 예", code("git log --oneline -- CLAUDE.md .claude · 예", esc(
            "7d2a913 Skill: 담당자를 맨 앞 열로 (11/17 회의 수정 요청)\n"
            "4c81e0b CLAUDE.md: 금액은 원문 그대로 (11/10 회의 수정 요청)\n"
            "2f9b6d4 Hook: 원본/ 수정 차단 (실습 3-6)\n"
            "a03c5e7 Skill: meeting-notes 첫 버전 (실습 3-5)"))
              + viz2.tiles([("왜 바뀌었나", "커밋 메시지에 수정 요청 출처"), ("나빠지면", "그 커밋만 되돌리기")], 2), t),
        light("업무 루프 예시", viz2.loop_cases([
            ("주간 회의록 정리", "매주 월요일 회의 뒤", "회의록 하나씩 정리 · 검토", "모든 회의록 끝", "공유 초안 확인 · 발송"),
            ("정기 보고서", "매일 아침 8시", "데이터 모으기 · 표 · 요약", "보고서 완성", "확인 후 발송"),
            ("문의 1차 답변", "새 문의 메일", "규정 찾기 · 답변 초안", "초안 완성", "확인 후 회신"),
            ("경비 증빙 대조", "월말", "영수증 하나씩 규정과 대조", "목록 끝", "예외 건 판단"),
            ("계약서 조항 점검", "새 계약서", "조항 하나씩 기준과 비교", "조항 끝", "위험 조항 검토"),
            ("일정 취합", "매주 금요일", "팀원 일정 모으기 · 겹침 표시", "전원 취합", "일정 확정")])
              + note("공통", "목록 단위 반복 · 확인 기준 · 최종 승인은 사람"), t),
        light("내 업무에 옮기는 순서", flow([("① 업무 하나", "매주 반복 · 결과가 파일"), ("② CLAUDE.md", "판단 기준 몇 줄"),
                                          ("③ Skill", "결과를 보고 절차로"), ("④ Hook", "사고 날 곳 하나"), ("⑤ 검토 Agent", "확인 기준 세 개")], hl=0)
              + note("크게 만들지 않기", "처음엔 CLAUDE.md 한 장 · 수정 요청이 쌓일 때 부품을 더함"), t),
        pick("하네스는 사람이 키운다", t, repl=[("하네스는 사람이 키운다", "사람이 키우는 하네스")]),
    ]
