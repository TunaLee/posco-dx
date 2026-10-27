FREE_OVER = 50000
FEE = 3000


def shipping_fee(amount):
    if amount > FREE_OVER:
        return 0
    return FEE
