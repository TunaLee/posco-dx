from shop.pricing import calc_total


def test_total_with_tax():
    assert calc_total([{"price": 10000, "qty": 2}]) == 22000


def test_coupon_amount():
    assert calc_total([{"price": 10000, "qty": 1}], {"amount": 3000}) == 7700


def test_coupon_rate():
    assert calc_total([{"price": 10000, "qty": 1}], {"rate": 10}) == 9900
