from __app__.utils.table.base_table import encode_url, decode_url


def test_encode_url():
    assert "aHR0cDovL3d3dy5nb29nbGUuY29t" == encode_url("http://www.google.com")


def test_encode_url():
    assert decode_url("aHR0cDovL3d3dy5nb29nbGUuY29t") == "http://www.google.com"
