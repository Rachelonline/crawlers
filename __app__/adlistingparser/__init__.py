import azure.functions as func
from __app__.adlistingparser.adlistingparser import parse_ad_listing
from __app__.utils.queue.message import decode_message, encode_message


def main(
    inmsg: func.ServiceBusMessage, admsg: func.Out[str], contmsg: func.Out[str]
) -> None:
    message = decode_message(inmsg)
    ad_url_msgs, continued_listing_msgs = parse_ad_listing(message)
    if ad_url_msgs:
        admsg.set(encode_message(ad_url_msgs))
    if continued_listing_msgs:
        contmsg.set(encode_message(continued_listing_msgs))
