import azure.functions as func
from __app__.adparser.adparser import parse_ad
from __app__.utils.queue.message import decode_message, encode_message


def main(
    inmsg: func.ServiceBusMessage, processmsg: func.Out[str], imgmsg: func.Out[str]
) -> None:
    message = decode_message(inmsg)
    process_msg, image_msgs = parse_ad(message)
    if process_msg:
        processmsg.set(encode_message(process_msg))
    if image_msgs:
        imgmsg.set(encode_message(image_msgs))
