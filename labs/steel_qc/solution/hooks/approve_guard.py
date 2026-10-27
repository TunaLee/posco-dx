"""PreToolUse Hook — 출하 승인 도구는 Claude 가 직접 부르지 못하게 막는다 (강사용 완성본).

.claude/settings.json 의 hooks.PreToolUse 에 matcher "mcp__lims__approve_shipment" 로 건다.
Claude Code 가 도구를 부르기 직전에 이 스크립트를 실행하고, deny 를 받으면 호출하지 않는다.
"""
import json
import sys
from datetime import datetime
from pathlib import Path

event = json.load(sys.stdin)
coil = (event.get("tool_input") or {}).get("coil_id", "?")
data = Path(__file__).resolve().parents[2] / "data"     # 콘솔 탭 ④ 출하 승인
data.mkdir(exist_ok=True)
with (data / "blocked.jsonl").open("a", encoding="utf-8") as f:
    f.write(json.dumps({"at": datetime.now().strftime("%H:%M:%S"), "tool": event.get("tool_name"),
                        "coil_id": coil, "input": event.get("tool_input")}, ensure_ascii=False) + "\n")
print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": f"출하 승인({coil})은 품질 담당자가 직접 한다 · 승인할 코일 목록과 근거만 정리해 보고할 것",
}}, ensure_ascii=False))
