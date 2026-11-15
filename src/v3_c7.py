"""3-7 검증 루프 (25분) — 배경 → 비유 → 루프 애니메이션 → 검증 기준 → Sub Agent 검토자 → 실습.

레퍼런스
- Claude Code 「Best practices」 · Give Claude a check to run — https://code.claude.com/docs/en/best-practices
  (일이 끝나 보이면 멈춤 · 통과/실패로 답하는 확인 · 확인의 강도 4단계 · 증거 요구 · 찾으라고 하면 뭐든 찾음)
- Claude Code 「Subagents」 — https://code.claude.com/docs/en/sub-agents
  (자기 컨텍스트 · 도구 제한 · 요약만 돌아옴 · name · description 필수 · .claude/agents/ · ~/.claude/agents/)
"""
import viz2
from anim import BG, G, K, N, O, OK, R, S, W, _D, _box, _flow, _path_dot, _t
from deck import divider, flow, lab, light
from hx import code, esc, table
from v3kit import phmap, F, brief, note

T = "3-7"
BP = "Claude Code 문서 「Best practices」 · Give Claude a check to run"
SA = "Claude Code 문서 「Subagents」"


def _twocol(left, right):
    return f'<div class="twocol">{left}<div>{right}</div></div>'


# ── 애니메이션 · 검증 루프 ───────────────────────────
def verify_loop():
    """정리 → 검토(체크리스트 대조) → 통과? → 아니오면 문제 줄 + 근거를 돌려보내 고침 → 다시 검토 → 예면 저장. 16초 · 한 번.
    참고: Claude Code 「How Claude Code works」(gather → act → verify) · 「Best practices」(통과/실패로 답하는 확인 · 새 컨텍스트 검토자)."""
    d = _D("vl", 16)
    MO = "#FFF3E6"
    s = ""
    # 원본
    s += (f'<g {d.show(1)}>' + "".join(f'<rect x="{30 + k * 8}" y="{252 - k * 8}" width="130" height="92" rx="8" fill="{W}" stroke="{G}" stroke-width="2"/>' for k in range(3))
          + _t(111, 290, "원본/", "tt") + _t(111, 314, "회의록 3개", "ts") + "</g>")
    s += f'<g {d.show(2)}><path d="M100 236 V120 H194" fill="none" stroke="{G}" stroke-width="3" stroke-dasharray="6 5" marker-end="url(#{d.id("k")})"/></g>'
    # 정리 Agent
    s += (f'<g {d.show(3)}><rect x="200" y="60" width="240" height="120" rx="16" fill="{K}"/>' + _t(320, 102, "정리", "tw", extra='style="font-size:21px"')
          + _t(320, 130, "out/11-10_정리.md", "tw", extra='style="font-weight:500;fill:#C9D3E0;font-size:14px;font-family:var(--mono,monospace)"') + "</g>")
    s += f'<g {d.show(6)}><path d="M444 120 H560" stroke="{K}" stroke-width="3.5" marker-end="url(#{d.id("k")})"/>' + _t(502, 104, "결과", "ts", extra='style="font-size:14px"') + "</g>"
    # 검토
    s += (f'<g {d.show(8)}><rect x="566" y="40" width="280" height="160" rx="16" fill="{MO}" stroke="{O}" stroke-width="3"/>'
          + _t(706, 92, "검토", "tt", extra='style="font-size:22px"') + _t(706, 122, "새 컨텍스트 · 원본과 대조", "ts") + _t(706, 148, "고치지 않고 돌려보냄", "ts") + "</g>")
    # 체크리스트
    items = ["원본의 할 일 모두 있음", "담당 · 근거 줄 있음", "원본에 없는 기한 없음", "개인정보 없음"]
    s += (f'<g {d.show(10)}><rect x="880" y="30" width="262" height="190" rx="14" fill="{W}" stroke="{N}" stroke-width="2"/>'
          + _t(900, 56, "체크리스트", "tn", "start") + "".join(_t(900, 92 + i * 34, x, "ts", "start", 'style="font-size:14px;fill:#16233A"') for i, x in enumerate(items)) + "</g>")
    s += f'<g {d.show(10)}><path d="M850 120 H876" stroke="{N}" stroke-width="2" stroke-dasharray="4 4"/></g>'
    # 통과?
    s += f'<g {d.show(12)}><path d="M706 204 V244" stroke="{O}" stroke-width="3.5" marker-end="url(#{d.id("o")})"/></g>'
    DM = "M706 250 L782 292 L706 334 L630 292 Z"
    s += f'<g {d.show(12)}><path d="{DM}" fill="{W}" stroke="{O}" stroke-width="3"/>' + _t(706, 293, "통과?", "tn", extra='style="font-size:16px"') + "</g>"
    s += (f'<g {d.show(14)}><path d="M630 292 H320 V186" fill="none" stroke="{R}" stroke-width="3.5" marker-end="url(#{d.id("r")})"/>'
          + _t(476, 278, "아니오 · 문제 줄 + 근거", "tn", extra=f'style="fill:{R};font-size:15px"') + "</g>")
    s += (f'<g {d.show(16)}><path d="M782 292 H900" stroke="{OK}" stroke-width="3.5" marker-end="url(#{d.id("g")})"/>' + _t(840, 278, "예", "tn", extra=f'style="fill:{OK}"')
          + f'<rect x="906" y="258" width="236" height="68" rx="14" fill="{W}" stroke="{N}" stroke-width="2.5"/>' + _t(1024, 292, "저장 · 공유 초안", "tt", extra='style="font-size:18px"') + "</g>")

    def mark(i, ok, t, end=None):
        y = 92 + i * 34
        c = OK if ok else R
        sym = (f'<path d="M1110 {y} l5 6 l10 -12" fill="none" stroke="{c}" stroke-width="3.5"/>' if ok
               else f'<path d="M1110 {y - 6} l12 12 M1122 {y - 6} l-12 12" stroke="{c}" stroke-width="3.5"/>')
        return f'<g {d.show(t, end)}><circle cx="1116" cy="{y}" r="12" fill="{"#E8F5E9" if ok else "#FDECEA"}"/>{sym}</g>'

    # 1회차 — 기한 하나를 지어냄
    s += _path_dot(d, [(444, 120), (560, 120)], 22, 26, O, 10)
    for i, ok in enumerate((True, True, False, True)):
        s += mark(i, ok, 28 + i * 2, 56)
    s += f'<path d="{DM}" fill="{R}" fill-opacity=".18" {d.show(37, 44)}/>'
    s += _path_dot(d, [(630, 292), (320, 292), (320, 186)], 40, 48, R, 10)
    s += (f'<g {d.show(42, 70)}><rect x="330" y="314" width="300" height="34" rx="8" fill="#FDECEA" stroke="{R}" stroke-width="2"/>'
          + _t(480, 331, "2행 기한 「11/14」 · 원본에 없음", "tn", extra=f'style="fill:{R};font-size:14px"') + "</g>")
    s += (f'<g {d.show(50)}><rect x="216" y="146" width="208" height="26" rx="7" fill="#2C4C75"/>'
          + _t(320, 159, "2행 → 「기한 미정」", "tw", extra='style="font-size:13px"') + "</g>")
    # 2회차 — 통과
    s += _path_dot(d, [(444, 120), (560, 120)], 58, 62, O, 10)
    for i in range(4):
        s += mark(i, True, 64 + i * 1.5)
    s += f'<path d="{DM}" fill="{OK}" fill-opacity=".18" {d.show(72)}/>'
    s += _path_dot(d, [(782, 292), (900, 292)], 75, 80, OK, 10)
    s += (f'<g {d.show(82)}><rect x="906" y="258" width="236" height="68" rx="14" fill="#E8F5E9" stroke="{OK}" stroke-width="3"/>'
          + _t(1024, 292, "저장 · 공유 초안", "tt", extra=f'style="fill:{OK};font-size:18px"') + "</g>")
    s += f'<g {d.show(86)}>' + _t(1024, 352, "발송은 사람이 확인 후", "ts") + _t(706, 392, "통과할 때까지 정리 → 검토를 반복", "tn", extra='style="font-size:16px"') + "</g>"
    return d.svg(1160, 410, s)


def slides():
    rows_ans = [
        ("보안팀 미팅 잡기", "이준호", "기한 미정", "「언제까지인지 정하지 않음」"),
        ("비밀번호 재설정 메일 수정 배포", "확인 필요", "11/12", "「11/12 수정 배포 예정」"),
    ]
    checklist = ("- [ ] 원본의 할 일이 표에 모두 있다\n"
                 "- [ ] 할 일마다 담당 · 기한 · 근거 한 줄이 있다\n"
                 "- [ ] 원본에 없는 기한이 없다 (없으면 「기한 미정」)\n"
                 "- [ ] 고객 명단 · 연락처가 결과에 없다\n"
                 "- [ ] 슬랙 초안은 세 줄 · 발송하지 않았다")
    check_out = ("$ python check.py out/2026-11-10_정리.md\n"
                 "PASS  할 일 표 형식 (5칸)\n"
                 "PASS  근거 칸 비어 있지 않음\n"
                 "FAIL  2행 기한 「11/14」 — 원본에 없는 날짜\n"
                 "통과 2 · 실패 1")
    # solution/dot_claude/agents/notes-checker.md 를 화면용으로 줄임 (10줄)
    agent_md = ("---\nname: notes-checker\ndescription: 회의록 정리 결과를 원본과 대조해\n"
                "  빠진 할 일 · 지어낸 기한을 찾는다\ntools: Read, Grep, Glob\n---\n"
                "너는 검토 담당이다. 정리와 원본을 나란히 읽는다.\n"
                "- 빠진 할 일 · 다른 담당 · 원본에 없는 기한\n- 결과에 들어간 개인정보\n"
                "찾은 것마다 줄 + 근거 · 파일은 고치지 않는다.")

    return [divider("07", "검증 루프", "")] + [
        # 배경
        light("완료처럼 보이는 결과", viz2.pair(
            "정리 결과 예", [("보안팀 미팅 잡기", "담당 이준호 · 기한 11/14"), ("인증 방식 변경", "결정으로 분류"), ("Claude의 마지막 말", "「정리 완료」")],
            "원본 11/10 대조", [("보안팀 미팅", "「언제까지인지 정하지 않음」"), ("인증 방식 변경", "「검토 제안」 · 결정 아님"), ("대조한 사람", "없음 · 그대로 공유")], hl="r")
              + note("공식 문서", "Claude는 일이 끝나 보이면 멈춘다 · 확인할 수단이 없으면 「끝나 보임」이 기준"), T),
        light("사람이 하는 확인", viz2.tiles([
            ("원본을 다시 읽음", "정리할 때마다 회의록 3개를 처음부터"), ("눈에 띌 때까지 남음", "지어낸 기한이 그대로 공유됨"),
            ("사람이 테스트", "실수를 잡는 장치가 사람 눈 하나")], 3)
              + code("원본/2026-11-10_주간회의.md · 정리할 때마다 다시 읽는 원문", esc(
                  "- 준호: 단계별 이탈 수치 공유. 휴대폰 인증에서 42% 이탈. 인증 방식 변경 검토 제안.\n"
                  "- 하늘: 인증 변경은 보안팀 의견 먼저 들어 보자고 함. 준호님이 보안팀 미팅 잡기로. (언제까지인지 정하지 않음)\n"
                  "- 민재: 비밀번호 재설정 메일 건, 정우님 확인 결과 메일 발송 서버 설정 문제였음. 11/12 수정 배포 예정."))
              + note("공식 문서", "확인 수단이 없으면 사람이 테스트 역할 · 실수는 누가 볼 때까지 남는다"), T),
        light("기자와 데스크 비유", phmap("copy_desk.webp", "신문사 데스크 (1942)", "사진 · Marjory Collins (미 의회도서관) · 퍼블릭 도메인", "https://commons.wikimedia.org/wiki/File:Financial_desk_copy_reader_on_the_New_York_Times_newspaper_8d22687v.jpg", viz2.maprows([
            ("기자가 쓴 기사", "정리 결과", "out/11-10_정리.md"), ("취재 원본", "원본 회의록", "원본/ 3개"),
            ("데스크의 확인 항목", "검증 기준", "체크리스트 · 정답 예시 · 자동 테스트"), ("데스크", "검토 Agent", "기사를 쓰지 않은 사람"),
            ("「이 숫자 출처는?」 반려", "문제 줄 + 근거를 돌려보냄", "고치는 건 기자")], "신문사", "검증 루프")), T),
        light("검증 루프", verify_loop() + note("참고", "Claude Code 문서 「How Claude Code works」 · 「Best practices」 — 통과 · 실패로 답하는 확인"), T),
        light("통과 · 실패로 답하는 확인", viz2.pair(
            "답이 흐린 확인", [("「잘 정리됐나」", "매번 다른 답"), ("「빠진 거 없나」", "무엇과 비교할지 없음")],
            "통과 · 실패가 나오는 확인", [("「할 일마다 근거 줄이 있나」", "있음 · 없음"), ("「원본에 없는 날짜가 있나」", "원문 대조로 판정")], hl="r")
              + note("공식 문서", "통과 · 실패가 돌아오는 확인이 있으면 Claude가 스스로 루프를 닫는다"), T),
        # 검증 기준
        light("검증 기준 세 가지", viz2.tiles([
            ("체크리스트", "예 · 아니오로 답할 문장 목록"), ("정답 예시", "좋은 결과 한 개와 나란히 비교"), ("자동 테스트", "스크립트가 매번 같은 판정")], 3)
              + table(["기준", "회의록 업무의 예", "판정하는 쪽"], [
                  ("체크리스트", "「원본에 없는 기한이 없다」", "검토 Agent가 원문과 대조"),
                  ("정답 예시", "11/10 정답 두 행 · 보안팀 미팅은 「기한 미정」", "정리 결과와 나란히 비교"),
                  ("자동 테스트", "할 일 표 5칸 · 근거 칸이 비지 않음", "스크립트 · 매번 같은 판정")]), T),
        light("체크리스트 예", code("검토 기준.md", esc(checklist))
              + note("쓰는 법", "「잘했나」 대신 원본과 대조해 예 · 아니오가 나오는 문장"), T),
        light("정답 예시 · 11/10", table(["할 일", "담당", "기한", "근거"], rows_ans)
              + note("모르는 칸", "원본에 없으면 「기한 미정」 · 「확인 필요」 · 채워 넣지 않기"), T),
        light("자동 테스트 예", code("터미널 · 예", esc(check_out))
              + note("나눠 맡기", "판정 기준은 사람이 · 스크립트는 Claude가 작성"), T),
        light("확인의 강도", flow([("요청에 넣기", "「끝나면 원본과 대조」"), ("목표 조건", "/goal · 다른 모델이 매 턴 확인"),
                                  ("Stop Hook", "통과 전엔 끝내지 못함"), ("다른 검토자", "새 컨텍스트의 Sub Agent")], hl=3)
              + table(["강도", "회의록 업무에서"], [
                  ("요청에 넣기", "「정리 끝나면 원본과 대조해 빠진 할 일을 보고해 줘」"),
                  ("Stop Hook", "근거 칸이 빈 줄이 있으면 응답을 끝내지 못하게"),
                  ("다른 검토자", "notes-checker 가 원본 3개와 정리 파일만 읽고 판정")])
              + note("공식 문서", BP), T),
        light("결과 대신 증거", viz2.pair(
            "말만 있는 보고", [("「검토 완료」", "무엇을 봤는지 없음"), ("「문제 없음」", "다시 확인할 방법 없음")],
            "증거가 있는 보고", [("「할 일 4건 대조」", "본 범위가 보임"), ("「2행 기한 · 원본에 없음」", "원문 한 줄과 함께")], hl="r")
              + code("검토 보고 · 예", esc(
                  "대조 범위: 원본 11/10 · out/2026-11-10_정리.md 할 일 4건\n"
                  "2행 보안팀 미팅 · 기한 「11/14」 — 원본: 「언제까지인지 정하지 않음」\n"
                  "나머지 3건: 담당 · 기한 · 근거가 원문과 같음"))
              + note("공식 문서", "실행한 확인과 그 출력을 함께 받기"), T),
        # Sub Agent
        light("스스로 확인의 한계", viz2.pair(
            "같은 대화에서 확인", [("정리할 때의 추측", "그대로 믿고 넘어감"), ("긴 대화", "원본 대신 기억으로 비교")],
            "새 컨텍스트에서 확인", [("원본 + 결과만", "정리 과정은 모름"), ("추측에 끌리지 않음", "원문과 줄 단위 대조")], hl="r")
              + note("공식 문서", "새 Sub Agent의 리뷰는 결과를 만든 추론에 흔들리지 않는다"), T),
        light("단일 Agent의 한계와 해소", viz2.single_to_multi([
            ("컨텍스트 과부하", "읽기 · 정리 · 검토가 한 대화에", "역할마다 따로 컨텍스트", "검토 Agent는 원본과 결과만"),
            ("자기 검증", "자기 결과를 자기가 확인 → 놓침", "검토 Agent가 따로 확인", "만든 Agent ≠ 확인하는 Agent"),
            ("순차 처리", "회의록 여러 개를 하나씩", "독립 작업은 동시에", "메인 Agent가 나눠 맡김")]), T),
        light("Sub Agent", viz2.tiles([
            ("자기 컨텍스트", "메인 대화와 따로 읽고 일함"), ("자기 지시문", "역할 · 기준을 적은 파일"),
            ("쓸 수 있는 도구", "읽기만 · 쓰기 막기 등 제한"), ("요약만 돌아옴", "많이 읽어도 메인엔 결과만")], 4)
              + table(["", "메인 대화", "notes-checker"], [
                  ("읽은 것", "요청 · 정리 과정 · 대화 전부", "원본 3개 + 정리 파일"),
                  ("도구", "전부", "Read · Grep · Glob"),
                  ("메인에 남는 것", "—", "문제 줄 · 원문 근거 요약")])
              + note("공식 문서", SA + " — 자기 컨텍스트 · 지시문 · 도구 · 권한을 따로 가진 보조 Agent"), T),
        light("Sub Agent의 흐름", viz2.subagent_flow(ask="「회의록 정리하고 검토해 줘」", name="notes-checker",
                                                  files=("11-03 주간회의", "11-05 프로모션", "11-10 주간회의", "out/정리.md"), back="빠진 할 일 · 근거 줄")
              + note("정리", "검토는 새 컨텍스트에서 원본과 대조 · 메인은 결과만 받음"), T),
        light("Sub Agent 정의 파일", _twocol(code(".claude/agents/notes-checker.md · 줄임", esc(agent_md)), viz2.tiles([
            ("name", "부를 때 쓰는 이름 · 필수"), ("description", "언제 맡길지 · 이 문장으로 Claude가 고름 · 필수"),
            ("tools", "쓸 수 있는 도구 · 생략하면 전부"), ("본문", "검토 기준 · 돌려줄 형식")], 1)), T),
        light("Sub Agent 저장 위치", viz2.tiles([
            (".claude/agents/", "이 프로젝트 · 팀과 공유"), ("~/.claude/agents/", "내 모든 프로젝트"),
            ("이름이 같으면", "프로젝트 쪽이 먼저")], 3)
              + code("실습 폴더", esc(
                  "meeting_agent/\n"
                  "├── CLAUDE.md\n"
                  "└── .claude/\n"
                  "    ├── skills/meeting-notes/SKILL.md\n"
                  "    └── agents/\n"
                  "        └── notes-checker.md      ← 이 프로젝트의 검토 Agent"))
              + note("부르는 법", "「notes-checker로 검토해 줘」처럼 이름을 말하거나 @멘션 · description이 맞으면 Claude가 알아서 맡김"), T),
        light("검토 Agent 설계", viz2.tiles([
            ("고치지 않음", "도구는 Read · Grep · Glob · 수정은 정리 쪽"), ("범위를 좁힘", "빠진 할 일 · 기한 · 개인정보만 · 문체 제외"),
            ("근거와 함께", "문제 줄 + 원문 한 줄 · 없으면 「검토 통과」")], 3)
              + code("notes-checker.md 에서 그 자리", esc(
                  "tools: Read, Grep, Glob                                  ← 고치지 않음\n"
                  "- 원본에 있는데 정리에 빠진 할 일                         ← 범위를 좁힘\n"
                  "- 담당자 · 기한이 원본과 다른 것 · 원본에 없는 기한\n"
                  "- 개인정보 · 외부 전달 금지 내용이 결과에 들어간 것\n"
                  "찾은 것마다 정리 파일 줄 · 원본 근거 한 줄. 없으면 「검토 통과」  ← 근거와 함께"))
              + note("공식 문서", "문제를 찾으라고 하면 무엇이든 찾음 · 볼 범위를 정해 두기"), T),
        # 실습
        lab("3-7", "검토 Agent 분리", T, "정리하는 Agent와 검토하는 Agent를 나눠 원본과 대조",
            ["검토 기준 3개 정하기", "검토 Sub Agent 요청", "정리 + 검토 요청", "검토 결과 반영"],
            ["<code>.claude/agents/notes-checker.md</code>", "검토가 잡은 것"], files=F, mine="내 업무 결과를 확인할 기준 하나"),
        brief("3-7", T,
              ["검토 기준 3개를 내가 정하기", "Sub Agent 요청 쓰기", "11/5 · 11/10 정리 + 검토 요청", "검토가 잡은 것 반영"],
              [("역할", "검토만 · 고치지 않음"), ("입력", "원본 회의록 + 정리 결과"), ("검토 기준", "내가 정한 3개"), ("돌려줄 것", "문제 줄 · 원문 근거")],
              ["Sub Agent", "읽기 도구만", "원본 대조", "notes-checker"],
              ["검토 Agent가 따로 돎", "원본에 없는 기한을 잡는가", "고객 명단이 결과에 없는가", "메인은 결과만 받음"],
              "<code>solution/dot_claude/agents/notes-checker.md</code>"),
        light("검토가 잡아야 할 것", table(["원본", "원문", "정리에서 생기기 쉬운 실수"], [
            ("11/10", "「언제까지인지 정하지 않음」", "보안팀 미팅에 기한을 채움"),
            ("11/5", "「외부 전달 금지」", "고객 명단 내용을 결과에 옮김"),
            ("11/5", "「11/12까지 전달 예정」", "에이전시 모바일 3종이 표에서 빠짐")])
              + note("확인", "검토 Agent가 세 줄을 원문과 함께 돌려주는지 · 없으면 「검토 통과」"), T),
        light("통과까지 반복", flow([("정리", "out/ 에 저장"), ("검토", "notes-checker"), ("문제 줄", "원문 근거와 함께"),
                                  ("고치기", "정리 쪽이 수정"), ("검토 통과", "공유 초안 확인")], hl=1)
              + code("11/10 정리 · 검토 기록 예", esc(
                  "1회차  검토: 2행 보안팀 미팅 기한 「11/14」 — 원본에 없음\n"
                  "       정리: 2행 기한 → 「기한 미정」\n"
                  "2회차  검토: 검토 통과 → 공유 초안을 사람이 확인"))
              + note("같은 지적이 반복되면", "Skill · CLAUDE.md 에 규칙으로 반영"), T),
    ]
