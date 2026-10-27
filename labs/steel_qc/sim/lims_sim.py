"""한빛스틸 가상 시험실(LIMS) 시뮬레이터 — 실습용 가상 자료.

몇 초마다 새 코일의 시험 결과(성분 · 기계적 성질)를 만든다.
    python sim/lims_sim.py            # http://127.0.0.1:8800
    python sim/lims_sim.py --port 8801 --interval 2

판정은 하지 않는다. 판정 정답은 /api/truth 로만 따로 본다 (평가 · 테스트용).
파이썬 표준 라이브러리만 쓴다.
"""
import argparse
import json
import random
import threading
import time
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent
SPECS = json.loads((HERE / "specs.json").read_text(encoding="utf-8"))
GRADES = list(SPECS["grades"])
ITEMS = list(SPECS["items"])
NEAR = SPECS["near_ratio"]
LINES = ["1열연", "2열연", "3냉연"]
DIGITS = {"C": 3, "Mn": 2, "P": 3, "S": 3, "YS": 0, "TS": 0, "EL": 1}
TYPICAL = {"YS": 1.25, "TS": None, "EL": 1.45}  # 하한만 있는 항목의 보통 값 = 하한 × 배수


def judge(grade, values):
    """정답 판정 (시뮬레이터 내부용 · 수강생 코드와 별개)."""
    out, near = [], []
    for k, (lo, hi) in SPECS["grades"][grade]["limits"].items():
        v = values[k]
        if (lo is not None and v < lo) or (hi is not None and v > hi):
            out.append(k)
        elif (hi is not None and v >= hi * (1 - NEAR)) or (lo is not None and v <= lo * (1 + NEAR)):
            near.append(k)
    verdict = "불합격" if out else ("근접" if near else "합격")
    return {"verdict": verdict, "out": out, "near": near}


class Lims:
    def __init__(self, seed=26, interval=3.0, preload=30):
        self.rng = random.Random(seed)
        self.interval = interval
        self.speed = 1.0
        self.playing = True
        self.rows, self.truth = [], []
        self.lock = threading.Lock()
        self.t0 = datetime(2026, 10, 28, 8, 0, 0)
        self.streak = {}  # 라인별 남은 연속 근접 횟수
        for _ in range(preload):
            self.make()

    def _normal(self, lo, hi, k):
        if lo is not None and hi is not None:
            return lo + (hi - lo) * self.rng.uniform(0.25, 0.75)
        if hi is not None:
            return hi * self.rng.uniform(0.45, 0.85)
        return lo * self.rng.uniform(1.12, TYPICAL.get(k) or 1.3)

    def _push(self, limits, k, kind):
        lo, hi = limits[k]
        if kind == "near":
            return hi * self.rng.uniform(1 - NEAR * 0.9, 0.999) if hi is not None else lo * self.rng.uniform(1.001, 1 + NEAR * 0.9)
        return hi * self.rng.uniform(1.02, 1.08) if hi is not None else lo * self.rng.uniform(0.92, 0.98)

    def make(self):
        n = len(self.rows) + 1
        grade = self.rng.choice(GRADES)
        line = self.rng.choice(LINES)
        limits = SPECS["grades"][grade]["limits"]
        vals = {k: self._normal(*limits[k], k) for k in ITEMS}
        r = self.rng.random()
        if self.streak.get(line):                     # 같은 라인 연속 근접 (추세 과제용)
            self.streak[line] -= 1
            vals["TS"] = self._push(limits, "TS", "near") if limits["TS"][1] else vals["TS"]
        elif r < 0.06:                                # 규격 이탈
            k = self.rng.choice(ITEMS)
            vals[k] = self._push(limits, k, "out")
        elif r < 0.16:                                # 한계 근접
            k = self.rng.choice(ITEMS)
            vals[k] = self._push(limits, k, "near")
        elif r < 0.18 and not any(self.streak.values()):
            self.streak[line] = 3
        vals = {k: round(v, DIGITS[k]) if DIGITS[k] else int(round(v)) for k, v in vals.items()}
        at = self.t0 + timedelta(minutes=4 * n)
        shift = "A" if 6 <= at.hour < 14 else ("B" if 14 <= at.hour < 22 else "C")
        row = {"seq": n, "coil_id": f"HB26-{n:05d}", "time": at.strftime("%Y-%m-%d %H:%M"),
               "grade": grade, "line": line, "shift": shift, "values": vals}
        with self.lock:
            self.rows.append(row)
            self.truth.append({"seq": n, "coil_id": row["coil_id"], **judge(grade, vals)})
        return row

    def loop(self):
        while True:
            time.sleep(self.interval / self.speed)
            if self.playing:
                self.make()


def page(lims):
    rows = "".join(
        f"<tr><td>{r['coil_id']}</td><td>{r['time']}</td><td>{r['grade']}</td><td>{r['line']}</td>"
        + "".join(f"<td>{r['values'][k]}</td>" for k in ITEMS) + "</tr>"
        for r in reversed(lims.rows[-12:]))
    head = "".join(f"<th>{k}</th>" for k in ITEMS)
    return f"""<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="3">
<title>가상 시험실 시뮬레이터</title>
<style>body{{font-family:sans-serif;margin:24px;color:#222}} table{{border-collapse:collapse}}
td,th{{border:1px solid #ccc;padding:4px 8px;font-size:13px}} button{{margin-right:6px}}</style>
<h2>한빛스틸 가상 시험실 시뮬레이터 <small>(실습용 가상 자료)</small></h2>
<p>상태: <b>{'재생 중' if lims.playing else '일시정지'}</b> · 속도 ×{lims.speed} · 누적 {len(lims.rows)}건</p>
<p><button onclick="c('play')">재생</button><button onclick="c('pause')">일시정지</button>
<button onclick="c('speed',1)">×1</button><button onclick="c('speed',5)">×5</button><button onclick="c('speed',20)">×20</button></p>
<p>API: <code>/api/results?since=0</code> · <code>/api/results/HB26-00001</code> · <code>/api/specs</code> · <code>/api/state</code></p>
<table><tr><th>코일</th><th>시각</th><th>강종</th><th>라인</th>{head}</tr>{rows}</table>
<script>function c(a,v){{fetch('/api/control',{{method:'POST',body:JSON.stringify({{action:a,value:v}})}}).then(()=>location.reload())}}</script>"""


def make_handler(lims):
    class H(BaseHTTPRequestHandler):
        def _send(self, code, body, ctype="application/json; charset=utf-8"):
            data = body if isinstance(body, bytes) else (
                body.encode("utf-8") if isinstance(body, str) else json.dumps(body, ensure_ascii=False).encode("utf-8"))
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, *a):
            pass

        def do_GET(self):
            u = urlparse(self.path)
            q = {k: v[0] for k, v in parse_qs(u.query).items()}
            since, limit = int(q.get("since", 0)), int(q.get("limit", 200))
            with lims.lock:
                rows, truth = list(lims.rows), list(lims.truth)
            if u.path == "/":
                return self._send(200, page(lims), "text/html; charset=utf-8")
            if u.path == "/api/results":
                out = [r for r in rows if r["seq"] > since and (not q.get("grade") or r["grade"] == q["grade"])]
                return self._send(200, out[:limit])
            if u.path.startswith("/api/results/"):
                cid = u.path.rsplit("/", 1)[1]
                hit = next((r for r in rows if r["coil_id"] == cid), None)
                return self._send(200 if hit else 404, hit or {"error": f"{cid} 없음"})
            if u.path == "/api/specs":
                return self._send(200, SPECS)
            if u.path == "/api/state":
                return self._send(200, {"playing": lims.playing, "speed": lims.speed, "count": len(rows),
                                        "last_seq": rows[-1]["seq"] if rows else 0})
            if u.path == "/api/truth":
                return self._send(200, [t for t in truth if t["seq"] > since][:limit])
            return self._send(404, {"error": "없는 경로"})

        def do_POST(self):
            if urlparse(self.path).path != "/api/control":
                return self._send(404, {"error": "없는 경로"})
            n = int(self.headers.get("Content-Length") or 0)
            try:
                body = json.loads(self.rfile.read(n) or b"{}")
            except ValueError:
                return self._send(400, {"error": "JSON 형식 오류"})
            a = body.get("action")
            if a == "play":
                lims.playing = True
            elif a == "pause":
                lims.playing = False
            elif a == "speed":
                lims.speed = max(0.5, min(50.0, float(body.get("value") or 1)))
            else:
                return self._send(400, {"error": "action 은 play · pause · speed"})
            return self._send(200, {"playing": lims.playing, "speed": lims.speed})

        def do_OPTIONS(self):
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()
    return H


def main():
    ap = argparse.ArgumentParser(description="한빛스틸 가상 시험실 시뮬레이터")
    ap.add_argument("--port", type=int, default=8800)
    ap.add_argument("--interval", type=float, default=3.0, help="새 결과 간격(초)")
    ap.add_argument("--seed", type=int, default=26)
    a = ap.parse_args()
    lims = Lims(seed=a.seed, interval=a.interval)
    threading.Thread(target=lims.loop, daemon=True).start()
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), make_handler(lims))
    print(f"가상 시험실 시뮬레이터 · http://127.0.0.1:{a.port}  (Ctrl+C 로 종료)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("종료")


if __name__ == "__main__":
    main()
