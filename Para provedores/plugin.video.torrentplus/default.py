import sys
import urllib.parse
import xbmcplugin
import xbmcaddon
import xbmcgui
from resources.lib import menus, resolver, search

addon_handle = int(sys.argv[1])
params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))
action = params.get('action')
url = params.get('url')
query = params.get('query')
method = params.get('method')  # resolveurl ou elementum

if action == 'play' and url:
    resolver.play_item(url, method)
elif action == 'list' and url:
    menus.list_directory(url)
elif action == 'search':
    search.search_dialog()
else:
    menus.list_main()

# menus.py
import xbmcplugin
import xbmcgui
import sys
from resources.lib.parser import get_navigation, get_content_items

addon_handle = int(sys.argv[1])

BASE = sys.argv[0]

def list_main():
    li = xbmcgui.ListItem('Buscar')
    xbmcplugin.addDirectoryItem(addon_handle, f'{BASE}?action=search', li, True)

    nav = get_navigation()
    for title, href in nav:
        url = f'{BASE}?action=list&url={href}'
        li = xbmcgui.ListItem(label=title)
        xbmcplugin.addDirectoryItem(addon_handle, url, li, True)
    xbmcplugin.endOfDirectory(addon_handle)

def list_directory(page_url):
    items = get_content_items(page_url)
    for item in items:
        li = xbmcgui.ListItem(label=item['title'])
        li.setArt({'thumb': item['img'], 'icon': item['img'], 'fanart': item['img']})
        li.setInfo('video', {'title': item['title'], 'plot': item['plot']})
        if item.get('magnet'):
            li.setProperty('IsPlayable', 'true')
            play_url_rurl = f'{BASE}?action=play&url={item["magnet"]}&method=resolveurl'
            play_url_elem = f'{BASE}?action=play&url={item["magnet"]}&method=elementum'
            li.addContextMenuItems([
                ("Play via ResolveURL", f'RunPlugin({play_url_rurl})'),
                ("Play via Elementum", f'RunPlugin({play_url_elem})')
            ])
            xbmcplugin.addDirectoryItem(addon_handle, play_url_rurl, li, False)
        elif item.get('href'):
            next_url = f'{BASE}?action=list&url={item["href"]}'
            xbmcplugin.addDirectoryItem(addon_handle, next_url, li, True)
    xbmcplugin.endOfDirectory(addon_handle)
