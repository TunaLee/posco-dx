from shop import db


def refund(order_id, amount):
    order = db.query("SELECT * FROM orders WHERE id = ?", (order_id,))[0]
    db.execute("UPDATE orders SET total = total - ?, status = 'refunded' WHERE id = ?", (amount, order_id))
    return {"order_id": order_id, "refunded": amount, "remain": order["total"] - amount}
