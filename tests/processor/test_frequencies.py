from datetime import datetime
import pytest
from unittest.mock import MagicMock, patch, PropertyMock

from __app__.processor.adscorer import score_ad
from __app__.processor.scorers.functions import (
    frequency_scores,
    frequency_score_helper,
    twilio_score,
)
from tests.fixtures.no_network import *
from tests.fixtures.spam_cache import test_cache


@pytest.mark.parametrize(
    "pnumber, locations, expected_scores",
    [
        (
            "+1-347-687-5904",
            [
                "NYC",
                "NYC",
                "PORTLAND",
                "BOSTON",
                "PORTLAND",
            ],
            [1, 2, 1, 1, 2],
        ),
        (
            "+1-347-687-5904",
            ["NYC", "NYC", "NYC", "NYC", "NYC"],
            [1, 2, 3, 4, 5],
        ),
    ],
)
def test_location_frequency_helper(
    test_cache,
    pnumber,
    locations,
    expected_scores,
):

    for loc, escore in zip(locations, expected_scores):
        score = frequency_score_helper(
            phone_number=pnumber,
            attribute="location",
            value=loc,
            cache=test_cache,
        )
        assert score == escore

@pytest.mark.parametrize(
    "pnumber, attributes, values, expected_scores",
    [
        (
            "+1-347-687-5904",
            ["location", "gender", "age"],
            ["NYC", "female", "25"],
            [1, 1, 1],
        )
    ],
)
def test_attributes_frequency(
    test_cache,
    pnumber,
    attributes,
    values,
    expected_scores,
):

    msg = {"primary-phone-number": pnumber}
    for attribute, value in zip(attributes, values):
        msg[attribute] = value

    scores = frequency_scores(
        msg, attributes, test_cache
    )
    for attribute, value, escore in zip(
        attributes, values, expected_scores
    ):
        assert scores[attribute][value] == escore


