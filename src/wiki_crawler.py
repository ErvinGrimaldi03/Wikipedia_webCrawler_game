from multiprocessing.pool import ThreadPool
import time
from collections import deque
import random

import requests
from requests import RequestException

from src.link_extractor import LinkExtractor
from src.wiki_config import WIKIPEDIA_BASE_URL, POOL_SIZE, MAX_DEPTH, MAX_PAGES_PER_DEPTH, WIKIPEDIA_API_RACC
from src.page_fetcher import PageFetcher
from src.page_classifier import PageClassifier
from src.data_store import PageDataStore
from src.page_classifier import PageClassifier

class WikiCrawler:
    def __init__(self, start_url):
        self.start_url = start_url
        self.visited_urls = set()
        self.page_fetcher = PageFetcher()
        self.link_extractor = LinkExtractor()
        self.data_store = PageDataStore()
        self.page_classifier = PageClassifier()
        self.pool = ThreadPool(POOL_SIZE)
        self.crawl_queue = deque()

    def _process_page(self, url, current_depth):
        """Internal method to fetch, extract, and store data for a single page."""
        if url in self.visited_urls:
            return None  # Already processed

        print(f"Crawling: {url} (Depth: {current_depth})")
        self.visited_urls.add(url)

        html_content = self.page_fetcher.fetch(url)
        if not html_content:
            return None

        page_title = self.link_extractor.get_page_title(url)
        extracted_links = self.link_extractor.extract_links(html_content)

        # Basic classification (TODO: EXPAND FURTHER)
        page_category = self.page_classifier.classify(html_content.decode('utf-8', errors='ignore'), page_title)

        page_data = {
            "url": url,
            "title": page_title,
            "links": extracted_links,
            "crawled_at": time.time(),
            "category": page_category  # Store classification
        }
        self.data_store.save_page_data(page_title, page_data)
        return extracted_links

    def start_crawl(self):
        self.crawl_queue.append((self.start_url, 0)) # (url, depth)

        while self.crawl_queue:
            current_url, current_depth = self.crawl_queue.popleft()

            if current_depth >= MAX_DEPTH:
                continue

            result = self._process_page(current_url, current_depth)
            if result:
                for link in result:
                    if link not in self.visited_urls:
                        self.crawl_queue.append((link, current_depth + 1))
            # MUST DELAY A BIT BECAUSE WE WOULD OVERWHELM THE SERVER OTHERWISE
            time.sleep(random.uniform(0.1, 0.5))

    def get_visited_pages(self):
        return self.visited_urls

    def get_pages_data(self, title):
        return self.data_store.load_page_data(title)

    def get_related_wikis_api(self, title):
        api_url = WIKIPEDIA_API_RACC + title
        try:
            response = requests.get(api_url, timeout=5)
            response.raise_for_status()
            return [i['title'] for i in response.json().get('pages', [])]
        except RequestException as e:
            print(f"Error fetching related wikis for {title} via API: {e}")
            return []