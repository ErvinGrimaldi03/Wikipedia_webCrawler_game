from bs4 import BeautifulSoup
import re
from urllib.parse import unquote
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
        """
        Extract page title from URL, preserving disambiguation markers.

        Examples:
        - http://en.wikipedia.org/wiki/Sheriff -> "Sheriff"
        - http://en.wikipedia.org/wiki/Sheriff_(disambiguation) -> "Sheriff (disambiguation)"
        - http://en.wikipedia.org/wiki/New_York_City -> "New York City"
        """
        parts = url.split("/")
        if parts and parts[-1]:
            # URL decode to handle special characters
            title = unquote(parts[-1])
            # Replace underscores with spaces
            #title = title.replace('_', ' ')
            return title
        return 'Unknown'