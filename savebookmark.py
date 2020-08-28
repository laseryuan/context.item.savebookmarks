import os
import sys
import re
from sqlite3 import dbapi2 as database

import xbmc
import xbmcgui
import xbmcvfs

from kodidb import KodiDB
from bookmark import Bookmark
import utils

class SaveBookmark(Bookmark):
    def __init__(self):
        Bookmark.__init__(self)
        self.bookmarks = self.kodidb.get_bookmark_by_idfile(self.idFile)

    def save_bmk_posts_to_file(self, data):
        file = self.path + '/' + utils.get_export_bookmarks_file_name()
        f = xbmcvfs.File (file, 'w')
        result = f.write(str(data))
        f.close()

    def save_imgs_to_folder(self, image, seconds):
        file = self.path + '/' + utils.get_export_bookmarks_image_name(
                                    sys.listitem.getLabel(), str(int(seconds))
                                 )
        xbmcvfs.copy(image, file)

    def save_thumbnails(self):
        if self.path != "":
            for bookmark in self.bookmarks:
                image = bookmark['thumbNailImage']
                if image:
                    xbmc.log( "context.item.savebookmarks: same thumbnail: %s" % image, xbmc.LOGNOTICE )
                    seconds = bookmark['timeInSeconds']
                    self.save_imgs_to_folder(image, seconds)

    def save_positions(self):
        positions = map(lambda x: x['timeInSeconds'], self.bookmarks)
        xbmcgui.Dialog().ok("positions", str(positions))
        xbmc.log( "context.item.savebookmarks: bookmark positions: %s" % str(positions), xbmc.LOGNOTICE )

        if self.path != "":
            xbmc.log( "context.item.savebookmarks: save to: %s" % self.path.encode('utf-8'), xbmc.LOGNOTICE )
            self.save_bmk_posts_to_file(utils.round_positions(positions))

def main():
    savebookmark = SaveBookmark()
    savebookmark.save_positions()
    savebookmark.save_thumbnails()

if __name__ == '__main__':
    main()
