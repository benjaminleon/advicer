import re

import requests
from bs4 import BeautifulSoup

for movie_id in range(1, 10):
    r = requests.get(f'https://www.imdb.com/title/tt000000{movie_id}')
    soup = BeautifulSoup(r.text, 'html.parser')
    url = soup.img['src']
    print(movie_id, url)
# b = soup.find("div", {"data-testid": "hero-media__poster"})

# m = re.match(".*src=\"(.*?)\"", a)
# if m:
#     print(m.group(1))
