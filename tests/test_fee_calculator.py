import pytest

from src import fee_calculator


@pytest.mark.parametrize(
    "payload, expected_fee",
    [
        (
            {
                "cart_value": 15000,
                "delivery_distance": 2235,
                "number_of_items": 4,
                "time": "2021-10-12T13:00:00Z",
            },
            0,
        ),
    ],
)
def test_calculate_fee(payload, expected_fee):
    assert fee_calculator.calculate_fee(payload) == expected_fee


@pytest.mark.parametrize(
    "payload, fee, expected_fee",
    [
        ({"cart_value": 8_46}, 0, 1_54),
        ({"cart_value": 10_00}, 0, 0),
        ({"cart_value": 10_01}, 0, 0),
    ],
)
def test_cart_value_fee(payload, fee, expected_fee):
    assert fee_calculator.cart_value_fee(payload, fee) == expected_fee


@pytest.mark.parametrize(
    "payload, fee, expected_fee",
    [
        ({"delivery_distance": 999}, 0, 2_00),
        ({"delivery_distance": 1499}, 0, 3_00),
        ({"delivery_distance": 1500}, 0, 3_00),
        ({"delivery_distance": 1501}, 0, 4_00),
    ],
)
def test_distance_fee(payload, fee, expected_fee):
    assert fee_calculator.distance_fee(payload, fee) == expected_fee