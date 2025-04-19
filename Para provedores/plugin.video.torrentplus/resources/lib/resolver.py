import xbmc
import xbmcplugin
import xbmcgui
import subprocess
import sys

def play_item(magnet_link, method):
    if method == 'elementum':
        xbmc.executebuiltin(f'PlayMedia(plugin://plugin.video.elementum/play?uri={magnet_link})')
    else:
        item = xbmcgui.ListItem(path=magnet_link)
        item.setProperty("IsPlayable", "true")
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem=item)
