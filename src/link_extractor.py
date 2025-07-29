from bs4 import BeautifulSoup
import re
from src.wiki_config import WIKIPEDIA_BASE_URL, VALID_WIKI_LINK_REGEX

class LinkExtractor:
    """entity responsible for extracting links from HTML content"""

    def extract_links(self, html_content):
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, 'html.parser')
        links = set()

        for anchor_tag in soup.find_all("a", href=True):
            href = anchor_tag.get("href")
            if href and VALID_WIKI_LINK_REGEX.match(href):
                absolute_url = WIKIPEDIA_BASE_URL + href
                links.add(absolute_url)
        return list(links)

    def get_page_title(self, url):
        parts = url.split("/")
        if parts and parts[-1]:
            return parts[-1].replace('_', ' ')
        return 'Unknown'
