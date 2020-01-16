from base64 import urlsafe_b64encode, urlsafe_b64decode
from __app__.utils.storage.blob_store import save_blob, get_blob

STORAGE_CONTAINER = "images"


def encode_url(url: str) -> str:
    """ we're b64 encoding the urls so that we can get the images if we ever need to."""
    return urlsafe_b64encode(bytes(url, "utf-8")).decode("utf-8")


def _build_image_path(url: str):
    return f"{STORAGE_CONTAINER}/{encode_url(url)}"


def save_image(image: str, url: str) -> str:
    blob_uri = save_blob(_build_image_path(url), image)
    return blob_uri


def get_image(url: str) -> str:
    return get_blob(url)
