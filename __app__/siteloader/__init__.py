import azure.functions as func
from __app__.utils.queue.message import encode_message
from __app__.siteloader.siteloader import sitemapping_jobs


def main(timer: func.TimerRequest, queuemsg: func.Out[str]) -> None:
    jobs = sitemapping_jobs()
    queuemsg.set(encode_message(jobs))
