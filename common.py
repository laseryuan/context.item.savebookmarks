import os
import sys
import re
from sqlite3 import dbapi2 as database

import xbmc
import xbmcgui
import xbmcvfs

import utils
from kodidb import KodiDB

class Common:
    def __init__(self):
        self.kodidb = KodiDB(self.getDbFile())

    def getDbFile(self):
        USERDATA = xbmc.translatePath('special://userdata').decode('utf-8')
        return utils.Latest_DB(USERDATA, "MyVideos")

    def get_file_name(self):
        itemPath = sys.listitem.getPath()
        filePath = utils.translateItemPath(itemPath)
        if not "plugin://" in filePath:
            filePath = os.path.basename(filePath)
        return filePath.decode('utf-8')

    def get_file_dir(self):
        itemPath = sys.listitem.getPath()
        filePath = utils.translateItemPath(itemPath)
        dirPath = os.path.dirname(filePath) + os.sep
        return dirPath.decode('utf-8')

    def getIdFile(self):
        fileName = self.get_file_name()
        dirPath = self.get_file_dir()
        return self.kodidb.getIdFileInDb(fileName, dirPath)
