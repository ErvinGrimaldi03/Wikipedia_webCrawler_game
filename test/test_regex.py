# test_regex.py
import re

# Test the regex
VALID_WIKI_LINK_REGEX = re.compile(r'^/wiki/(?!Special:|Template:|Category:|File:|Portal:)[^:#]+$')

test_urls = [
    "/wiki/Sheriff",
    "/wiki/Sheriff_(disambiguation)",
    "/wiki/Everybody%27s_Golf_(1997_video_game)",
    "/wiki/New_York_City",
    "/wiki/COVID-19",
    "/wiki/Special:Search",  # Should NOT match
    "/wiki/Template:Infobox",  # Should NOT match
    "/wiki/Mario#History",  # Should NOT match (has #)
    "/wiki/Help:Contents",  # Should match (Help: is allowed)
]

print("Testing Wikipedia URL regex:")
print("-" * 60)

for url in test_urls:
    match = VALID_WIKI_LINK_REGEX.match(url)
    print(f"URL: {url}")
    print(f"Matches: {bool(match)}")
    if match:
        print(f"Full match: {match.group()}")
    print("-" * 60)

# Test what BeautifulSoup might be returning
from bs4 import BeautifulSoup

html_sample = '''
<a href="/wiki/Everybody%27s_Golf_(1997_video_game)">Everybody's Golf</a>
<a href="/wiki/Sheriff_(disambiguation)">Sheriff (disambiguation)</a>
'''

soup = BeautifulSoup(html_sample, 'html.parser')
print("\nTesting BeautifulSoup extraction:")
print("-" * 60)

for link in soup.find_all('a', href=True):
    href = link.get('href')
    print(f"Raw href from BeautifulSoup: {href}")
    print(f"Text: {link.get_text()}")
    print(f"Regex matches: {bool(VALID_WIKI_LINK_REGEX.match(href))}")
    print("-" * 60)