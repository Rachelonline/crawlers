from __app__.adparser.scores.cache import RedisCache
from twilio.rest import Client
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

def frequency_scores(msg: dict, attribute_list: str, rc: RedisCache) -> dict:
    """
    Calls frequency_score_helper on a list of attributes
    Aggregates scores in a dictionary and returns
    """
    frequencies = {}
    phone_number = msg.get("primary-phone-number")

    if not phone_number:
        logger.error(
            "No primary-phone-number in message...returning no frequency scores"
        )
        return frequencies

    for attribute in attribute_list:
        attributes = msg.get(attribute)
        if not attributes:
            logger.warning(
                f"Message missing attribute {attribute} for frequency score"
            )

        else:
            frequencies[attribute] = frequency_score_helper(
                phone_number,
                attributes,
                rc
            )

    return frequencies

def frequency_score_helper(phone_number: str, attribute: str, cache: RedisCache) -> int:
    """
    Takes in a phone number and an attribute, outputs how many times that number
    has corresponded to the attribute
    """
    freq_score = cache.increment_cached_score(
        phone_number=phone_number,
        score_key=f"frequency_score_{attribute}",
        amount=0
    )
    return freq_score


def twilio_score(msg: dict, account_sid: str, auth_token: str, rc: RedisCache = None) -> dict:
    """
    Takes in a phone number and returns a twilio spam score

    :param phone_number: phone number with or without +country code
    :param account_sid: twilio account id
    :param auth_token: generated twillion auth token

    :returns scores: {"spam_score": score, "spam_database_match": bool}
    """
    phone_number = msg.get("primary-phone-number")

    if not phone_number:
        logger.error(
            "No primary-phone-number in message...returning no twilio scores"
        )
        return {}
    
    client = Client(account_sid, auth_token)

    # This request would need to get changed if there is a need for other add-ons
    resp = client.lookups.phone_numbers(phone_number).fetch(add_ons=['truecnam_truespam'])

    if (resp.add_ons.get("status") != "successful") or (len(resp.add_ons) < 1):
        # No response from twilio API
        return {}

    # This response would need to get changed if there is a need for other add-ons
    scores = resp.add_ons.get("results").get("truecnam_truespam").get("result")
    
    if rc:
        
        rc.put_cached_score(
            phone_number=phone_number,
            score_key="twilio_score",
            score=scores, 
            expire=604800 # Expire after a week
        )

    return scores
    