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




@patch("__app__.processor.scorers.functions.twilio_request")
@pytest.mark.parametrize(
    "pnumber, tstatus, tscore, expected_score",
    [
        ("+1-347-687-5904", "successful", 0.1, 0.1),
        ("+1-347-687-5904", "successful", 0.2, 0.2),
        ("+1-347-687-5905", "failure", None, None),
        ("+1-347-687-5906", "successful", 0.5, 0.5),
        (None, "successful", None, None),
    ],
)
def test_twilio_result(
    mock_twilio, test_cache, pnumber, tstatus, tscore, expected_score
):
    msg = {"primary-phone-number": pnumber}
    mock_twilio_resp = MagicMock()
    mock_twilio_resp.add_ons = {
        "status": tstatus,
        "results": {"truecnam_truespam": {"result": {"spam_score": tscore}}},
    }

    mock_twilio.return_value = mock_twilio_resp

    score = twilio_score(msg, "TEST_SID", "TEST_TOKEN", test_cache)
    assert score == expected_score
    assert (
        test_cache.get_cached_score(
            phone_number=msg["primary-phone-number"], score_key="truespam"
        )
        == expected_score
    )


def test_twilio_cached_result(test_cache):
    msg = {"primary-phone-number": "+1-347-687-5904"}
    test_cache.put_cached_score(
        phone_number=msg["primary-phone-number"], score_key="truespam", score=10
    )

    score = twilio_score(msg, "TEST_SID", "TEST_TOKEN", test_cache)
    assert score == 10
