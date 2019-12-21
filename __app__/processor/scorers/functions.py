from __app__.processor.scorers.cache import RedisCache
from twilio.rest import Client
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def location_distance(msg: dict):
    """
    Calculate the distance between the current location
    and one most previously seen
    """
    raise NotImplementedError


def days_since_seen(msg: dict):
    """
    Output the number of days since this number was
    last seen
    """
    raise NotImplementedError


def frequency_scores(msg: dict, attribute_list: str, cache: RedisCache) -> dict:
    """
    Calls frequency_score_helper on a list of attributes
    Aggregates scores in a dictionary and returns
    """
    frequencies = defaultdict(dict)
    phone_number = msg.get("primary-phone-number")

    if not phone_number:
        logger.error(
            "No primary-phone-number in message...returning no frequency scores"
        )
        return frequencies

    for attribute in attribute_list:
        attribute_value = msg.get(attribute)
        if not attribute_value:
            logger.warning(
                f"Message missing attribute {attribute_value} for frequency score"
            )

        else:
            frequencies[attribute][attribute_value] = frequency_score_helper(
                phone_number=phone_number,
                attribute=attribute,
                value=attribute_value,
                cache=cache,
            )
            attribute_history = cache.get_values_at_attribute(
                phone_number=phone_number,
                score_type="frequency_score",
                attribute=attribute,
            )
            for ah_key, ah_val in attribute_history.items():
                frequencies[attribute][ah_key] = ah_val

    return dict(frequencies)


def frequency_score_helper(
    phone_number: str, attribute: str, value: str, cache: RedisCache
) -> int:
    """
    Takes in a phone number and an attribute, outputs how many times that number
    has corresponded to the attribute
    """
    freq_score = cache.increment_cached_score(
        phone_number=phone_number,
        score_key=f"frequency_score_{attribute}_{value}",
        amount=1,
    )
    return freq_score


def twilio_request(client: Client, number: str):
    """
    Helper for making a twilio request
    """
    # This request would need to get changed if there is a need for other add-ons
    return client.lookups.phone_numbers(number).fetch(add_ons=["truecnam_truespam"])


def twilio_score(
    msg: dict, account_sid: str, auth_token: str, cache: RedisCache
) -> dict:
    """
    Takes in a phone number and returns a twilio spam score

    :param phone_number: phone number with or without +country code
    :param account_sid: twilio account id
    :param auth_token: generated twillion auth token

    :returns scores: {"spam_score": score, "spam_database_match": bool}
    """
    phone_number = msg.get("primary-phone-number")

    cached_score = cache.get_cached_score(
        phone_number=phone_number, score_key="truespam"
    )
    if cached_score:
        return cached_score.decode()

    if not phone_number:
        logger.error("No primary-phone-number in message...returning no twilio scores")
        return None

    client = Client(account_sid, auth_token)

    resp = twilio_request(client, phone_number)

    if (resp.add_ons.get("status") != "successful") or (len(resp.add_ons) < 1):
        # No response from twilio API
        logger.exception("No response from twilio API...returning no twilio score")
        return None

    # This response would need to get changed if there is a need for other add-ons
    scores = (
        resp.add_ons.get("results")
        .get("truecnam_truespam")
        .get("result")
        .get("spam_score")
    )

    cache.put_cached_score(
        phone_number=phone_number,
        score_key="truespam",
        score=scores,
        expire=604800,  # Expire after a week
    )

    return scores
