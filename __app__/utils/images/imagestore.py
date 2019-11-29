import os
from datetime import datetime
import json
from uuid import uuid4
from azure.storage.blob import BlobClient
from base64 import urlsafe_b64encode, urlsafe_b64decode


STORAGE_URL = "https://picrawling.blob.core.windows.net/test-images"


def encode_url(url: str) -> str:
    """ We're b64 encoding the URLs so that we can get the images if we ever need to."""
    return urlsafe_b64encode(bytes(url, "utf-8")).decode("utf-8")


def _build_image_url(url: str):
    return f"{STORAGE_URL}/{encode_url(url)}"


def save_image(html: str, url: str) -> str:
    ACCOUNT_KEY = os.getenv("BLOB_STORAGE_KEY")
    blob_uri = _build_image_url(url)
    blob = BlobClient.from_blob_url(blob_uri, credential=ACCOUNT_KEY)
    blob.upload_blob(html)
    return blob_uri


def get_image(url: str) -> str:
    blob_uri = _build_image_url(url)
    ACCOUNT_KEY = os.getenv("BLOB_STORAGE_KEY")
    blob = BlobClient.from_blob_url(blob_uri, credential=ACCOUNT_KEY)
    return blob.download_blob().content_as_text()
