"""미니 깃 MCP 서버 (강사용 완성본 · 수업에서는 Claude Code 로 직접 만든다).

GitHub 공식 MCP 서버(github/github-mcp-server)의 도구 이름 · 모양을 따른다 → 진짜 GitHub 로 바꿔도 Skill · Hook 을 그대로.
    claude mcp add repo -- python solution/mcp_server.py

도구 (repo 인자 · 기본 shop)
    list_pull_requests          PR 목록
    pull_request_read           method: get · get_diff · get_files · get_comments
    get_changed_functions       바뀐 함수만 (GitHub 에 없는 우리 도구 · 컨텍스트 절약 · 실습 5-1)
    create_pull_request         push 한 브랜치에 제목 · 설명
    add_comment_to_pending_review  파일 · 줄에 리뷰 코멘트
    pull_request_review_write   리뷰 제출 · event APPROVE 면 승인   ← Hook 으로 사람만 (실습 4-4)
    merge_pull_request          병합                                ← Hook 으로 사람만
    list_branches · list_commits · get_file_contents
호출마다 data/mcp_calls.jsonl 에 한 줄
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
R = {"repo": {"type": "string", "description": "저장소 이름 · 기본 shop"}}
N = {**R, "pullNumber": {"type": "integer", "description": "PR 번호 · 예: 104"}}


def obj(props, req=()):
    return {"type": "object", "properties": props, "required": list(req)}


TOOLS = [
    {"name": "list_pull_requests", "description": "저장소의 PR 목록 (번호 · 제목 · 작성자 · 상태 · 변경 줄 수 · 코멘트 수).",
     "inputSchema": obj({**R, "state": {"type": "string", "description": "open · merged · all (기본 all)"}})},
    {"name": "pull_request_read", "description": "PR 한 건 읽기. method: get(설명) · get_diff(변경 전체 · 큼) · get_files(바뀐 파일 전체) · get_comments(리뷰 코멘트).",
     "inputSchema": obj({**N, "method": {"type": "string", "enum": ["get", "get_diff", "get_files", "get_comments"]}}, ["pullNumber", "method"])},
    {"name": "get_changed_functions", "description": "PR 에서 바뀐 함수 · 바뀐 줄만. 리뷰는 이걸 먼저 쓴다.", "inputSchema": obj(N, ["pullNumber"])},
    {"name": "create_pull_request", "description": "push 한 브랜치(head)에 PR 제목 · 설명을 붙인다.",
     "inputSchema": obj({**R, "head": {"type": "string"}, "title": {"type": "string"}, "body": {"type": "string"}}, ["head", "title"])},
    {"name": "add_comment_to_pending_review", "description": "PR 의 파일 · 줄에 리뷰 코멘트를 단다.",
     "inputSchema": obj({**N, "body": {"type": "string"}, "path": {"type": "string"}, "line": {"type": "integer"}}, ["pullNumber", "body"])},
    {"name": "pull_request_review_write", "description": "리뷰를 제출한다. event: COMMENT · APPROVE.",
     "inputSchema": obj({**N, "event": {"type": "string", "enum": ["COMMENT", "APPROVE"]}, "body": {"type": "string"}}, ["pullNumber", "event"])},
    {"name": "merge_pull_request", "description": "승인된 PR 을 병합한다.", "inputSchema": obj(N, ["pullNumber"])},
    {"name": "list_branches", "description": "브랜치 목록.", "inputSchema": obj(R)},
    {"name": "list_commits", "description": "커밋 이력 (최근 20개).", "inputSchema": obj({**R, "ref": {"type": "string"}})},
    {"name": "get_file_contents", "description": "파일 내용.", "inputSchema": obj({**R, "path": {"type": "string"}, "ref": {"type": "string"}}, ["path"])},
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
    if name == "list_pull_requests":
        prs = api(f"/{r}/prs"); st = a.get("state") or "all"
        return prs if st == "all" else [x for x in prs if (x["status"] == "merged") == (st == "merged")]
    if name == "list_branches":
        return api(f"/{r}/branches")
    if name == "list_commits":
        return api(f"/{r}/commits?ref={a.get('ref') or 'main'}")
    if name == "get_file_contents":
        return api(f"/{r}/files/{a['path']}?ref={a.get('ref') or 'main'}")
    if name == "create_pull_request":
        return api(f"/{r}/prs", {"head": a["head"], "title": a["title"], "body": a.get("body", "")})
    n = int(a["pullNumber"])
    if name == "pull_request_read":
        return api(f"/{r}/prs/{n}" + {"get": "", "get_diff": "/diff", "get_files": "/files", "get_comments": "/comments"}[a.get("method", "get")])
    if name == "get_changed_functions":
        return changed_functions(r, n)
    if name == "add_comment_to_pending_review":
        return api(f"/{r}/prs/{n}/comments", {"author": "claude", "body": a["body"], "file": a.get("path"), "line": a.get("line")})
    if name == "pull_request_review_write":
        if a.get("event") == "APPROVE":
            return api(f"/{r}/prs/{n}/approve", {"reviewer": "claude"})
        return api(f"/{r}/prs/{n}/comments", {"author": "claude", "body": a.get("body", "")})
    if name == "merge_pull_request":
        return api(f"/{r}/prs/{n}/merge", {"by": "claude"})
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
