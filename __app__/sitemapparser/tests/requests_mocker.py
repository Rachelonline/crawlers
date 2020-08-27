from urllib.parse import urlparse
import responses
import re
import os

MOCK_RESPONSE_FOLDER = "__app__/sitemapparser/tests/test-html/mock_responses"

# Mapping of domain to associated mock responses.
SITE_MOCKS = {
    "adultsearch": [
        "20200827_adultsearch_com-region.html",
        "20200827_adultsearch_com-category.html",
    ]
}


def get_html_text(filename):
    with open(os.path.join(MOCK_RESPONSE_FOLDER, filename), encoding="utf8") as html:
        return html.read()


def mock_responses(domain):
    if domain == "adultsearch.com":
        print("in adultsearch domain")

        def req_callback(request):
            path_segments = urlparse(request.url).path.strip("/").split("/")

            print("request url is " + request.url)

            if path_segments.length == 1:  # region page
                print("Returning region page.")
                resp_text = get_html_text(SITE_MOCKS["adultsearch"][0])
            elif path_segments.length == 2:  # category page
                print("Returning category page.")
                resp_text = get_html_text(SITE_MOCKS["adultsearch"][1])

            return (200, {}, resp_text)

        responses.add_callback(
            responses.GET,
            re.compile("adultsearch.com"),  # match all incoming get requests
            callback=req_callback,
            content_type="text/html",
        )
