import azure.functions as func
from __app__.adlistingcrawler.adlistingcrawler import crawl_ad_listing
from __app__.utils.crawling.crawl_job import crawl_job
from __app__.utils.queue.message import encode_message

def main(inmsg: func.ServiceBusMessage, outmsg: func.Out[str]) -> None:
    ad_listing_parse_message = crawl_job(inmsg, "regioncrawl", crawl_ad_listing)
    if ad_listing_parse_message:
        outmsg.set(encode_message(ad_listing_parse_message))
