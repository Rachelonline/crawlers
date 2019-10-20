import datetime
import json
import logging
import azure.functions as func

from __app__.adlistingloader.adlistingloader import ad_listing_loader


def main(timer: func.TimerRequest, queuemsg: func.Out[str]) -> None:
    if timer.past_due:
        logging.info("Ad Listing loader timer is past due!")
    jobs = ad_listing_loader()
    queuemsg.set(json.dumps(jobs))
