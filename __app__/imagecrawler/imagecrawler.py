from datetime import datetime
import logging
from __app__.utils.network.network import get_url
from __app__.utils.table.images import ImagesTable
from __app__.utils.images.imagestore import save_image
from __app__.utils.metrics.metrics import get_client, enable_logging
from __app__.utils.throttle.throttle import check_throttle

TABLE = ImagesTable()


def crawl_image(message: dict) -> dict:
    azure_tc = get_client()
    enable_logging()

    image_url = message["image-url"]
    logging.info("starting image url: %s", image_url)
    check_throttle(image_url, azure_tc=azure_tc)
    domain = message["domain"]
    # We've already crawled this image
    if TABLE.is_crawled(image_url):
        logging.info("already crawled image: %s", image_url)
        azure_tc.track_metric(
            "image-already-crawled", 1, properties={"domain": message["domain"]}
        )
        return None

    image = get_url(image_url)
    crawled_on = datetime.utcnow().replace(microsecond=0)
    uri = save_image(image, image_url)

    message["metadata"].update({"image-crawled": crawled_on.isoformat()})

    logging.info("crawled image: %s", image_url)
    TABLE.mark_crawled(image_url, uri, message["metadata"])

    azure_tc.track_metric(
        "image-crawl-success", 1, properties={"domain": message["domain"]}
    )
    azure_tc.flush()
