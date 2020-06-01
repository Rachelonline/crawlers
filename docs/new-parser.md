# New Parser

Before you get started, be sure to check out the [design doc](./design.md) to understand the set up and provide context for your new parser.This doc is intended as a guide to go step-by-step through all the things you need to do to open a complete pull request for a new crawler.

![walkthrough](./imgs/walkthrough.gif)

Before we begin there are some overall concepts to understand:

- First, you will download some sample pages from the site you are targeting. - You will need the "site map" page, i.e. the page where all the different categories or locations are listed out. - You will also need a few examples of those listing pages. The listing page is where there is a collection of links to individual ads. - Be sure to grab a few ads to get a good sample. Choose some from different categories, as well as varying levels of detail included in the ads.

- Then you will use Beautiful Soup to parse out relevant information from the ad. Not all ads will have all the fields! We really recommend starting with the ad parser itself, as it is usually the bulk of the work and also allows you to get a good understanding of code be referencing other ad parsers.

- After the ad parser, then move on to the ad listings page and site map.

💡Pro-tip: you can disable images in your browser before doing this work if you are going to use the devtools to inspect elements to grab ids or classnames. This will help limit your exposure if you are sensitive to the imagery.

### Step 1: Creating an Ad Parser

1. Create a new file for the ad in `__app__/adparser/tests/test-html`. Paste the HTML from the ad you want to parse. You can download the HTML or use "view source" in your browser to copy and paste. Be sure to give the file a name that includes the site you are looking at and the date.

2) Add the expected JSON file for the ad to `__app__/adparser/ad-test-data`. You can do this in conjunction with writing the parser so that you aren't manually pulling out each bit of data, but if it's your first crawler or a particularly tricky site, we suggest manually looking at at least one ad so that you can be sure you are pulling out the data you expect.

3. Create a new file for the parser in `__app__/adparser/sites`. Check out the other parsers in the directory. You'll see they all have the same methods. One great way to ensure that you are getting all the fields is to copy the methods in `base_ad_parser` so that you can be sure you got them all.

4) If you want to test out the parser to see if it gets the HTML tag you wanted, you can load the HTML in the repl and test it first. Open the repl in your terminal by typing `python`. Then type each of these command individually in the repl.

`import os`

`import re`

`from bs4 import BeautifulSoup`

`file_path = "__app__/adparser/tests/test-html/{INSERT THE NEW FILENAME YOU JUST CREATED}.html"`

`html = open(file_path, encoding="utf8").read()`

`soup = BeautifulSoup(html, "html.parser")`

You can now play around with the Beautiful soup library to try to see what you are grabbing. For example, you can run `soup.find("a")` so that you can inspect an `a` tag.

5. Open the file `__app__/adparser/adparser.py` to get your new ad parser into the collection.

- First, add an import statement for your parser like the following:

  `from __app__.adparser.sites.cityxguide_com import CityXGuide`

- Next, add the domain and the parser name to the `AD_PARSERS` dictionary:

  `AD_PARSERS = { "cityxguide.com": CityXGuide, ... }`

6. Make sure the tests pass by running `python -m pytest`. You did it!

### Ad Listing Parser

Now that you've created your ad parser, the rest of the work will fall into place more easily! Many of these steps are similar to what is described above.

1. Create and/or copy the ad listing HTML file to `__app__/adlistingparser/tests/test-html`. Be sure to include multiple examples again!

2. Add the expected ad listing JSON data to `__app__/adlistingparser/tests/test-data`.

3. Create a new parser file for the ad listings page in `__app__/adlistingparser/sites/`. Again, feel free to use other parsers or the `base_adlisting_parser` files as examples to ensure you have all the methods you need.

4. Add your parser to the `__app__/adlistingparser/adlistingparser.py` by importing the parser as well as adding it to the `AD_LISTING_PARSERS` dictionary.

5. Run all the tests with `python -m pytest`.

### Site Mapping Parser

Let's wrap up the new site! All we need to do now is add the site map parser.

1. Create and/or copy the ad listing HTML file in the `__app__/sitemapparser/tests/test-html` directory. Since this is the top level of the site navigation, you will only have one file here instead of the many examples like in the other steps.

2. Create the JSON for the expected results of the parsing in `__app__/sitemapparser/tests/test-data`.

3. Create a sitemap parser and include it in the directory `__app__/sitemapparser/sites/`.

4. Add your parser to the `__app__/sitemapparser/sitemapparser.py` via the import statement and the `SITE_PARSERS` dictionary.

5. Run all the tests with `python -m pytest`.

![good work](./imgs/good-work.gif)
