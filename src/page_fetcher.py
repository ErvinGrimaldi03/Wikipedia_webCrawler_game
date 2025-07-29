import requests
from requests.exceptions import RequestException
import time

class PageFetcher:
    def __init__(self, retries=3, delay=1):
        self.retries = retries
        self.delay = delay

    def fetch(self, url):
        for i in range(self.retries):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                return response.content
            except RequestException as e:
                print(f"Error fetching {url}: {e}. Attempt {i + 1}/{self.retries}")
                time.sleep(self.delay)
        return None

