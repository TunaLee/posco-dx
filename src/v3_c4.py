"""3-4 CLAUDE.md (5분).

배경(긴 작업) → 비유(책상) → 애니메이션(컨텍스트) → CLAUDE.md 정의 · 범위 · 예 · 쓰는 법 → 실습.
사실 출처: code.claude.com/docs/en/memory · code.claude.com/docs/en/context-window
"""
import anim
import viz2
from deck import ba, divider, flow, light
from hx import code, esc, note
from v3kit import SOL, brief

T = "3-4"


def slides():
    md = (SOL / "CLAUDE.md").read_text(encoding="utf-8").strip()
    return [divider("04", "CLAUDE.md", "")] + [
        # ── 배경 → 비유 → 애니메이션
        light("긴 작업에서 생기는 일", viz2.tiles([
            ("처음 정한 규칙을 놓침", "대화가 길어지면 앞부분은 요약으로"), ("새 대화마다 처음부터", "「원본은 고치지 마」를 또 설명"),
            ("파일을 많이 읽으면", "금방 차고 느려짐")], 3), T),
        light("책상 비유", viz2.maprows([
            ("책상 크기", "컨텍스트 한도", "한 번에 읽는 양"), ("늘 펴 둔 메모", "시스템 프롬프트 · CLAUDE.md", "입력 전부터"),
            ("서랍 속 책 목록", "MCP 도구 이름 · Skill 설명", "이름 · 설명만"), ("꺼내 펼친 자료", "읽은 파일 · 도구 결과", "가장 많이 차지"),
            ("책상이 차면 메모 한 장으로 정리", "자동 요약", "한도 근처에서")], "책상", "컨텍스트"), T),
        light("컨텍스트의 구성", anim.context_fill()
              + note("참고", "Claude Code 문서 「Explore the context window」 · NetworkChuck 「Why LLMs get dumb」 · IBM Technology 「What is a Context Window?」"), T),
        # ── CLAUDE.md
        light("대화마다 먼저 읽는 메모", viz2.pair(
            "CLAUDE.md 없이", [("새 대화마다 다시 설명", "「원본은 고치지 마 · 결과는 out/ 에」"), ("설명을 빠뜨리면", "원본에 바로 씀")],
            "CLAUDE.md 있으면", [("대화 시작 때 자동으로 읽음", "요청 전에 규칙이 올라가 있음"), ("요약 뒤에도", "디스크에서 다시 읽어 올림")])
              + note("공식 문서", "새 대화는 빈 컨텍스트로 시작 · CLAUDE.md 가 대화 사이에 규칙을 이어 줌"), T),
        light("CLAUDE.md에 적을 내용", viz2.tiles([
            ("같은 실수가 두 번", "기한 없는 할 일에 날짜를 지어냄"), ("같은 설명을 또 함", "「결과는 out/ 에 저장」"),
            ("새 팀원도 알아야 함", "원본 폴더는 읽기만")], 3)
              + note("공식 문서", "다시 설명하게 되는 것을 적어 두는 곳"), T),
        # ── 범위
        light("적용 범위 세 곳", viz2.tiles([
            ("Project · ./CLAUDE.md", "이 프로젝트 · git으로 팀 공유"), ("User · ~/.claude/CLAUDE.md", "내 모든 프로젝트 · 나만"),
            ("Local · ./CLAUDE.local.md", "이 프로젝트 · 나만 · .gitignore 에 추가")], 3)
              + note("회사 단위", "IT 부서가 까는 관리 정책(Managed policy) CLAUDE.md 도 있음"), T),
        light("범위별 내용", viz2.maprows([
            ("Project", "폴더 규칙 · 판단 기준", "「원본/ 은 읽기만」"), ("User", "내 말투 · 내 습관", "「답은 한국어로 짧게」"),
            ("Local", "나만 쓰는 이 폴더 설정", "내 노션 페이지 주소")], "범위", "넣을 것"), T),
        light("겹친 범위의 읽는 순서", flow([("관리 정책", "회사"), ("User", "~/.claude/"), ("Project", "./CLAUDE.md"), ("Local", "./CLAUDE.local.md")], hl=2)
              + note("모두 읽힘", "넓은 범위부터 차례로 · 서로 어긋나면 어느 쪽을 따를지 모름 → 문장을 맞춰 두기"), T),
        # ── 예 · 쓰는 법
        light("CLAUDE.md 예 · 회의록 정리", code("CLAUDE.md", esc(md))
              + note("네 줄", "폴더 · 판단 기준 · 금지 · 사람이 할 일"), T),
        ba("확인할 수 있는 문장", T, "「정리를 잘 해 줘」\n「파일을 함부로 고치지 마」",
           "「할 일은 담당자 · 기한 · 근거를 함께」\n「원본/ 은 읽기만 · 결과는 out/ 에」",
           "지켰는지 확인할 수 있게 · 공식 문서 권장"),
        light("넣을 것 · 뺄 것", viz2.fit(
            [("폴더 규칙", "원본/ 읽기만 · 결과 out/"), ("판단 기준", "기한 없으면 「기한 미정」"), ("금지", "외부 전달 · 개인정보")],
            [("여러 단계 절차", "Skill 로 (3-5)"), ("한 번만 쓰는 지시", "그 대화에서 말로"), ("반드시 막아야 할 것", "Hook 으로 (3-6)")],
            gt="CLAUDE.md 에 넣을 것", bt="다른 곳으로")
              + note("길이", "공식 권장 200줄 이내 · 길수록 컨텍스트를 차지하고 덜 지킴"), T),
        light("만들고 확인하는 명령", viz2.tiles([
            ("/init", "폴더를 읽고 CLAUDE.md 초안 생성"), ("/memory", "불러온 CLAUDE.md 열어 고치기"), ("/context all", "Memory files 에 올라갔는지 확인")], 3)
              + note("초안 다음", "Claude가 모르는 규칙은 사람이 덧붙임"), T),
        # ── 실습
        brief(T, T,
              ["넣을 규칙 3줄을 메모에 직접 쓰기", "CLAUDE.md 만들기 요청 쓰기", "새 대화에서 11/3 회의록 정리 요청", "결과 위치 · 표시 확인"],
              [("목표", "새 대화마다 같은 규칙으로 시작"), ("입력", "내가 쓴 규칙 3줄"), ("산출물", "폴더 맨 위 CLAUDE.md · 짧게"), ("하지 말 것", "절차 넣기 · 내가 안 쓴 규칙 추가")],
              ["CLAUDE.md", "원본/ 읽기만", "out/", "기한 미정"],
              ["폴더 맨 위에 CLAUDE.md", "10줄 안팎", "새 대화 결과가 <code>out/</code> 에", "정우님 전달 건이 「기한 미정」"],
              "<code>solution/CLAUDE.md</code>"),
    ]
