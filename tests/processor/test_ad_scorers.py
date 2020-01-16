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



@pytest.fixture()
def test_functions(test_cache):
    CACHE = test_cache
    return {
        "frequency": {
            "attribute_list": [
                "gender",
                "location",
                "age",
            ],
            "cache": CACHE,
        },
        "twilio": {
            "account_sid": "test_account_sid",
            "auth_token": "test_auth_token",
            "cache": CACHE,
        },
    }

@patch(
    "__app__.processor.scorers.functions.twilio_request",
    MagicMock(
        return_value=MagicMock(
            add_ons={
                "status": "successful",
                "results": {
                    "truecnam_truespam": {"result": {"spam_score": 0.5}}
                },
            }
        )
    ),
)
@patch(
    "__app__.processor.adscorer.get_client", MagicMock()
)
@patch(
    "__app__.processor.adscorer.enable_logging",
    MagicMock(),
)
@pytest.mark.parametrize(
    "pnumber, attributes, values, expected_freq_scores, expected_twilio_score",
    [
        (
            "+1-347-687-5904",
            ["location", "gender", "age"],
            ["NYC", "female", "25"],
            [1, 2, 3],
            0.5,
        )
    ],
)
def test_score_ad(
    test_functions,
    pnumber,
    attributes,
    values,
    expected_freq_scores,
    expected_twilio_score,
):

    msg = {"ad-data": {"primary-phone-number": pnumber}}
    for attribute, value in zip(attributes, values):
        msg["ad-data"][attribute] = value

    for fscore in expected_freq_scores:

        scores = score_ad(msg, test_functions)

        for attribute, value in zip(attributes, values):
            assert (
                scores["frequency"][attribute][value]
                == fscore
            )

        assert scores["twilio"] == expected_twilio_score
