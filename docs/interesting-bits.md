# Interesting Bits

This is a small collection of interesting or unique bits of the code base. And some rough edges, because every system has some 😉


### Oversized Messages

**Problem:** Azure Service bus only allows a max message size of 256 kb. 

When we sitecrawl/adlistingcrawl we save the html as part of the message that goes to the parser steps. We don't save these to durable storage (Blob) because they are temporary data. We only need them long enough to get ad-urls. Ads themselves we save to durable storage because we want to save them forever.

Unfortunately, some sites will have very large pages that are larger than 256kb.

We handle this by using some custom message encoding and decoding logic under [utils/queues/message.py](../__app__/utils/queues/message.py)

When a message would be oversized it instead saves that message to a uuid in blob storage in the `oversized-msgs` container. The message is then replaced with `{"blob-message": blob_uri}`. 

When the message is decoded, if it has the `"blob-message"` the decoder will get the message from blob storage and send it on for processing. 

We don't want to save *all* messages to blob store - that's more expensive and slow. Plus we don't really need it most of the time. 

**Rough Edges**: There's 2 rough edges

* Calculating message size
  - We encode the message as json just to check the size. That's wasteful, but it gets the job done. There's probably a smarter way
* Cleaning up blob store
  - Right now we don't delete the message from blob. That's a silly expense. There might be a way to set a TTL for the blob object - you can in s3 😛


### Locations

**Problem:** We need to know the locations of potential victims.

At a high level what we do is collect location information from the ads, then geocode that into a lat/lon and store that in our database.

When we are crawling we collect named locations when parsing the ads. Sometimes the ads only list 'downtown' as the named location, so we use the context of where the ad was posted to get a more complete named location. For example, we might see "downtown" in the ad, but it was posted in the Huntsville AL page. We'll combine them to say "Huntsville AL downtown" as the named location.

Sometimes the ads don't list where they were posted. So we also parse the location from the ad listing metadata. We only do this when we need to - not on all sites. This happens in the adlistingparsers.

In the processor is where we do the actual geocoding. There we take the named location from the ad, combine it with the named location from the adlisting parser (if it's exists). We then lowercase everything, strip out punctuation and stop words (such as 'incall/outcall/etc'). Then we use the google maps api to get back a geocoded location.

The full location is stored in our redis cached, indexed by the search string. That way we avoid having to do a lookup for every ad. Preliminary tests show about a 90% cache hit rate, though we don't directly measure it. We can approximate the hit rate by looking at the number of ads parsed vs the number of calls to the geocode api.

We then store a lat/long and a place_id (from google) in the db. The fields are spacially indexed, allowing for fast searches of "give me all the ads found in {arbitrary polygon}". This means we can quickly search for all ads in Washington or King County or Seattle or even Queen Anne.

 
