"""기계적으로 찾을 수 있는 문제만 코드로 검사 (강사용 완성본 · 실습 7-1).

LLM 은 이 결과를 받아 「진짜 문제인지 · 어떻게 고칠지」만 판단한다.
    python solution/checks.py
"""
import json
import re
import urllib.request

RULES = [
    ("보안", "비밀 키 하드코딩", re.compile(r"(sk_live_|api[_-]?key\s*=\s*[\"'][^\"']{8,})", re.I)),
    ("보안", "SQL 문자열 조립", re.compile(r"f[\"']\s*(SELECT|INSERT|UPDATE|DELETE)\b", re.I)),
    ("버그", "예외 무시", re.compile(r"except[^:]*:\s*\n\s*pass")),
    ("버그", "가변 기본 인자", re.compile(r"def \w+\([^)]*=\s*(\{\}|\[\])")),
    ("보안", "비밀번호 로그", re.compile(r"log\.\w+\([^)]*password", re.I)),
]

prs = json.loads(urllib.request.urlopen("http://127.0.0.1:8900/api/repos/shop/prs", timeout=5).read())
out = []
for p in prs:
    files = json.loads(urllib.request.urlopen(f"http://127.0.0.1:8900/api/repos/shop/prs/{p['id']}/files", timeout=5).read())
    for path, text in files.items():
        for kind, name, rx in RULES:
            for m in rx.finditer(text):
                out.append({"pr": p["id"], "kind": kind, "rule": name, "file": path, "line": text[:m.start()].count("\n") + 1})
print(json.dumps(out, ensure_ascii=False, indent=1))
