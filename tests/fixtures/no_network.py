import pytest
from unittest.mock import MagicMock


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.delattr("requests.sessions.Session.request")


@pytest.fixture(autouse=True)
def no_azure_table_service(monkeypatch):
    mock_table_service = MagicMock()
    monkeypatch.setattr(
        "__app__.utils.table.base_table.TableService", mock_table_service
    )


@pytest.fixture(autouse=True)
def no_azure_blob_service(monkeypatch):
    mock_blob_client = MagicMock()
    monkeypatch.setattr("__app__.utils.ads.adstore.BlobClient", mock_blob_client)
    monkeypatch.setattr("__app__.utils.images.imagestore.BlobClient", mock_blob_client)
    monkeypatch.setattr("__app__.utils.queue.message.BlobClient", mock_blob_client)
    return mock_blob_client.from_blob_url


@pytest.fixture(autouse=True)
def no_azure_metrics(monkeypatch):
    mock_telem_client = MagicMock()
    monkeypatch.setattr(
        "__app__.utils.metrics.metrics.TelemetryClient", mock_telem_client
    )
    monkeypatch.setattr("__app__.utils.metrics.metrics.enable", lambda _: None)
    return mock_telem_client.from_blob_url


@pytest.fixture(autouse=True)
def no_service_bus(monkeypatch):
    mock_sb_client = MagicMock()
    monkeypatch.setattr(
        "__app__.utils.crawling.crawl_job.ServiceBusClient", mock_sb_client
    )
    return mock_sb_client


@pytest.fixture(autouse=True)
def no_redis_throttle(monkeypatch):
    mock_redis = MagicMock()
    mock_redis.llen.return_value = 0  # Throttles are wide open!
    monkeypatch.setattr(
        "__app__.utils.throttle.throttle.get_connection", lambda: mock_redis
    )
    return mock_redis
