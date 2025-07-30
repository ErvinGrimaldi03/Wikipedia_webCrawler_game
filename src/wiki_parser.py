from bs4 import BeautifulSoup
import re
import time
from src.wiki_config import WIKIPEDIA_BASE_URL, VALID_WIKI_LINK_REGEX

class WikiParser:
    def __init__(self):
        self.paragraph_tags_regex = re.compile(r'<(p|ul|ol)>')

    def parse_articles(self, html_content: bytes, article_url:str) -> dict | None:
        """
        extract from Wiki:
        - Article title
        - Infobox data
        - Categories
        - Lead section text
        - Internal links
        """
        if not html_content:
            return None
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            title_tag = soup.find('h1', {"firstHeading"})
            article_title = title_tag.get_text(strip=True) if title_tag else self._get_title_from_url(article_url)

            infobox_data = self._extract_infobox(soup)
            categories = self._extract_categories(soup)
            lead_text = self._extract_lead_section(soup)
            all_internal_link = self._extract_internal_links(soup)

            return {
                "title"             : article_title,
                "url"               : article_url,
                "infobox"           : infobox_data,
                "categories"        : categories,
                "lead_text"         : lead_text,
                "internal_links"    : all_internal_link,
                'crawled_at'        : ''
            }
        except Exception as e:
            print(f"Error parsing article {article_url}: {e}")
            return None

    def _extract_infobox(self, soup: BeautifulSoup) -> dict:
        """ This is responsible for key-values from the infobox table"""
        infobox = soup.find("table", {"class": "infobox"})
        data = {}
        if infobox:
            for row in infobox.find_all('tr', recursive=False):
                header = row.find('th', recursive=False)
                value_td = row.find('td', recursive=False)

                if header and value_td:
                    key = header.get_text(strip=True)
                    value_parts = []
                    for content in value_td.contents:
                        if content.name == 'sup' and 'class' in content.attrs and 'reference' in content.attrs['class']:
                            continue
                        if hasattr(content, 'get_text'):
                            value_parts.append(content.get_text(separator=' ', strip=True))
                        else:
                            value_parts.append(str(content).strip())
                    value = ' '.join(value_parts).replace('\n', ' ').strip()