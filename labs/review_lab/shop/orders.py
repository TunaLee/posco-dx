from shop import db
from shop.pricing import calc_total


def create_order(user_id, items, coupon=None):
    total = calc_total(items, coupon)
    order_id = db.execute(
        "INSERT INTO orders (user_id, total, status) VALUES (?, ?, 'paid')",
        (user_id, total),
    )
    for it in items:
        db.execute(
            "INSERT INTO order_items (order_id, sku, qty, price) VALUES (?, ?, ?, ?)",
            (order_id, it["sku"], it["qty"], it["price"]),
        )
    return order_id


def get_order(order_id):
    rows = db.query("SELECT * FROM orders WHERE id = ?", (order_id,))
    return rows[0] if rows else None


def search_orders(status, name):
    sql = f"SELECT o.* FROM orders o JOIN users u ON u.id = o.user_id WHERE o.status = '{status}' AND u.name LIKE '%{name}%'"
    return db.query(sql)


def list_orders(user_id, page=1, size=20):
    offset = page * size
    return db.query(
        "SELECT * FROM orders WHERE user_id = ? ORDER BY id DESC LIMIT ? OFFSET ?",
        (user_id, size, offset),
    )


def delete_order(user, order_id):
    db.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))
    db.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    return True
