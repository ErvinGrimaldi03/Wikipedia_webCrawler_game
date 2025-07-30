from multiprocessing.pool import ThreadPool
import time
from collections import deque
import random
import threading
from queue import Queue, Empty
import requests
from requests import RequestException

from src.link_extractor import LinkExtractor
from src.wiki_config import WIKIPEDIA_BASE_URL, POOL_SIZE, MAX_DEPTH, MAX_PAGES_PER_DEPTH, WIKIPEDIA_API_RACC
from src.page_fetcher import PageFetcher
from src.page_classifier import PageClassifier
from src.data_store import PageDataStore


class RateLimiter:
    """Thread-safe rate limiter to respect Wikipedia's servers"""

    def __init__(self, min_interval=1.0):
        self.min_interval = min_interval  # Minimum seconds between requests
        self.last_request_time = 0
        self.lock = threading.Lock()

    def wait_if_needed(self):
        """Wait if necessary to maintain rate limit"""
        with self.lock:
            current_time = time.time()
            time_since_last_request = current_time - self.last_request_time

            if time_since_last_request < self.min_interval:
                sleep_time = self.min_interval - time_since_last_request
                time.sleep(sleep_time)

            self.last_request_time = time.time()


class WikiCrawler:
    def __init__(self, start_url, num_threads=3, requests_per_second=1):
        self.start_url = start_url
        self.visited_urls = set()
        self.visited_urls_lock = threading.Lock()

        self.page_fetcher = PageFetcher()
        self.link_extractor = LinkExtractor()
        self.data_store = PageDataStore()
        self.page_classifier = PageClassifier()

        # Thread pool with limited workers
        self.num_threads = min(num_threads, POOL_SIZE)  # Respect configured max
        self.pool = ThreadPool(self.num_threads)

        # Thread-safe queue for URLs to crawl
        self.crawl_queue = Queue()

        # Rate limiter - shared across all threads
        self.rate_limiter = RateLimiter(min_interval=1.0 / requests_per_second)

        # Statistics
        self.stats_lock = threading.Lock()
        self.pages_crawled = 0
        self.pages_failed = 0

    def _process_page(self, url, current_depth):
        """Process a single page (thread-safe)"""
        # Check if already visited (thread-safe)
        with self.visited_urls_lock:
            if url in self.visited_urls:
                return None
            self.visited_urls.add(url)

        # Rate limit before making request
        self.rate_limiter.wait_if_needed()

        print(f"[Thread-{threading.get_ident()}] Crawling: {url} (Depth: {current_depth})")

        try:
            html_content = self.page_fetcher.fetch(url)
            if not html_content:
                with self.stats_lock:
                    self.pages_failed += 1
                return None

            page_title = self.link_extractor.get_page_title(url)
            extracted_links = self.link_extractor.extract_links(html_content)

            # Basic classification
            page_category = self.page_classifier.classify(
                html_content.decode('utf-8', errors='ignore'),
                page_title
            )

            page_data = {
                "url": url,
                "title": page_title,
                "links": extracted_links,
                "crawled_at": time.time(),
                "category": page_category
            }

            # Thread-safe save
            self.data_store.save_page_data(page_title, page_data)

            with self.stats_lock:
                self.pages_crawled += 1

            return extracted_links, current_depth

        except Exception as e:
            print(f"[Thread-{threading.get_ident()}] Error processing {url}: {e}")
            with self.stats_lock:
                self.pages_failed += 1
            return None

    def _worker(self):
        """Worker thread function"""
        while True:
            try:
                # Get next URL from queue (blocks for up to 1 second)
                url, depth = self.crawl_queue.get(timeout=1)

                if depth >= MAX_DEPTH:
                    self.crawl_queue.task_done()
                    continue

                # Process the page
                result = self._process_page(url, depth)

                if result:
                    extracted_links, current_depth = result

                    # Add new links to queue
                    links_added = 0
                    for link in extracted_links:
                        if links_added >= MAX_PAGES_PER_DEPTH:
                            break

                        with self.visited_urls_lock:
                            if link not in self.visited_urls:
                                self.crawl_queue.put((link, current_depth + 1))
                                links_added += 1

                self.crawl_queue.task_done()

            except Empty:
                # No more URLs to process
                break
            except Exception as e:
                print(f"[Thread-{threading.get_ident()}] Worker error: {e}")
                try:
                    self.crawl_queue.task_done()
                except:
                    pass

    def start_crawl(self):
        """Start the multi-threaded crawl"""
        start_time = time.time()

        # Add initial URL to queue
        self.crawl_queue.put((self.start_url, 0))

        print(f"Starting crawl with {self.num_threads} threads...")
        print(f"Rate limit: {1 / self.rate_limiter.min_interval:.1f} requests/second")

        # Start worker threads
        workers = []
        for i in range(self.num_threads):
            worker = threading.Thread(target=self._worker)
            worker.start()
            workers.append(worker)

        # Monitor progress
        last_stats_time = time.time()
        while not self.crawl_queue.empty() or any(w.is_alive() for w in workers):
            time.sleep(5)  # Check every 5 seconds

            # Print statistics
            current_time = time.time()
            if current_time - last_stats_time >= 10:  # Every 10 seconds
                with self.stats_lock:
                    print(f"\n--- Progress Update ---")
                    print(f"Pages crawled: {self.pages_crawled}")
                    print(f"Pages failed: {self.pages_failed}")
                    print(f"Queue size: {self.crawl_queue.qsize()}")
                    print(f"Active threads: {sum(1 for w in workers if w.is_alive())}")
                    print(f"Time elapsed: {current_time - start_time:.1f}s")
                    print("----------------------\n")
                last_stats_time = current_time

        # Wait for all threads to complete
        for worker in workers:
            worker.join()

        # Clean up
        self.pool.close()
        self.pool.join()

        end_time = time.time()

        # Final statistics
        print(f"\n=== Crawl Completed ===")
        print(f"Total time: {end_time - start_time:.2f} seconds")
        print(f"Pages crawled: {self.pages_crawled}")
        print(f"Pages failed: {self.pages_failed}")
        print(f"Total pages visited: {len(self.visited_urls)}")
        print("=====================\n")

    def get_visited_pages(self):
        """Get a copy of visited pages (thread-safe)"""
        with self.visited_urls_lock:
            return self.visited_urls.copy()

    def get_page_data(self, title):
        """Get data for a specific page"""
        return self.data_store.load_page_data(title)

    def get_related_wikis_api(self, title):
        """Get related wikis using API (rate-limited)"""
        self.rate_limiter.wait_if_needed()

        api_url = WIKIPEDIA_API_RACC + "/" + title
        try:
            response = requests.get(api_url, timeout=5)
            response.raise_for_status()
            return [i['title'] for i in response.json().get('pages', [])]
        except RequestException as e:
            print(f"Error fetching related wikis for {title} via API: {e}")
            return []