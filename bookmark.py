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
        self.kodidb = self.get_kodidb()
        if itemPath:
            self.itemPath = itemPath
        else:
            self.itemPath = self.get_file_path()
        self.path = utils.BookmarkUtils.get_file_dir(self.itemPath)
        self.idFile = self.get_idFile()
        self.get_work_dir()

    def get_file_path(self):
        itemPath = sys.listitem.getPath()
        ret = utils.translateItemPath(itemPath)
        return ret

    def get_kodidb(self):
        USERDATA = xbmc.translatePath('special://userdata').decode('utf-8')
        return KodiDB( utils.Latest_DB(USERDATA, "MyVideos") )

    def get_idFile(self):
        fileName = utils.BookmarkUtils.get_file_name(self.itemPath)
        return self.kodidb.getIdFileInDb(fileName, self.path)

    def get_work_dir(self):
        if self.path == "" or "plugin://" in self.path:
            dialog = xbmcgui.Dialog()
            self.path = dialog.browseSingle(0, 'Select directory for save .bmk', 'video')

    def add_position(self, timeInSeconds):
        self.kodidb.add_position(self.idFile, timeInSeconds)
