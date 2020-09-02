## Sitemap Parsers Using Network Requests

For some sitemaps, it may not be possible to directly retrieve ad listing urls by grabbing links on the page or appending category and locations to the domain. For example, *adultsearch.com* does not have a search bar (which, as with *adultlook.com*, can be queried with an empty string for an informal adlisting page), and adlistings are stored in a nested structure.
<img src="C:\Users\Lucy\Documents\GitHub\crawlers\docs\imgs\nested_sitemap.JPG" alt="nested_sitemap" style="zoom: 33%;" />

As shown (blurrily) above, the structure of *adultsearch.com* goes **sitemap>region>category>ad listings by city**. In order to retrieve each of these subsequent pages, `app/sitemapparser/sites/adultsearch.py` uses the [requests](https://requests.readthedocs.io/en/master/) module. At each level, it finds a link to the next page (e.g. on the landing sitemap page, it selects all `h5 >a` tags, which are regional links like "Alabama"), makes a `requests.get(url)` call, and then parses the response using BeautifulSoup.

Aside from these calls, the parser is much the same as any other, just crawling through tags until it eventually finds the adlisting urls it's looking for. However, these types of parsers have an additional layer of testing.

#### Handling different subdomains

If the site uses multiple domains (e.g. *adultsearch.com* uses `ca.adultsearch.com` for Canada), the parser may need to prepend or retrieve a given page's subdomain. For an example, see `_find_domain` in the adultsearch sitemap parser, which grabs the domain from each page's canonical link.

### Testing with Requests

By default, `test_site_map_parsers.py` imports a [pytest fixture](https://docs.pytest.org/en/stable/fixture.html) from `no_network.py` which deletes the request attribute from the *requests* module. In effect, this isolates our sitemap tests, ignoring any external calls.

However, when writing a sitemap parser that actually needs to make request calls, we have to re-add this attribute and mock our `requests.get` (or other method) calls. *adultsearch.com* has already been implemented this way, and future tests should follow the same pattern:

1. For any page your parser needs to check through, add the HTML source of a sample page to `__app__/sitemapparser/tests/test-html/mock_responses`. This is the response your parser will be receiving in our mocked out tests.

      >  For *adultsearch.com*, there is a *regional* page (e.g. result of clicking "Alabama") and a *categorical* page (e.g. result of clicking Alabama's "Female Escorts" button). In addition, it uses a Canadian regional and categorical page to test alternative subdomains.

2. Add a mocking class for your site to `app/sitemapparsers/tests/requests_mocks.py`. It must implement the method(s) you are mocking in the requests module. It should grab a test html file from `__app__/sitemapparser/tests/test-html/mock_responses` using `get_html_text` and pass the return value into a `MockResponse` object, which is returned from your mock *requests* method. When your parser is being tested, it can grab the test html as if were a properly returned response with a `.text` attribute.

         The example, `AdultSearchMock`, is described in more detail below.

         > The AdultSearch implementation has two additional layers of complexity. If they don't apply to your parser, *you can totally ignore this.*
         >
         > First, there are *many* (50 states + provinces and areas in the UK and CA) regional links, as well as 3+ category links for each region page, and we don't want to test hundreds of duplicate pages every time we're running the parser. Instead, `AdultSearchMock` uses a dict called `should_return` to track whether it's responded to a `get` request with a page, and once it has, it returns `None` for future requests. Because `adultsearch.py` skips empty responses (see `_get_linked_soup`), this narrows its test results.
         >
         > Second, different countries on AdultSearch use subdomains - the US is simply `www.adultsearch.com`, but Canada is `www.ca.adultsearch.com`, etc. If your parser is also handling different subdomains, you should test at least one alternative subdomain like AdultSearch does. It has additional test files for a Canadian region - British Columbia - and its category page, and it checks `request.get`'s url netloc to see whether it's asking for a US or Canadian page.

3. In `app/sitemapparsers/tests/test_site_map_parsers.py -> test_site_map_parsers()`, add your site's domain to the existing conditional and monkeypatch `requests.get` (or any other requests methods you're using) to a method that returns a fake HTML page.

      ```
          if "adultsearch.com" == test_case["domain"]:
              mock_requests = AdultSearchMock()
              monkeypatch.setattr(
                  requests, "get", mock_requests.get
              )  # override deletion in no_network fixture with specific mocked responses
      ```

And just like that (although it may have seemed like a bit!), you're all done!

![rapunzel](C:\Users\Lucy\Documents\GitHub\crawlers\docs\imgs\good-work-2.gif)