from datetime import datetime
import json
from uuid import uuid4
from azure.storage.blob import BlobClient
from base64 import urlsafe_b64encode, urlsafe_b64decode


ACCOUNT_KEY = ""
STORAGE_URL = "https://picrawling.blob.core.windows.net/test-ads"


def _build_ad_page_url(date: datetime, domain: str):
    return f"{STORAGE_URL}/{date.year}/{date.month:02}/{date.day:02}/{domain.replace('/','')}/{str(uuid4())}"


def save_ad_page(html: str, crawled_on: datetime, domain: str) -> str:
    blob_uri = _build_ad_page_url(crawled_on, domain)
    blob = BlobClient(blob_uri, credential=ACCOUNT_KEY)
    blob.upload_blob(html)
    return blob_uri


def get_ad_page(blob_uri: str) -> str:
    blob = BlobClient(blob_uri, credential=ACCOUNT_KEY)
    return blob.download_blob().content_as_text()
