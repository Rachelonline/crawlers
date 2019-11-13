import json
import azure.functions as func
from __app__.adlistingcrawler.adlistingcrawler import crawl_ad_listing
from __app__.utils.crawling.crawl_job import crawl_job


def main(inmsg: func.ServiceBusMessage, outmsg: func.Out[str]) -> None:
    ad_listing_parse_message = crawl_job(inmsg, "regioncrawl", crawl_ad_listing)
    if ad_listing_parse_message:
        outmsg.set(json.dumps(ad_listing_parse_message))
