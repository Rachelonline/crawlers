from datetime import datetime
import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from __app__.processor.spam_check import in_customer_region
from tests.fixtures.no_network import *


SEA_LOC_DATA = {
    "address_components": [
        {
            "long_name": "King County",
            "short_name": "King County",
            "types": ["administrative_area_level_2", "political"],
        }
    ]
}

NDAKOTA = {
    "address_components": [
        {
            "long_name": "North Dakota",
            "short_name": "North Dakota",
            "types": ["administrative_area_level_1", "political"],
        }
    ]
}

NOT_CUST_DATA = {
    "address_components": [
        {
            "long_name": "Narnia",
            "short_name": "Narnia",
            "types": ["administrative_area_level_2", "political"],
        }
    ]
}


@pytest.fixture(autouse=True)
def mock_get_place(monkeypatch):
    fake_location_data = {
        "seattle": SEA_LOC_DATA,
        "north dakota": NDAKOTA,
        "not_customer": NOT_CUST_DATA,
    }

    monkeypatch.setattr(
        "__app__.utils.locations.redis_cache.get_connection", lambda: fake_location_data
    )

    # so we don't have to json encode our test data
    monkeypatch.setattr("__app__.utils.locations.redis_cache.json.loads", lambda x: x)


@pytest.mark.parametrize(
    "message, expected",
    [
        ({"location": {"placeid": "seattle"}}, True),
        ({"location": {"placeid": "north dakota"}}, True),
        ({"location": {"placeid": "not_customer"}}, False),
        ({"location": {"malformed": "data"}}, False),  # shouldn't happen
        ({}, False),
    ],
)
def test_in_customer_region(message, expected):
    assert in_customer_region(message) == expected
