import glob
import os
import re
from sqlite3 import dbapi2 as database

import utils

import xbmc

class KodiDB:
    def __init__(self):
        self.dbcon = self.__kodidb_conn()
        self.dbcon.row_factory = database.Row
        self.dbcur =  self.dbcon.cursor()

    def __del__(self):
        self.dbcon.close()

    def __kodidb_conn(self):
        USERDATA = xbmc.translatePath('special://userdata').decode('utf-8')
        dbFile = utils.Latest_DB(USERDATA, "MyVideos")
        return database.connect(dbFile)
