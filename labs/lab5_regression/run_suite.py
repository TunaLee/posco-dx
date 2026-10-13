"""Lab 5 — 평가 스위트: 데이터셋 전체를 K번씩 돌려 채점하고 결과 파일과 보고서를 남긴다.

실행:  python lab5_regression/run_suite.py --track pangyo -n 10 --k 3
       python lab5_regression/run_suite.py --track pohang --agent multi --k 2
출력:  results/<시각>_<track>.json  +  같은 이름의 .md 보고서
비용:  건수 × K 번 Agent 를 부른다 (멀티는 한 번에 여러 모델 호출). 처음에는 -n 5 --k 2 로 시작.
"""
import argparse
import asyncio
import json
import statistics
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import config
from common.data import load_cases
from lab3_sdk_agent.agent_multi import run_with_retry
from lab3_sdk_agent.agent_single import run_single
from lab4_eval_design.judge import judge_one
from lab5_regression.scoring import WEIGHTS, consistency, score_pangyo, score_pohang, weighted_total

HERE = Path(__file__).parent


async def run_case(case, track, agent, use_judge=False):
    t0 = time.time()
    try:
        r = await (run_single(case["input"], track) if agent == "single" else run_with_retry(case["input"], track))
    except Exception as e:                      # 한 건이 실패해도 스위트는 계속
        r = {"output": None, "cost": 0.0, "error": str(e)}
    r.setdefault("duration_ms", int((time.time() - t0) * 1000))
    s = score_pangyo(r["output"], case["gold"]) if track == "pangyo" else \
        score_pohang(r["output"], case["gold"], case["input"])
    if use_judge and r["output"]:               # 답변 문장 품질은 LLM judge 로 (1–5)
        j = await judge_one(track, case["input"], r["output"])
        s.update(judge=j["score"], judge_cost=j["cost"])
    return {**s, "output": r["output"], "cost": r.get("cost", 0.0), "duration_ms": r["duration_ms"],
            "input_tokens": r.get("input_tokens", 0), "output_tokens": r.get("output_tokens", 0),
            "cache_read": r.get("cache_read", 0), "error": r.get("error")}


def summarize(items):
    runs = [run for it in items for run in it["runs"]]
    mean = lambda key: statistics.mean(r[key] for r in runs)  # noqa: E731
    lat = sorted(r["duration_ms"] for r in runs)
    stages = {k: statistics.mean(r["stage"][k] for r in runs) for k in runs[0]["stage"]}
    s = {
        "accuracy": mean("accuracy"), "grounding": mean("grounding"), "safety": mean("safety"),
        "consistency": statistics.mean(it["consistency"] for it in items),
        "hallucination_rate": statistics.mean(float(r["hallucination"]) for r in runs),
        "safety_violations": sum(r["safety"] < 1 for r in runs),
        "e2e_pass_rate": statistics.mean(float(r["e2e"]) for r in runs),
        "avg_latency_ms": mean("duration_ms"), "p95_latency_ms": lat[int(0.95 * (len(lat) - 1))],
        "avg_cost_usd": mean("cost"), "total_cost_usd": sum(r["cost"] for r in runs),
        "avg_input_tokens": mean("input_tokens"), "avg_output_tokens": mean("output_tokens"),
        "avg_cache_read": mean("cache_read"), "errors": sum(bool(r["error"]) for r in runs),
        "stage": stages,
    }
    judged = [r["judge"] for r in runs if r.get("judge")]
    if judged:
        s["judge_avg"] = statistics.mean(judged)
        s["judge_cost_usd"] = sum(r.get("judge_cost", 0) for r in runs)
    s["weighted_total"] = weighted_total(s)
    return s


def write_report(path, meta, s, items):
    lines = [f"# 평가 결과 — {meta['track']} / {meta['agent']}", "",
             f"- 실행: {meta['started']} · 건수 {meta['n_cases']} × K={meta['k']} · 모델 {meta['model']}", "",
             "| 지표 | 값 |", "|---|---|"]
    for key in ["weighted_total", "accuracy", "grounding", "safety", "consistency", "hallucination_rate",
                "safety_violations", "e2e_pass_rate", "avg_latency_ms", "p95_latency_ms",
                "avg_cost_usd", "total_cost_usd", "avg_input_tokens", "avg_output_tokens", "errors",
                "judge_avg"]:
        if key not in s:
            continue
        v = s[key]
        lines.append(f"| {key} | {v:.3f} |" if isinstance(v, float) else f"| {key} | {v} |")
    lines += ["", "## 단계별", ""] + [f"- {k}: {v:.3f}" for k, v in s["stage"].items()]
    lines += ["", "## 실패한 건", ""]
    for it in items:
        bad = [r for r in it["runs"] if not r["e2e"]]
        if bad:
            notes = sorted({n for r in bad for n in r["notes"]}) or ["(정답과 다름)"]
            lines.append(f"- **{it['id']}** {len(bad)}/{len(it['runs'])}회 실패 · 일관성 {it['consistency']:.2f} · "
                         + ", ".join(notes))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--track", default=config.TRACK, choices=["pangyo", "pohang"])
    ap.add_argument("-n", type=int, default=0, help="앞에서 n건만 (0 = 전부)")
    ap.add_argument("--k", type=int, default=3, help="같은 입력 반복 횟수 (일관성 측정)")
    ap.add_argument("--agent", default="single", choices=["single", "multi"])
    ap.add_argument("--judge", action="store_true", help="LLM judge 채점도 한다 (비용 추가)")
    ap.add_argument("--out", help="결과 파일 경로 (기본: results/<시각>_<track>.json)")
    args = ap.parse_args()

    cases = load_cases(args.track)[: args.n or None]
    meta = {"track": args.track, "agent": args.agent, "k": args.k, "n_cases": len(cases),
            "model": config.MODEL, "judge_model": config.JUDGE_MODEL, "weights": WEIGHTS,
            "started": datetime.now().isoformat(timespec="seconds")}
    items = []
    for case in cases:
        runs = [await run_case(case, args.track, args.agent, args.judge) for _ in range(args.k)]
        c = consistency([r["label"] for r in runs])
        items.append({"id": case["id"], "consistency": c, "runs": runs})
        print(f"{case['id']}: e2e {sum(r['e2e'] for r in runs)}/{args.k} · 일관성 {c:.2f} · "
              f"${sum(r['cost'] for r in runs):.4f}")

    s = summarize(items)
    out = Path(args.out) if args.out else HERE / "results" / f"{datetime.now():%Y%m%d_%H%M%S}_{args.track}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"meta": meta, "summary": s, "items": items}, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    write_report(out.with_suffix(".md"), meta, s, items)
    print(f"\n종합 {s['weighted_total']:.3f} · 정확도 {s['accuracy']:.3f} · 환각 {s['hallucination_rate']:.2%}"
          f" · 안전 위반 {s['safety_violations']} · 비용 합계 ${s['total_cost_usd']:.4f}\n저장: {out}")


if __name__ == "__main__":
    asyncio.run(main())
