import re

WIKIPEDIA_BASE_URL = "http://en.wikipedia.org"
WIKIPEDIA_API_RACC = "https://en.wikipedia.org/api/rest_v1/page/related"
POOL_SIZE = 10
MAX_DEPTH = 3 # THIS IS TO TELL HOW DEEP FROM CURRENT PAGE WE CAN GO
MAX_PAGES_PER_DEPTH = 100 # WE DO NOT WANT A SINGLE CRAWLER TO GO LOOK FOR THE ENTIRE WIKIPEDIA

VALID_WIKI_LINK_REGEX = re.compile(r'^/wiki/(?!Special:|Template:|Category:|File:|Portal:)[^:#]*$')
