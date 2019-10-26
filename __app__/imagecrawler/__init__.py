import azure.functions as func
from __app__.imagecrawler.imagecrawler import crawl_image
from __app__.utils.crawling.crawl_job import crawl_job


def main(inmsg: func.ServiceBusMessage) -> None:
    crawl_job(inmsg, "imagecrawl", crawl_image)
