import math


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
        distance_fee,
        num_item_fee,
        # friday_fee,
        # max_allowed_fee,
    ]

    fee = 0

    for strategy in strategies:
        fee = strategy(payload, fee)

    return fee


def cart_value_fee(payload: dict, fee: int) -> int:
    return fee + max(0, 1000 - payload["cart_value"])


def distance_fee(payload: dict, fee: int) -> int:
    if payload["delivery_distance"] <= 1000:
        return fee + BASE_FEE_DISTANCE
    # every segment = 500 meters
    segment = math.ceil((payload["delivery_distance"] - 1000) / 500)
    return fee + BASE_FEE_DISTANCE + EXTRA_FEE_DISTANCE * segment


def num_item_fee(payload: dict, fee: int) -> int:
    if payload["number_of_items"] < 5:
        return fee

    additional_surcharge = (payload["number_of_items"] - 4) * NUM_ITEM_SURCHARGE
    if payload["number_of_items"] <= 12:
        return fee + additional_surcharge
    return fee + additional_surcharge + EXTRA_BULK_FEE

