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

def main():
    positions = [10, 20]
    xbmcgui.Dialog().ok("positions", str(positions))
    xbmc.log( "context.item.savebookmarks: bookmark positions: %s" % str(positions), xbmc.LOGNOTICE )

    add_posts_to_bookmark(positions)

def add_posts_to_bookmark(positions):
    common = Common()
    idFile = common.getIdFile()

    for timeInSeconds in positions:
        common.kodidb.add_position(idFile, timeInSeconds)

if __name__ == '__main__':
    main()
