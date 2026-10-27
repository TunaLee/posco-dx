"""PreToolUse Hook — 승인 · 병합 도구는 Claude 가 직접 부르지 못하게 막는다 (강사용 완성본).

.claude/settings.json 의 hooks.PreToolUse 에 matcher "mcp__repo__merge_pull_request|mcp__repo__pull_request_review_write" 로 건다.
막을 때마다 data/blocked.jsonl 에 한 줄 (콘솔 탭 ④ 막은 기록).
"""
import json
import sys
from datetime import datetime
from pathlib import Path

event = json.load(sys.stdin)
pr = (event.get("tool_input") or {}).get("pullNumber", "?")
data = Path(__file__).resolve().parents[2] / "data"
data.mkdir(exist_ok=True)
with (data / "blocked.jsonl").open("a", encoding="utf-8") as f:
    f.write(json.dumps({"at": datetime.now().strftime("%H:%M:%S"), "tool": event.get("tool_name"), "pr": pr,
                        "input": event.get("tool_input")}, ensure_ascii=False) + "\n")
print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": f"PR {pr} 승인 · 병합은 사람이 직접 한다 · 리뷰 의견과 근거만 정리해 보고할 것",
}}, ensure_ascii=False))
