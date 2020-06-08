import os
import sys
import re
from sqlite3 import dbapi2 as database

import xbmc
import xbmcgui
import xbmcvfs

import utils


def getDbFile():
    USERDATA = xbmc.translatePath('special://userdata').decode('utf-8')
    return utils.Latest_DB(USERDATA, "MyVideos")

def get_file_name():
    itemPath = sys.listitem.getPath()
    filePath = translateItemPath(itemPath)
    if not "plugin://" in filePath:
        filePath = os.path.basename(filePath)
    return filePath.decode('utf-8')

def get_file_dir():
    itemPath = sys.listitem.getPath()
    filePath = translateItemPath(itemPath)
    dirPath = os.path.dirname(filePath) + os.sep
    return dirPath.decode('utf-8')

def translateItemPath(itemPath):
    ret = itemPath
    if "PlayMedia" in itemPath:
        ret = re.findall('"([^"]*)"', ret).pop()
    return ret

def getIdFile(dbcur):
    fileName = get_file_name()
    dirPath = get_file_dir()

    #  dbcur.execute('SELECT player FROM bookmark').fetchall()
    idFiles = dbcur.execute('SELECT idFile FROM main.files WHERE idPath=(SELECT idPath FROM main.path WHERE strPath=?) AND strFilename=?',(dirPath, fileName,)).fetchall()
    if len(idFiles) < 1:
        raise RuntimeError("Can't get idFile!")
    return idFiles[-1]