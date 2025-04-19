import sys
import xbmcaddon
import xbmcgui
import xbmcplugin

# Adicione o caminho do addon ao sys.path para permitir imports
ADDON_PATH = xbmcaddon.Addon().getAddonInfo("path")
sys.path.append(ADDON_PATH + "/resources/lib")  # Caminho absoluto para a pasta lib

# Agora importe os módulos locais
from parser import parse_main_menu, parse_category, parse_movie_page
from utils import get_cache, set_cache
from debrid import resolve_debrid
from constants import MAIN_URL, PROVIDERS_URL

addon = xbmcaddon.Addon()
_URL = "https://raw.githubusercontent.com/Linekodi/provedores/main/Para%20provedores/"

def router(paramstring):
    params = dict(pair.split("=") for pair in paramstring.split("&") if "=" in pair)
    mode = params.get("mode", "main")

    if mode == "main":
        items = parse_main_menu(_URL + "torrentplus.org.html")
        for item in items:
            add_directory_item(item["title"], f"?mode=category&url={item['url']}")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    elif mode == "category":
        url = params.get("url", "")
        items = parse_category(url)
        for item in items:
            add_directory_item(item["title"], f"?mode=play&url={item['url']}", is_folder=False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    elif mode == "play":
        magnet = parse_movie_page(params.get("url", ""))
        resolve_debrid(magnet)  # Integração com RealDebrid/Elementum

def add_directory_item(label, url, is_folder=True):
    li = xbmcgui.ListItem(label=label)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, li, is_folder)

if __name__ == "__main__":
    router(sys.argv[2][1:])
