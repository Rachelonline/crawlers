# Processor

This is the function that takes in an ad (phone number) and produces a score document and repeats 
the same document to the ads data store

## How it works


## Testing

`pytest`

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

