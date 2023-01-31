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
        (
            {
                "cart_value": 790,
                "delivery_distance": 2235,
                "number_of_items": 4,
                "time": "2021-10-12T13:00:00Z",
            },
            7_10,
        ),
        (
            {
                "cart_value": 1900,
                "delivery_distance": 4235,
                "number_of_items": 6,
                "time": "2023-01-20T15:01:00Z",
            },
            12_00,
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


@pytest.mark.parametrize(
    "payload, fee, expected_fee",
    [
        ({"number_of_items": 4}, 0, 0),
        ({"number_of_items": 12}, 0, 4_00),
        ({"number_of_items": 13}, 0, 5_70),
    ],
)
def test_num_item_fee(payload, fee, expected_fee):
    assert fee_calculator.num_item_fee(payload, fee) == expected_fee


@pytest.mark.parametrize(
    "payload, fee, expected_fee",
    [
        ({"time": "2021-10-12T13:00:00Z"}, 1_00, 1_00),
        ({"time": "2023-01-20T18:00:01Z"}, 1_00, 1_20),
        ({"time": "2023-01-20T18:01:11Z"}, 25_35, 30_42),
        ({"time": "2023-01-20T19:00:01Z"}, 1_00, 1_00),
    ],
)
def test_friday_fee(payload, fee, expected_fee):
    assert fee_calculator.friday_fee(payload, fee) == expected_fee


@pytest.mark.parametrize(
    "payload, fee, expected_fee",
    [
        ({}, 1_56, 1_56),
        ({}, 15_01, 15_00),
    ],
)
def test_max_allowed_fee(payload, fee, expected_fee):
    assert fee_calculator.max_allowed_fee(payload, fee) == expected_fee
