import logging
import json
import azure.functions as func

from __app__.imagecrawler.imagecrawler import crawl_image


def main(inmsg: func.ServiceBusMessage) -> None:
    message = json.loads(inmsg.get_body().decode("utf-8"))
    crawl_image(message)
