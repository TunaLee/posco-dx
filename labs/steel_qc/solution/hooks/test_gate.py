"""Stop Hook — 작업을 끝내기 전에 판정 테스트를 돌리고, 실패하면 끝내지 못하게 한다 (강사용 완성본).

.claude/settings.json 의 hooks.Stop 에 건다. exit 2 + stderr 메시지면 Claude 가 멈추지 않고 이어서 고친다.
"""
import json
import subprocess
import sys

event = json.load(sys.stdin)
if event.get("stop_hook_active"):      # 이미 한 번 막았으면 무한 반복을 피해 통과
    sys.exit(0)
r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "solution/tests"],
                   capture_output=True, text=True)
if r.returncode != 0:
    tail = "\n".join(r.stderr.strip().splitlines()[-8:])
    print(f"판정 테스트 실패 · 끝내기 전에 고칠 것\n{tail}", file=sys.stderr)
    sys.exit(2)
