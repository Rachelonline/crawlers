import pytest
from unittest.mock import ANY
from datetime import datetime
from tests.fixtures.no_network import *
from __app__.utils.storage.images import save_image, get_image


def test_save_image(no_azure_blob_service):
    expected = "https://blob.store/images/aW1nLXVybA=="
    actual = save_image("img", "img-url")
    assert expected == actual
    no_azure_blob_service.assert_called_with(expected, credential=ANY)
    no_azure_blob_service.return_value.upload_blob.assert_called_with("img")


def test_get_image(no_azure_blob_service):
    get_image("img-uri")
    no_azure_blob_service.assert_called_with("img-uri", credential=ANY)
    no_azure_blob_service.return_value.download_blob.return_value.content_as_text.assert_called()

