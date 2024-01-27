from bs4 import BeautifulSoup
import requests
import json
import re


WIKIPEDIA_BASE = 'https://en.wikipedia.org/wiki/'
WIKIPEDIA_ROOT = '<a href="/wiki/'
UNDESIRED_TAGS = ['/wiki/Special', '/wiki/Template']
WIKIPEDIA_API_RACC = 'https://en.wikipedia.org/api/rest_v1/page/related/'
REG_EX = f'^<a href="\/wiki\/[^\/:"]+"'


class WikiCrawler:
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.page = WIKIPEDIA_BASE+title

        self.url = None
        self.url_content = None
        self.url_api = None

        self.wiki_racc = None
        self.wiki_childs = []

        self.connect()
        self.related_wikis()
        self.soup = BeautifulSoup(self.url_content, features='html')

        self.extract_child()

    def connect(self):
        self.url_content = requests.get(self.page)
        if self.url_content.status_code != 200:
            return
        self.url = self.url_content
        self.url_api = WIKIPEDIA_API_RACC + self.title
        self.url_content = self.url_content.content

    def related_wikis(self):
        with requests.get(self.url_api) as url:
            self.wiki_racc = [i['title'] for i in url.json()['pages']]

    def extract_child(self):
        for href in (self.soup.find_all("a", attrs={"title" : True})):
            href_str = href.__str__()
            if bool(re.match(REG_EX, href_str)):
                self.wiki_childs.append(href)


