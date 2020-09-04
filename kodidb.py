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

    def idFiles(self, file_dir, fileName):
        return self.dbcur.execute('SELECT idFile FROM main.files WHERE idPath=(SELECT idPath FROM main.path WHERE strPath=?) AND strFilename=?',(file_dir, fileName,)).fetchall()

    def bookmarks(self, idFile):
        return self.dbcur.execute('SELECT * FROM main.bookmark WHERE idFile=? AND type=0', [idFile]).fetchall()

    def insert_bookmark_with_thumb(self, idFile, timeInSeconds, thumb):
        self.dbcur.execute("INSERT INTO bookmark(idFile, timeInSeconds, type, player, thumbNailImage) Values (?, ?, 0, ?, ?)", (idFile, timeInSeconds, "VideoPlayer", thumb))
        self.dbcon.commit()

    def insert_bookmark(self, idFile, timeInSeconds):
        self.dbcur.execute("INSERT INTO bookmark(idFile, timeInSeconds, type, player) Values (?, ?, 0, ?)", (idFile, timeInSeconds, "VideoPlayer"))
        self.dbcon.commit()
