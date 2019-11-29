import itertools
import pytest
from unittest.mock import MagicMock, ANY

from tests.fixtures.no_network import *
from __app__.utils.queue.message import decode_message, encode_message


@pytest.fixture
def mock_small_msg():
    mock_msg = MagicMock()
    mock_msg.get_body.return_value = b'{"small": "msg"}'
    return mock_msg


@pytest.fixture
def mock_large_msg(monkeypatch):
    mock_msg = MagicMock()
    mock_msg.get_body.return_value = b'{"blob-message": "blob-uri"}'
    return mock_msg


def test_decode_small_msg(mock_small_msg):
    assert decode_message(mock_small_msg) == {"small": "msg"}


def test_decode_large_msg(mock_large_msg, no_azure_blob_service):
    expected = {"large": "msg"}
    no_azure_blob_service.return_value.download_blob.return_value.content_as_text.return_value = (
        '{"large": "msg"}'
    )

    assert decode_message(mock_large_msg) == expected
    no_azure_blob_service.assert_called_with("blob-uri", credential=ANY)
    no_azure_blob_service.return_value.download_blob.return_value.content_as_text.assert_called()


def test_encode_small_msg():
    assert encode_message({"small": "msg"}) == '{"small": "msg"}'


@pytest.fixture
def large_msg(monkeypatch):
    monkeypatch.setattr("__app__.utils.queue.message.MAX_MESSAGE_BYTES", 100)
    monkeypatch.setattr("__app__.utils.queue.message.STORAGE_URL", "blob-storage")
    monkeypatch.setattr("__app__.utils.queue.message.uuid4", lambda: "uuid")
    return {"very large message": "that should go to blob yo!"}  # should be 101 bytes


def test_encode_large_msg(large_msg, no_azure_blob_service):
    expected = '{"blob-message": "blob-storage/uuid"}'
    actual = encode_message(large_msg)

    assert expected == actual
    no_azure_blob_service.assert_called_with("blob-storage/uuid", credential=ANY)
    no_azure_blob_service.return_value.upload_blob.assert_called()


def test_send_list_of_msgs(large_msg, no_azure_blob_service):
    expected = '[{"small": "msg"}, {"blob-message": "blob-storage/uuid"}]'
    actual = encode_message([{"small": "msg"}, large_msg])

    assert expected == actual
    no_azure_blob_service.assert_called_with("blob-storage/uuid", credential=ANY)
    no_azure_blob_service.return_value.upload_blob.assert_called()
