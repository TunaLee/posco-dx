"""vibe3 3-3 MCP 연결 (20분).

배경(도구 없이 노션 회의록) → 비유(USB-C) → 구조 · 호출 순서(애니메이션) → 서비스별 MCP → 등록 · 확인 → 권한 → 실습.
사실 출처
- MCP 구조 · 호출: modelcontextprotocol.io/docs/learn/architecture
- 등록 · 범위 · 상태: code.claude.com/docs/en/mcp
- 권한 규칙: code.claude.com/docs/en/permissions (deny → ask → allow · mcp__<서버>__<도구>)
- 노션: developers.notion.com/guides/mcp/get-started-with-mcp · tools-search · tools-pages
- 슬랙: docs.slack.dev/ai/mcp-server
- 구글 드라이브: developers.google.com/workspace/drive/api/guides/configure-mcp-server
"""
import anim
import mcp_fig
import viz2
from deck import divider, lab, light
from hx import code, esc, note
from v3kit import F, brief, pick

T = "3-3"


def _perm(deny=(), ask=()):
    rows = []
    if deny:
        rows.append('    "deny": [\n' + ",\n".join(f'      "{x}"' for x in deny) + "\n    ]")
    if ask:
        rows.append('    "ask": [\n' + ",\n".join(f'      "{x}"' for x in ask) + "\n    ]")
    return '{\n  "permissions": {\n' + ",\n".join(rows) + "\n  }\n}"


def _ba(title, ch, before, after, nlabel, ntext):
    """Before → After 두 칸 + 일반 메모 (deck.ba 의 메모는 「구성」 라벨이 고정이라 따로)."""
    b, a = before.replace("\n", "<br/>"), after.replace("\n", "<br/>")
    return light(title, f'<div class="ba"><div class="b"><div class="lab">Before</div><div class="q">{b}</div></div>'
                 f'<div class="arr">→</div><div class="a"><div class="lab">After</div><div class="q">{a}</div></div></div>'
                 + note(nlabel, ntext), ch)


def slides():
    t = T
    return [divider("03", "MCP 연결", "")] + [
        # ── 배경 ──
        pick("도구가 필요한 이유", t),
        light("노션에 있는 회의록", viz2.pair(
            "도구 없이", [("회의록 위치", "노션 페이지 · Claude는 열지 못함"), ("사람이 하는 일", "페이지 복사 → 대화창에 붙여 넣기"),
                        ("다음 회의록도", "같은 복사 · 붙여 넣기")],
            "노션 도구가 있으면", [("찾기", "notion-search · 제목으로 페이지 찾기"), ("읽기", "notion-fetch · 페이지 내용 가져오기"),
                              ("다음 회의록도", "「11/17 회의록 정리해 줘」 한 줄")])
              + note("도구", "Claude Code 밖의 서비스를 읽고 쓰게 하는 손"), t),
        light("내장 도구와 외부 도구", viz2.pair(
            "Claude Code 내장 도구", [("Read · Write · Edit", "내 PC 파일 읽기 · 쓰기 · 고치기"), ("Glob · Grep", "파일 · 글자 찾기"),
                                   ("Bash · WebFetch", "명령 실행 · 웹 페이지 읽기")],
            "외부 도구 · MCP로 연결", [("노션", "회의록 · 문서"), ("슬랙", "채널 · 메시지"), ("구글 드라이브", "공유 파일")]), t),
        light("연결 규격의 부재", mcp_fig.tangle(("노션", "슬랙", "구글 드라이브"))
              + note("MCP", "Model Context Protocol · 도구 목록 · 호출 · 결과 전달 형식을 하나로"), t),
        # ── 비유 ──
        light("USB-C 비유", viz2.maprows([
            ("노트북", "Claude Code", "MCP 호스트"), ("USB-C 포트 규격", "MCP", "주고받는 순서 · 형식"),
            ("모니터 · 외장 디스크", "MCP 서버", "노션 · 슬랙 · 드라이브"), ("꽂으면 할 수 있는 일을 알림", "도구 목록", "notion-search · notion-fetch …"),
            ("기기마다 케이블 하나", "서버마다 클라이언트 하나", "")], "USB-C", "MCP")
              + note("공식 소개", "modelcontextprotocol.io — 「AI 앱을 위한 USB-C 포트」"), t),
        # ── 구조 ──
        light("MCP 서버와 MCP 클라이언트", viz2.tiles([
            ("MCP 서버", "도구를 내주는 쪽 · 노션 · 슬랙 · 드라이브"), ("MCP", "주고받는 순서 · 형식의 규격"), ("MCP 클라이언트", "도구를 쓰는 쪽 · Claude Code 안")], 3)
              + note("서버마다 하나", "Claude Code(호스트)가 연결한 서버 수만큼 클라이언트를 만듦"), t),
        light("서버가 보내는 도구 목록 예", code("노션 MCP · 도구 목록 일부", esc(
            "notion-search      페이지 · 데이터베이스를 제목이나 주제로 찾기\n"
            "notion-fetch       페이지 · 데이터베이스 내용 열기\n"
            "notion-query-meeting-notes   회의록을 제목 등으로 찾기\n"
            "notion-create-pages          새 페이지 만들기\n"
            "notion-update-page           페이지 내용 · 속성 고치기"))
              + note("고르는 기준", "Claude는 도구 이름 · 설명만 보고 무엇을 부를지 정함"), t),
        light("MCP 호출 순서", anim.mcp_call()
              + note("참고", "MCP 공식 문서 「Architecture overview」 · IBM Technology 「What is MCP?」 · ByteByteGo 「Why Everyone's Talking About MCP?」"), t),
        light("로컬 서버와 URL 서버", viz2.pair(
            "로컬 · 내 PC에서 실행", [("예", "내 PC 파일 · 사내 DB"), ("등록", "<code>claude mcp add 이름 -- 실행 명령</code>")],
            "URL · 인터넷 주소로 접속", [("예", "노션 · 슬랙 · 구글 드라이브"), ("등록", "<code>claude mcp add --transport http 이름 주소</code>")])
              + note("업무 서비스", "대부분 URL 연결 · 로그인은 /mcp 에서"), t),
        light("연결 범위 세 곳", viz2.tiles([
            ("Local · 기본", "이 프로젝트 · 나만 · <code>~/.claude.json</code>"), ("Project", "이 프로젝트 · 팀 공유 · <code>.mcp.json</code>"),
            ("User", "내 모든 프로젝트 · 나만 · <code>~/.claude.json</code>")], 3)
              + note("고르는 법", "등록할 때 <code>--scope project</code> 처럼 붙임 · 팀이 같이 쓸 연결만 Project"), t),
        # ── 업무 도구별 ──
        light("노션 MCP", viz2.pair(
            "읽기 도구", [("notion-search", "제목 · 주제로 찾기"), ("notion-fetch", "페이지 열기"), ("notion-query-meeting-notes", "회의록 찾기")],
            "쓰기 도구", [("notion-create-pages", "새 페이지"), ("notion-update-page", "내용 · 속성 고치기"), ("notion-delete-pages", "휴지통으로")], hl="l")
              + note("주소 · 로그인", "<code>https://mcp.notion.com/mcp</code> · OAuth 로그인"), t),
        light("슬랙 MCP", viz2.pair(
            "읽기", [("검색", "메시지 · 파일 · 채널 · 사용자"), ("읽기", "채널 · 스레드 · 캔버스")],
            "쓰기", [("보내기", "메시지 보내기 · 예약"), ("만들기", "채널 · 캔버스 · 리액션")], hl="l")
              + note("주소 · 승인", "<code>https://mcp.slack.com/mcp</code> · 워크스페이스 관리자가 앱 승인"), t),
        light("구글 드라이브 MCP", viz2.pair(
            "읽기", [("search_files", "파일 찾기"), ("read_file_content", "파일 내용 읽기"), ("get_file_metadata", "파일 정보")],
            "쓰기 · 동작", [("create_file", "파일 만들기"), ("copy_file", "파일 복사"), ("download_file_content", "내용 내려받기")], hl="l")
              + note("주소 · 조건", "<code>https://drivemcp.googleapis.com/mcp/v1</code> · Developer Preview · Google Cloud 프로젝트와 OAuth 클라이언트 필요"), t),
        light("서비스별 연결 조건", viz2.tiles([
            ("노션", "OAuth 로그인 · 관리자가 MCP 연결을 막을 수 있음 · 게스트는 연결 불가"),
            ("슬랙", "OAuth 로그인 · 관리자가 앱 승인 · 마켓플레이스 앱 · 사내 앱만"),
            ("구글 드라이브", "Developer Preview 신청 · Cloud 프로젝트에서 API 켜기 · OAuth 클라이언트")], 3)
              + note("실습", "가장 가벼운 노션으로 · 막히면 <code>labs/meeting_agent/원본/</code>"), t),
        # ── 등록 · 확인 ──
        light("노션 MCP 등록 순서", code("터미널 · 한 번만", esc("claude mcp add --transport http notion https://mcp.notion.com/mcp"))
              + viz2.tiles([("① 등록", "위 명령 한 줄 · 또는 Claude에게 요청"), ("② 로그인", "/mcp → notion → 브라우저 로그인"),
                            ("③ 허용", "읽을 워크스페이스 선택"), ("④ 확인", "/mcp 에 연결 표시")], 4), t),
        light("연결 상태 확인", viz2.tiles([
            ("Connected", "연결됨 · 바로 사용"), ("Needs authentication", "로그인 필요 · /mcp 에서 로그인"), ("Failed to connect", "연결 실패 · 주소 · 네트워크 확인")], 3)
              + note("보는 곳", "터미널 <code>claude mcp list</code> · 대화 안 <code>/mcp</code>"), t),
        light("회사 계정 연결 제한", viz2.tiles([
            ("관리자 허용 요청", "워크스페이스의 외부 연결 허용"), ("개인 공간으로 복제", "읽을 페이지만 복제해 연결"), ("내보내기 파일", "Markdown으로 받아 폴더에")], 3)
              + note("실제 사례", "회사 워크스페이스는 연결 거절 → 페이지를 개인 공간으로 복제하자 연결됨"), t),
        light("연결 전 확인", viz2.tiles([
            ("공식 주소인가", "서비스 공식 문서의 MCP 주소"), ("무엇을 읽어 오나", "밖의 글을 가져오는 서버 · 글 속 지시가 섞일 수 있음"),
            ("어떤 쓰기 도구가 있나", "고치기 · 지우기 · 보내기")], 3)
              + note("Claude Code 문서", "믿을 수 있는 서버만 연결 · 밖의 글을 가져오는 서버는 프롬프트 주입 위험"), t),
        # ── 권한 ──
        light("필요한 도구만 열기", viz2.pair(
            "열어 둘 것", [("찾기 · 읽기", "notion-search · notion-fetch"), ("이유", "회의록을 읽어야 정리 가능")],
            "막을 것", [("고치기 · 지우기", "notion-update-page · notion-delete-pages"), ("만들기", "notion-create-pages · 정리는 out/ 파일로")])
              + note("기준", "실습 업무에 필요 없는 쓰기 도구는 처음부터 닫기"), t),
        light("쓰기 도구 막기 예", code(".claude/settings.json", esc(_perm(
            deny=("mcp__notion__notion-update-page", "mcp__notion__notion-delete-pages", "mcp__notion__notion-create-pages"))))
              + note("이름 규칙", "<code>mcp__서버이름__도구이름</code> · <code>mcp__notion__*</code> = 노션 도구 전부 · 판단 순서는 3-6"), t),
        # ── 실습 ──
        lab("3-3", "노션 MCP 붙이기", t, "노션을 Claude Code에 붙여 회의록을 직접 읽게",
            ["회의록 하나를 내 노션에 붙여 넣기", "노션 MCP 연결 · 로그인", "회의록 페이지 읽기", "쓰기 도구 막기"],
            ["답 위 노션 도구 호출", "쓰기 도구 막힘"], files=F, mine="내 업무에 붙일 도구 하나"),
        brief("3-3", t,
              ["11/10 회의록을 내 노션에 붙여 넣기", "연결 요청 쓰기 → <code>/mcp</code> 로그인", "새 대화 · 읽기 요청 쓰기", "막을 도구 정해 요청"],
              [("목표", "노션의 회의록을 읽어 할 일 뽑기"), ("입력", "어느 페이지인지 · 제목 · 날짜"), ("산출물", "할 일 · 담당 · 기한"), ("하지 말 것", "노션에 쓰기 · 페이지 수정")],
              ["노션 MCP", "읽기만", "쓰기 도구 막기", "/mcp"],
              ["<code>/mcp</code> 에 notion 연결 표시", "답 위 노션 호출 표시", "쓰기 도구가 막혔는가", "페이지를 바꾸지 않았는가"],
              "회사 노션이 막혔으면 <code>labs/meeting_agent/원본/</code> 으로 계속"),
        _ba("실습 3-3 결과 비교", t,
           "회의록 내용을 복사해 대화창에 붙여 넣음\n노션 쓰기 도구도 열려 있음",
           "「11/10 회의록 정리해 줘」 → notion-search · notion-fetch 호출\n쓰기 요청 → deny 규칙으로 거부",
           "볼 곳", "답 위 도구 호출 표시 · <code>.claude/settings.json</code> 의 deny 세 줄"),
    ]
