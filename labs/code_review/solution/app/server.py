"""리뷰 콘솔 — 실습마다 탭이 하나씩 늘어나는 화면 (파이썬 표준 라이브러리만).

    python app/server.py        # http://127.0.0.1:8810

탭 하나 = app/tabs/ 의 HTML 파일 하나. 파일을 넣으면 새로 고침 없이 탭이 생긴다.
탭이 읽을 수 있는 주소
    /repo/<경로>       팀 코드 저장소 API (127.0.0.1:8900/api/<경로>)
    /files/data/...    기록(JSON · JSONL)   · 폴더면 파일 목록
    /files/out/...     보고서(Markdown)      · 폴더면 파일 목록
"""
import json
import re
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

APP = Path(__file__).resolve().parent
ROOT = APP.parent
REPO = "http://127.0.0.1:8900/api/"
READABLE = ("data", "out")
TYPES = {".json": "application/json", ".html": "text/html", ".md": "text/plain", ".jsonl": "text/plain", ".csv": "text/plain"}


def tabs():
    out = []
    for f in sorted((APP / "tabs").glob("*.html")):
        m = re.search(r"<title>(.*?)</title>", f.read_text(encoding="utf-8", errors="ignore"), re.S)
        out.append({"file": f.name, "title": (m.group(1).strip() if m else f.stem), "mtime": f.stat().st_mtime})
    return out


class H(SimpleHTTPRequestHandler):
    def send(self, body, ctype="application/json", code=200):
        b = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        u = urlsplit(self.path)
        path = unquote(u.path)
        if path in ("/", "/index.html"):
            return self.send((APP / "index.html").read_bytes(), "text/html")
        if path == "/tabs.json":
            return self.send(json.dumps(tabs(), ensure_ascii=False))
        if path.startswith("/tabs/"):
            f = (APP / "tabs" / path[6:]).resolve()
            if f.parent == (APP / "tabs").resolve() and f.is_file():
                return self.send(f.read_bytes(), "text/html")
        if path.startswith("/repo/"):
            try:
                with urllib.request.urlopen(REPO + path[6:] + (f"?{u.query}" if u.query else ""), timeout=5) as r:
                    return self.send(r.read(), r.headers.get_content_type())
            except Exception as e:
                return self.send(json.dumps({"error": f"저장소 연결 실패 · {e}"}, ensure_ascii=False), code=502)
        if path.startswith("/files/"):
            rel = path[7:]
            f = (ROOT / rel).resolve()
            if rel.split("/")[0] in READABLE and ROOT.resolve() in f.parents:
                if f.is_dir():
                    items = [{"name": x.name, "dir": x.is_dir(), "mtime": x.stat().st_mtime}
                             for x in sorted(f.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True) if not x.name.startswith(".")]
                    return self.send(json.dumps(items, ensure_ascii=False))
                if f.is_file():
                    return self.send(f.read_bytes(), TYPES.get(f.suffix, "text/plain"))
                return self.send(json.dumps({"error": "아직 없음"}, ensure_ascii=False), code=404)
        self.send(json.dumps({"error": "없는 주소"}, ensure_ascii=False), code=404)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "out").mkdir(exist_ok=True)
    print("리뷰 콘솔 · http://127.0.0.1:8810 · 끄려면 Ctrl+C")
    ThreadingHTTPServer(("127.0.0.1", 8810), H).serve_forever()
