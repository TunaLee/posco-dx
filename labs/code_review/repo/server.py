"""팀 코드 저장소 서버 — 팀원 PR 을 보고 리뷰 코멘트 · 승인 · 병합을 받는 작은 저장소 (파이썬 표준 라이브러리만).

    python repo/server.py        # http://127.0.0.1:8900 · 끄려면 Ctrl+C

주소
    GET  /api/prs                    PR 목록
    GET  /api/prs/<번호>             PR 한 건 (설명 · 바뀐 파일)
    GET  /api/prs/<번호>/diff        변경 내용 (unified diff)
    GET  /api/prs/<번호>/files       바뀐 파일 전체 내용
    GET  /api/files/<경로>           main 브랜치 파일
    GET  /api/prs/<번호>/comments    리뷰 코멘트
    POST /api/prs/<번호>/comments    {"author", "body", "file"?, "line"?}
    POST /api/prs/<번호>/approve     {"reviewer"}       승인
    POST /api/prs/<번호>/merge       {"by"}             병합 (승인된 PR 만)
    GET  /api/answer                 심어 둔 문제 목록 — 채점용 · 리뷰할 때는 보지 않는다
"""
import difflib
import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

import data

STATE = Path(__file__).resolve().parent.parent / "data" / "repo_state.json"   # 코멘트 · 승인 · 병합 기록


def load():
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"comments": {}, "approvals": {}, "merged": {}}


def save(st):
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")


def pr(n):
    return next((p for p in data.PRS if p["id"] == n), None)


def diff(p):
    out = []
    for path, new in p["files"].items():
        old = data.BASE.get(path, "")
        out += difflib.unified_diff(old.splitlines(True), new.splitlines(True),
                                    f"a/{path}" if old else "/dev/null", f"b/{path}")
    return "".join(out)


def summary(p, st):
    d = diff(p).splitlines()
    k = str(p["id"])
    status = "merged" if k in st["merged"] else ("approved" if k in st["approvals"] else "open")
    return {"id": p["id"], "title": p["title"], "author": p["author"], "created_at": p["created_at"], "status": status,
            "files": list(p["files"]), "additions": sum(1 for l in d if l.startswith("+") and not l.startswith("+++")),
            "deletions": sum(1 for l in d if l.startswith("-") and not l.startswith("---")),
            "comments": len(st["comments"].get(k, []))}


PAGE = """<!doctype html><meta charset="utf-8"><title>팀 코드 저장소</title>
<style>body{font-family:-apple-system,"Malgun Gothic",sans-serif;margin:32px;color:#16233A}td,th{padding:6px 12px;border-bottom:1px solid #eee;text-align:left}</style>
<h2>팀 코드 저장소 · shop</h2><p>실습용 가상 자료 · API 는 <code>/api/prs</code></p><table id=t></table>
<script>fetch('/api/prs').then(r=>r.json()).then(ps=>{t.innerHTML='<tr><th>#</th><th>제목</th><th>작성자</th><th>상태</th><th>+/-</th></tr>'+
ps.map(p=>`<tr><td>${p.id}</td><td>${p.title}</td><td>${p.author}</td><td>${p.status}</td><td>+${p.additions} -${p.deletions}</td></tr>`).join('')})</script>"""


class H(BaseHTTPRequestHandler):
    def send(self, obj, code=200, ctype="application/json"):
        b = (obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False)).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(b)

    def do_OPTIONS(self):
        self.send("")

    def parts(self):
        return [unquote(x) for x in urlsplit(self.path).path.strip("/").split("/")]

    def do_GET(self):
        p = self.parts(); st = load()
        if p == [""]:
            return self.send(PAGE, ctype="text/html")
        if p == ["api", "prs"]:
            return self.send([summary(x, st) for x in data.PRS])
        if p == ["api", "answer"]:
            return self.send({"issues": data.ISSUES, "clean": data.CLEAN})
        if p[:2] == ["api", "files"]:
            path = "/".join(p[2:])
            return self.send({"path": path, "content": data.BASE[path]}) if path in data.BASE else self.send({"error": f"없는 파일 {path}"}, 404)
        if len(p) >= 3 and p[:2] == ["api", "prs"] and p[2].isdigit():
            x = pr(int(p[2]))
            if not x:
                return self.send({"error": f"없는 PR {p[2]}"}, 404)
            if len(p) == 3:
                return self.send({**summary(x, st), "description": x["description"]})
            if p[3] == "diff":
                return self.send(diff(x), ctype="text/plain")
            if p[3] == "files":
                return self.send(x["files"])
            if p[3] == "comments":
                return self.send(st["comments"].get(p[2], []))
        self.send({"error": "없는 주소"}, 404)

    def do_POST(self):
        p = self.parts(); st = load()
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
        if len(p) == 4 and p[:2] == ["api", "prs"] and p[2].isdigit() and pr(int(p[2])):
            k, now = p[2], datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if p[3] == "comments":
                c = {"author": body.get("author", "?"), "body": body.get("body", ""), "file": body.get("file"), "line": body.get("line"), "at": now}
                st["comments"].setdefault(k, []).append(c); save(st)
                return self.send(c, 201)
            if p[3] == "approve":
                st["approvals"][k] = {"reviewer": body.get("reviewer", "?"), "at": now}; save(st)
                return self.send({"approved": int(k)})
            if p[3] == "merge":
                if k not in st["approvals"]:
                    return self.send({"error": "승인되지 않은 PR 은 병합할 수 없음"}, 409)
                st["merged"][k] = {"by": body.get("by", "?"), "at": now}; save(st)
                return self.send({"merged": int(k)})
        self.send({"error": "없는 주소"}, 404)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print("팀 코드 저장소 · http://127.0.0.1:8900 · 끄려면 Ctrl+C")
    ThreadingHTTPServer(("127.0.0.1", 8900), H).serve_forever()
