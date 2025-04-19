import requests
from bs4 import BeautifulSoup
from .utils import get_cache, set_cache

def parse_main_menu(html_url):
    cached = get_cache("main_menu")
    if cached: return cached

    response = requests.get(html_url)
    soup = BeautifulSoup(response.text, "html.parser")
    items = []

    for link in soup.find_all("a", href=True):
        if "filme" in link["href"] or "serie" in link["href"]:
            items.append({"title": link.text.strip(), "url": link["href"]})

    set_cache("main_menu", items)
    return items

def parse_movie_page(movie_url):
    response = requests.get(movie_url)
    soup = BeautifulSoup(response.text, "html.parser")
    magnet = soup.find("a", href=lambda x: x and x.startswith("magnet:?xt="))["href"]
    return magnet
