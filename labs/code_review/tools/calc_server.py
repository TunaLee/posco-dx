"""계산 도구 하나짜리 MCP 서버 — 실습 3-1 · Claude Code 에 도구를 붙여 호출하게 해 보기.

    claude mcp add calc -- python tools/calc_server.py
    /mcp 로 연결 확인 → 「calc 도구로 4817 × 293 × 1.1 을 원 미만 버림으로 계산해 줘」

도구 calc(expr): 사칙연산 · 괄호 · 거듭제곱 · 소수만 계산한다 (코드 실행 없음).
"""
import ast
import json
import operator
import sys
from decimal import ROUND_DOWN, Decimal

OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
       ast.Pow: operator.pow, ast.USub: operator.neg, ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod}
TOOLS = [{"name": "calc", "description": "수식을 정확히 계산한다. 사칙연산 · 괄호 · ** · 소수. 금액 계산은 이 도구로.",
          "inputSchema": {"type": "object", "properties": {
              "expr": {"type": "string", "description": "예: 4817 * 293 * 1.1"},
              "floor": {"type": "boolean", "description": "true 면 소수점 아래 버림"}}, "required": ["expr"]}}]


def ev(n):
    if isinstance(n, ast.Expression):
        return ev(n.body)
    if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
        return Decimal(str(n.value))
    if isinstance(n, ast.BinOp) and type(n.op) in OPS:
        return OPS[type(n.op)](ev(n.left), ev(n.right))
    if isinstance(n, ast.UnaryOp) and type(n.op) in OPS:
        return OPS[type(n.op)](ev(n.operand))
    raise ValueError("숫자와 + - * / ** ( ) 만 쓸 수 있음")


def reply(id_, result=None, error=None):
    msg = {"jsonrpc": "2.0", "id": id_}
    msg.update({"error": error} if error else {"result": result})
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + "\n")
    sys.stdout.flush()


for line in sys.stdin:
    try:
        m = json.loads(line)
    except ValueError:
        continue
    method, id_ = m.get("method"), m.get("id")
    if id_ is None:
        continue
    if method == "initialize":
        reply(id_, {"protocolVersion": m.get("params", {}).get("protocolVersion", "2025-06-18"),
                    "capabilities": {"tools": {}}, "serverInfo": {"name": "calc", "version": "0.1.0"}})
    elif method == "tools/list":
        reply(id_, {"tools": TOOLS})
    elif method == "tools/call":
        a = m.get("params", {}).get("arguments") or {}
        try:
            v = ev(ast.parse(a["expr"].replace("×", "*").replace(",", ""), mode="eval"))
            if a.get("floor"):
                v = v.quantize(Decimal("1"), rounding=ROUND_DOWN)
            reply(id_, {"content": [{"type": "text", "text": f"{a['expr']} = {v:,}"}]})
        except Exception as e:
            reply(id_, {"content": [{"type": "text", "text": f"오류: {e}"}], "isError": True})
    elif method == "ping":
        reply(id_, {})
    else:
        reply(id_, error={"code": -32601, "message": f"지원하지 않는 메서드 {method}"})
