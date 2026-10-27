from shop import db


def order_stats():
    users = db.query("SELECT id, name FROM users")
    out = []
    for u in users:
        rows = db.query("SELECT total FROM orders WHERE user_id = ?", (u["id"],))
        out.append({"user": u["name"], "count": len(rows), "sum": sum(r["total"] for r in rows)})
    return out
