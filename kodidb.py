import glob
import os
import re
from sqlite3 import dbapi2 as database

class KodiDB:
    def __init__(self, dbFile):
        self.dbcon = database.connect(dbFile)
        self.dbcon.row_factory = lambda cursor, row: row[0]
        self.dbcur =  self.dbcon.cursor()

    def __del__(self):
        self.dbcon.close()

    def get_posts_from_bookmark(self, idFile):
        #  self.dbcur.execute('SELECT strFilename FROM files').fetchall()
        #  self.dbcur.execute('SELECT strPath FROM path').fetchall()
        #  self.dbcur.execute('SELECT strFilename FROM files WHERE strFilename=?', [fileName]).fetchall()
        #  self.dbcur.execute('SELECT strFilename FROM files WHERE strFilename=?', [itemPath]).fetchall()
        ret = self.dbcur.execute('SELECT timeInSeconds FROM main.bookmark WHERE idFile=?', [idFile]).fetchall()
        return ret

    def getIdFileInDb(self, fileName, dirPath):
        #  self.dbcur.execute('SELECT player FROM bookmark').fetchall()
        idFiles = self.dbcur.execute('SELECT idFile FROM main.files WHERE idPath=(SELECT idPath FROM main.path WHERE strPath=?) AND strFilename=?',(dirPath, fileName,)).fetchall()
        if len(idFiles) < 1:
            raise RuntimeError("Can't get idFile!")
        return idFiles[-1]

    def add_position(self, idFile, timeInSeconds):
        self.dbcur.execute("INSERT INTO bookmark(idFile, timeInSeconds, type, player) Values (?, ?, 0, ?)", (idFile, timeInSeconds, "VideoPlayer"))
        self.dbcon.commit()

def test_get_posts_from_bookmark():
    kodidb = KodiDB(u'/home/kodi/.kodi/userdata/Database/MyVideos107.db')

    idFile = 5
    posts = kodidb.get_posts_from_bookmark(idFile)

def test_getIdFileInDb():
    kodidb = KodiDB(u'/home/kodi/.kodi/userdata/Database/MyVideos107.db')

    fileName = u'back to the future.mp4'
    dirPath = u'/home/kodi/Videos/back to future/'

    idFile = kodidb.getIdFileInDb(fileName, dirPath)
