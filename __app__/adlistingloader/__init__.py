import azure.functions as func
from __app__.adlistingloader.adlistingloader import ad_listing_loader
from __app__.utils.queue.message import encode_message

def main(timer: func.TimerRequest, queuemsg: func.Out[str]) -> None:
    jobs = ad_listing_loader()
    queuemsg.set(encode_message(jobs))
