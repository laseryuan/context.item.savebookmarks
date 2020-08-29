import os
import sys
import re
from sqlite3 import dbapi2 as database

import xbmc
import xbmcgui
import xbmcvfs

import utils
from kodidb import KodiDB
from bookmark import Bookmark

class AddBookmark():
    def __init__(self):
        self.bookmark = Bookmark()

    def get_positions(self):
        plot = sys.listitem.getVideoInfoTag().getPlot()
        return utils.retrieve_positions(plot)

    def add_posts_to_bookmark(self, positions):
        xbmcgui.Dialog().ok("positions", str(positions))
        xbmc.log( "context.item.savebookmarks: bookmark positions: %s" % str(positions), xbmc.LOGNOTICE )
        for timeInSeconds in positions:
            self.bookmark.add_position(timeInSeconds)

    def add_thumb(self, thumb, position):
        xbmcvfs.copy(image, file)
        xbmcvfs.delete(image, file)
        return

def main():
    addbookmark = AddBookmark()

    positions = addbookmark.get_positions()
    addbookmark.add_posts_to_bookmark(positions)

if __name__ == '__main__':
    main()
