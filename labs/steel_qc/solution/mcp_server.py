"""가상 시험실 MCP 서버 (강사용 완성본 · 수업에서는 Claude Code 로 직접 만든다).

Claude Code 가 표준 입출력(stdio)으로 띄워 쓰는 MCP 서버. 파이썬 표준 라이브러리만 쓴다.
    claude mcp add lims -- python solution/mcp_server.py

도구
    recent_results   최근 시험 결과 원문 (판정 없음)
    reject_summary   이상 건만 · 판정과 이탈 항목 (컨텍스트를 아끼는 도구)
    coil_detail      코일 한 건 원문 + 판정
    get_spec         강종 규격
    approve_shipment 출하 승인 기록 (Hook 으로 사람 확인을 거치게 한다)
"""
import json
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from judge import SPECS, judge  # noqa: E402

BASE = "http://127.0.0.1:8800"
APPROVALS = Path(__file__).resolve().parent.parent / "data" / "approvals.json"

TOOLS = [
    {"name": "recent_results", "description": "가상 시험실의 최근 코일 시험 결과 원문을 돌려준다. 판정은 하지 않는다.",
     "inputSchema": {"type": "object", "properties": {
         "limit": {"type": "integer", "description": "최근 몇 건 (기본 20)"},
         "grade": {"type": "string", "description": "강종 필터 · 예: HS-355"}}}},
    {"name": "reject_summary", "description": "불합격 · 근접 코일만 골라 판정과 이탈 항목을 돌려준다. 합격 건은 개수만.",
     "inputSchema": {"type": "object", "properties": {
         "since": {"type": "integer", "description": "이 seq 다음부터 (기본 0 = 처음부터)"}}}},
    {"name": "coil_detail", "description": "코일 한 건의 시험 결과 원문과 판정 근거(항목별 값 · 규격)를 돌려준다.",
     "inputSchema": {"type": "object", "properties": {"coil_id": {"type": "string", "description": "예: HB26-00012"}},
                     "required": ["coil_id"]}},
    {"name": "get_spec", "description": "강종의 사내 규격(항목별 하한 · 상한)을 돌려준다.",
     "inputSchema": {"type": "object", "properties": {"grade": {"type": "string", "description": "예: HS-420"}},
                     "required": ["grade"]}},
    {"name": "approve_shipment", "description": "코일의 출하 승인을 기록한다. 불합격 코일은 거절한다.",
     "inputSchema": {"type": "object", "properties": {
         "coil_id": {"type": "string"}, "approver": {"type": "string", "description": "승인자 이름"}},
         "required": ["coil_id", "approver"]}},
]


def api(path):
    with urllib.request.urlopen(BASE + path, timeout=5) as r:
        return json.loads(r.read().decode("utf-8"))


def call(name, args):
    if name == "recent_results":
        q = "/api/results?since=0&limit=100000" + (f"&grade={args['grade']}" if args.get("grade") else "")
        return api(q)[-int(args.get("limit") or 20):]
    if name == "reject_summary":
        rows = api(f"/api/results?since={int(args.get('since') or 0)}&limit=100000")
        js = [judge(r) for r in rows]
        bad = [{"coil_id": j["coil_id"], "grade": j["grade"], "verdict": j["verdict"], "detail": j["detail"]}
               for j in js if j["verdict"] != "합격"]
        return {"checked": len(js), "pass": len(js) - len(bad), "last_seq": rows[-1]["seq"] if rows else None, "issues": bad}
    if name == "coil_detail":
        row = api(f"/api/results/{args['coil_id']}")
        return {"result": row, "judgment": judge(row)}
    if name == "get_spec":
        g = SPECS["grades"].get(args["grade"])
        if not g:
            raise ValueError(f"없는 강종 {args['grade']} · 가능: {', '.join(SPECS['grades'])}")
        return {"grade": args["grade"], **g, "items": SPECS["items"]}
    if name == "approve_shipment":
        j = judge(api(f"/api/results/{args['coil_id']}"))
        if j["verdict"] == "불합격":
            raise ValueError(f"{args['coil_id']} 는 불합격({', '.join(j['out'])}) · 출하 승인 불가")
        rec = json.loads(APPROVALS.read_text(encoding="utf-8")) if APPROVALS.exists() else []
        rec.append({"coil_id": args["coil_id"], "approver": args["approver"], "verdict": j["verdict"],
                    "at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        APPROVALS.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"approved": args["coil_id"], "total_approvals": len(rec)}
    raise ValueError(f"없는 도구 {name}")


def reply(id_, result=None, error=None):
    msg = {"jsonrpc": "2.0", "id": id_}
    msg.update({"error": error} if error else {"result": result})
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            m = json.loads(line)
        except ValueError:
            continue
        method, id_ = m.get("method"), m.get("id")
        if id_ is None:  # 알림(notifications/initialized 등)은 답하지 않는다
            continue
        if method == "initialize":
            reply(id_, {"protocolVersion": m.get("params", {}).get("protocolVersion", "2025-06-18"),
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "lims", "version": "0.1.0"}})
        elif method == "tools/list":
            reply(id_, {"tools": TOOLS})
        elif method == "tools/call":
            p = m.get("params", {})
            try:
                out = call(p.get("name"), p.get("arguments") or {})
                reply(id_, {"content": [{"type": "text", "text": json.dumps(out, ensure_ascii=False)}]})
            except Exception as e:  # 도구 오류는 LLM 이 읽을 수 있게 결과로 돌려준다
                reply(id_, {"content": [{"type": "text", "text": f"오류: {e}"}], "isError": True})
        elif method == "ping":
            reply(id_, {})
        else:
            reply(id_, error={"code": -32601, "message": f"지원하지 않는 메서드 {method}"})


if __name__ == "__main__":
    main()
