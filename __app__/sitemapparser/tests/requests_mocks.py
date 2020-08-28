from urllib.parse import urlparse
import os

MOCK_RESPONSE_FOLDER = "__app__/sitemapparser/tests/test-html/mock_responses"


class MockResponse:
    def __init__(self, text):
        self.text = text


def get_html_text(filename):
    with open(os.path.join(MOCK_RESPONSE_FOLDER, filename), encoding="utf8") as html:
        return html.read()


class AdultSearchMock:
    RESPONSES = {
        "us_region": "20200827_adultsearch_com-region-alabama.html",
        "ca_region": "20200828_adultsearch_com-region-britishcolumbia.html",
        "us_category": "20200827_adultsearch_com-category-al-female-escorts.html",
        "ca_category": "20200828_adultsearch_com-category-bc-female-escorts.html",
    }

    def __init__(self):
        # Only return 1 province, state, and linked category pages for dozens of links.
        self.should_return = {
            "region": {"us": True, "ca": True},
            "category": {"us": True, "ca": True},
        }

    def _get_resp_for(self, url, key):
        if self.should_return[key]["ca"] and url.netloc == "ca.adultsearch.com":
            self.should_return[key]["ca"] = False
            return MockResponse(get_html_text(AdultSearchMock.RESPONSES["ca_" + key]))
        elif self.should_return[key]["us"] and url.netloc == "adultsearch.com":
            self.should_return[key]["us"] = False
            return MockResponse(get_html_text(AdultSearchMock.RESPONSES["us_" + key]))
        else:
            return None  # so parser does not get duplicate responses

    def get(self, *args):
        url = urlparse(args[0])
        num_path_segments = len(url.path.strip("/").split("/"))

        if num_path_segments == 1:  # e.g. domain/alabama/
            return self._get_resp_for(url, "region")
        elif num_path_segments == 2:  # e.g. domain/alabama/female-escorts
            return self._get_resp_for(url, "category")
        else:
            raise Exception("Unexpected request made, no matching mock.")
