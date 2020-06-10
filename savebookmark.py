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

class SaveBookmark():
    def __init__(self):
        self.common = Common()
        idFile = self.common.getIdFile()
        self.bookmarks = self.common.kodidb.get_bookmark_by_idfile(idFile)

    def save_bmk_to_folder(self, path, data):
        file = path + '/' + utils.make_filename(sys.listitem.getLabel()) + '.bmk'
        f = xbmcvfs.File (file, 'w')
        result = f.write(str(data))
        f.close()

    def save_positions(self):
        positions = map(lambda x: x['timeInSeconds'], self.bookmarks)
        xbmcgui.Dialog().ok("positions", str(positions))
        xbmc.log( "context.item.savebookmarks: bookmark positions: %s" % str(positions), xbmc.LOGNOTICE )

        path = self.common.get_file_dir()

        if path == "" or "plugin://" in path:
            dialog = xbmcgui.Dialog()
            path = dialog.browseSingle(0, 'Select directory for save .bmk', 'video')

        if path != "":
            xbmc.log( "context.item.savebookmarks: save to: %s" % path.encode('utf-8'), xbmc.LOGNOTICE )
            self.save_bmk_to_folder(path, positions)

def main():
    savebookmark = SaveBookmark()
    savebookmark.save_positions()

if __name__ == '__main__':
    main()
