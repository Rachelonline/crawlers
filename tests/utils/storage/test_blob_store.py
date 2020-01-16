import pytest
from unittest.mock import ANY
from tests.fixtures.no_network import *
from __app__.utils.storage.blob_store import save_blob, get_blob


def test_save_blob(no_azure_blob_service):
    expected = "https://blob.store/blob/path"
    actual = save_blob("blob/path", "<html>")
    assert expected == actual
    no_azure_blob_service.assert_called_with(
        "https://blob.store/blob/path", credential=ANY
    )
    no_azure_blob_service.return_value.upload_blob.assert_called_with("<html>")


def test_get_blob(no_azure_blob_service):
    get_blob("blob-uri")
    no_azure_blob_service.assert_called_with(
        "blob-uri", credential=ANY
    )
    no_azure_blob_service.return_value.download_blob.return_value.content_as_text.assert_called()
