from urllib.request import urlopen, Request
import urllib.parse as urlparse
from urllib.parse import urlencode
import json
import os

# Load the API key
API_KEY: str
if os.path.exists("API_KEY.txt"):
    API_KEY = open('API_KEY.txt').read()
else:
    raise Exception("API key not found. Please create a file named 'API_KEY_.txt' with your Google Developer API key")


def get_google_results(query):
    """Perform a google search with `query` and return a list of URLs"""

    url = 'https://customsearch.googleapis.com/customsearch/v1?cx=003416eaf4b4649c6&q=hello&key=[YOUR_API_KEY]'.replace(
        '[YOUR_API_KEY]', API_KEY)
    url_parts = list(urlparse.urlparse(url))
    url_query = dict(urlparse.parse_qsl(url_parts[4]))
    url_query.update({
        'q': query
    })
    url_parts[4] = urlencode(url_query)

    request = Request(urlparse.urlunparse(url_parts),
                      headers={
                          'Accept': 'application/json'
                      }
                      )

    with urlopen(request) as f:
        response = json.loads(f.read())
        print(response)
        return [
            item['link']
            for item in response['items']
        ]

