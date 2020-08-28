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
        self.return_ca_region = True
        self.return_us_region = True
        self.return_ca_category = True
        self.return_us_category = True

    def get(self, *args):
        url = urlparse(args[0])
        num_path_segments = len(url.path.strip("/").split("/"))

        if num_path_segments == 1:  # region page
            if self.return_ca_region and url.netloc == "ca.adultsearch.com":
                resp_text = get_html_text(AdultSearchMock.RESPONSES["ca_region"])
                self.return_ca_region = False
            elif self.return_us_region and url.netloc == "adultsearch.com":
                resp_text = get_html_text(AdultSearchMock.RESPONSES["us_region"])
                self.return_us_region = False
            else:
                return None  # so parser skips subsequent regions
        elif num_path_segments == 2:  # category page
            if self.return_ca_category and url.netloc == "ca.adultsearch.com":
                resp_text = get_html_text(AdultSearchMock.RESPONSES["ca_category"])
                self.return_ca_category = False
            elif self.return_us_category:
                resp_text = get_html_text(AdultSearchMock.RESPONSES["us_category"])
                self.return_us_category = False
            else:
                return None  # so parser skips subsequent categories
        else:
            raise Exception("Unexpected request made, no matching mock.")

        return MockResponse(resp_text)
