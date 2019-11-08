# Ad Scorer

This is the function that takes in an ad (phone number) and produces a score

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
            "emails",
            "location"
        ],
        "rc": CACHE
    },
    "twilio": {
        "account_sid": os.environ["account_sid"],
        "auth_token": os.environ["auth_token"],
        "rc": CACHE
    }
}

message = # Some message

score_ad(message=message, functions-DEFAULT_FUNCTIONS)
```

