"""Stop Hook — 작업을 끝내기 전에 판정 테스트를 돌리고, 실패하면 끝내지 못하게 한다 (강사용 완성본).

.claude/settings.json 의 hooks.Stop 에 건다. exit 2 + stderr 메시지면 Claude 가 멈추지 않고 이어서 고친다.
"""
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

event = json.load(sys.stdin)
if event.get("stop_hook_active"):      # 이미 한 번 막았으면 무한 반복을 피해 통과
    sys.exit(0)
tests = "tests" if (ROOT / "tests").is_dir() else "solution/tests"
r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", tests], capture_output=True, text=True, cwd=ROOT)
ran = re.search(r"Ran (\d+) test", r.stderr)
fails = re.findall(r"^(?:FAIL|ERROR): (\S+)", r.stderr, re.M)
(ROOT / "data").mkdir(exist_ok=True)
(ROOT / "data" / "test_results.json").write_text(json.dumps({     # 콘솔 탭 ⑦ 테스트
    "at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "total": int(ran.group(1)) if ran else 0,
    "failed": len(fails), "failures": fails, "ok": r.returncode == 0}, ensure_ascii=False, indent=2), encoding="utf-8")
if r.returncode != 0:
    tail = "\n".join(r.stderr.strip().splitlines()[-8:])
    print(f"판정 테스트 실패 · 끝내기 전에 고칠 것\n{tail}", file=sys.stderr)
    sys.exit(2)
