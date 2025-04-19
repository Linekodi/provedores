import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://raw.githubusercontent.com/Linekodi/provedores/refs/heads/main/Para%20provedores/'

CACHE = {}

def fetch_html(url):
    if url in CACHE:
        return CACHE[url]
    r = requests.get(url)
    CACHE[url] = r.text
    return r.text

def get_navigation():
    html = fetch_html(BASE_URL + 'torrentplus.org.html')
    soup = BeautifulSoup(html, 'html.parser')
    nav = []
    for a in soup.select('a'):
        text = a.text.strip()
        href = a.get('href')
        if href and href.endswith('.html'):
            nav.append((text, BASE_URL + href))
    return nav

def get_content_items(url):
    html = fetch_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    items = []

    for block in soup.select('a'):
        href = block.get('href', '')
        text = block.text.strip()
        if href.startswith('magnet:'):
            items.append({
                'title': text or 'Play',
                'magnet': href,
                'img': '',
                'plot': ''
            })
        elif href.endswith('.html'):
            items.append({
                'title': text or href,
                'href': BASE_URL + href,
                'img': '',
                'plot': ''
            })

    imgs = soup.find_all('img')
    ps = soup.find_all('p')
    for i, item in enumerate(items):
        if i < len(imgs):
            item['img'] = imgs[i].get('src')
        if i < len(ps):
            item['plot'] = ps[i].text.strip()

    return items
