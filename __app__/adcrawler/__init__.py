import azure.functions as func
from __app__.adcrawler.adcrawler import crawl_ad
from __app__.utils.crawling.crawl_job import crawl_job
from __app__.utils.queue.message import encode_message

def main(inmsg: func.ServiceBusMessage, outmsg: func.Out[str]) -> None:
    ad_parse_message = crawl_job(inmsg, "pagecrawl", crawl_ad)
    if ad_parse_message:
        outmsg.set(encode_message(ad_parse_message))
