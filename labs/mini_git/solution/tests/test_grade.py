"""채점 규칙 테스트 — 같은 PR · 같은 종류면 찾음, clean PR 지적은 오탐."""
import unittest


def score(issues, clean, reviews):
    found = sum(any(r["pr"] == i["pr"] and r["kind"] == i["kind"] for r in reviews) for i in issues)
    return found, sum(r["pr"] in clean for r in reviews)


class GradeTest(unittest.TestCase):
    def test_match_by_pr_and_kind(self):
        issues = [{"pr": 104, "kind": "버그"}, {"pr": 105, "kind": "보안"}]
        self.assertEqual(score(issues, [107], [{"pr": 104, "kind": "버그"}]), (1, 0))

    def test_false_positive_on_clean(self):
        self.assertEqual(score([], [107], [{"pr": 107, "kind": "버그"}]), (0, 1))


if __name__ == "__main__":
    unittest.main()
