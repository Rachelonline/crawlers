import logging
import json
import azure.functions as func

from adcrawler.adcrawler import crawl_ad


def main(inmsg: func.ServiceBusMessage, outmsg: func.Out[str]) -> None:
    message = json.loads(inmsg.get_body().decode("utf-8"))
    ad_parse_message = crawl_ad(message)
    outmsg.set(json.dumps(ad_parse_message))
