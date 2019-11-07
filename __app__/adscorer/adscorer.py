from datetime import datetime
from copy import deepcopy
from functools import partial
import logging
from __app__.utils.table.scores import ScoresTable
from __app__.utils.metrics.metrics import get_client, enable_logging
from __app__.phonescorer.scores.functions import (
    twilio_score,
    frequency_score
)

TABLE = ScoresTable()

PHONE_SCORERS = {
    "twilio": twilio_score,
    "frequency": frequency_score
}


def build_score_message(msg: str, score_data: dict) -> dict:
    score_msg = deepcopy(msg)
    score_msg["scores"] = score_data
    return score_msg

def score_ad(message: dict, functions={}) -> dict:
    azure_tc = get_client()
    enable_logging()

    ppn = message.get("primary-phone-number")
    
    if not ppn:
        logging.warning(
            "No primary phone number to score for ad"
        )
        azure_tc.track_metric("ad-score-no-number", 1)
        return {}

    score_data = {}
    for f,args in functions.items():
        scorer = partial(
            PHONE_SCORERS[f],
            **args
        )
        try:
            score_data[f] = scorer(message)
        except Exception as e :
            logging.warning(
                f"Error while running {f} scorer. Error: {e}"
            )
            azure_tc.track_metric(
                "ad-score-failure", 1, properties={
                    "primary-phone-number": ppn,
                    "scorer": f
                }
            )
    score_msg = build_score_message(message, score_data)
    score_msg["scored_on"] = datetime.now().replace(microsecond=0)
    score_msg["phone"] = ppn

    TABLE.save_score(ppn, score_msg)
    
    azure_tc.track_metric(
        "ad-score-success", 1, properties={"primary-phone-number": ppn}
    )
    azure_tc.flush()
    return score_msg
        

        
            

