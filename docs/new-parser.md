# New Parser

Please read the [design](./design.md) to understand the structure of the code. To add a new parser for a website:

### Ad Parser
1. Create a new HTML for the ad in `__app__/adparser/tests/test-html`. Paste the HTML from the ad you want to parse.
2. Add the expected JSON file for the ad to `__app__/adparser/ad-test-data`.
3. Create a new file for the parser in `__app__/adparser/sites`.
    1. If you want to test out the parser to see if it gets the HTML tag you wanted, you can load the HTML in the repl and test it first. Open the repl by typing `python`. Then type each of these command individually in the repl.

        ```
            import os
            import re
            import from bs4 import BeautifulSoup

            file_path = "__app__/adparser/tests/test-html/20191106-escortdirectory_com.html"
            html = open(file_path, encoding="utf8").read()
            soup = BeautifulSoup(html, "html.parser")
        ```
4. Open `__app__/adparser/adparser.py`
    1. Add an import for your parser
    2. Add the domain and the parser name to the `AD_PARSERS` dictionary
5. Run all the tests `python -m pytest`

### Ad Listing Parser
1. Add the ad listing HTML to `__app__/adlistingparser/tests/test-html`
2. Add the expected ad listing JSON data to `__app__/adlistingparser/tests/test-data`
3. Add your parser to `__app__/adlistingparser/sites/`
4. Add your parser to the `__app__/adlistingparser/adlistingparser.py`
    1. Import your parser
    2. Add it to the `AD_LISTING_PARSERS`
5. Run all the tests `python -m pytest`

### Site Mapping Parser
1. Add the site mapping HTML to `__app__/sitemapparser/tests/test-html`
2. Add the expected ad listing JSON file to `__app__/sitemapparser/tests/test-data`
3. Add your parsing code to `__app__/sitemapparser/sites/`
4. Add your parser to the `__app__/sitemapparser/sitemapparser.py`
    1. Import your parser
    2. Add it to the `SITE_PARSERS`
4. Run all the tests `python -m pytest`
