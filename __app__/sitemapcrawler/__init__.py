import azure.functions as func
from __app__.sitemapcrawler.sitemapcrawler import sitemap
from __app__.utils.crawling.crawl_job import crawl_job
from __app__.utils.queue.message import encode_message

def main(inmsg: func.ServiceBusMessage, outmsg: func.Out[str]) -> None:
    sitemap_parse_message = crawl_job(inmsg, "sitecrawl", sitemap)
    if sitemap_parse_message:
        outmsg.set(encode_message(sitemap_parse_message))
