import pytest
from unittest.mock import MagicMock

@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.delattr("requests.sessions.Session.request")

@pytest.fixture(autouse=True)
def no_azure_table_service(monkeypatch):
    mock_table_service = MagicMock()
    monkeypatch.setattr("utils.table.base_table.TableService", mock_table_service)

