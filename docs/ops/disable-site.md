# How to Stop Crawling a Domain

## Temporary disable a domain:

When you want to just disable the crawling of a domain you can use `tools/adlistings/stop_crawling_domain.py`. It will disable the aslistings from being loaded as part of the hourly crawl. This will then prevent the downstream ad crawling and image crawling.

It will also go through the existing adlistingcrawl queue and remove any crawl jobs for that domain. 

This is a soft delete, you can re-enable the domain in the table and it will start crawling again. 

**manual step** you'll also need to disable the `SITEMAP_URL` in the site-loader and deploy. This is a less critical step, but you'll still need to do it.


## Permanently disable a domain:

First temporary disable, then delete the code. 

