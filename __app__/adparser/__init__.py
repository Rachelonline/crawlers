import logging
import json
import azure.functions as func

#from __app__.adparser.adparser import parse_ad


def main(
    inmsg: func.ServiceBusMessage, processmsg: func.Out[str], imgmsg: func.Out[str]
) -> None:
    message = json.loads(inmsg.get_body().decode("utf-8"))
    print(message)
    return
    process_msg, image_msgs = parse_ad(message)
    if process_msg:
        processmsg.set(json.dumps(process_msg))
    if image_msgs:
        imgmsg.set(json.dumps(image_msgs))
