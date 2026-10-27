"""PreToolUse Hook — 리뷰 중에는 shop/ · tests/ 를 고치지 못하게 막는다 (강사용 완성본 · 실습 2-2).

.claude/settings.json 의 hooks.PreToolUse 에 matcher "Edit|Write|MultiEdit" 로 건다.
"""
import json
import sys
from pathlib import Path

event = json.load(sys.stdin)
path = (event.get("tool_input") or {}).get("file_path", "")
root = Path(event.get("cwd") or ".").resolve()
try:
    rel = Path(path).resolve().relative_to(root).as_posix()
except ValueError:
    rel = path
if rel.startswith(("shop/", "tests/")):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": f"{rel} — 리뷰어는 코드를 고치지 않는다 · 지적과 고칠 방법만 out/review.md 에",
    }}, ensure_ascii=False))
