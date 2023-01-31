FREE_DELIVERY_MIN_AMOUNT = 100_00
MAX_FEE = 15_00
EXTRA_BULK_FEE = 1_20
NUM_ITEM_SURCHARGE = 50
BASE_FEE_DISTANCE = 2_00
EXTRA_FEE_DISTANCE = 1_00

def calculate_fee(payload: dict) -> int:
    if payload["cart_value"] >= FREE_DELIVERY_MIN_AMOUNT:
        return 0

    strategies = [
        cart_value_fee,
        # distance_fee,
        # num_item_fee,
        # friday_fee,
        # max_allowed_fee,
    ]

    fee = 0

    for strategy in strategies:
        fee = strategy(payload, fee)

    return fee


def cart_value_fee(payload: dict, fee: int) -> int:
    return fee + max(0, 1000 - payload["cart_value"])

