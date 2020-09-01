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
        self.kodidb = self.kodidb_conn()
        self.save_dir = None
        self.itemPath = itemPath or utils.translateItemPath(sys.listitem.getPath())
        self.file_dir = utils.BookmarkUtils.get_file_dir(self.itemPath)
        self.idFile = self.idFile(self.itemPath)

    def kodidb_conn(self):
        USERDATA = xbmc.translatePath('special://userdata').decode('utf-8')
        return KodiDB( utils.Latest_DB(USERDATA, "MyVideos") )

    def idFile(self, itemPath):
        fileName = utils.BookmarkUtils.get_file_name(itemPath)
        return self.kodidb.getIdFileInDb(fileName, self.file_dir)

    def get_save_dir(self):
        if not self.save_dir:
            self.save_dir = self.file_dir
            if self.save_dir == "" or "plugin://" in self.save_dir:
                dialog = xbmcgui.Dialog()
                self.save_dir = dialog.browseSingle(0, 'Select directory for save .bmk', 'video')
        return self.save_dir

    def add_position(self, timeInSeconds, image = None):
        thumb = None
        if image:
            thumb = u'special://profile/Thumbnails/Video/Bookmarks/%s_%s.jpg' % ( utils.getHash(image), timeInSeconds )
            xbmcvfs.copy(image, thumb)

        self.kodidb.add_position(self.idFile, timeInSeconds, thumb)

        if image:
            xbmcvfs.delete(image)
