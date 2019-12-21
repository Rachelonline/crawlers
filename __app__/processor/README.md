# Processor

This is the function that takes in an ad (phone number) and produces 2 outputs:

* A score document - essentially a phone number and its spam related analytics (described below)
* The original unaltered document for later processor or saving

The score document gets saved in a data base called `scores`.
The original unaltered crawled document is saved in `ads`.


## How it works
Processor steps:

* The `adscorer` function will score a phone number based on the configured "scorer" functions
shown in the section below. The various scorers can be found in `processor/scorers/`.
* The processor returns a dictionary containing the phone number and its associated scores. 

### Frequency

`frequency_scorers` keep track of the number of times a phone number is associated with a
particular attribute, for example like a particular city. It works by incrementing a redis
counter where the key is the attribute type and the value, e.g. `city_new_york`. The
function returns the counts for all the attributes in the `attribute_list` argument matching
the attribute type - so in the prior example it would return all the values matching `city_*`.


### Twilio Request 

This function scores a particular phone number using twilios `truespam` function.

## Testing

`pytest tests/processor/test_ad_scorers.py`

## Runbook


The following is what an argument for `functions` in a call to
`score_ad` looks like:

```python3
import os
from __app__.adparser.scores.cache import RedisCache

CACHE = RedisCache()

DEFAULT_FUNCTIONS = {
    "frequency": {
        "attribute_list": [
            "age",
            "location",
            "gender"
        ],
        "cache": CACHE
    },
    "twilio": {
        "account_sid": os.environ["account_sid"],
        "auth_token": os.environ["auth_token"],
        "cache": CACHE
    }
}

message = # Some message

score_ad(message=message, functions-DEFAULT_FUNCTIONS)
```

