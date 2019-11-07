import os
import logging
import json
import azure.functions as func

from __app__.adscorer.adscorer import score_ad

DEFAULT_FUNCTIONS = {
    "frequency": {
        "attribute_list": [
            "emails",
            "location"
        ]
    },
    "twilio": {
        "account_sid": os.environ["account_sid"],
        "auth_token": os.environ["auth_token"]
    }
}
def main(
    inmsg: func.ServiceBusMessage, scoremsg: func.Out[str]) -> None:
    message = json.loads(inmsg.get_body().decode("utf-8"))
    score_msg = score_ad(message, functions=DEFAULT_FUNCTIONS)
    if score_msg != {}:
        scoremsg.set(json.dumps(score_msg))
