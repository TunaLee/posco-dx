"""3-5 Skill 제작 (35분) — 배경 → 비유 → 구조 → 호출 → 좋은 Skill 네 요소 → 실습 → 고치기.

사실 출처: code.claude.com/docs/en/skills · github.com/anthropics/skills · Anthropic 엔지니어링 블로그(매뉴얼 비유).
예시는 labs/meeting_agent 의 원본 회의록 · solution SKILL.md 에서만 가져온다.
"""
import anim
import viz2
from deck import ba, divider, flow, lab, light
from hx import code, esc, note
from v3kit import F, SOL, brief, pick

T = "3-5"
SK = (SOL / "dot_claude" / "skills" / "meeting-notes" / "SKILL.md").read_text(encoding="utf-8").strip()
FRONT = "\n".join(SK.split("\n")[:4])
STEPS = SK[SK.index("1. "):SK.index("## 형식")].strip()
FORM = SK[SK.index("## 형식"):].strip()


def side(title, src, rows, cols=1):
    """왼쪽 코드 · 오른쪽 카드."""
    return ('<div class="twocol"><div>' + code(title, esc(src)) + "</div><div>"
            + viz2.tiles(rows, cols) + "</div></div>")


def background():
    return [
        light("매번 같은 설명", viz2.tiles([
            ("회의록 정리", "「결정 · 할 일 · 열린 질문으로 나눠 줘」"), ("주간 보고", "「지난주 대비 · 경고는 빨간색」"),
            ("메일 답장", "「규정 근거 한 줄 · 존댓말」")], 3)
              + note("반복해서 설명하는 것", "Skill 후보 · 한 번 써 두고 필요할 때 불러옴"), T),
        light("업무 매뉴얼 비유", viz2.maprows([
            ("책장의 책 제목", "name · description", "시작할 때 이것만"), ("필요한 책의 해당 장", "SKILL.md 본문", "요청과 맞으면"),
            ("부록 · 양식", "부속 파일", "본문이 가리킬 때만"), ("계산기", "스크립트", "실행 결과만 올라감")], "매뉴얼", "Skill")
              + note("Anthropic 엔지니어링 블로그", "목차 → 장 → 부록 순서로 펼치는 매뉴얼"), T),
        light("Skill의 정의", flow([("한 번 써 둠", "절차 · 형식 · 기준"), ("요청이 들어옴", "「회의록 정리해 줘」"),
                                  ("Claude가 꺼냄", "description 과 맞으면"), ("같은 결과", "매번 같은 절차 · 형식")], hl=2)
              + viz2.tiles([("폴더 하나", "SKILL.md + 참고 파일"), ("마크다운 글", "코드를 몰라도 작성"), ("다시 쓰는 지시서", "대화가 바뀌어도 그대로")], 3), T),
    ]


def structure():
    tree = ("meeting_agent/\n"
            "└── .claude/\n"
            "    └── skills/\n"
            "        └── meeting-notes/      ← 폴더 이름 = Skill 이름\n"
            "            ├── SKILL.md        ← 필수 · 설명 + 절차\n"
            "            ├── 양식.md          ← 선택 · 본문이 가리킬 때 읽음\n"
            "            └── check.py        ← 선택 · 실행만 · 결과만 올라감")
    return [
        light("Skill 저장 위치", viz2.tiles([
            ("개인", "~/.claude/skills/이름/SKILL.md · 내 모든 프로젝트"), ("프로젝트", ".claude/skills/이름/SKILL.md · 이 폴더 · 팀 공유"),
            ("플러그인", "플러그인/skills/이름/SKILL.md · 설치한 묶음")], 3)
              + note("회의록 실습", "프로젝트 위치 · <code>labs/meeting_agent/.claude/skills/</code>"), T),
        light("Skill 폴더 구조", code("폴더", esc(tree))
              + note("SKILL.md 하나면 시작", "양식 · 스크립트는 필요해질 때 추가"), T),
        light("frontmatter의 두 줄", side("SKILL.md 맨 위", FRONT, [
            ("name", "/ 메뉴에 뜨는 이름 · 생략하면 폴더 이름"), ("description", "무엇을 · 언제 · Claude가 고르는 기준"),
            ("--- 사이", "YAML · 모든 필드는 선택 · description 권장")]), T),
        light("자주 쓰는 추가 필드", viz2.tiles([
            ("when_to_use", "호출 예문 추가 · description 뒤에 붙음"), ("disable-model-invocation", "true → 사람만 /이름 으로 호출"),
            ("allowed-tools", "Skill 실행 중 묻지 않고 쓸 도구"), ("paths", "특정 파일을 다룰 때만 자동 호출")], 2), T),
        light("본문", side("SKILL.md 본문 · 절차", STEPS, [
            ("마크다운", "제목 · 번호 · 표 그대로"), ("한 줄에 한 동작", "고르기 · 나누기 · 붙이기 · 저장"),
            ("하라는 말로", "이유 설명보다 할 일을 적음"), ("500줄 이내", "긴 자료는 부속 파일로")]), T),
        light("부속 파일과 스크립트", viz2.tiles([
            ("양식 · 예시 파일", "본문이 「양식.md 참고」라고 가리킬 때만 읽음"), ("스크립트", "읽지 않고 실행 · 결과만 컨텍스트에"),
            ("나누는 기준", "SKILL.md 가 500줄에 가까우면 떼어 냄")], 3)
              + note("Claude Code 문서", "Scripts are executed, not loaded"), T),
    ]


def calling():
    return [
        light("Skill이 호출되는 순간", anim.skill_trigger()
              + note("참고", "Claude Code 문서 「Skills」 · Claude 「What are skills?」 · IBM Technology 「What AI Agent Skills Are and How They Work」"), T),
        ba("description 비교", T, "description: 회의록 관련\n\n무엇을 하는지 없음\n언제 쓰는지 없음\n→ 비슷한 요청에도 안 불리거나 엉뚱할 때 불림",
           "description: 회의록을 할 일 · 결정 · 공유 초안으로 정리할 때.\n「회의록 정리해 줘」 「할 일 뽑아 줘」 같은 요청에 쓴다.\n\n→ 하는 일 + 요청 예문"),
        light("description 작성 규칙", viz2.tiles([
            ("하는 일 먼저", "「회의록을 할 일 · 결정으로 정리」"), ("요청 예문", "「할 일 뽑아 줘」 같은 실제 말투"),
            ("핵심을 앞에", "목록에선 1,536자에서 잘림"), ("겹치지 않게", "Skill 끼리 설명이 비슷하면 엉뚱한 쪽")], 2)
, T),
        light("자동 호출과 직접 호출", viz2.pair(
            "자동", [("언제", "요청이 description 과 맞을 때"), ("예", "「11/10 회의록 정리해 줘」")],
            "직접", [("언제", "/ 뒤에 Skill 이름"), ("예", "<code>/meeting-notes 11/10</code> → 11/10 이 인자로")], hl="r")
              + note("인자", "본문의 <code>$ARGUMENTS</code> 자리에 / 뒤의 말이 들어감"), T),
        light("사람만 부르는 Skill", side("SKILL.md 맨 위", "---\nname: send-summary\ndescription: 정리본을 슬랙에 보낼 때\ndisable-model-invocation: true\n---", [
            ("자동 호출 꺼짐", "Claude가 스스로 부르지 않음"), ("/send-summary 로만", "사람이 시작"),
            ("맞는 일", "발송 · 배포처럼 시점을 사람이 정할 일")]), T),
        pick("Skill과 command의 차이", T),
        light("CLAUDE.md vs Skill", '<div class="twocol"><div>'
              + code("나쁜 예 · CLAUDE.md 에 절차까지", esc("- 원본은 읽기만 · 결과는 out/\n1. 회의록 고르기\n2. 결정 · 할 일 · 열린 질문\n3. 담당 · 기한 · 근거\n4. 지난 할 일 · 슬랙 초안\n| 할 일 | 담당 | 기한 | 상태 | 근거 |"))
              + "</div><div>"
              + code("좋은 예 · 규칙만 · 절차는 Skill", esc("- 원본은 읽기만 · 결과는 out/\n- 기한이 없으면 「기한 미정」\n- 외부 발송은 사람이\n절차 · 형식 → meeting-notes Skill"))
              + "</div></div>"
              + note("차이", "CLAUDE.md 는 요청마다 읽힘 · Skill 본문은 회의록 요청 때만"), T),
    ]


def good_skill():
    ex = ("## 예시\n"
          "| 할 일 | 담당 | 기한 | 상태 | 근거 |\n"
          "| 보안팀 미팅 잡기 | 이준호 | 기한 미정 | - | 「준호님이 보안팀 미팅 잡기로」 |")
    return [
        light("좋은 Skill의 네 요소", viz2.tiles([
            ("① 언제 쓰는지", "description · 요청 예문"), ("② 단계별 절차", "번호 · 한 줄에 한 동작"),
            ("③ 산출물 형식", "표 머리 · 저장 위치"), ("④ 예시", "잘 된 결과 한 줄")], 4), T),
        light("① 언제 쓰는지", side("meeting-notes · description", FRONT, [
            ("하는 일", "할 일 · 결정 · 공유 초안으로 정리"), ("요청 예문", "「회의록 정리해 줘」 「할 일 뽑아 줘」"),
            ("빠지면", "요청과 맞춰 볼 근거가 없음")]), T),
        light("② 단계별 절차", side("meeting-notes · 절차", STEPS, [
            ("순서가 있음", "고르기 → 나누기 → 붙이기 → 확인 → 초안 → 저장"), ("판단 기준 포함", "기한 없으면 「기한 미정」"),
            ("멈출 곳", "발송은 하지 않음")]), T),
        light("③ 산출물 형식", side("meeting-notes · 형식", FORM, [
            ("표 머리 고정", "할 일 · 담당 · 기한 · 상태 · 근거"), ("맨 위 한 줄", "결정 · 할 일 · 기한 미정 개수"),
            ("하지 않는 것", "원본 수정 · 외부 발송 · 개인정보")]), T),
        light("④ 예시", side("SKILL.md 에 붙이는 예시", ex, [
            ("원본에서 고름", "11/10 회의록 · 기한이 없던 할 일"), ("형식을 보여 줌", "근거는 원문 그대로"),
            ("한두 줄", "많으면 예시를 베끼려 함")]), T),
        ba("흐린 절차와 구체적 절차", T,
           "1. 회의록을 잘 정리한다\n2. 중요한 것 위주로\n3. 깔끔한 형식으로\n\n→ 「잘 · 중요 · 깔끔」은 매번 다르게 해석",
           "2. 결정 · 할 일 · 열린 질문으로 나눈다\n3. 할 일마다 담당 · 기한 · 근거\n   기한이 없으면 「기한 미정」\n\n→ 누가 해도 같은 결과"),
    ]


def practice():
    without = ("11/10 주간 회의 요약\n\n"
               "- 휴대폰 인증 단계 이탈이 커서 인증 방식 변경을 검토한다.\n"
               "- 보안팀 의견을 먼저 듣기로 했다.\n"
               "- 「첫 달 무료」는 법무 검토를 마쳤다.\n"
               "- 비밀번호 재설정 메일 문제는 11/12 배포로 해결된다.")
    with_ = ("결정 2 · 할 일 2 · 기한 미정 1\n\n"
             "| 할 일              | 담당     | 기한     | 상태 | 근거 |\n"
             "| 보안팀 미팅 잡기    | 이준호   | 기한 미정 | -   | 「준호님이 보안팀 미팅 잡기로」 |\n"
             "| 메일 서버 수정 배포 | 확인 필요 | 11/12   | 진행 | 「11/12 수정 배포 예정」 |\n\n"
             "지난 할 일 (11/3)\n"
             "| 이탈 수치 정리 | 이준호 | 완료      | 「단계별 이탈 수치 공유」 |\n"
             "| 메일 건 전달   | 최민재 | 진행      | 「11/12 수정 배포 예정」 |\n"
             "| 배너 시안 확인 | 박서연 | 확인 필요 | 11/10 회의록에 언급 없음 |")
    return [
        light("Skill로 만드는 순서", flow([("Skill 없이", "「회의록 정리해 줘」"), ("결과 보고 말하기", "좋았던 것 · 바꿀 것"),
                                       ("Skill로", "「반영해서 Skill로 만들어 줘」"), ("새 대화", "같은 요청 · 비교")], hl=1)
              + note("말로 수정", "SKILL.md는 Claude가 작성 · 규칙은 사람이 정함"), T),
        lab("3-5", "회의록 정리 Skill", T, "Skill 없이 받은 결과를 보고 말로 다듬어 Skill로 고정",
            ["Skill 없이 정리 요청", "바꿀 것 · 규칙을 내가 정하기", "Skill로 만들게 요청", "새 대화에서 비교"],
            ["<code>.claude/skills/meeting-notes/</code>", "매번 같은 형식"], files=F, mine="내 반복 업무 절차 하나"),
        brief("3-5", T,
              ["Skill 없이 11/10 정리 요청", "결과에서 바꿀 것 3개 고르기", "Skill 요청 쓰기", "새 대화 · 짧은 요청으로 비교"],
              [("목표", "매번 같은 형식으로 정리"), ("내가 정한 규칙", "기한 없는 할 일 · 지난 할 일 확인 · 공유 초안"),
               ("산출물", "회의록 정리 Skill"), ("하지 말 것", "내가 정하지 않은 규칙 추가")],
              ["Skill", "방금 결과 반영", "description · 언제 쓰는지", "기한 미정"],
              ["기한 미정: 준호 · 보안팀 미팅", "11/3 할 일: 이탈 수치 완료 · 메일 건 진행 · 배너 확인 필요", "슬랙 공유 초안 세 줄", "Skill 이름이 호출 표시에"],
              "<code>solution/dot_claude/skills/meeting-notes/</code>"),
        light("Skill 없이 받은 결과 예", side("대화창 · 11/10 정리", without, [
            ("기한 표시 없음", "보안팀 미팅 · 기한 미정이 안 보임"), ("근거 없음", "원문 어느 줄인지 모름"),
            ("지난 할 일 없음", "11/3 배너 시안 확인이 빠짐"), ("저장 안 됨", "대화창에만 · 매번 형식이 다름")]), T),
        light("Skill로 받은 결과 예", code("out/2026-11-10_정리.md", esc(with_))
              + note("달라진 곳", "기한 미정 · 근거 · 지난 할 일 상태 · 파일 저장 — 모두 SKILL.md 의 한 줄씩"), T),
        light("SKILL.md 수정 루프", flow([("결과 읽기", "out/ 정리 파일"), ("바꿀 것 말하기", "「담당을 맨 앞 열로」"),
                                       ("Claude가 수정", "SKILL.md 형식 줄"), ("새 대화", "같은 요청으로 확인")], hl=1)
              + code("SKILL.md · 형식 줄", esc("- | 할 일 | 담당 | 기한 | 상태 | 근거 |\n+ | 담당 | 할 일 | 기한 | 상태 | 근거 |"))
              + note("한 번에 하나", "여러 개를 한꺼번에 바꾸면 무엇이 효과였는지 모름"), T),
    ]


def wrap():
    return [
        light("Skill 후보 고르는 기준", viz2.tiles([
            ("자주 반복", "주 1회 이상 같은 일"), ("같은 설명", "매번 같은 규칙 · 형식을 말함"),
            ("형식이 정해짐", "표 · 양식 · 보고 순서"), ("판단 기준이 글로", "「기한 없으면 기한 미정」처럼")], 4)
              + viz2.tiles([("주간 보고", "업무 기록 → 요약 · 경고 표"), ("문의 1차 답변", "문의 메일 → 규정 근거 · 답변 초안"),
                            ("경비 증빙 대조", "영수증 → 규정 위반 표시")], 3), T),
        light("Anthropic 공개 Skill", viz2.tiles([
            ("docx", "Word 문서 만들기 · 고치기"), ("xlsx", "엑셀 표 · 수식"), ("pptx", "발표 자료"), ("pdf", "PDF 읽기 · 양식 채우기")], 4)
              + code("Claude Code에서 설치", esc("/plugin marketplace add anthropics/skills\n/plugin install document-skills@anthropic-agent-skills"))
              + note("github.com/anthropics/skills", "시연 · 교육용 예제 · 내 Skill 을 쓸 때 구조 참고"), T),
    ]


def slides():
    return ([divider("05", "Skill 제작", "")] + background() + structure() + calling()
            + good_skill() + practice() + wrap())
