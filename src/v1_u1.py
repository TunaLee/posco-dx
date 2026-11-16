"""1-1 바이브코딩이란 (20분) — 실습 없음.

코딩 → 바이브코딩(정의 · 비유 · 흐름) → 어디까지 왔나(이정표 한 장씩) → 가능성과 한계 → 1부 완성 화면.
사실 출처: scratchpad/v1_facts.md (Karpathy · Collins · levels.io · MenuGen · Anthropic · Simon Willison · Veracode · Wiz · Replit · METR)
"""
import viz2
from deck import flow, light
from hx import code, esc, note
from stats_hx import big, hbars, quote, src
from v1kit import shot
from v3kit import phmap

T = "1-1"

TL = [("2025.02", "용어 탄생", "Karpathy 글 한 편"), ("2025.03", "3D 멀티플레이 게임", "fly.pieter.com"),
      ("2025.04", "실제 서비스", "MenuGen"), ("2025.05", "에이전트 정식 출시", "Claude Code"),
      ("2026.02", "10만 줄 컴파일러", "에이전트 16개"), ("2026.08", "프롬프트 한 번에 3D 게임", "두 모델 비교")]


def timeline(hl=None):
    cells = "".join(
        f'<div class="v1tp{" on" if i == hl else ""}"><i></i><span class="d">{d}</span><b>{t}</b><small>{s}</small></div>'
        for i, (d, t, s) in enumerate(TL))
    return f'<div class="v1tl"><div class="v1tline"></div>{cells}</div>'


CSS = """
  /* 1-1 · 변천사 타임라인 */
  .v1tl{position:relative; display:grid; grid-template-columns:repeat(6,1fr); gap:12px; margin:18px 0 22px; padding-top:30px;}
  .v1tline{position:absolute; left:4%; right:4%; top:38px; height:4px; background:linear-gradient(90deg,#D9DDE3,#F28C28); border-radius:4px;}
  .v1tp{position:relative; display:flex; flex-direction:column; align-items:center; text-align:center; gap:6px;}
  .v1tp i{width:20px; height:20px; border-radius:50%; background:#fff; border:4px solid #1F3A5F; margin-bottom:10px; position:relative; z-index:1;}
  .v1tp .d{font-family:var(--mono); font-size:15px; font-weight:800; color:#6B7785;}
  .v1tp b{font-size:20px; color:#16233A; line-height:1.3;} .v1tp small{font-size:15px; color:#3A4657;}
  .v1tp.on i{border-color:#F28C28; background:#F28C28;} .v1tp.on b{color:#E07A12;}
  .v1tl.sm{margin:0 0 14px; padding-top:22px;} .v1tl.sm .v1tline{top:30px;} .v1tl.sm b{font-size:15px;} .v1tl.sm small, .v1tl.sm .d{font-size:12px;}
  .v1tl.sm .v1tp{opacity:.45;} .v1tl.sm .v1tp.on{opacity:1;}
"""


def mini(i):
    return timeline(i).replace('class="v1tl"', 'class="v1tl sm"', 1)


def slides():
    return [
        # ── A. 코딩 → 바이브코딩
        light("코딩이란", '<div class="twocol"><div>'
              + viz2.tiles([("코딩", "컴퓨터가 할 일을 정해진 문법의 글로 쓰는 일"),
                            ("코드", "그 글 · 컴퓨터는 적힌 그대로만 실행"),
                            ("예 · 회의실 예약", "「같은 방 · 겹치는 시간이면 막는다」")], 1)
              + "</div><div>"
              + code("app.js · 겹치는 예약 막기 (1부 예제)", esc(
                  "const clash = load().some((x) =>\n"
                  "  x.room === b.room &&\n"
                  "  x.date === b.date &&\n"
                  "  x.start < b.end && b.start < x.end);\n"
                  "if (clash) {\n"
                  "  $(\"err\").textContent = \"이미 예약된 시간\";\n"
                  "  return;\n"
                  "}"))
              + "</div></div>"
              + note("한 줄 규칙", "사람 말로는 한 문장 · 코드로는 여덟 줄"), T),
        light("기존 개발 방식", flow([("언어 배우기", "문법 · 도구"), ("설계", "화면 · 데이터"), ("직접 타이핑", "한 줄씩"),
                                    ("오류 찾기", "빨간 글씨 해석"), ("고치기", "다시 실행")], hl=2)
              + viz2.tiles([("배우는 데", "문법 · 개발 도구부터"), ("만드는 데", "기능마다 직접 작성"),
                            ("고치는 데", "오류 문장을 읽고 원인 찾기")], 3), T),
        light("바이브코딩의 등장", quote(
            "There's a new kind of coding I call “vibe coding”, where you fully give in to the vibes, "
            "embrace exponentials, and forget that the code even exists.", "Andrej Karpathy · X · 2025-02-02")
              + viz2.tiles([("말로 설명", "무엇을 원하는지 사람 말로"), ("AI가 작성", "코드는 AI가 쓴다"),
                            ("결과로 판단", "코드 대신 화면 · 동작을 본다")], 3)
              + src(("Karpathy · X", "https://x.com/karpathy/status/1886192184808149383")), T),
        light("사전에 오른 말", big([("2025", "", "Collins 사전 올해의 단어 · vibe coding", True),
                                    ("2025-02-02", "", "Karpathy 가 처음 쓴 날")], 2)
              + quote("the use of artificial intelligence prompted by natural language to assist with the writing of computer code",
                      "Collins 사전 정의 · 자연어로 지시한 AI가 코드 작성을 돕게 하는 것")
              + src(("Collins · 2025-11-06", "https://blog.collinsdictionary.com/language-lovers/collins-word-of-the-year-2025-ai-meets-authenticity-as-society-shifts/")), T),
        light("집 짓기 비유", phmap("v1_framing.webp", "목조 주택 골조 공사", "사진 · NIOSH · 퍼블릭 도메인",
                                 "https://commons.wikimedia.org/wiki/File:Framing_fall_prevention_(9253620155).jpg", viz2.maprows([
                                     ("건축주", "나", "원하는 집을 설명"), ("요구 설명 · 설계 도면", "기획서 · PRD", "1-3 · 1-4"),
                                     ("시공팀", "Claude Code", "직접 짓는다"), ("공정마다 현장 점검", "실행해 보기", "1-6"),
                                     ("입주 · 문패", "배포 · 주소", "1-7")], "집 짓기", "바이브코딩")), T),
        light("바이브코딩의 흐름", flow([("말로 요청", "「겹치는 예약은 막아 줘」"), ("AI가 코드 작성", "app.js 에 규칙 추가"),
                                       ("실행해 보기", "겹치게 예약 → 막힘?"), ("말로 고치기", "「오류 문구를 빨간색으로」")], hl=2)
              + viz2.tiles([("한 바퀴", "요청 → 작성 → 확인"), ("여러 바퀴", "작게 나눠 여러 번 돌린다 (1-6)"),
                            ("사람의 일", "원하는 것을 말하고 결과를 판단")], 3), T),
        light("내 일과 AI의 일", viz2.pair(
            "내 일", [("무엇을 만들지", "기획서 · PRD"), ("되는지 판단", "화면을 눌러 확인"), ("공개 여부 결정", "배포 · 공유")],
            "AI의 일", [("코드 작성", "화면 · 규칙 · 저장"), ("오류 수정", "오류 문장 읽고 고침"), ("반복 작업", "파일 만들기 · 명령 실행")], hl="l")
              + note("판단은 사람", "AI는 시킨 것을 만들고 · 맞는지는 사람이 본다"), T),
        # ── B. 어디까지 왔나
        light("바이브코딩 변천사", timeline()
              + viz2.tiles([("2025 초", "혼자 만든 게임 · 웹 서비스"), ("2025 중반", "에이전트 정식 출시"),
                            ("2026", "여러 에이전트 · 큰 프로젝트")], 3), T),
        light("3D 멀티플레이 게임", mini(1)
              + big([("17일", "", "제작 시작부터 연 매출 환산 100만 달러까지", True), ("32만 명", "", "게임에 접속한 사람")], 2)
              + note("fly.pieter.com", "브라우저 3D 비행 게임 · Pieter Levels 가 2025-02-22 시작 · 수치는 본인 발표")
              + src(("levelsio · X · 2025-03-11", "https://x.com/levelsio/status/1899596115210891751")), T),
        light("실제 서비스 · MenuGen", mini(2)
              + viz2.pair("내 컴퓨터에서 돌릴 때", [("데모", "「신나고 재미있는 일」"), ("메뉴판 사진", "→ 음식 그림")],
                          "배포한 실제 서비스", [("로그인 · 결제 · 서버", "「고된 노동」"), ("만든 사람", "Karpathy 본인")], hl="r")
              + note("배포가 따로 어렵다", "그래서 1부에 배포 단원(1-7)이 따로 있다")
              + src(("Karpathy · 2025-04-27", "https://karpathy.bearblog.dev/vibe-coding-menugen/")), T),
        light("에이전트 정식 출시", mini(3)
              + viz2.pair("채팅", [("코드를 답으로 줌", "복사 · 붙여넣기는 사람이"), ("파일을 못 봄", "설명을 매번 붙여 넣음")],
                          "Claude Code", [("파일을 직접 읽고 씀", "내 폴더에서 작업"), ("명령 실행", "서버 띄우기 · 저장")], hl="r")
              + note("2025-05-22", "Claude 4 와 함께 Claude Code 정식 출시 · VS Code · JetBrains 연동")
              + src(("Anthropic · 2025-05-22", "https://www.anthropic.com/news/claude-4")), T),
        light("10만 줄 컴파일러", mini(4)
              + big([("16개", "", "함께 일한 Claude 에이전트"), ("약 2,000", "", "Claude Code 작업 세션"),
                     ("10만 줄", "", "Rust 로 쓴 C 컴파일러", True), ("2만", "달러 미만", "든 비용")], 4)
              + note("결과", "리눅스 6.9 를 빌드 · 단 일부 기능은 기존 컴파일러에 맡김 (글에 명시)")
              + src(("Anthropic Engineering · 2026-02-05", "https://www.anthropic.com/engineering/building-c-compiler")), T),
        light("프롬프트 한 번에 3D 게임", mini(5)
              + viz2.pair("Claude Fable 5 · Claude Code", [("결과", "3D 「Raccoon Heist」"), ("만든 사람 평가", "출발점으로는 인상적 · 완성작으론 평범")],
                          "GPT-5.6 Sol Ultra · Codex", [("결과", "3D 「Moonlight & Mayhem」"), ("만든 사람 평가", "앞의 것보다 훨씬 낫다")], hl="r")
              + note("같은 프롬프트", "모델 · 도구가 바뀌면 결과도 바뀐다")
              + src(("Simon Willison · 2026-08-05", "https://simonwillison.net/2026/Aug/5/raccoon-heist/"),
                    ("2026-08-07", "https://simonwillison.net/2026/Aug/7/moonlight-mayhem/")), T),
        # ── C. 가능성과 한계
        light("가능성과 한계", viz2.fit(
            [("화면 1~3개 웹 페이지", "예약 · 투표 · 체크리스트"), ("내 업무 도우미", "계산기 · 정리 도구"), ("시제품", "아이디어를 화면으로")],
            [("돈 · 개인정보를 다루는 서비스", "보안 점검이 따로 필요"), ("많은 사람이 동시에 쓰는 서비스", "서버 · DB 설계"),
             ("코드를 안 보고 운영", "고장 원인을 못 찾음")],
            gt="지금 만들기 좋은 앱", bt="아직 어려운 앱"), T),
        light("AI가 쓴 코드의 보안", big([("62%", "", "보안 검사 평균 통과율"), ("약 38%", "", "취약점이 생긴 작업", True)], 2)
              + hbars([("Python", 64.22), ("C#", 59.55), ("JavaScript", 56.99, True), ("Java", 31.00)], unit="%", top=100,
                      title="언어별 보안 통과율 · 모델 18개")
              + src(("Veracode · 2026-10-29", "https://www.veracode.com/blog/fall-2026-genai-code-security")), T),
        light("사고 사례 · 키 유출", big([("150만 개", "", "새어 나간 API 인증 토큰", True), ("3만 5천 개", "", "새어 나간 이메일 주소")], 2)
              + viz2.tiles([("서비스", "AI 에이전트 SNS · Moltbook"), ("만든 사람", "「코드는 한 줄도 직접 안 썼다」"),
                            ("원인", "화면 코드에 DB 키 · 접근 제한 설정 없음")], 3)
              + src(("Wiz · 2026-02-02", "https://www.wiz.io/blog/exposed-moltbook-database-reveals-millions-of-api-keys")), T),
        light("사고 사례 · 데이터 삭제", viz2.tiles([("상황", "코드 동결 기간 · 에이전트에 작업을 맡김"),
                                                 ("사고", "에이전트가 운영 DB 데이터 삭제"),
                                                 ("이후", "개발용 · 운영용 DB 를 자동으로 분리")], 3)
              + quote("Replit agent in development deleted data from the production database. Unacceptable and should never be possible.",
                      "Amjad Masad · Replit CEO · 2025-07-20")
              + src(("Amjad Masad · X", "https://x.com/amasad/status/1946986468586721478")), T),
        light("체감 속도와 실제 속도", big([("19%", "", "AI를 쓴 숙련 개발자 · 실제로 더 걸린 시간", True),
                                         ("20%", "", "같은 개발자들이 「빨라졌다」고 느낀 정도")], 2)
              + note("2026 후속", "AI 없이 일하려는 개발자가 줄어 같은 방식으로는 재기 어려워짐 · 측정 설계를 바꿈")
              + src(("METR · 2025-07-10", "https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/"),
                    ("METR · 2026-02-24", "https://metr.org/blog/2026-02-24-uplift-update/")), T),
        light("문제와 1부의 순서", viz2.maprows([
            ("원하는 것을 AI가 추측으로 채움", "기획서 · PRD 를 먼저", "1-3 · 1-4"),
            ("고친 뒤 망가지면 되돌릴 수 없음", "Git 으로 저장 시점 남기기", "1-5"),
            ("한 번에 다 만들면 어디가 틀렸는지 모름", "작게 나눠 확인하며", "1-6"),
            ("키 · 개인정보가 그대로 공개", "공개 전 확인", "1-7")], "바이브코딩의 문제", "1부에서 하는 일"), T),
        light("1부 완성 화면", shot("room_main.webp", "회의실 예약 · 1부 공통 예제 완성본", [
            ("날짜 하나 · 회의실 3곳", "하루 시간표 · 30분 칸"), ("빈 칸 클릭", "예약 · 겹치면 막힘"),
            ("인터넷 주소로 공유", "1-7 배포까지"), ("내 아이디어", "같은 순서로 하나 더")]), T),
    ]
