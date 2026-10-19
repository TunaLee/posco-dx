"""PreToolUse Hook — 설계 승인 전에는 docs/ 밖에 쓰지 못하게 · APPROVED 는 사람만."""
import json
import os
import re
import sys
from pathlib import Path

e = json.load(sys.stdin)
inp = e.get("tool_input", {})
root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or e.get("cwd", "."))
path = str(inp.get("file_path", ""))
cmd = str(inp.get("command", ""))


def block(msg):
    print(f"[메타 하네스] {msg}", file=sys.stderr)
    sys.exit(2)


if "APPROVED" in path or ("APPROVED" in cmd and re.search(r"(>|touch|cp |mv |tee|rm )", cmd)):
    block("APPROVED 는 사용자가 직접 만든다 · 설계 요약을 보여 주고 기다릴 것")

if e.get("tool_name") in ("Write", "Edit", "MultiEdit") and path:
    target = Path(path).resolve()
    in_docs = str(target).startswith(str((root / "docs").resolve()))
    approved = any(root.glob("docs/*/APPROVED"))
    if not in_docs and not approved:
        block("아직 설계 승인 전 · docs/<이름>/spec.md 를 보여 주고 사용자가 APPROVED 를 만들 때까지 생성하지 않는다")
sys.exit(0)
