import os
from urllib.parse import urljoin
from azure.storage.blob import BlobClient
from azure.core.exceptions import ResourceNotFoundError, ClientAuthenticationError


OLD_STORAGE_URL = "https://picrawling.blob.core.windows.net"
STORAGE_URL = "https://crawlin.blob.core.windows.net"


def save_blob(blob_path: str, content) -> None:
    ACCOUNT_KEY = os.getenv("STORAGE_KEY")
    blob_uri = urljoin(STORAGE_URL, blob_path)
    blob = BlobClient.from_blob_url(blob_uri, credential=ACCOUNT_KEY)
    blob.upload_blob(content)
    return blob_uri

def _fall_back_get_blob(blob_uri: str) -> str:
    ACCOUNT_KEY = os.getenv("BLOB_STORAGE_KEY")
    blob = BlobClient.from_blob_url(blob_uri, credential=ACCOUNT_KEY)
    return blob.download_blob().content_as_text()

def get_blob(blob_uri: str) -> str:
    try:
        ACCOUNT_KEY = os.getenv("STORAGE_KEY")
        blob = BlobClient.from_blob_url(blob_uri, credential=ACCOUNT_KEY)
        return blob.download_blob().content_as_text()
    except (ResourceNotFoundError, ClientAuthenticationError):
        return _fall_back_get_blob(blob_uri)
