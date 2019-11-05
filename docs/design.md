# Architecture:

## Stage 1: Sitemapping

Site mapping is where we figure out where lists of ads live on a site. It stores those ad listing urls in an Azure Table which is used in the next stage. 

This stage is fairly self contained with a loader, a crawler and a parser.

![Sitemap](./imgs/sitemaparch.png)

Sitemap starts with sitemaploader on a timer. Currently it runs 1x per day. It loads crawl jobs on the sitemapcrawl queue. 

The sitemapcrawler is triggered when jobs are on the sitemap crawl queue. It takes the job, downloads the page where we could find ad listing urls and puts that page on the sitemapparse queue. 

The site map parser takes jobs from the sitemap parse queue, extracts ad listing urls and loads *new* ones into the adlistings azure table. These new adlistings are saved into the azure table.

## Stage 2: Ad Listings

Ad listings is all about collecting urls for individual ads. It puts the ad urls on the ad-crawl queue to start the next stage.

Similar to sitmapping this stage contains a loader, crawler and parser, however this ends in a queue instead of a crawl.

![Ad Listings](./imgs/adlistingarch.png)

The Ad listing loader starts on 1x hour timer. It loads ad listing crawl jobs onto the adlisting crawl queue.

The ad listing crawler takes jobs from the adlisting crawl queue, downloads the url and puts the page on the adlisting parse queue.

The ad listing parser then extracts the individual ad urls. It then checks the azure ad table to see if the ad url has alredy been crawled.

If we've not crawled the ad then it will put the ad on the ad crawl queue for the next stage.


