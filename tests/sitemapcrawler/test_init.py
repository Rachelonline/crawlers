import pytest
import json
from unittest.mock import MagicMock
from tests.fixtures.no_network import *
from __app__.sitemapcrawler import main


def test_main(monkeypatch):
    mock_output = MagicMock()

    mock_crawl_job = MagicMock()
    monkeypatch.setattr("__app__.sitemapcrawler.crawl_job", mock_crawl_job)
    mock_sitemap = MagicMock()
    monkeypatch.setattr("__app__.sitemapcrawler.sitemap", mock_sitemap)

    inmsg = "sitemap-crawl-msg"
    mock_crawl_job.return_value = None
    main(inmsg, mock_output)
    mock_crawl_job.assert_called_with(inmsg, "sitecrawl", mock_sitemap)
    assert mock_output.not_called()

    mock_crawl_job.return_value = {"sitemapparse": "message"}
    mock_crawl_job.assert_called_with(inmsg, "sitecrawl", mock_sitemap)
    assert mock_output.set.asser_called_with(json.dumps({"sitemapparse": "message"}))
