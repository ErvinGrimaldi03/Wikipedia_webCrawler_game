# page_fetcher.py
import requests
from requests.exceptions import RequestException, Timeout
import time


class PageFetcher:
    def __init__(self, retries=3, delay=1):
        self.retries = retries
        self.delay = delay  # seconds to wait between retries

    def fetch(self, url: str) -> bytes | None:
        """
        Fetches the content of a given URL with retries and exponential backoff.
        Returns content as bytes, or None on failure.
        """
        for i in range(self.retries):
            try:
                response = requests.get(url, timeout=10)  # Added timeout
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                return response.content
            except Timeout:
                print(f"Timeout fetching {url}. Attempt {i + 1}/{self.retries}")
            except RequestException as e:
                print(f"Error fetching {url}: {e}. Attempt {i + 1}/{self.retries}")

            if i < self.retries - 1:  # Don't sleep after last attempt
                time.sleep(self.delay * (i + 1))  # Exponential backoff
        return None