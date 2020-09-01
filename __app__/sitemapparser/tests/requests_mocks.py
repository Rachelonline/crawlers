from urllib.parse import urlparse
import os
from unittest.mock import Mock

MOCK_RESPONSE_FOLDER = "__app__/sitemapparser/tests/test-html/mock_responses"


def get_html_text(filename):
    with open(os.path.join(MOCK_RESPONSE_FOLDER, filename), encoding="utf8") as html:
        return html.read()


class MockResponse:
    def __init__(self, text):
        self.text = text


class RespondOnce:
    def __init__(self, filename):
        self.page = MockResponse(get_html_text(filename))
        self.generator = self.gen()

    def gen(self):
        yield self.page
        while True:
            yield None  # skip response for subsequent calls

    @property
    def resp(self):
        return next(self.generator)


class AdultSearchMock:
    def __init__(self):
        # Only return 1 province, state, and linked category pages for dozens of links.
        self.us_region = RespondOnce("20200827_adultsearch_com-region-alabama.html")
        self.ca_region = RespondOnce(
            "20200828_adultsearch_com-region-britishcolumbia.html"
        )
        self.ca_category = RespondOnce(
            "20200828_adultsearch_com-category-bc-female-escorts.html"
        )
        self.us_category = RespondOnce(
            "20200827_adultsearch_com-category-al-female-escorts.html"
        )

    def get(self, *args):
        url = urlparse(args[0])
        num_path_segments = len(url.path.strip("/").split("/"))

        if num_path_segments == 1:  # e.g. domain/alabama/
            return (
                self.ca_region.resp
                if url.netloc == "ca.adultsearch.com"
                else self.us_region.resp
            )
        elif num_path_segments == 2:  # e.g. domain/alabama/female-escorts
            return (
                self.ca_category.resp
                if url.netloc == "ca.adultsearch.com"
                else self.us_category.resp
            )
        else:
            raise Exception("Unexpected request made, no matching mock.")
