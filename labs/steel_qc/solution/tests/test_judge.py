"""판정 로직 회귀 테스트 — 시뮬레이터의 정답과 1,000건을 대조한다 (서버 없이 실행).
    python -m unittest discover -s solution/tests   (tests/ 로 복사해도 됨)
"""
import sys
import unittest
from pathlib import Path

ROOT = next(d for d in Path(__file__).resolve().parents if (d / "sim").is_dir())   # solution/tests · tests 어디서나
sys.path[:0] = [str(ROOT / "sim"), str(ROOT / "solution")]
import lims_sim  # noqa: E402
from judge import judge  # noqa: E402


class JudgeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lims = lims_sim.Lims(preload=1000)

    def test_verdict_matches_truth(self):
        wrong = [(r["coil_id"], judge(r)["verdict"], t["verdict"])
                 for r, t in zip(self.lims.rows, self.lims.truth) if judge(r)["verdict"] != t["verdict"]]
        self.assertEqual(wrong, [], f"정답과 다른 판정 {len(wrong)}건 · 예: {wrong[:3]}")

    def test_out_items_match(self):
        for r, t in zip(self.lims.rows, self.lims.truth):
            self.assertEqual(sorted(judge(r)["out"]), sorted(t["out"]), r["coil_id"])

    def test_boundary(self):
        row = {"coil_id": "T-1", "grade": "HS-275",
               "values": {"C": 0.25, "Mn": 1.0, "P": 0.01, "S": 0.01, "YS": 275, "TS": 550, "EL": 21}}
        self.assertNotEqual(judge(row)["verdict"], "불합격", "한계값과 같으면 합격 범위")


if __name__ == "__main__":
    unittest.main()
