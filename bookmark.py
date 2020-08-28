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
    def __init__(self):
        self.kodidb = self.get_kodidb()
        self.listitem = sys.listitem
        itemPath = self.listitem.getPath()
        self.filePath = utils.translateItemPath(itemPath)
        self.path = utils.BookmarkUtils.get_file_dir(self.filePath)
        self.idFile = self.get_idFile()
        self.get_work_dir()

    def get_kodidb(self):
        USERDATA = xbmc.translatePath('special://userdata').decode('utf-8')
        return KodiDB( utils.Latest_DB(USERDATA, "MyVideos") )

    def get_idFile(self):
        fileName = utils.BookmarkUtils.get_file_name(self.filePath)
        return self.kodidb.getIdFileInDb(fileName, self.path)

    def get_work_dir(self):
        if self.path == "" or "plugin://" in self.path:
            dialog = xbmcgui.Dialog()
            self.path = dialog.browseSingle(0, 'Select directory for save .bmk', 'video')

