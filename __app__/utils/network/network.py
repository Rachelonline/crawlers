import requests
from urllib.parse import urlparse
from __app__.utils.network.headers import get_headers
from __app__.utils.network.cookies import get_cookies
from __app__.utils.metrics.metrics import get_client

MAX_RETRIES = 4
CONNECTION_TIMEOUT = 0.7


class BaseCrawlError(Exception):
    def __init__(self, code, url):
        self.code = code
        self.url = url

    def __str__(self):
        return f"{self.code}: {self.url}"


class CrawlError(BaseCrawlError):
    pass


class NotFound(BaseCrawlError):
    pass


def get_url(url, params={}):
    azure_tc = get_client()
    domain = "{uri.scheme}://{uri.netloc}".format(uri=urlparse(url))

    try:
        headers = get_headers()
        cookies = get_cookies(domain)
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=CONNECTION_TIMEOUT,
            cookies=cookies,
        )
        response.raise_for_status()
        azure_tc.track_metric("crawl", 1, properties={"code": 200, "domain": domain})
        azure_tc.flush()
        return response.text
    except requests.exceptions.HTTPError as err:
        status_code = err.response.status_code
        azure_tc.track_metric(
            "crawl", 1, properties={"code": status_code, "domain": domain}
        )
        azure_tc.flush()
        if status_code == 404:
            raise NotFound(status_code, url)
        if status_code == 400 or status_code > 404:
            raise CrawlError(status_code, url)
        raise
    except requests.exceptions.ReadTimeout as err:
        status_code = 999
        azure_tc.track_metric(
            "crawl", 1, properties={"code": status_code, "domain": domain}
        )
        azure_tc.flush()
        raise CrawlError(status_code, url)
    except requests.exceptions.ConnectTimeout as err:
        status_code = 888
        azure_tc.track_metric(
            "crawl", 1, properties={"code": status_code, "domain": domain}
        )
        azure_tc.flush()
        raise CrawlError(status_code, url)
    except ConnectionError as err:
        status_code = 998
        azure_tc.track_metric(
            "crawl", 1, properties={"code": status_code, "domain": domain}
        )
        azure_tc.flush()
        raise CrawlError(status_code, url)
