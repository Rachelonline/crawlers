import json
import azure.functions as func
from __app__.adcrawler.adcrawler import crawl_ad
from __app__.utils.crawling.crawl_job import crawl_job


def main(inmsg: func.ServiceBusMessage, outmsg: func.Out[str]) -> None:
    ad_parse_message = crawl_job(inmsg, "pagecrawl", crawl_ad)
    if ad_parse_message:
        outmsg.set(json.dumps(ad_parse_message))
