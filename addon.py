import os
import sys
import re
from sqlite3 import dbapi2 as database

import xbmc
import xbmcgui
import xbmcvfs

import utils

def make_filename(title):
    filename = title.replace("|", "_").replace("?", "_").replace("/", "_")
    return filename

def save_file_to_folder(path, data):
    file = path + '/' + make_filename(sys.listitem.getLabel()) + '.bmk'
    f = xbmcvfs.File (file, 'w')
    result = f.write(str(data))
    f.close()

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

def main():
    positions = get_posts_from_bookmark()
    xbmcgui.Dialog().ok("positions", str(positions))
    xbmc.log( "context.item.savebookmarks: bookmark positions: %s" % str(positions), xbmc.LOGNOTICE )

    path = get_file_dir()

    if path == "" or "plugin://" in path:
        dialog = xbmcgui.Dialog()
        path = dialog.browseSingle(0, 'Select directory for save .bmk', 'video')

    if path != "":
        xbmc.log( "context.item.savebookmarks: save to: %s" % path.encode('utf-8'), xbmc.LOGNOTICE )
        save_file_to_folder(path, positions)

def getDbFile():
    USERDATA = xbmc.translatePath('special://userdata').decode('utf-8')
    return utils.Latest_DB(USERDATA, "MyVideos")

def translateItemPath(itemPath):
    ret = itemPath
    if "PlayMedia" in itemPath:
        ret = re.findall('"([^"]*)"', ret).pop()
    return ret

def get_posts_from_bookmark():
    dbcon = database.connect(getDbFile())
    dbcon.row_factory = lambda cursor, row: row[0]
    dbcur =  dbcon.cursor()

    fileName = get_file_name()
    dirPath = get_file_dir()
    #  dbcur.execute('SELECT strFilename FROM files').fetchall()
    #  dbcur.execute('SELECT strPath FROM path').fetchall()
    #  dbcur.execute('SELECT strFilename FROM files WHERE strFilename=?', [fileName]).fetchall()
    #  dbcur.execute('SELECT strFilename FROM files WHERE strFilename=?', [itemPath]).fetchall()
    ret = dbcur.execute('SELECT timeInSeconds FROM main.bookmark WHERE idFile=(SELECT idFile FROM main.files WHERE idPath=(SELECT idPath FROM main.path WHERE strPath=?) AND strFilename=?) ORDER BY timeInSeconds',(dirPath, fileName,)).fetchall()
    dbcon.close()
    return ret

if __name__ == '__main__':
    main()
