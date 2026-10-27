from decimal import Decimal, ROUND_DOWN

TAX_RATE = Decimal("0.1")


def subtotal(items):
    return sum(Decimal(str(it["price"])) * it["qty"] for it in items)


def calc_total(items, coupon=None):
    amount = subtotal(items)
    if coupon:
        amount -= Decimal(str(coupon.get("amount", 0)))
        if "rate" in coupon:
            amount = amount * (1 - Decimal(str(coupon["rate"])) / 100)
    amount = max(amount, Decimal("0"))
    total = amount * (1 + TAX_RATE)
    return int(total.quantize(Decimal("1"), rounding=ROUND_DOWN))
