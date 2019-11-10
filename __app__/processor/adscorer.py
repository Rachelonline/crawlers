from datetime import datetime
from copy import deepcopy
import logging
from __app__.utils.metrics.metrics import get_client, enable_logging
from __app__.processor.scorers.functions import (
    twilio_score,
    frequency_scores
)

PHONE_SCORERS = {
    "twilio": twilio_score,
    "frequency": frequency_scores
}


def score_ad(message: dict, functions={}) -> dict:
    """
    Takes in a message and a dictionary of scoring functions 
    and the function arguments. Please see the README for a
    sample argument for functions
    """

    azure_tc = get_client()
    enable_logging()

    ad_data = message.get("ad-data")

    if not ad_data:
        logging.warning(
            "No ad-data in message"
        )
        azure_tc.track_metric("ad-score-no-data", 1)
        return {}
    
    ppn = ad_data.get("primary-phone-number")
    
    if not ppn:
        logging.warning(
            "No primary phone number to score for ad"
        )
        azure_tc.track_metric("ad-score-no-number", 1)
        return {}

    score_msg = {}
    
    for func, args in functions.items():
        try:
            score = PHONE_SCORERS[func](
                msg=ad_data,
                **args
            )
            if score:
                score_msg[func] = score
            else:
                azure_tc.track_metric(
                    "ad-score-failure", 1, properties={
                        "primary-phone-number": ppn,
                        "scorer": func
                    }
                )

        except Exception as e:
            logging.error(
                f"Error while running {func} scorer. Error: {e}"
            )
            raise e

    score_msg["scored_on"] = datetime.utcnow().replace(microsecond=0)
    score_msg["phone"] = ppn
    
    azure_tc.track_metric(
        "ad-score-success", 1, properties={"primary-phone-number": ppn}
    )
    azure_tc.flush()
    return score_msg
            

