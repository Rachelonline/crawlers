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
