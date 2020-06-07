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

def main():
    positions = get_posts_from_bookmark()
    xbmcgui.Dialog().ok("positions", str(positions))
    xbmc.log( "context.item.savebookmarks: bookmark positions: %s" % str(positions), xbmc.LOGNOTICE )

    dialog = xbmcgui.Dialog()
    path = dialog.browseSingle(0, 'Select directory for save .bmk', 'video')

    if path != "":
        xbmc.log( "context.item.savebookmarks: save to: %s" % path, xbmc.LOGNOTICE )
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

    itemPath = sys.listitem.getPath()
    filePath = translateItemPath(itemPath)
    dirPath = os.path.dirname(filePath) + os.sep
    ret = dbcur.execute('SELECT timeInSeconds FROM main.bookmark WHERE idFile=(SELECT idFile FROM main.files WHERE idPath=(SELECT idPath FROM main.path WHERE strPath=?) AND strFilename=?) ORDER BY timeInSeconds',(dirPath, os.path.basename(filePath),)).fetchall()
    dbcon.close()
    return ret

if __name__ == '__main__':
    main()
