import json, os, xbmcvfs

CACHE_DIR = xbmcvfs.translatePath("special://temp/torrentplus_cache/")

def get_cache(key):
    path = os.path.join(CACHE_DIR, f"{key}.json")
    if xbmcvfs.exists(path):
        with xbmcvfs.File(path) as f:
            return json.loads(f.read())
    return None

def set_cache(key, data):
    if not xbmcvfs.exists(CACHE_DIR):
        xbmcvfs.mkdirs(CACHE_DIR)
    path = os.path.join(CACHE_DIR, f"{key}.json")
    with xbmcvfs.File(path, "w") as f:
        f.write(json.dumps(data))
