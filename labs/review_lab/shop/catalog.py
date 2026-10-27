from shop import db


def get_price(sku, cache={}):
    if sku not in cache:
        rows = db.query("SELECT price FROM products WHERE sku = ?", (sku,))
        cache[sku] = rows[0]["price"]
    return cache[sku]
