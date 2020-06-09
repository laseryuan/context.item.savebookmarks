import os
import sys
import re
from sqlite3 import dbapi2 as database

import xbmc
import xbmcgui
import xbmcvfs

from kodidb import KodiDB
from common import Common
import utils

def make_filename(title):
    filename = title.replace("|", "_").replace("?", "_").replace("/", "_")
    return filename

def save_bmk_to_folder(path, data):
    file = path + '/' + make_filename(sys.listitem.getLabel()) + '.bmk'
    f = xbmcvfs.File (file, 'w')
    result = f.write(str(data))
    f.close()

def main():
    common = Common()

    idFile = common.getIdFile()
    positions = common.kodidb.get_posts_from_bookmark(idFile)

    xbmcgui.Dialog().ok("positions", str(positions))
    xbmc.log( "context.item.savebookmarks: bookmark positions: %s" % str(positions), xbmc.LOGNOTICE )

    path = common.get_file_dir()

    if path == "" or "plugin://" in path:
        dialog = xbmcgui.Dialog()
        path = dialog.browseSingle(0, 'Select directory for save .bmk', 'video')

    if path != "":
        xbmc.log( "context.item.savebookmarks: save to: %s" % path.encode('utf-8'), xbmc.LOGNOTICE )
        save_bmk_to_folder(path, positions)

if __name__ == '__main__':
    main()
