"""루프 하네스 실행기 — features.json 이 모두 통과하거나 최대 횟수가 될 때까지
PROMPT.md 를 새 세션(claude -p)으로 반복 실행한다. 매번 새 세션이라 컨텍스트가 쌓이지 않는다.
Claude Code 로그인 계정으로 돈다 (API 키 불필요).
    python loop.py 5        # 최대 5회
"""
import json
import subprocess
import sys
import time
from pathlib import Path

MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 5
TOOLS = ["Read", "Write", "Edit", "Grep", "Glob", "Bash(python:*)", "Bash(python3:*)", "Bash(curl:*)",
         "Bash(git add:*)", "Bash(git commit:*)", "Bash(git checkout:*)", "Bash(git push:*)", "Bash(git status:*)", "Bash(git log:*)"]


def left():
    return [f for f in json.loads(Path("features.json").read_text(encoding="utf-8")) if not f["passes"]]


for f in ("PROMPT.md", "features.json", "CLAUDE.md"):
    if not Path(f).exists():
        sys.exit(f"{f} 가 없다 · 장표의 하네스 파일을 먼저 만든다")
Path("runs").mkdir(exist_ok=True)
for i in range(1, MAX + 1):
    todo = left()
    if not todo:
        print("모든 기능 통과 · 루프 종료")
        break
    print(f"[{i}/{MAX}] 남은 기능 {len(todo)}개 · 다음 후보 {todo[0]['id']} {todo[0]['title']}")
    t0 = time.time()
    r = subprocess.run(["claude", "-p", "--permission-mode", "acceptEdits", "--allowedTools", *TOOLS,
                        "--output-format", "json"],
                       input=Path("PROMPT.md").read_text(encoding="utf-8"), capture_output=True, text=True, encoding="utf-8")
    Path(f"runs/{i:02d}.json").write_text(r.stdout or r.stderr, encoding="utf-8")
    try:
        d = json.loads(r.stdout)
        u = d.get("usage", {})
        tok = sum(u.get(k, 0) for k in ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
        print(f"  {round(time.time() - t0)}초 · {d.get('num_turns')}턴 · {tok:,} 토큰")
    except ValueError:
        print("  실행 오류 · runs/ 기록 확인")
print(f"남은 기능 {len(left())}개 · 진행 기록은 progress.md · 커밋은 git log")
