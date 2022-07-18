import requests
from bs4 import BeautifulSoup
import random as rand

# A list of all visited links
visited = []

'''
Recursive Function
This function is passed with the starting link(current link) and the ending link
The function also returns feedback 
'''


def linkRetrieval(start, end):

    try:
        global visited
        print(f'we are at {start}\n')
        visited.append(start)
        link_wikipidia = []
        if start != end:
            r = requests.get(start)
            soup = BeautifulSoup(r.content, "html.parser")
            main_wrap = soup.find("div", "mw-parser-output")
            all_a = main_wrap.find_all("a", href=True)

            for element in all_a:
                sliced = str(element)[:15]
                if sliced == '<a href="/wiki/' and f"https://en.wikipedia.org/{element['href']}" not in visited:
                    if "https://en.wikipedia.org//wiki/Special:" not in element:
                        link_wikipidia.append(f"https://en.wikipedia.org/{element['href']}")
        next = rand.choice(link_wikipidia)
        return linkRetrieval(next, end)
    except:
        print(len(visited))


def _input():
    start = input("Insert starting word: ")
    test = requests.get(f"https://en.wikipedia.org/wiki/{start}")
    if test.status_code != 200:
        print(f"{start} page on wikipedia doesn't exists")
        _input()
    _wikiStart = f"https://en.wikipedia.org/wiki/{start}"

    end = input("Insert ending word: ")
    test = requests.get(f"https://en.wikipedia.org/wiki/{end}")
    if test.status_code != 200:
        print(f"{start} page on wikipedia doesn't exists")
        _input()
    _wikiEnd = f"https://en.wikipedia.org/wiki/{end}"

    linkRetrieval(_wikiStart, _wikiEnd)

if __name__ == '__main__':
    _input()