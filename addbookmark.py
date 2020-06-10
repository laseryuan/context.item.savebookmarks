import os
import sys
import re
from sqlite3 import dbapi2 as database

import xbmc
import xbmcgui
import xbmcvfs

import common
import utils
from kodidb import KodiDB
from common import Common

class AddBookmark():
    def __init__(self):
        self.common = Common()
        self.idFile = self.common.getIdFile()

    def add_posts_to_bookmark(self, positions):
        xbmcgui.Dialog().ok("positions", str(positions))
        xbmc.log( "context.item.savebookmarks: bookmark positions: %s" % str(positions), xbmc.LOGNOTICE )
        for timeInSeconds in positions:
            self.common.kodidb.add_position(self.idFile, timeInSeconds)

def main():
    addbookmark = AddBookmark()

    positions = [10, 20]
    addbookmark.add_posts_to_bookmark(positions)

if __name__ == '__main__':
    main()
