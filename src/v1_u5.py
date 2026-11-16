"""1-5 Git · GitHub 기초 (10분).

배경(최종_진짜최종) → 비유(세이브 포인트) → Git · commit · 되돌리기 → 말로 시키기 → GitHub · push / pull → 실습(첫 커밋).
사실 출처: git-scm.com/docs/git-commit · git-scm.com/docs/git · docs.github.com/en/get-started/using-git/about-git
"""
import viz2
from deck import flow, lab, light
from hx import code, esc, note
from stats_hx import src
from v1kit import brief, chat
from v3kit import phmap

T = "1-5"


def slides():
    return [
        # ── 배경 → 비유
        light("최종_진짜최종", viz2.tiles([
            ("기획서_v1.md", "처음 쓴 것"), ("기획서_최종.md", "피드백 반영"), ("기획서_최종_진짜.md", "PRD 쓰다 다시 고침")], 3)
              + viz2.tiles([
                  ("어느 게 최신", "파일 날짜를 열어 봐야 앎"), ("무엇이 바뀌었나", "두 파일을 나란히 놓고 비교"),
                  ("어제 상태로", "복사본이 없으면 못 돌아감")], 3)
              + note("코드에서는", "파일 수십 개가 함께 바뀜 · 이름 붙여 복사하는 방식이 통하지 않음"), T),
        light("세이브 포인트 비유", phmap(
            "v1_savepoint.webp", "게임 속 세이브 포인트", "그림 · David Revoy · CC BY 4.0",
            "https://commons.wikimedia.org/wiki/File:2023-03-30_Concept-art-for-a-fictive-video-game-Save-Point_by-David-Revoy.jpg",
            viz2.maprows([
                ("세이브 포인트에서 저장", "커밋 (commit)", "지금 상태를 기록"), ("저장 슬롯 이름", "커밋 메시지", "「예약 창 추가」"),
                ("저장 목록", "기록 (log)", "언제 · 무엇을"), ("불러오기", "되돌리기", "저장한 시점으로"),
                ("클라우드 저장", "GitHub", "다른 컴퓨터에서도")], "게임", "Git")), T),
        # ── Git · commit · 되돌리기
        light("Git", flow([
            ("파일 수정", "기획서.md · PRD.md"), ("저장할 파일 고르기", "add"), ("이름 붙여 기록", "commit"), ("기록에 쌓임", "log 로 보기")], hl=2)
              + viz2.pair(
                  "복사본으로 관리", [("파일마다 사본", "기획서_최종_진짜.md"), ("바뀐 곳", "눈으로 비교")],
                  "Git으로 관리", [("파일은 하나", "기획서.md 그대로"), ("바뀐 곳", "커밋마다 자동으로 남음")])
              + note("공식 정의", "git commit — 「Record changes to the repository」 · 저장소에 변경을 기록"), T),
        light("커밋 하나에 남는 것", viz2.tiles([
            ("바뀐 내용", "어느 파일의 어느 줄"), ("메시지", "「PRD 완료 기준 추가」"),
            ("시각 · 작성자", "언제 · 누가"), ("고유 번호", "a3f9c1e 같은 해시")], 4)
              + code("기록 보기 · 예", esc(
                  "a3f9c1e  PRD 완료 기준 추가        2026-11-20 14:12\n"
                  "7b21d04  기획서 · PRD 첫 버전      2026-11-20 13:40"))
              + note("메시지", "무엇을 바꿨는지 한 줄 · 나중에 되돌릴 시점을 찾는 이름표"), T),
        light("되돌리기 두 가지", viz2.pair(
            "아직 커밋 전", [("restore", "마지막 커밋 상태로 파일을 되돌림"), ("쓰는 때", "방금 고친 것이 마음에 안 들 때")],
            "이미 커밋한 뒤", [("revert", "그 커밋을 되돌리는 새 커밋을 만듦"), ("기록", "지우지 않고 「되돌림」도 남김")], hl="r")
              + flow([("커밋 A", "기획서"), ("커밋 B", "PRD"), ("고치는 중", "PRD 수정"), ("restore", "커밋 B 상태로"), ("revert", "커밋 C · B를 취소")], hl=2)
              + note("공식 문서", "revert 는 새 커밋 · restore 는 작업 폴더의 파일만 · 둘 다 기록을 지우지 않음")
              + src(("git-scm · git", "https://git-scm.com/docs/git")), T),
        light("말로 시키기", viz2.maprows([
            ("「지금 상태 커밋해 줘」", "git add · git commit", "메시지도 Claude가 씀"),
            ("「커밋 기록 보여 줘」", "git log", "시점 · 메시지 목록"),
            ("「방금 고친 거 취소해 줘」", "git restore", "커밋 전 수정 버림"),
            ("「마지막 커밋 되돌려 줘」", "git revert", "되돌리는 새 커밋")], "Claude Code에 하는 말", "실행되는 명령")
              + note("명령어", "외우지 않아도 됨 · 무엇을 하는지만 알면 됨"), T),
        # ── GitHub · push / pull
        light("GitHub", viz2.pair(
            "Git", [("어디에", "내 컴퓨터"), ("하는 일", "저장 시점 기록 · 되돌리기"), ("없으면", "기록이 이 컴퓨터에만")],
            "GitHub", [("어디에", "인터넷 (원격 저장소)"), ("하는 일", "기록 보관 · 공유 · 다른 컴퓨터에서 받기"), ("1-7 에서", "Vercel 배포와 연결")])
              + note("원격 저장소", "내 컴퓨터 밖에 둔 같은 기록 · Free 요금제도 비공개 저장소 무제한")
              + src(("GitHub plans", "https://docs.github.com/en/get-started/learning-about-github/githubs-plans")), T),
        light("push · pull", flow([
            ("내 컴퓨터", "커밋 3개"), ("push", "원격에 올림"), ("GitHub", "같은 커밋 3개"), ("pull", "원격 변경을 받아 합침"), ("다른 컴퓨터", "같은 상태")], hl=1)
              + viz2.tiles([
                  ("push", "로컬 커밋을 원격 저장소에 올림"), ("pull", "원격의 변경을 내 컴퓨터로 가져와 합침")], 2)
              + src(("GitHub Docs · About Git", "https://docs.github.com/en/get-started/using-git/about-git")), T),
        light("커밋하는 시점", viz2.tiles([
            ("기능 하나가 됐을 때", "「예약 창 저장까지 동작」"), ("크게 바꾸기 전", "디자인을 갈아엎기 전"),
            ("확인이 끝났을 때", "브라우저로 보고 이상 없음")], 3)
              + flow([("요청", "기능 하나"), ("확인", "브라우저"), ("커밋", "세이브"), ("다음 요청", "")], hl=2)
              + note("1-6 에서", "이 고리를 태스크마다 반복"), T),
        # ── 실습
        lab(T, "첫 커밋", T, "기획서.md · PRD.md 가 든 내 폴더를 Git으로 기록 시작",
            ["VS Code로 내 프로젝트 폴더 열기", "기획서.md · PRD.md 가 있는지 확인", "Claude Code에 Git 시작 · 첫 커밋 요청",
             "커밋 기록 보기 요청", "PRD 한 줄 고친 뒤 되돌리기 요청"],
            ["커밋 기록에 첫 커밋 1개", "되돌린 뒤 PRD.md 가 커밋 상태와 같음"], files="기획서.md · PRD.md (1-3 · 1-4)"),
        brief(T, T,
              ["폴더 열기 · Claude Code 실행", "Git 시작 + 첫 커밋 요청", "기록 보기", "PRD.md 아무 줄 고치기", "「방금 고친 거 취소」 요청"],
              [("목표", "이 폴더를 Git으로 관리 · 첫 커밋"), ("대상", "기획서.md · PRD.md"), ("메시지", "무엇을 담았는지 한 줄")],
              ["Git 시작", "첫 커밋", "커밋 기록", "되돌리기"],
              ["기록에 내 메시지가 보임", "취소한 줄이 원래대로 돌아옴"],
              "Git이 없다고 나오면 「Git 설치 방법 알려 줘」 · 이름 · 이메일을 물으면 GitHub 가입 정보로"),
        light("실습 1-5 확인", chat([
            ("me", "이 폴더를 Git으로 관리하고, 기획서랑 PRD를 첫 커밋으로 남겨 줘."),
            ("ai", "Git 저장소를 만들고 기획서.md · PRD.md 를 커밋했다.\n메시지: 「기획서 · PRD 첫 버전」")], "첫 커밋 대화 예")
              + code("커밋 기록 · 예", esc("7b21d04  기획서 · PRD 첫 버전"))
              + viz2.tiles([
                  ("커밋 1개", "메시지에 무엇을 담았는지"), ("되돌리기", "PRD.md 가 커밋 상태 그대로"), ("다음 단원", "이 폴더에 앱을 만듦")], 3), T),
    ]
