import requests
from bs4 import BeautifulSoup
import os

def downloadReplays(page, format = "gen8ou"):
    url = f"https://replay.pokemonshowdown.com/search?user=&format={format}&page={page}&output=html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="lxml")
    urls = list()
    for tag in soup.findAll('a', href = True):
       urls.append(tag['href'])
    print(urls)
    for url in urls:
        filename = "data/"+url.replace("/","")+".log"
        if not os.path.exists(filename):
            u = f"https://replay.pokemonshowdown.com{url}.log"
            r = requests.get(u)
            with open(filename, 'w') as f:
                f.write(r.text)

for i in range(10,50):
    downloadReplays(i)
