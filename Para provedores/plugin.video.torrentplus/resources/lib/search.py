import xbmc
import xbmcgui
import urllib.parse
import sys
from .parser import BASE_URL



BASE = sys.argv[0]


def search_dialog():
    keyboard = xbmc.Keyboard('', 'Buscar conteúdo')
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        search_url = f'{BASE_URL}torrentplus.org.html'
        search_list(query, search_url)


def search_list(query, url):
    import xbmcplugin
    import sys
    from .parser import get_content_items

    handle = int(sys.argv[1])
    query = query.lower()
    items = get_content_items(url)
    for item in items:
        if query in item['title'].lower():
            li = xbmcgui.ListItem(label=item['title'])
            li.setArt({'thumb': item['img'], 'icon': item['img'], 'fanart': item['img']})
            li.setInfo('video', {'title': item['title'], 'plot': item['plot']})
            if item.get('magnet'):
                li.setProperty('IsPlayable', 'true')
                play_url = f'{BASE}?action=play&url={item["magnet"]}&method=resolveurl'
                li.addContextMenuItems([
                    ("Play via ResolveURL", f'RunPlugin({play_url})'),
                    ("Play via Elementum", f'RunPlugin({BASE}?action=play&url={item["magnet"]}&method=elementum)')
                ])
                xbmcplugin.addDirectoryItem(handle, play_url, li, False)
    xbmcplugin.endOfDirectory(handle)
