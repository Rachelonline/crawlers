from datetime import datetime
from __app__.utils.storage.ads import save_ad_page as new_save_ad_page, get_ad_page as new_get_ad_page


def save_ad_page(html: str, crawled_on: datetime, domain: str) -> str:
    return new_save_ad_page(html)


def get_ad_page(blob_uri: str) -> str:
    return new_get_ad_page(blob_uri)
