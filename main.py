from urllib.request import urlopen
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool as Pool
import re
import time
import random
from _JSON import save_json
from functools import lru_cache
from crawler import WikiCrawler

import requests

WIKIPEDIA_BASE_URL = "https://en.wikipedia.org"
WIKIPEDIA_ROOT_URL = '<a href="/wiki/'
POOL_SIZE = 5
UNDERSIRED_TAGS = ['/wiki/Special', '/wiki/Template']
REG_EX = f'^<a href="\/wiki\/[^\/:"]+"'



def connect(webstie):
    url_website = requests.get(webstie)
    if url_website.status_code != 200: return
    return url_website




def extract_childs(soup):
    a_href_candidates = []
    for href in soup.find_all("a", attrs={"title" : True}):
        href_str = href.__str__()
        if bool(re.match(REG_EX, href_str)):
            a_href_candidates.append(href)
    selected_five = []
    #print(len(a_href_candidates))
    return ([(WIKIPEDIA_BASE_URL+i['href']) for i in random.choices(a_href_candidates, k=5) if connect(WIKIPEDIA_BASE_URL+i['href'])], a_href_candidates)

def run(wiki_page):
    connection_website = connect(wiki_page)
    title = wiki_page[30:]
    wiki_page_childs = {title: []}

    soup = BeautifulSoup(connection_website.content, features="html")
    childs, candidates = extract_childs(soup)
    print(len(candidates), title)
    for link in candidates:
        wiki_page_childs[title].append(WIKIPEDIA_BASE_URL+link['href'])
    save_json(wiki_page_childs, title)
    run(random.choice(childs))



if __name__ == "__main__":
    #startingname_user = input()
    startingname_user = "Mario"

    wiki_crawl = WikiCrawler(startingname_user)

    print(wiki_crawl.wiki_childs)




