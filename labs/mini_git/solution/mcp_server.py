"""미니 깃 MCP 서버 (강사용 완성본 · 수업에서는 Claude Code 로 직접 만든다).

Claude Code 가 표준 입출력(stdio)으로 띄워 쓰는 MCP 서버. 파이썬 표준 라이브러리만 쓴다.
    claude mcp add repo -- python solution/mcp_server.py
도구마다 repo 인자 (기본 shop)

도구
    list_prs           PR 목록 · 상태 · 변경 줄 수
    get_pr             PR 한 건 설명
    get_diff           PR 변경 내용 전체 (원문 · 큼)
    changed_functions  바뀐 함수만 (컨텍스트를 아끼는 도구 · 실습 5-1)
    get_comments       리뷰 코멘트 목록
    add_comment        리뷰 코멘트 남기기
    approve_pr         승인            ← Hook 으로 사람만 (실습 4-2)
    merge_pr           병합            ← Hook 으로 사람만
호출마다 data/mcp_calls.jsonl 에 한 줄 (콘솔 탭 ② 도구 호출)
"""
import json
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

BASE = "http://127.0.0.1:8900/api/repos"
DATA = Path(__file__).resolve().parent.parent / "data"   # 미니 깃 폴더의 data/
CALLS = DATA / "mcp_calls.jsonl"

REPO = {"type": "string", "description": "저장소 이름 · 기본 shop"}
PR = {"type": "object", "properties": {"repo": REPO, "pr": {"type": "integer", "description": "PR 번호 · 예: 104"}}, "required": ["pr"]}
TOOLS = [
    {"name": "list_repos", "description": "미니 깃의 저장소 목록.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "list_prs", "description": "저장소의 PR 목록 (번호 · 제목 · 작성자 · 상태 · 변경 줄 수 · 코멘트 수).",
     "inputSchema": {"type": "object", "properties": {"repo": REPO}}},
    {"name": "get_pr", "description": "PR 한 건의 설명과 바뀐 파일 목록.", "inputSchema": PR},
    {"name": "get_diff", "description": "PR 의 변경 내용 전체(unified diff). 크다 · 필요할 때만.", "inputSchema": PR},
    {"name": "changed_functions", "description": "PR 에서 추가 · 변경된 함수만 골라 돌려준다. 리뷰는 이걸 먼저 쓴다.", "inputSchema": PR},
    {"name": "get_comments", "description": "PR 에 달린 리뷰 코멘트.", "inputSchema": PR},
    {"name": "add_comment", "description": "PR 에 리뷰 코멘트를 남긴다.",
     "inputSchema": {"type": "object", "properties": {
         "repo": REPO, "pr": {"type": "integer"}, "body": {"type": "string", "description": "코멘트 내용"},
         "file": {"type": "string"}, "line": {"type": "integer"}, "author": {"type": "string", "description": "기본 claude"}},
         "required": ["pr", "body"]}},
    {"name": "approve_pr", "description": "PR 을 승인한다.",
     "inputSchema": {"type": "object", "properties": {"repo": REPO, "pr": {"type": "integer"}, "reviewer": {"type": "string"}}, "required": ["pr"]}},
    {"name": "merge_pr", "description": "승인된 PR 을 병합한다.",
     "inputSchema": {"type": "object", "properties": {"repo": REPO, "pr": {"type": "integer"}, "by": {"type": "string"}}, "required": ["pr"]}},
]


def api(path, body=None):
    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Content-Type": "application/json"}, method="POST" if body is not None else "GET")
    with urllib.request.urlopen(req, timeout=5) as r:
        raw = r.read().decode("utf-8")
        return json.loads(raw) if r.headers.get_content_type() == "application/json" else raw


def changed_functions(r, pr):
    """diff 에서 + 줄이 들어 있는 함수만 · 새 파일 내용에서 그 함수 전체를 잘라 돌려준다."""
    files = api(f"/{r}/prs/{pr}/files")
    diff = api(f"/{r}/prs/{pr}/diff")
    out = []
    for path, text in files.items():
        added = {l[1:].strip() for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++") and l[1:].strip()}
        blocks = re.split(r"(?m)^(?=def |class )", text)
        top = [l for l in blocks[0].splitlines() if l.strip() in added]          # 함수 밖에서 바뀐 줄 (상수 · 키 · import)
        if top:
            out.append({"file": path, "code": "\n".join(top)})
        for b in blocks:
            if b.startswith(("def ", "class ")) and any(a in b for a in added):
                out.append({"file": path, "code": b.rstrip()})
        if not any(o["file"] == path for o in out) and path.endswith((".md", ".txt")):
            out.append({"file": path, "code": "(문서 파일 · 코드 아님)"})
    return out


def call(name, a):
    r = a.get("repo") or "shop"
    if name == "list_repos":
        return api("")
    if name == "list_prs":
        return api(f"/{r}/prs")
    n = int(a["pr"])
    if name == "get_pr":
        return api(f"/{r}/prs/{n}")
    if name == "get_diff":
        return api(f"/{r}/prs/{n}/diff")
    if name == "changed_functions":
        return changed_functions(r, n)
    if name == "get_comments":
        return api(f"/{r}/prs/{n}/comments")
    if name == "add_comment":
        return api(f"/{r}/prs/{n}/comments", {"author": a.get("author", "claude"), "body": a["body"], "file": a.get("file"), "line": a.get("line")})
    if name == "approve_pr":
        return api(f"/{r}/prs/{n}/approve", {"reviewer": a.get("reviewer", "claude")})
    if name == "merge_pr":
        return api(f"/{r}/prs/{n}/merge", {"by": a.get("by", "claude")})
    raise ValueError(f"없는 도구 {name}")


def log(tool, args, size):
    DATA.mkdir(exist_ok=True)
    with CALLS.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"at": datetime.now().strftime("%H:%M:%S"), "tool": tool, "args": args, "bytes": size}, ensure_ascii=False) + "\n")


def reply(id_, result=None, error=None):
    msg = {"jsonrpc": "2.0", "id": id_}
    msg.update({"error": error} if error else {"result": result})
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            m = json.loads(line)
        except ValueError:
            continue
        method, id_ = m.get("method"), m.get("id")
        if id_ is None:            # 알림(notifications/initialized 등)은 답하지 않는다
            continue
        if method == "initialize":
            reply(id_, {"protocolVersion": m.get("params", {}).get("protocolVersion", "2025-06-18"),
                        "capabilities": {"tools": {}}, "serverInfo": {"name": "repo", "version": "0.1.0"}})
        elif method == "tools/list":
            reply(id_, {"tools": TOOLS})
        elif method == "tools/call":
            p = m.get("params", {})
            try:
                out = call(p.get("name"), p.get("arguments") or {})
                text = out if isinstance(out, str) else json.dumps(out, ensure_ascii=False)
                log(p.get("name"), p.get("arguments") or {}, len(text.encode("utf-8")))
                reply(id_, {"content": [{"type": "text", "text": text}]})
            except Exception as e:  # 도구 오류는 모델이 읽을 수 있게 결과로
                reply(id_, {"content": [{"type": "text", "text": f"오류: {e}"}], "isError": True})
        elif method == "ping":
            reply(id_, {})
        else:
            reply(id_, error={"code": -32601, "message": f"지원하지 않는 메서드 {method}"})


if __name__ == "__main__":
    main()
