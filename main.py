# main.py
from src.wiki_crawler import WikiCrawler
from src.wiki_config import WIKIPEDIA_BASE_URL
import time

if __name__ == "__main__":
    start_page_title = input("Enter the Wikipedia page title to start crawling from (e.g., Mario): ")
    if not start_page_title:
        start_page_title = "Mario" # Default for demonstration because MAMMA MIAAAAAA

    start_url = f"{WIKIPEDIA_BASE_URL}/wiki/{start_page_title.replace(' ', '_')}"

    crawler = WikiCrawler(start_url)
    print(f"Starting crawl from: {start_url}")

    start_time = time.time()
    crawler.start_crawl()
    end_time = time.time()

    print(f"\nCrawl completed in {end_time - start_time:.2f} seconds.")

    # Example: Retrieve data for a crawled page
    example_title = "Luigi" # Or any other page you expect to be crawled
    # To get a title that was definitely crawled, we could iterate `crawler.get_visited_pages()`
    # and pick one, or simply use the start_page_title if it was successfully crawled.

    # Let's try to load the data for the starting page
    retrieved_data = crawler.get_page_data(start_page_title)
    if retrieved_data:
        print(f"\nData for '{start_page_title}':")
        # print(json.dumps(retrieved_data, indent=2)) # Requires import json
        print(f"  URL: {retrieved_data['url']}")
        print(f"  Category: {retrieved_data['category']}")
        print(f"  Number of links found: {len(retrieved_data['links'])}")
    else:
        print(f"\nCould not retrieve data for '{start_page_title}'.")

    # Example: Get related wikis using the API for the starting page
    related_api = crawler.get_related_wikis_api(start_page_title)
    if related_api:
        print(f"\nRelated wikis for '{start_page_title}' (from API): {related_api[:5]}...") # Show first 5