"""PreToolUse Hook — 원본/ 회의록은 고치지 못하게 막는다 (실습 3-6 완성본).

.claude/settings.json 의 hooks.PreToolUse 에 matcher "Edit|Write" 로 건다.
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
if rel.startswith("원본/"):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": f"{rel} — 원본 회의록은 고치지 않는다 · 결과는 out/ 에",
    }}, ensure_ascii=False))
