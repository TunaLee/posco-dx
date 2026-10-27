"""미니 깃 — 내 PC 안의 작은 GitHub (파이썬 표준 라이브러리 + git).

    python server.py            # http://127.0.0.1:8900 · 끄려면 Ctrl+C

git 원격 저장소
    git clone http://127.0.0.1:8900/shop.git                 리뷰용 팀 저장소 (팀원 PR 12개)
    git remote add team http://127.0.0.1:8900/내저장소.git   처음 push 하면 저장소가 생김
    main 이 아닌 브랜치를 push 하면 PR 이 된다

화면    /  저장소 목록 · /r/shop  PR 목록 · /r/shop/pr/104  변경 내용 · 코멘트 · 승인 · 병합
API     GET  /api/repos
        GET  /api/repos/<저장소>/prs                PR 목록
        GET  /api/repos/<저장소>/prs/<번호>         PR 한 건
        GET  /api/repos/<저장소>/prs/<번호>/diff    변경 내용 (unified diff)
        GET  /api/repos/<저장소>/prs/<번호>/files   바뀐 파일 전체 내용
        GET  /api/repos/<저장소>/files/<경로>        main 의 파일
        GET  /api/repos/<저장소>/prs/<번호>/comments
        POST /api/repos/<저장소>/prs/<번호>/comments {"author", "body", "file"?, "line"?}
        POST /api/repos/<저장소>/prs/<번호>/approve  {"reviewer"}
        POST /api/repos/<저장소>/prs/<번호>/merge    {"by"}      승인된 PR 만 · 실제 git merge
        GET  /api/answer                             shop 에 심어 둔 문제 — 채점용 · 리뷰할 때 보지 않는다
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
REPOS = HERE / "repos"
WEB = HERE / "web"
PORT = 8900
sys.path.insert(0, str(HERE / "seed"))


# ── git ─────────────────────────────────────────────
def git(repo, *args, check=True):
    r = subprocess.run(["git", "--git-dir", str(REPOS / f"{repo}.git"), *args], capture_output=True, text=True, encoding="utf-8")
    if check and r.returncode:
        raise RuntimeError(r.stderr.strip())
    return r.stdout


def repo_names():
    return sorted(p.name[:-4] for p in REPOS.glob("*.git"))


def meta_path(repo):
    return REPOS / f"{repo}.meta.json"


def load(repo):
    p = meta_path(repo)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"prs": {}, "comments": {}, "approvals": {}, "merged": {}}


def save(repo, m):
    meta_path(repo).write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")


def sync(repo):
    """main 이 아닌 브랜치마다 PR 번호를 붙인다 · 새로 push 된 브랜치는 다음 번호."""
    m = load(repo)
    fmt = "%(refname:short)\x1f%(authorname)\x1f%(authordate:format:%Y-%m-%d %H:%M)\x1f%(subject)\x1f%(body)\x1e"
    for rec in git(repo, "for-each-ref", "refs/heads", f"--format={fmt}").split("\x1e"):
        f = rec.strip("\n").split("\x1f")
        if len(f) < 5 or f[0] == "main" or f[0] in m["prs"]:
            continue
        nid = max([p["id"] for p in m["prs"].values()] + [0]) + 1
        m["prs"][f[0]] = {"id": nid, "title": f[3], "author": f[1], "created_at": f[2], "description": f[4].strip()}
    save(repo, m)
    return m


def find(repo, n):
    m = sync(repo)
    br = next((b for b, p in m["prs"].items() if p["id"] == n), None)
    return m, br


def diff(repo, m, br):
    if br in m["merged"]:
        return m["merged"][br].get("diff", "")
    return git(repo, "diff", f"main...{br}", check=False)


def summary(repo, m, br):
    p, k = m["prs"][br], br
    d = diff(repo, m, br).splitlines()
    status = "merged" if k in m["merged"] else ("approved" if k in m["approvals"] else "open")
    return {"id": p["id"], "branch": br, "title": p["title"], "author": p["author"], "created_at": p["created_at"], "status": status,
            "additions": sum(1 for l in d if l.startswith("+") and not l.startswith("+++")),
            "deletions": sum(1 for l in d if l.startswith("-") and not l.startswith("---")),
            "comments": len(m["comments"].get(k, []))}


def merge(repo, m, br, by):
    with tempfile.TemporaryDirectory() as w:
        who = ["-c", f"user.name={by}", "-c", "user.email=merge@minigit.local"]
        subprocess.run(["git", "clone", "-q", str(REPOS / f"{repo}.git"), w], check=True, capture_output=True)
        r = subprocess.run(["git", *who, "merge", "--no-ff", f"origin/{br}", "-m", f"Merge PR #{m['prs'][br]['id']} {m['prs'][br]['title']}"],
                           cwd=w, capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError("충돌 · 자동 병합 불가 · " + r.stdout.strip()[-200:])
        subprocess.run(["git", "push", "-q", "origin", "main"], cwd=w, check=True, capture_output=True)


# ── HTTP ────────────────────────────────────────────
GIT_PATH = re.compile(r"^/([\w.-]+)\.git(/.*)$")


class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"

    def send(self, obj, code=200, ctype="application/json"):
        b = obj if isinstance(obj, bytes) else (obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False)).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_OPTIONS(self):
        self.send("")

    def body(self):
        n = int(self.headers.get("Content-Length") or 0)
        return self.rfile.read(n) if n else b""

    def git_http(self, repo, rest):
        """git clone · fetch · push 를 git http-backend 에 넘긴다 (스마트 HTTP)."""
        u = urlsplit(self.path)
        if "git-receive-pack" in (rest + u.query) and not (REPOS / f"{repo}.git").exists():
            subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(REPOS / f"{repo}.git")], check=True)
        data = self.body()
        if self.headers.get("Transfer-Encoding", "").lower() == "chunked":
            data = self.read_chunked()
        env = {**os.environ, "GIT_PROJECT_ROOT": str(REPOS), "GIT_HTTP_EXPORT_ALL": "1", "REMOTE_USER": "student",
               "REMOTE_ADDR": "127.0.0.1", "REQUEST_METHOD": self.command, "PATH_INFO": f"/{repo}.git{rest}",
               "QUERY_STRING": u.query, "CONTENT_TYPE": self.headers.get("Content-Type", ""),
               "CONTENT_LENGTH": str(len(data)), "HTTP_CONTENT_ENCODING": self.headers.get("Content-Encoding", ""),
               "GIT_PROTOCOL": self.headers.get("Git-Protocol", "")}
        r = subprocess.run(["git", "http-backend"], input=data, env=env, capture_output=True)
        head, _, out = r.stdout.partition(b"\r\n\r\n")
        code, hdrs = 200, []
        for line in head.decode("latin-1").split("\r\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                if k.lower() == "status":
                    code = int(v.strip().split()[0])
                else:
                    hdrs.append((k, v.strip()))
        self.send_response(code)
        for k, v in hdrs:
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)

    def read_chunked(self):
        out = b""
        while True:
            n = int(self.rfile.readline().strip() or b"0", 16)
            if n == 0:
                self.rfile.readline()
                return out
            out += self.rfile.read(n)
            self.rfile.readline()

    def do_GET(self):
        path = unquote(urlsplit(self.path).path)
        g = GIT_PATH.match(path)
        if g:
            return self.git_http(g.group(1), g.group(2))
        if path == "/" or path.startswith("/r/"):
            page = "index.html" if path == "/" else ("pr.html" if "/pr/" in path else "repo.html")
            return self.send((WEB / page).read_bytes(), ctype="text/html")
        if path.startswith("/web/"):
            f = (WEB / path[5:]).resolve()
            if f.parent == WEB and f.is_file():
                return self.send(f.read_bytes(), ctype="text/css" if f.suffix == ".css" else "application/javascript")
        try:
            return self.api_get(path.strip("/").split("/"))
        except Exception as e:
            return self.send({"error": str(e)}, 500)

    def api_get(self, p):
        if p == ["api", "repos"]:
            out = []
            for r in repo_names():
                m = sync(r)
                out.append({"name": r, "clone": f"http://127.0.0.1:{PORT}/{r}.git",
                            "prs": len(m["prs"]), "open": sum(1 for b in m["prs"] if b not in m["merged"])})
            return self.send(out)
        if p == ["api", "answer"]:
            import shop_data
            return self.send({"issues": shop_data.ISSUES, "clean": shop_data.CLEAN})
        if len(p) >= 4 and p[:2] == ["api", "repos"] and p[2] in repo_names():
            repo = p[2]
            if p[3] == "prs" and len(p) == 4:
                m = sync(repo)
                return self.send(sorted((summary(repo, m, b) for b in m["prs"]), key=lambda x: x["id"]))
            if p[3] == "files":
                path = "/".join(p[4:])
                return self.send({"path": path, "content": git(repo, "show", f"main:{path}")})
            if p[3] == "prs" and p[4].isdigit():
                m, br = find(repo, int(p[4]))
                if not br:
                    return self.send({"error": f"없는 PR {p[4]}"}, 404)
                if len(p) == 5:
                    return self.send({**summary(repo, m, br), "description": m["prs"][br]["description"]})
                if p[5] == "diff":
                    return self.send(diff(repo, m, br), ctype="text/plain")
                if p[5] == "files":
                    ref = "main" if br in m["merged"] else br
                    names = [n for n in git(repo, "diff", "--name-only", f"main...{br}", check=False).split("\n") if n] or \
                            [l[6:] for l in diff(repo, m, br).splitlines() if l.startswith("+++ b/")]
                    return self.send({n: git(repo, "show", f"{ref}:{n}", check=False) for n in names})
                if p[5] == "comments":
                    return self.send(m["comments"].get(br, []))
        self.send({"error": "없는 주소"}, 404)

    def do_POST(self):
        path = unquote(urlsplit(self.path).path)
        g = GIT_PATH.match(path)
        if g:
            return self.git_http(g.group(1), g.group(2))
        p = path.strip("/").split("/")
        if len(p) == 6 and p[:2] == ["api", "repos"] and p[2] in repo_names() and p[3] == "prs" and p[4].isdigit():
            repo = p[2]
            m, br = find(repo, int(p[4]))
            if not br:
                return self.send({"error": f"없는 PR {p[4]}"}, 404)
            b = json.loads(self.body() or b"{}")
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if p[5] == "comments":
                c = {"author": b.get("author", "?"), "body": b.get("body", ""), "file": b.get("file"), "line": b.get("line"), "at": now}
                m["comments"].setdefault(br, []).append(c); save(repo, m)
                return self.send(c, 201)
            if p[5] == "approve":
                m["approvals"][br] = {"reviewer": b.get("reviewer", "?"), "at": now}; save(repo, m)
                return self.send({"approved": int(p[4])})
            if p[5] == "merge":
                if br not in m["approvals"]:
                    return self.send({"error": "승인되지 않은 PR 은 병합할 수 없음"}, 409)
                if br in m["merged"]:
                    return self.send({"error": "이미 병합됨"}, 409)
                d = diff(repo, m, br)
                try:
                    merge(repo, m, br, b.get("by", "?"))
                except Exception as e:
                    return self.send({"error": str(e)}, 409)
                m["merged"][br] = {"by": b.get("by", "?"), "at": now, "diff": d}; save(repo, m)
                return self.send({"merged": int(p[4])})
        self.send({"error": "없는 주소"}, 404)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    REPOS.mkdir(exist_ok=True)
    if not (REPOS / "shop.git").exists():
        import make_shop
        make_shop.make(REPOS)
        print("shop.git 을 만들었다 · 팀원 PR 12개")
    print(f"미니 깃 · http://127.0.0.1:{PORT} · 끄려면 Ctrl+C")
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
