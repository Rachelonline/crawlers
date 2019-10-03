import logging
import json
import azure.functions as func

from __app__.adlistingcrawler.adlistingcrawler import crawl_ad_listing


def main(inmsg: func.ServiceBusMessage, outmsg: func.Out[str]) -> None:
    message = json.loads(inmsg.get_body().decode("utf-8"))
    ad_listing_parse_message = crawl_ad_listing(message)
    if ad_listing_parse_message:
        outmsg.set(json.dumps(ad_listing_parse_message))
