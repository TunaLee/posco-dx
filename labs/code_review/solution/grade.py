"""리뷰 채점 — data/reviews.json 을 저장소의 정답(/api/answer)과 대조한다 (강사용 완성본 · 실습 8-1).

같은 PR · 같은 종류(보안 · 버그 · 성능 · 테스트)의 지적이 있으면 찾은 것으로 본다.
문제 없는 PR(clean)에 붙은 지적은 오탐. 결과는 data/grade.json (콘솔 탭 ⑥ 채점).
    python solution/grade.py
"""
import json
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ans = json.loads(urllib.request.urlopen("http://127.0.0.1:8900/api/answer", timeout=5).read())
reviews = json.loads((ROOT / "data" / "reviews.json").read_text(encoding="utf-8")) if (ROOT / "data" / "reviews.json").exists() else []

found, missed = [], []
for i in ans["issues"]:
    hit = any(r.get("pr") == i["pr"] and r.get("kind") == i["kind"] for r in reviews)
    (found if hit else missed).append(i)
false_pos = [r for r in reviews if r.get("pr") in ans["clean"]]
res = {"at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "total": len(ans["issues"]), "found": len(found),
       "missed": [{"pr": i["pr"], "kind": i["kind"], "key": i["key"]} for i in missed],
       "false_positive": [{"pr": r["pr"], "title": r.get("title")} for r in false_pos], "reviews": len(reviews)}
(ROOT / "data" / "grade.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"찾음 {res['found']} / {res['total']} · 오탐 {len(false_pos)} · 놓침 {[m['pr'] for m in res['missed']]}")
