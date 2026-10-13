"""Lab 4 — LLM-as-judge: Agent 출력을 judge_prompt.md 기준으로 1–5점 채점한다.

실행:  python lab4_eval_design/judge.py --track pangyo -n 10
입력:  sample_outputs_<track>.jsonl (또는 --input 으로 다른 jsonl: {id, input, output})
출력:  judge_scores.csv  →  agreement.py --judge lab4_eval_design/judge_scores.csv 로 사람 채점과 비교
고칠 곳: judge_prompt.md
"""
import argparse
import asyncio
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from claude_agent_sdk import ClaudeAgentOptions

from common import config
from common.data import DATA, load_kb, read_jsonl
from common.run import extract_json, run_once

HERE = Path(__file__).parent


def evidence_for(track):
    """judge 에게 줄 근거 자료 — 판교는 지식베이스 전체, 포항은 단가표."""
    if track == "pangyo":
        return "\n".join(f"[{cid}] {body}" for cid, body in load_kb().items())
    return (DATA / "pohang" / "price_table.csv").read_text(encoding="utf-8")


def judge_options():
    return ClaudeAgentOptions(model=config.JUDGE_MODEL, system_prompt="너는 엄격한 채점자다. JSON 하나만 출력한다.",
                              allowed_tools=[], permission_mode="dontAsk", setting_sources=[], max_turns=1)


async def judge_one(track, input_text, output):
    """출력 하나 채점 → {score, reason, cost}. 점수를 못 읽으면 score=None."""
    rubric = re.sub(r"<!--.*?-->", "", (HERE / "judge_prompt.md").read_text(encoding="utf-8"), flags=re.S)
    out_text = output if isinstance(output, str) else json.dumps(output, ensure_ascii=False)
    prompt = (rubric.replace("{INPUT}", input_text).replace("{EVIDENCE}", evidence_for(track))
              .replace("{OUTPUT}", out_text))
    r = await run_once(prompt, judge_options())
    data = extract_json(r["text"]) or {}
    score = data.get("score")
    return {"score": int(score) if str(score).isdigit() else None, "reason": data.get("reason", r["text"][:100]),
            "cost": r["cost"]}


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--track", default=config.TRACK, choices=["pangyo", "pohang"])
    ap.add_argument("-n", type=int, default=10, help="채점할 건수")
    ap.add_argument("--input", help="채점할 jsonl (기본: sample_outputs_<track>.jsonl)")
    ap.add_argument("--out", default=str(HERE / "judge_scores.csv"))
    args = ap.parse_args()

    rows = read_jsonl(args.input or HERE / f"sample_outputs_{args.track}.jsonl")[: args.n]
    results, total = [], 0.0
    for row in rows:
        j = await judge_one(args.track, row["input"], row["output"])
        total += j["cost"]
        results.append({"id": row["id"], "judge_score": j["score"], "reason": j["reason"]})
        print(f"{row['id']}: {j['score']}점 — {j['reason']}")

    with open(args.out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "judge_score", "reason"])
        w.writeheader(); w.writerows(results)
    print(f"\n저장: {args.out} | judge 비용 합계 ${total:.4f}")


if __name__ == "__main__":
    asyncio.run(main())
