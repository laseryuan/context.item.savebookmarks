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

class AddBookmark(Bookmark):
    def __init__(self):
        Bookmark.__init__(self)

    def get_positions(self):
        plot = self.listitem.getVideoInfoTag().getPlot()
        return utils.retrieve_positions(plot)

    def add_posts_to_bookmark(self, positions):
        xbmcgui.Dialog().ok("positions", str(positions))
        xbmc.log( "context.item.savebookmarks: bookmark positions: %s" % str(positions), xbmc.LOGNOTICE )
        for timeInSeconds in positions:
            self.kodidb.add_position(self.idFile, timeInSeconds)

    def add_thumb(self, thumb, position):
        import ipdb; ipdb.set_trace()
        from IPython import embed; embed(colors="neutral")
        xbmcvfs.copy(image, file)
        xbmcvfs.delete(image, file)
        return

def main():
    addbookmark = AddBookmark()

    positions = addbookmark.get_positions()
    addbookmark.add_posts_to_bookmark(positions)

if __name__ == '__main__':
    main()
