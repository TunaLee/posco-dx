// 루프 하네스 실행기 — features.json 이 모두 통과하거나 최대 횟수가 될 때까지
// PROMPT.md 를 새 세션(claude -p)으로 반복 실행한다. 매번 새 세션이라 컨텍스트가 쌓이지 않는다.
//   node loop.mjs 8        # 최대 8회
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { spawnSync } from "node:child_process";

const MAX = Number(process.argv[2] || 8);
const left = () => JSON.parse(readFileSync("features.json", "utf8")).filter((f) => !f.passes);
const tools = ["Read", "Write", "Edit", "Grep", "Glob", "Bash(node:*)", "Bash(npm test:*)", "Bash(git add:*)", "Bash(git commit:*)", "Bash(git status:*)", "Bash(git log:*)"];

for (const f of ["PROMPT.md", "features.json", "CLAUDE.md"]) {
  if (!existsSync(f)) { console.error(`${f} 가 없다 · 장표의 하네스 파일을 먼저 만든다`); process.exit(1); }
}
mkdirSync("runs", { recursive: true });
for (let i = 1; i <= MAX; i++) {
  const todo = left();
  if (todo.length === 0) { console.log("모든 기능 통과 · 루프 종료"); break; }
  console.log(`[${i}/${MAX}] 남은 기능 ${todo.length}개 · 다음 후보 ${todo[0].id}`);
  const t0 = Date.now();
  const r = spawnSync("claude", ["-p", "--permission-mode", "acceptEdits", "--allowedTools", ...tools, "--output-format", "json"],
    { input: readFileSync("PROMPT.md", "utf8"), encoding: "utf8", maxBuffer: 1 << 26 });
  writeFileSync(`runs/${String(i).padStart(2, "0")}.json`, r.stdout || r.stderr || "");
  try {
    const d = JSON.parse(r.stdout);
    const u = d.usage || {};
    const tok = (u.input_tokens || 0) + (u.output_tokens || 0) + (u.cache_read_input_tokens || 0) + (u.cache_creation_input_tokens || 0);
    console.log(`  ${Math.round((Date.now() - t0) / 1000)}초 · ${d.num_turns}턴 · ${tok.toLocaleString()} 토큰`);
  } catch { console.log("  실행 오류 · runs/ 기록 확인"); }
}
console.log(`남은 기능 ${left().length}개 · 진행 기록은 progress.md · 커밋은 git log`);
