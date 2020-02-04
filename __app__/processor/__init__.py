import os
import logging
import json
import azure.functions as func
from __app__.processor.adscorer import score_ad
from __app__.processor.scorers.cache import RedisCache
from __app__.processor.spam_check import in_customer_region
from __app__.utils.metrics.metrics import get_client, enable_logging
from __app__.utils.queue.message import decode_message
from __app__.utils.locations.geocode import get_location


def geocode(message: dict) -> dict:
    ad_location = message["ad-data"].get("location")
    adlisting_location = message.get("ad-listing-data", {}).get("location")
    if adlisting_location:
        ad_location = f"{adlisting_location} {ad_location}"
    location = get_location(ad_location)
    message["location"] = location
    return message


def spam_detection(message: dict) -> dict:
    CACHE = RedisCache()
    score_fns = {
        "frequency": {"attribute_list": ["age", "location", "gender"], "cache": CACHE}
    }
    if in_customer_region(message):
        score_fns.update(
            {
                "twilio": {
                    "account_sid": os.environ["TWILIO_ACCOUNT_SID"],
                    "auth_token": os.environ["TWILIO_AUTH_TOKEN"],
                    "cache": CACHE,
                }
            }
        )
    return score_ad(message, functions=score_fns)


def main(
    inmsg: func.ServiceBusMessage,
    doc: func.Out[func.Document],
    sdoc: func.Out[func.Document],
) -> None:

    azure_tc = get_client()
    enable_logging()

    # processing ad data
    message = decode_message(inmsg)
    message = geocode(message)
    doc.set(func.Document.from_json(json.dumps(message)))

    # spam scoring
    score_msg = spam_detection(message)
    if score_msg:
        sdoc.set(func.Document.from_json(json.dumps(score_msg))

    azure_tc.track_metric("ad-processed", 1, properties={"domain": message["domain"]})
    azure_tc.flush()
