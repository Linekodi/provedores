from .constants import DEBRID_SERVICES

def resolve_debrid(magnet):
    addon = xbmcaddon.Addon()
    service = addon.getSetting("debrid_service")

    if service == "0":  # RealDebrid
        url = f"{DEBRID_SERVICES['realdebrid']}?url={magnet}"
    elif service == "1":  # AllDebrid
        url = f"{DEBRID_SERVICES['alldebrid']}?url={magnet}"
    else:  # Elementum
        url = f"{DEBRID_SERVICES['elementum']}{magnet}"

    xbmc.executebuiltin(f"RunPlugin({url})")
