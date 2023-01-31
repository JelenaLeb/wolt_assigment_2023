from unittest import mock

import pytest
from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)


@pytest.mark.parametrize(
    "payload, status_code, expected_result",
    [
        (
            {
                "cart_value": 150_00,
                "delivery_distance": 2235,
                "number_of_items": 4,
                "time": "2021-10-12T13:00:00Z",
            },
            200,
            {"delivery_fee": 0},
        ),
        (
            {
                "cart_value": 7_90,
                "delivery_distance": 2235,
                "number_of_items": 4,
                "time": "2021-10-12T13:00:00Z",
            },
            200,
            {"delivery_fee": 710},
        ),
        (
            {
                "cart_value": 19_00,
                "delivery_distance": 4235,
                "number_of_items": 6,
                "time": "2023-01-20T15:01:00Z",
            },
            200,
            {"delivery_fee": 1200},
        ),
    ],
)
def test_post_fee_payload(payload, status_code, expected_result):
    response = client.post("/fee/", json=payload)

    assert response.status_code == status_code
    assert response.json() == expected_result


def test_post_fee_unknown_exception():
    payload = {
        "cart_value": 150_00,
        "delivery_distance": 2235,
        "number_of_items": 4,
        "time": "2021-10-12T13:00:00Z",
    }

    with mock.patch("src.api.fee_calculator.calculate_fee") as fn:
        fn.side_effect = RuntimeError("something happened")
        response = client.post("/fee/", json=payload)

    assert response.status_code == 500
    assert response.json() == {"detail": "Temporarily unavailable, try later"}
