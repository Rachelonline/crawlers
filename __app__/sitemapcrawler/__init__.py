import logging
import json
import azure.functions as func


from __app__.sitemapcrawler.sitemapcrawler import sitemap


def main(inmsg: func.ServiceBusMessage, outmsg: func.Out[str]) -> None:
    message = json.loads(inmsg.get_body().decode("utf-8"))
    sitemap_parse_message = sitemap(message)
    if sitemap_parse_message:
        outmsg.set(json.dumps(sitemap_parse_message))
