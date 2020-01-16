import pytest
from datetime import datetime
from unittest.mock import ANY
from tests.fixtures.no_network import *
from __app__.utils.ads.adstore import save_ad_page, get_ad_page


@pytest.fixture(autouse=True)
def mock_uuid_storage_url(monkeypatch):
    monkeypatch.setattr("__app__.utils.storage.ads.uuid4", lambda: "uuid")



def test_save_ad_page(no_azure_blob_service):
    expected = "https://blob.store/ads/uuid"
    actual = save_ad_page("<html>", datetime(2525, 1, 1), "test-domain")

    assert expected == actual
    no_azure_blob_service.return_value.upload_blob.assert_called_with("<html>")


def test_get_ad_page(no_azure_blob_service):
    get_ad_page("blob-uri")
    no_azure_blob_service.assert_called_with("blob-uri", credential=ANY)
    no_azure_blob_service.return_value.download_blob.return_value.content_as_text.assert_called()
