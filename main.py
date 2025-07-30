# main.py
from src.wiki_crawler import WikiCrawler
from src.wiki_config import WIKIPEDIA_BASE_URL
import time
import sys

if __name__ == "__main__":
    # Get starting page
    start_page_title = input("Enter the Wikipedia page title to start crawling from (e.g., Mario): ")
    if not start_page_title:
        start_page_title = "Mario"  # Default for demonstration

    # Configure crawler settings
    print("\nCrawler Configuration:")
    print("1. Conservative (2 threads, 0.5 requests/sec) - Safest")
    print("2. Moderate (5 threads, 1 request/sec) - Balanced")
    print("3. Aggressive (10 threads, 2 requests/sec) - Faster")
    print("4. Custom configuration")

    choice = input("\nSelect configuration (1-4) [default: 2]: ").strip()

    if choice == "1":
        num_threads = 2
        requests_per_second = 0.5
    elif choice == "3":
        num_threads = 10
        requests_per_second = 2
    elif choice == "4":
        num_threads = int(input("Number of threads (1-20): ") or "5")
        num_threads = max(1, min(20, num_threads))  # Clamp between 1-20
        requests_per_second = float(input("Requests per second (0.1-5): ") or "1")
        requests_per_second = max(0.1, min(5, requests_per_second))  # Clamp between 0.1-5
    else:  # Default to moderate
        num_threads = 5
        requests_per_second = 1

    start_url = f"{WIKIPEDIA_BASE_URL}/wiki/{start_page_title.replace(' ', '_')}"

    # Create and start crawler
    crawler = WikiCrawler(
        start_url,
        num_threads=num_threads,
        requests_per_second=requests_per_second
    )

    print(f"\nStarting crawl from: {start_url}")
    print(f"Configuration: {num_threads} threads, {requests_per_second} requests/second")
    print("Press Ctrl+C to stop crawling gracefully\n")

    try:
        start_time = time.time()
        crawler.start_crawl()
        end_time = time.time()

    except KeyboardInterrupt:
        print("\n\nCrawl interrupted by user. Waiting for threads to finish...")
        # The crawler will handle cleanup gracefully
        sys.exit(0)

    # Example: Retrieve data for the starting page
    retrieved_data = crawler.get_page_data(start_page_title)
    if retrieved_data:
        print(f"\nData for '{start_page_title}':")
        print(f"  URL: {retrieved_data['url']}")
        print(f"  Category: {retrieved_data.get('category', 'N/A')}")
        print(f"  Number of links found: {len(retrieved_data.get('links', []))}")

        # Show a few example links
        if retrieved_data.get('links'):
            print(f"  Example links:")
            for link in retrieved_data['links'][:5]:
                print(f"    - {link}")
    else:
        print(f"\nCould not retrieve data for '{start_page_title}'.")

    # Show some statistics
    visited_pages = crawler.get_visited_pages()
    print(f"\nTotal unique pages visited: {len(visited_pages)}")

    # Example: Get related wikis using the API
    print(f"\nFetching related articles for '{start_page_title}' via API...")
    related_api = crawler.get_related_wikis_api(start_page_title)
    if related_api:
        print(f"Related articles: {', '.join(related_api[:5])}...")
    else:
        print("Could not fetch related articles.")