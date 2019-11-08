import os
import logging
import json
import azure.functions as func
from __app__.adparser.scores.cache import RedisCache
from __app__.adscorer.adscorer import score_ad

CACHE = RedisCache()

DEFAULT_FUNCTIONS = {
    "frequency": {
        "attribute_list": [
            "emails",
            "location"
        ],
        "rc": CACHE
    },
    "twilio": {
        "account_sid": os.environ["account_sid"],
        "auth_token": os.environ["auth_token"],
        "rc": CACHE
    }
}
def main(
    inmsg: func.ServiceBusMessage, scoremsg: func.Out[str]) -> None:
    message = json.loads(inmsg.get_body().decode("utf-8"))
    score_msg = score_ad(message, functions=DEFAULT_FUNCTIONS)
    if score_msg:
        scoremsg.set(json.dumps(score_msg))
