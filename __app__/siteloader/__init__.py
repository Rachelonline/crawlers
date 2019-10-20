import datetime
import json
import logging
import azure.functions as func

from .siteloader import sitemapping_jobs


def main(timer: func.TimerRequest, queuemsg: func.Out[str]) -> None:
    if timer.past_due:
        logging.info("Sitemapping timer is past due!")
    jobs = sitemapping_jobs()
    queuemsg.set(json.dumps(jobs))
