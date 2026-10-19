// Stop Hook — 테스트가 모두 통과해야 작업을 끝낼 수 있다.
import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";

const e = JSON.parse(readFileSync(0, "utf8"));
if (e.stop_hook_active) process.exit(0);          // 이미 한 번 막았으면 무한 반복 방지

const r = spawnSync("node", ["--test"], { cwd: process.env.CLAUDE_PROJECT_DIR || e.cwd, encoding: "utf8" });
if (r.status === 0) process.exit(0);

const fail = (r.stdout + r.stderr).split("\n").filter((l) => /not ok|fail|Error|expected|actual/i.test(l)).slice(0, 15).join("\n");
console.log(JSON.stringify({
  decision: "block",
  reason: "테스트가 통과하지 않아 끝낼 수 없다. 실패 원인을 고치거나, 테스트 기대값이 틀렸다면 근거와 함께 고쳐라.\n" + fail,
}));
process.exit(0);
