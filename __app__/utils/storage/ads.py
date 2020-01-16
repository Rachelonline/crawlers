from datetime import datetime
from uuid import uuid4
from __app__.utils.storage.blob_store import save_blob, get_blob

STORAGE_CONTAINER = "ads"


def save_ad_page(html: str) -> str:
    blob_uri = save_blob(f"{STORAGE_CONTAINER}/{str(uuid4())}", html)
    return blob_uri


def get_ad_page(ad_uri: str) -> str:
    return get_blob(ad_uri)
