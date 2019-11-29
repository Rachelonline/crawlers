import os
import logging
import json
import azure.functions as func
from __app__.processor.adscorer import score_ad
from __app__.processor.scorers.cache import RedisCache
from __app__.utils.metrics.metrics import get_client, enable_logging
from __app__.utils.queue.message import decode_message


def main(
    inmsg: func.ServiceBusMessage,
    doc: func.Out[func.Document],
    sdoc: func.Out[func.Document],
) -> None:
    CACHE = RedisCache()

    DEFAULT_FUNCTIONS = {
        "frequency": {"attribute_list": ["age", "location", "gender"], "cache": CACHE},
        "twilio": {
            "account_sid": os.environ["account_sid"],
            "auth_token": os.environ["auth_token"],
            "cache": CACHE,
        },
    }
    azure_tc = get_client()
    enable_logging()

    message = decode_message(inmsg)
    score_msg = score_ad(message, functions=DEFAULT_FUNCTIONS)
    
    print(score_msg)
    # if score_msg:
    #     sdoc.set(func.Document.from_json(score_msg))

    # doc.set(func.Document.from_json(inmsg.get_body()))

    azure_tc.track_metric("ad-processed", 1, properties={"domain": message["domain"]})
    azure_tc.flush()
