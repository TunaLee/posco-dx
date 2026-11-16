"""1-2 도구 · 실습 환경 (30분).

도구 네 개 → Claude · Claude Code · GitHub · Vercel 한 장씩(정의 · 요금 · 쓰는 단원) → 실습 1-2(계정 · 설치 · 첫 요청).
사실 출처: scratchpad/v1_facts.md (claude.com/pricing · code.claude.com/docs setup · overview · docs.github.com · vercel.com/docs)
"""
import viz2
from deck import flow, lab, light
from hx import code, esc, note, table
from stats_hx import src
from v1kit import brief, chat

T = "1-2"


def slides():
    return [
        # ── 도구 네 개
        light("1부의 도구 네 개", viz2.tiles([
            ("Claude", "대화로 기획서 · PRD 작성 · 1-3 · 1-4"), ("Claude Code", "내 폴더에서 코드 작성 · 실행 · 1-6"),
            ("GitHub", "코드와 변경 기록 보관 · 1-5 · 1-7"), ("Vercel", "인터넷 주소를 붙여 공개 · 1-7")], 2), T),
        light("도구의 흐름", flow([("Claude", "기획서.md · PRD.md"), ("Claude Code", "앱 코드"),
                                 ("GitHub", "코드 보관"), ("Vercel", "공개 주소")], hl=1)
              + viz2.tiles([("생각 정리", "무엇을 만들지 · 말로"), ("만들기", "파일 · 명령 · 확인"),
                            ("내보내기", "보관 → 공개 → 공유")], 3), T),
        # ── Claude
        light("Claude", '<div class="twocol"><div>'
              + viz2.tiles([("대화형 AI", "claude.ai · 웹 · 앱"), ("1부에서 맡는 일", "아이디어 → 기획서 → PRD"),
                            ("못 하는 일", "내 컴퓨터 파일을 직접 고치기")], 1)
              + "</div><div>"
              + chat([("me", "팀 회의실 예약 페이지를 만들고 싶어. 기획서에 들어갈 내용을 정리해 줘"),
                      ("ai", "배경 · 문제점 · 목표 이용자 · 서비스 컨셉 · 화면 구성 순서로 정리한다.\n먼저 회의실은 몇 곳인가?")], "Claude 대화 예")
              + "</div></div>", T),
        light("Claude 요금제", table(["요금제", "월 요금", "사용량", "Claude Code"], [
            ["Free", "$0", "기본", "✕"],
            ["<b>Pro</b>", "<b>$20</b> · 연 결제 시 월 $17", "기준", "<b>○</b>"],
            ["Max", "$100", "Pro 의 5배", "○"],
            ["Ultra", "$200", "Pro 의 10배", "○"]])
              + note("1부 기준", "Claude Code 를 쓰려면 Pro 이상 · 회사 Team · Enterprise 계정도 가능")
              + src(("claude.com/pricing · 2026-11", "https://claude.com/pricing"), ("Claude Code setup", "https://code.claude.com/docs/en/setup")), T),
        light("첫 프롬프트", chat([
            ("me", "회의실 예약 페이지를 만들려고 해. 기획을 시작하기 전에 나한테 물어볼 질문 다섯 개만 해 줘"),
            ("ai", "1. 회의실은 몇 곳이고 이름은?\n2. 누가 예약하나 — 팀원 전체?\n3. 예약 단위는 30분 · 1시간?\n"
                   "4. 겹치는 예약은 막아야 하나?\n5. 휴대폰에서도 보나?")], "Claude 대화 예")
              + note("질문을 받는 요청", "바로 만들게 하지 않고 · 빠진 것을 먼저 묻게 한다 (1-3 에서 다시 씀)"), T),
        # ── Claude Code
        light("Claude Code", '<div class="twocol"><div>'
              + viz2.tiles([("내 폴더에서 일하는 Claude", "파일을 읽고 · 만들고 · 고친다"), ("명령 실행", "서버 띄우기 · 저장 · 올리기"),
                            ("결과 확인", "실행 결과를 보고 다시 고침")], 1)
              + "</div><div>"
              + chat([("me", "PRD.md 를 읽고 시간표 화면부터 만들어 줘"),
                      ("ai", "PRD.md 를 읽었다.\nindex.html · style.css · app.js 를 만든다.\n파일을 만들어도 될까?")], "Claude Code 대화 예")
              + "</div></div>", T),
        light("Claude와 Claude Code", viz2.pair(
            "Claude (채팅)", [("결과", "답변 글 · 코드 조각"), ("파일", "내가 복사해 붙여 넣음"), ("1부", "기획서 · PRD")],
            "Claude Code", [("결과", "내 폴더의 파일"), ("파일", "직접 만들고 고침"), ("1부", "앱 만들기 · 올리기")], hl="r")
              + note("같은 모델", "차이는 내 컴퓨터를 직접 다룰 수 있는지"), T),
        light("Claude Code를 쓰는 곳", viz2.tiles([
            ("터미널", "명령어 창 · 기능이 가장 많음"), ("VS Code", "확장 프로그램 · 파일을 보며"),
            ("JetBrains", "플러그인"), ("데스크톱 앱", "macOS · Windows"), ("웹", "claude.ai/code · 클라우드에서")], 5)
              + note("같은 엔진", "어디서 쓰든 설정 · CLAUDE.md 가 같다")
              + src(("Claude Code 문서 · platforms", "https://code.claude.com/docs/en/platforms")), T),
        light("이 강의의 선택 · VS Code", viz2.tiles([
            ("파일 트리", "Claude Code 가 만든 파일이 바로 보임"), ("변경 확인", "고친 줄을 색으로 비교"),
            ("한 화면", "편집기 · 대화 · 터미널")], 3)
              + flow([("VS Code 설치", "code.visualstudio.com"), ("확장 검색", "「Claude Code」"), ("설치", "공식 확장"),
                      ("폴더 열기", "내 프로젝트 폴더"), ("로그인", "Claude 계정")], hl=1), T),
        light("Claude Code 설치", '<div class="twocol"><div>'
              + code("macOS · 터미널", esc("curl -fsSL https://claude.ai/install.sh | bash"))
              + code("Windows · PowerShell", esc("irm https://claude.ai/install.ps1 | iex"))
              + "</div><div>"
              + code("설치 확인", esc("claude --version\nclaude          # 실행 · 처음엔 로그인"))
              + viz2.tiles([("Windows", "Git for Windows 설치 권장"), ("요구 사항", "macOS 13 이상 · Windows 10 1809 이상")], 1)
              + "</div></div>"
              + src(("Claude Code 문서 · setup", "https://code.claude.com/docs/en/setup")), T),
        light("첫 실행 · 로그인", flow([("claude 실행", "또는 VS Code 확장"), ("로그인 방법 선택", "Claude 계정"),
                                     ("브라우저 인증", "Pro 이상 계정"), ("폴더 신뢰", "이 폴더에서 작업 허용"), ("입력창", "첫 요청")], hl=2)
              + viz2.tiles([("로그인은 한 번", "다음 실행부터 바로 입력창"), ("폴더 신뢰", "처음 여는 폴더마다 묻는다"),
                            ("Free 계정", "Claude Code 를 쓸 수 없다 · 로그인 단계에서 막힘")], 3), T),
        # ── GitHub · Vercel
        light("GitHub", viz2.tiles([
            ("코드 보관함", "인터넷에 있는 내 프로젝트 폴더"), ("변경 기록", "언제 · 무엇을 바꿨는지 (1-5)"),
            ("배포 출발점", "Vercel 이 여기서 코드를 가져감 (1-7)")], 3)
              + viz2.tiles([("가입", "github.com · 이메일"), ("요금", "Free 로 충분 · 비공개 저장소도 무제한")], 2)
              + src(("GitHub plans", "https://docs.github.com/en/get-started/learning-about-github/githubs-plans")), T),
        light("Vercel", viz2.tiles([
            ("공개 주소", "내 앱에 프로젝트이름.vercel.app 주소"), ("자동 배포", "GitHub 에 올리면 다시 배포 (1-7)"),
            ("가입", "GitHub 계정으로 가입 · 연동")], 3)
              + table(["요금제", "요금", "용도"], [["<b>Hobby</b>", "<b>무료</b>", "개인 · 비상업용"], ["Pro", "월 $20", "상업용 · 팀"]])
              + src(("Vercel pricing", "https://vercel.com/pricing"), ("Hobby plan", "https://vercel.com/docs/plans/hobby")), T),
        light("Hobby 플랜 한도", viz2.tiles([
            ("데이터 전송", "월 100GB"), ("함수 호출", "월 100만 회"), ("배포", "하루 100회"), ("프로젝트", "200개")], 4)
              + note("1부 앱", "화면 파일만 있는 작은 앱 · 한도 걱정 없음 · 회사 업무용 공개는 Pro")
              + src(("Vercel Hobby plan", "https://vercel.com/docs/plans/hobby")), T),
        light("계정 연결", flow([("GitHub 가입", "아이디 하나"), ("Vercel 가입", "GitHub 로 계속하기"),
                               ("저장소 연결", "1-7 에서"), ("올리면 배포", "자동")], hl=1)
              + viz2.tiles([("아이디", "GitHub 하나로 두 곳"), ("비밀번호", "Vercel 에 따로 만들지 않음"),
                            ("연결", "Vercel 이 내 저장소를 읽도록 허용")], 3), T),
        # ── 실습
        lab("1-2", "실습 환경 준비", T, "계정 세 개 · Claude Code 설치 · 프로젝트 폴더에서 첫 요청",
            ["Claude 가입 · Pro 이상", "GitHub 가입 · Vercel 은 GitHub 로 가입", "VS Code · Claude Code 확장 설치",
             "내 프로젝트 폴더를 만들어 VS Code 로 열기", "Claude Code 에 첫 요청"],
            ["claude --version 이 버전을 보여 줌", "Claude Code 가 첫 요청에 답함", "GitHub · Vercel 로그인 상태"],
            files="labs/room_booking (예시)"),
        brief("1-2 ①", T, ["claude.ai 가입 · 요금제 확인", "github.com 가입", "vercel.com → GitHub 로 계속하기",
                            "VS Code 설치 → 확장 「Claude Code」", "터미널에서 claude --version"],
              [("계정", "Claude (Pro 이상) · GitHub · Vercel"), ("설치", "VS Code · Claude Code 확장"),
               ("폴더", "바탕화면에 room 또는 내 아이디어 이름")],
              ["Pro", "GitHub로 계속하기", "Claude Code 확장", "claude --version"],
              ["세 사이트 모두 로그인된 상태", "VS Code 왼쪽에 Claude 아이콘"],
              "회사 PC 에서 설치가 막히면 웹(claude.ai/code)으로 · 1-6 전까지 해결", folder="바탕화면/내 프로젝트 폴더"),
        brief("1-2 ②", T, ["VS Code → 폴더 열기", "Claude Code 열기 · 로그인", "폴더 신뢰 허용", "첫 요청 보내기", "답 읽기"],
              [("목표", "이 폴더가 지금 어떤 상태인지 듣기"), ("범위", "이 폴더 안만"),
               ("하지 말 것", "아직 파일을 만들지 않기")],
              ["폴더 열기", "로그인", "첫 요청"],
              ["Claude Code 가 폴더 내용을 답함", "파일이 새로 생기지 않음"],
              "로그인 창이 안 뜨면 VS Code 를 껐다 켜기", folder="바탕화면/내 프로젝트 폴더"),
        light("첫 요청 결과 예", '<div class="twocol"><div>'
              + chat([("me", "이 폴더에 지금 뭐가 있는지 알려 줘. 아직 파일은 만들지 마"),
                      ("ai", "이 폴더는 비어 있다.\n파일 · 하위 폴더가 없다.\n만들 앱을 알려 주면 구조를 제안한다.")], "Claude Code 대화 예")
              + "</div><div>"
              + code("터미널 · 설치 확인 예", esc("$ claude --version\n2.x.x (Claude Code)\n\n$ git --version\ngit version 2.x"))
              + "</div></div>"
              + note("확인", "답이 오면 계정 · 설치 · 로그인 모두 끝"), T),
        light("막히는 곳", viz2.tiles([
            ("claude 명령이 없다", "터미널을 새로 열기 · 설치 후 다시"), ("Free 계정", "Claude Code 로그인 불가 → Pro 이상"),
            ("Windows · Git 없음", "Git for Windows 설치"), ("회사 PC 설치 막힘", "웹 claude.ai/code 로")], 2)
              + src(("Claude Code 문서 · setup", "https://code.claude.com/docs/en/setup")), T),
    ]
