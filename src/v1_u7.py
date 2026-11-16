"""1-7 배포 (30분).

배포란 → 비유(가게 문 열기) → localhost 의 한계 → 흐름(GitHub → Vercel → 주소)
→ GitHub에 올리기(gh · 말로) → Vercel 가져오기 · 주소 → push 하면 자동 재배포 · Production / Preview → 공개 전 확인 → 실습.
사실 출처: cli.github.com (gh 설치 · gh auth login · gh repo create) · vercel.com/docs/git · vercel.com/docs/deployments/generated-urls
· vercel.com/docs/plans/hobby · docs.github.com (plans)
Git 개념(commit · push)은 1-5 에서 설명 — 여기서는 다시 설명하지 않는다.
"""
import viz2
from deck import flow, lab, light
from hx import code, esc, note
from stats_hx import src
from v1kit import brief, chat, shot
from v3kit import phmap

T = "1-7"


def slides():
    return [
        # ── 배포란 · 비유
        light("배포", viz2.pair(
            "배포 전", [("주소", "localhost — 내 컴퓨터 안"), ("열 수 있는 사람", "나 혼자"), ("컴퓨터를 끄면", "앱도 꺼짐")],
            "배포 후", [("주소", "room-booking.vercel.app 형식"), ("열 수 있는 사람", "주소를 받은 누구나"), ("컴퓨터를 끄면", "그대로 열림")])
              + note("배포", "내 컴퓨터에서 돌던 앱을 인터넷 주소로 공개하는 일"), T),
        light("가게 문 열기 비유", phmap(
            "v1_shopdoor.webp", "가게 문의 영업시간 안내", "사진 · dvorty (Mapillary) · CC BY-SA 4.0",
            "https://commons.wikimedia.org/wiki/File:Door_signs_at_Stan%27s_Donuts,_Santa_Clara,_California.jpg",
            viz2.maprows([
                ("주방에서 혼자 맛보기", "localhost 확인", "1-6"), ("문 열고 간판 달기", "배포", "Vercel"),
                ("가게 주소", "배포 주소", "*.vercel.app"), ("메뉴를 바꿔 다시 진열", "재배포", "push 하면 자동")], "가게", "배포")), T),
        light("localhost는 내 컴퓨터만", viz2.tiles([
            ("내 브라우저", "localhost 주소로 열림"), ("팀원 노트북", "같은 주소를 넣어도 안 열림"), ("내 휴대폰", "안 열림 · 다른 기기")], 3)
              + code("1-6 에서 띄운 주소 · 예", esc("http://localhost:3000   ← 「이 컴퓨터」라는 뜻"))
              + note("localhost", "주소 자체가 「지금 이 컴퓨터」를 가리킴 · 다른 기기에서는 그 기기 자신을 가리킴"), T),
        light("배포가 필요한 순간", viz2.tiles([
            ("링크로 보여 주기", "팀원에게 주소 하나만 전달"), ("휴대폰에서 확인", "PRD 완료 기준 · 390px 폭"),
            ("컴퓨터를 꺼도", "앱은 계속 열림"), ("고치면 같은 주소에", "새 링크를 돌릴 필요 없음")], 2), T),
        light("배포 흐름", flow([
            ("내 컴퓨터", "앱 · 커밋"), ("GitHub", "코드 보관 (1-5)"), ("Vercel", "코드를 가져가 공개"),
            ("주소", "*.vercel.app"), ("팀원", "링크로 접속")], hl=2)
              + viz2.tiles([
                  ("연결 ① Claude Code → GitHub", "gh 로 저장소 만들고 올리기 · 말로 시킴"),
                  ("연결 ② GitHub → Vercel", "한 번 연결해 두면 이후 자동")], 2), T),
        # ── GitHub 에 올리기
        light("gh · GitHub 명령 도구", viz2.tiles([
            ("gh", "GitHub 공식 명령 도구 · 저장소 만들기 · 올리기"), ("Claude Code가 대신 실행", "명령을 외울 필요 없음"),
            ("한 번만", "설치 · 로그인 연결")], 3)
              + '<div class="twocol"><div>' + code("macOS", esc("brew install gh")) + "</div><div>"
              + code("Windows", esc("winget install --id GitHub.cli --source winget")) + "</div></div>"
              + note("Windows", "설치 뒤 터미널을 새 창으로 열어야 gh 가 잡힘")
              + src(("GitHub CLI", "https://cli.github.com/")), T),
        light("gh 로그인 연결", flow([
            ("gh auth login", "터미널에서 실행"), ("GitHub.com · HTTPS", "기본값 선택"), ("브라우저 인증", "코드 입력 · 승인"),
            ("연결 완료", "내 계정으로 명령 실행")], hl=2)
              + code("터미널 · 예", esc("$ gh auth login\n? Where do you use GitHub?  GitHub.com\n...\n✓ Logged in as 내계정"))
              + note("직접 할 것", "브라우저 승인은 사람이 · 비밀번호를 Claude에게 알려 주지 않음")
              + src(("gh auth login", "https://cli.github.com/manual/gh_auth_login")), T),
        light("「GitHub에 올려 줘」", chat([
            ("me", "이 폴더를 GitHub 비공개 저장소 room-booking 으로 올려 줘"),
            ("ai", "gh repo create room-booking --private --source=. --push 를 실행해도 될까요?"),
            ("me", "응"),
            ("ai", "완료 · https://github.com/내계정/room-booking")], "Claude Code 대화 예")
              + note("Claude가 쓰는 명령", "gh repo create — 원격 저장소 만들기 + 지금까지의 커밋 올리기")
              + src(("gh repo create", "https://cli.github.com/manual/gh_repo_create")), T),
        light("공개 · 비공개 저장소", viz2.pair(
            "공개 (public)", [("누가 보나", "인터넷의 누구나 코드를 봄"), ("맞는 경우", "공개해도 되는 연습 코드")],
            "비공개 (private)", [("누가 보나", "나와 초대한 사람만"), ("맞는 경우", "회사 업무 · 이 실습")], hl="r")
              + note("GitHub Free", "비공개 저장소도 개수 제한 없음 · 일부 기능만 유료")
              + src(("GitHub plans", "https://docs.github.com/en/get-started/learning-about-github/githubs-plans")), T),
        light("올라간 저장소 확인", '<div class="twocol"><div>'
              + code("github.com/내계정/room-booking · 예", esc(
                  "room-booking/\n├── index.html\n├── style.css\n├── app.js\n├── 기획서.md     1-3\n└── PRD.md        1-4"))
              + "</div><div>" + viz2.tiles([
                  ("파일 목록", "내 폴더와 같은가"), ("커밋 기록", "1-5 · 1-6 커밋이 보이나"), ("자물쇠 표시", "비공개인가")], 1)
              + "</div></div>", T),
        # ── Vercel
        light("Vercel 프로젝트 가져오기", flow([
            ("Vercel 로그인", "GitHub 계정 (1-2)"), ("새 프로젝트", "Git 저장소 가져오기"), ("room-booking 선택", "저장소 접근 허용"),
            ("Deploy", "설정은 기본값"), ("주소 발급", "1분 안팎")], hl=2)
              + note("저장소가 안 보이면", "GitHub 쪽에서 Vercel 에 그 저장소 접근을 허용")
              + note("설정", "HTML · CSS · JS 만 있는 폴더 → 빌드 설정을 바꿀 것 없음"), T),
        light("배포 주소", viz2.tiles([
            ("프로젝트 기본 주소", "프로젝트명.vercel.app"), ("배포마다 고유 주소", "버전마다 따로 생김 · 기본 공개")], 2)
              + code("배포 완료 · 예", esc("✓ Production   https://room-booking.vercel.app\n  이번 배포     https://room-booking-a1b2c3.vercel.app"))
              + note("공유할 주소", "프로젝트 기본 주소 · 다시 배포해도 바뀌지 않음")
              + src(("Vercel · Generated URLs", "https://vercel.com/docs/deployments/generated-urls")), T),
        light("같은 화면이 주소로", shot("room_main.webp", "배포 주소로 연 회의실 예약 · localhost 와 같은 화면", [
            ("주소만 다름", "localhost → *.vercel.app"), ("코드는 그대로", "GitHub 에 올린 그 파일"), ("예약 데이터", "여는 브라우저마다 따로 · 1-8")]), T),
        light("휴대폰에서 열기", shot("room_mobile.webp", "390px 폭 · 휴대폰 화면", [
            ("PRD 완료 기준", "모바일 폭에서 가로 스크롤 없음"), ("확인 방법", "주소를 휴대폰으로 보내 열기"),
            ("깨지면", "화면 캡처를 Claude Code에 붙여 수정 요청 (1-6)")]), T),
        # ── 재배포
        light("수정 → 재배포", flow([
            ("말로 수정", "Claude Code"), ("localhost 확인", "1-6 처럼"), ("커밋 · push", "「GitHub에 올려 줘」"),
            ("Vercel 자동 배포", "push 를 감지"), ("같은 주소에 반영", "새 링크 없음")], hl=3)
              + note("한 번 연결 뒤", "Vercel 화면을 다시 열 필요 없음 · push 가 곧 배포")
              + src(("Vercel · Git", "https://vercel.com/docs/git")), T),
        light("재배포 대화 예", chat([
            ("me", "예약 칸 색을 연한 초록으로 바꿔 줘"),
            ("ai", "style.css 의 .cell.busy 색 변경 완료"),
            ("me", "localhost 에서 확인했어 · 커밋하고 GitHub에 올려 줘"),
            ("ai", "커밋 「예약 칸 색 변경」 → push 완료 · Vercel 새 배포 시작")], "Claude Code 대화 예")
              + note("확인", "1~2분 뒤 같은 주소를 새로고침"), T),
        light("Production · Preview", viz2.pair(
            "Production", [("언제", "main 브랜치에 커밋 · push"), ("주소", "프로젝트 기본 주소"), ("누가 봄", "공유한 팀원 모두")],
            "Preview", [("언제", "다른 브랜치 · PR"), ("주소", "브랜치마다 고유 주소"), ("쓰임", "공개 전에 미리 확인")], hl="l")
              + note("1부에서는", "main 하나로 Production 만 · Preview 는 이름만 알아 두기")
              + src(("Vercel · Environments", "https://vercel.com/docs/deployments/environments")), T),
        # ── 공개 전 확인
        light("공개 전 확인", viz2.tiles([
            ("키 · 비밀번호", "코드 · 파일에 들어 있지 않은가"), ("개인정보", "실제 이름 · 연락처 대신 예시 값"),
            ("배포 주소는 공개", "주소를 아는 누구나 열 수 있음"), ("Hobby 는 개인 · 비상업", "회사 서비스는 Pro 이상")], 2)
              + note("Claude Code에게", "「올리기 전에 키 · 개인정보가 들어간 파일이 있는지 찾아 줘」")
              + src(("Vercel Terms", "https://vercel.com/legal/terms"), ("Hobby", "https://vercel.com/docs/plans/hobby")), T),
        # ── 실습
        lab("1-7", "내 앱 배포", T, "1-6 에서 만든 앱을 GitHub 에 올리고 Vercel 주소로 공개",
            ["gh 설치 · 로그인 연결", "Claude Code에게 「GitHub 비공개 저장소로 올려 줘」",
             "Vercel 에서 저장소 가져오기 · Deploy → 휴대폰으로 열기", "한 곳 고쳐 push → 같은 주소에 반영 확인"],
            ["저장소에 내 파일 · 커밋 기록", "*.vercel.app 주소로 앱이 열림", "수정 한 번이 재배포로 반영"],
            files="1-6 의 내 앱 폴더"),
        brief("1-7", T,
              ["gh auth login (브라우저 승인)", "올리기 전 키 · 개인정보 점검 요청", "저장소 만들고 올리기 요청",
               "Vercel 가져오기 · Deploy", "수정 → 「GitHub에 올려 줘」"],
              [("목표", "이 폴더를 GitHub 에 올리기"), ("저장소", "이름 · 비공개"), ("올리기 전", "키 · 개인정보 점검"),
               ("하지 말 것", "기존 커밋 지우기 · 공개 저장소")],
              ["GitHub", "비공개", "gh", "push", "Vercel"],
              ["저장소 주소가 열림", "배포 주소가 열림", "수정 뒤 같은 주소에 반영"],
              "오류 문구를 그대로 Claude Code에 붙여 넣기 · 아래 「막히는 곳」", folder="1-6 의 내 앱 폴더"),
        light("실습 1-7 확인", viz2.maprows([
            ("저장소", "github.com/내계정/저장소 이름", "파일 · 커밋 · 자물쇠"), ("배포 주소", "프로젝트명.vercel.app", "PC · 휴대폰에서 열림"),
            ("재배포", "push 1~2분 뒤 새로고침", "고친 곳이 보임"), ("공개 전 점검", "키 · 개인정보 없음", "Claude Code 점검 결과")], "볼 것", "확인")
              + note("공유", "배포 주소를 1-8 결과 공유에 사용"), T),
        light("막히는 곳", viz2.tiles([
            ("gh 를 못 찾음", "설치 뒤 터미널 새 창 · VS Code 재시작"), ("로그인 창이 안 뜸", "gh auth login 을 직접 실행 · 브라우저 승인"),
            ("Vercel 에 저장소가 없음", "GitHub 에서 Vercel 저장소 접근 허용"), ("주소가 404", "index.html 이 폴더 맨 위에 있는지"),
            ("고쳤는데 그대로", "push 했는지 · 새로고침 · 1~2분 대기"), ("휴대폰에서 깨짐", "화면 캡처 붙여 수정 요청")], 3), T),
    ]
