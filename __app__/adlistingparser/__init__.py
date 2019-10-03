import logging
import json
import azure.functions as func

from __app__.adlistingparser.adlistingparser import parse_ad_listing


def main(
    inmsg: func.ServiceBusMessage, admsg: func.Out[str], contmsg: func.Out[str]
) -> None:
    message = json.loads(inmsg.get_body().decode("utf-8"))
    ad_url_msgs, continued_listing_msgs = parse_ad_listing(message)
    if ad_url_msgs:
        admsg.set(json.dumps(ad_url_msgs))
    if continued_listing_msgs:
        contmsg.set(json.dumps(continued_listing_msgs))
