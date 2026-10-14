"""PreToolUse Hook — 되돌릴 수 없는 명령 · .env 쓰기를 막는다. 막을 때는 exit 2 + 이유."""
import json
import re
import sys

BLOCK = [
    (r"\brm\s+-\w*(rf|fr)", "rm -rf 는 되돌릴 수 없음"),
    (r"\bgit\s+push\b.*(--force|\s-f\b)", "git push --force 는 원격 기록을 덮어씀"),
    (r">>?\s*\S*\.env\b", ".env 에는 비밀 값 · Agent가 쓰지 않음"),
]

e = json.load(sys.stdin)
tool, inp = e.get("tool_name", ""), e.get("tool_input", {})
if tool in ("Write", "Edit", "MultiEdit") and re.search(r"(^|[\\/])\.env$", inp.get("file_path", "")):
    print("[가드레일] .env 에는 비밀 값 · Agent가 쓰지 않음", file=sys.stderr)
    sys.exit(2)
for pattern, reason in BLOCK:
    if tool == "Bash" and re.search(pattern, inp.get("command", "")):
        print(f"[가드레일] {reason}", file=sys.stderr)
        sys.exit(2)
sys.exit(0)
