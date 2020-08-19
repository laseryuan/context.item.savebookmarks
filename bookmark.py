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
        self.kodidb = KodiDB(self.getDbFile())
        self.listitem = sys.listitem
        itemPath = self.listitem.getPath()
        xbmc.log( "context.item.savebookmarks: itemPath: %s" % itemPath, xbmc.LOGNOTICE )
        self.filePath = utils.translateItemPath(itemPath)
        self.idFile = self.get_idFile()
        self.path = self.get_file_dir()
        self.get_work_dir()

    def getDbFile(self):
        USERDATA = xbmc.translatePath('special://userdata').decode('utf-8')
        return utils.Latest_DB(USERDATA, "MyVideos")

    def get_file_name(self):
        filePath = self.filePath
        if not "plugin://" in filePath:
            filePath = os.path.basename(filePath)
        return filePath.decode('utf-8')

    def get_file_dir(self):
        dirPath = os.path.dirname(self.filePath) + os.sep
        return dirPath.decode('utf-8')

    def get_idFile(self):
        fileName = self.get_file_name()
        dirPath = self.get_file_dir()
        return self.kodidb.getIdFileInDb(fileName, dirPath)

    def get_work_dir(self):
        if self.path == "" or "plugin://" in self.path:
            dialog = xbmcgui.Dialog()
            self.path = dialog.browseSingle(0, 'Select directory for save .bmk', 'video')

