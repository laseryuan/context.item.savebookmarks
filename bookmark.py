import os
import sys
import re
from sqlite3 import dbapi2 as database

import xbmc
import xbmcgui
import xbmcvfs

import utils
from kodidb import KodiDB

class Bookmark:
    def __init__(self, itemPath = None):
        self.kodidb = KodiDB()
        self.save_dir = None
        self.bookmarks = None
        self.itemPath = itemPath or utils.translateItemPath(sys.listitem.getPath())
        self.file_dir = utils.BookmarkUtils.get_file_dir(self.itemPath)
        self.idFile = self.__get_idFile(self.itemPath)

    def __get_idFile(self, itemPath):
        fileName = utils.BookmarkUtils.get_file_name(itemPath)

        idFiles = self.kodidb.idFiles(self.file_dir, fileName)
        if len(idFiles) < 1:
            raise RuntimeError("Can't get idFile!")
        return idFiles[-1]['idFile']

    def __get_save_dir(self):
        if not self.save_dir:
            self.save_dir = self.file_dir
            if self.save_dir == "" or "plugin://" in self.save_dir:
                dialog = xbmcgui.Dialog()
                self.save_dir = dialog.browseSingle(0, 'Select directory for save .bmk', 'video')
        return self.save_dir

    def __save_bmk_posts_to_file(self, data):
        file = self.__get_save_dir() + '/' + utils.get_export_bookmarks_file_name(sys.listitem.getLabel())
        f = xbmcvfs.File (file, 'w')
        f.write(str(data))
        f.close()

    def __save_imgs_to_folder(self, image, seconds):
        file = self.__get_save_dir() + '/' + utils.get_export_bookmarks_image_name(
                                    sys.listitem.getLabel(), str(int(seconds))
                                 )
        xbmcvfs.copy(image, file)

    def __get_bookmarks(self):
        if not self.bookmarks:
            self.bookmarks = self.kodidb.bookmarks(self.idFile)
        return self.bookmarks

    def add_position(self, timeInSeconds, image = None):
        thumb = None
        if image:
            thumb = u'special://profile/Thumbnails/Video/Bookmarks/%s_%s.jpg' % ( utils.getHash(image), timeInSeconds )
            xbmcvfs.copy(image, thumb)

        if thumb:
            self.kodidb.insert_bookmark_with_thumb(self.idFile, timeInSeconds, thumb)
        else:
            self.kodidb.insert_bookmark(self.idFile, timeInSeconds)

        if image:
            xbmcvfs.delete(image)

    def save_thumbnails(self):
        if self.__get_save_dir() != "":
            for bookmark in self.__get_bookmarks():
                image = bookmark['thumbNailImage']
                if image:
                    xbmc.log( "context.item.savebookmarks: same thumbnail: %s" % image, xbmc.LOGNOTICE )
                    seconds = bookmark['timeInSeconds']
                    self.__save_imgs_to_folder(image, seconds)

    def save_positions(self):
        positions = map(lambda x: x['timeInSeconds'], self.__get_bookmarks())
        xbmcgui.Dialog().ok("positions", str(positions))
        xbmc.log( "context.item.savebookmarks: bookmark positions: %s" % str(positions), xbmc.LOGNOTICE )

        if self.__get_save_dir() != "":
            xbmc.log( "context.item.savebookmarks: save to: %s" % self.__get_save_dir().encode('utf-8'), xbmc.LOGNOTICE )
            self.__save_bmk_posts_to_file(utils.round_positions(positions))
