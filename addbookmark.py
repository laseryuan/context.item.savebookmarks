import os
import sys
import re
from sqlite3 import dbapi2 as database

import xbmc
import xbmcgui
import xbmcvfs

import utils
from common import *

def main():
    positions = [10, 20]
    xbmcgui.Dialog().ok("positions", str(positions))
    xbmc.log( "context.item.savebookmarks: bookmark positions: %s" % str(positions), xbmc.LOGNOTICE )

    add_posts_to_bookmark(positions)

def add_posts_to_bookmark(positions):
    dbcon = database.connect(getDbFile())
    dbcon.row_factory = lambda cursor, row: row[0]
    dbcur = dbcon.cursor()

    fileName = get_file_name()
    dirPath = get_file_dir()
    #  dbcur.execute('SELECT player FROM bookmark').fetchall()
    idFiles = dbcur.execute('SELECT idFile FROM main.files WHERE idPath=(SELECT idPath FROM main.path WHERE strPath=?) AND strFilename=?',(dirPath, fileName,)).fetchall()
    if len(idFiles) < 1:
        raise RuntimeError("Can't get idFile!")
    idFile = idFiles[-1]
    for timeInSeconds in positions:
        dbcur.execute("INSERT INTO bookmark(idFile, timeInSeconds, type, player) Values (?, ?, 0, ?)", (idFile, timeInSeconds, "VideoPlayer"))
    dbcon.commit()
    dbcon.close()

if __name__ == '__main__':
    main()
