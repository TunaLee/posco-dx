"""코일 시험 결과 판정 (강사용 완성본 · 수업에서는 Claude Code 로 직접 만든다).

규격 범위를 벗어나면 불합격, 한계값의 3% 안쪽이면 근접, 나머지는 합격.
"""
import json
from pathlib import Path

SPECS = json.loads((Path(__file__).resolve().parent.parent / "sim" / "specs.json").read_text(encoding="utf-8"))


def judge(row, specs=SPECS):
    """row: 시뮬레이터 결과 한 건 → {"verdict", "out": [항목], "near": [항목], "detail": [...]}"""
    limits = specs["grades"][row["grade"]]["limits"]
    near_ratio = specs["near_ratio"]
    out, near, detail = [], [], []
    for k, (lo, hi) in limits.items():
        v = row["values"][k]
        if (lo is not None and v < lo) or (hi is not None and v > hi):
            out.append(k)
            detail.append({"item": k, "value": v, "min": lo, "max": hi, "state": "이탈"})
        elif (hi is not None and v >= hi * (1 - near_ratio)) or (lo is not None and v <= lo * (1 + near_ratio)):
            near.append(k)
            detail.append({"item": k, "value": v, "min": lo, "max": hi, "state": "근접"})
    verdict = "불합격" if out else ("근접" if near else "합격")
    return {"coil_id": row["coil_id"], "grade": row["grade"], "verdict": verdict, "out": out, "near": near, "detail": detail}
