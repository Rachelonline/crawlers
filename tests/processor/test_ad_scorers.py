from datetime import datetime
import pytest
from unittest.mock import MagicMock, patch, PropertyMock

from __app__.processor.adscorer import score_ad
from __app__.processor.scorers.functions import (
    frequency_scores,
    frequency_score_helper,
    twilio_score,
)


class TestCache(object):
    def __init__(self):
        self.test_cache = {}

    def get_cached_score(
        self, phone_number, score_key, default_score=None
    ):
        return self.test_cache.get(
            f"{phone_number}:{score_key}", default_score
        )

    def put_cached_score(
        self, phone_number, score_key, score, expire=False
    ):
        self.test_cache[
            f"{phone_number}:{score_key}"
        ] = score
        return score

    def increment_cached_score(
        self, phone_number, score_key, amount=1
    ):
        """
        Increment the cached score by a certain amount and return
        the incremeneted score
        """
        # If the key doesnt exist and is incremented then there is no expiration
        current_score = self.test_cache.get(
            f"{phone_number}:{score_key}", 0
        )
        self.test_cache[f"{phone_number}:{score_key}"] = (
            current_score + amount
        )
        return self.get_cached_score(
            phone_number, score_key
        )


class TestTwilio:
    @pytest.fixture(autouse=True)
    def test_cache(self):
        return TestCache()

    @patch(
        "__app__.processor.scorers.functions.twilio_request"
    )
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
        self,
        mock_twilio,
        test_cache,
        pnumber,
        tstatus,
        tscore,
        expected_score,
    ):
        msg = {"primary-phone-number": pnumber}
        mock_twilio_resp = MagicMock()
        mock_twilio_resp.add_ons = {
            "status": tstatus,
            "results": {
                "truecnam_truespam": {"result": tscore}
            },
        }

        mock_twilio.return_value = mock_twilio_resp

        score = twilio_score(
            msg, "TEST_SID", "TEST_TOKEN", test_cache
        )
        assert score == expected_score
        assert (
            test_cache.get_cached_score(
                phone_number=msg["primary-phone-number"],
                score_key="twilio_score",
            )
            == expected_score
        )

    def test_twilio_cached_result(self, test_cache):
        msg = {"primary-phone-number": "+1-347-687-5904"}
        test_cache.put_cached_score(
            phone_number=msg["primary-phone-number"],
            score_key="twilio_score",
            score=10,
        )

        score = twilio_score(
            msg, "TEST_SID", "TEST_TOKEN", test_cache
        )
        assert score == 10


class TestFrequency:
    @pytest.fixture()
    def test_cache(self):
        return TestCache()

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
        self,
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
        self,
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


class TestAdScorer:
    @pytest.fixture()
    def test_functions(self):
        CACHE = TestCache()
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
                        "truecnam_truespam": {"result": 0.5}
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
        self,
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
