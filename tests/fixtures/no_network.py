import pytest
from unittest.mock import MagicMock

@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.delattr("requests.sessions.Session.request")

@pytest.fixture(autouse=True)
def no_azure_table_service(monkeypatch):
    mock_table_service = MagicMock()
    monkeypatch.setattr("__app__.utils.table.base_table.TableService", mock_table_service)


@pytest.fixture(autouse=True)
def no_azure_blob_service(monkeypatch):
    mock_blob_client = MagicMock()
    monkeypatch.setattr("__app__.utils.ads.adstore.BlobClient", mock_blob_client)
    return mock_blob_client

@pytest.fixture(autouse=True)
def no_azure_metrics(monkeypatch):
    mock_telem_client = MagicMock()
    monkeypatch.setattr("__app__.utils.metrics.metrics.TelemetryClient", mock_telem_client)
    monkeypatch.setattr("__app__.utils.metrics.metrics.enable", lambda _: None)
    return mock_telem_client
