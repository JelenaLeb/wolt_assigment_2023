import math

import dateutil.parser


FREE_DELIVERY_MIN_AMOUNT = 100_00
MAX_FEE = 15_00
EXTRA_BULK_FEE = 1_20
NUM_ITEM_SURCHARGE = 50
BASE_FEE_DISTANCE = 2_00
EXTRA_FEE_DISTANCE = 1_00


class InvalidPayload(Exception):
    "raises domain exception when payload does not comply with specification"


def guard_payload(payload: dict) -> None:
    expected_payload = [
        ("cart_value", int, lambda x: x >= 0),
        ("delivery_distance", int, lambda x: x > 0),
        ("number_of_items", int, lambda x: x > 0),
        ("time", str, None),
    ]

    for key, value_type, value_check in expected_payload:
        if key not in payload:
            raise InvalidPayload(f"missing {key!r} key")

        if not isinstance(payload[key], value_type):
            raise InvalidPayload(f"expecting {key!r} as {value_type.__name__}")

        if value_check and not value_check(payload[key]):
            raise InvalidPayload(f"value of {key!r} does not comply")


def calculate_fee(payload: dict) -> int:
    guard_payload(payload)

    if payload["cart_value"] >= FREE_DELIVERY_MIN_AMOUNT:
        return 0

    strategies = [
        cart_value_fee,
        distance_fee,
        num_item_fee,
        friday_fee,
        max_allowed_fee,
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


def friday_fee(payload: dict, fee: int) -> int:
    try:
        dt = dateutil.parser.parse(payload["time"])
    except Exception:
        raise InvalidPayload("not a datetime string")

    # Friday between 15h and 19h
    if dt.weekday() == 4 and dt.hour in range(15, 19):
        return int(fee * 1.2)

    return fee


def max_allowed_fee(payload: dict, fee: int) -> int:
    return min(fee, MAX_FEE)
