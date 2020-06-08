import glob
import os
import re
from sqlite3 import dbapi2 as database

# Function to find the latest version of a database
def Latest_DB(USERDATA, DB):
    if DB in ['Addons', 'ADSP', 'Epg', 'MyMusic', 'MyVideos', 'Textures', 'TV', 'ViewModes']:
        DATABASE = os.path.join(USERDATA,'Database')
        match = glob.glob(os.path.join(DATABASE,'%s*.db' % DB))
        comp = '%s(.+?).db' % DB[1:]
        highest = 0
        for file in match:
            try:
                check = int(re.compile(comp).findall(file)[0])
            except:
                check = 0
            if highest < check:
                highest = check
        db_file = '%s%s.db' % (DB, highest)
        return os.path.join(DATABASE, db_file)
    else:
        return False

def getHash(string):
    string = string.lower()
    bytes = bytearray(string)
    crc = 0xffffffff;
    for b in bytes:
        crc = crc ^ (b << 24)
        for i in range(8):
            if (crc & 0x80000000): crc = (crc << 1) ^ 0x04C11DB7
            else: crc = crc << 1;
        crc = crc & 0xFFFFFFFF
    return "%08x" % crc

def get_posts_from_bookmark(dbcur, idFile):
    #  dbcur.execute('SELECT strFilename FROM files').fetchall()
    #  dbcur.execute('SELECT strPath FROM path').fetchall()
    #  dbcur.execute('SELECT strFilename FROM files WHERE strFilename=?', [fileName]).fetchall()
    #  dbcur.execute('SELECT strFilename FROM files WHERE strFilename=?', [itemPath]).fetchall()
    ret = dbcur.execute('SELECT timeInSeconds FROM main.bookmark WHERE idFile=?', [idFile]).fetchall()
    return ret

def getIdFileInDb(dbcur, fileName, dirPath):
    #  dbcur.execute('SELECT player FROM bookmark').fetchall()
    idFiles = dbcur.execute('SELECT idFile FROM main.files WHERE idPath=(SELECT idPath FROM main.path WHERE strPath=?) AND strFilename=?',(dirPath, fileName,)).fetchall()
    if len(idFiles) < 1:
        raise RuntimeError("Can't get idFile!")
    return idFiles[-1]

def test_Latest_DB():
    #  USERDATA = xbmc.translatePath(os.path.join('special://home/userdata'))
    USERDATA = '/home/kodi/.kodi/userdata/'
    ret = Latest_DB(USERDATA, "MyVideos")
    assert "MyVideos" in ret

def test_getHash():
    string = "Thumbnail-Name"
    hash = getHash(string)
    assert hash == 'ed7bca40'

def test_get_posts_from_bookmark():
    dbFile = u'/home/kodi/.kodi/userdata/Database/MyVideos107.db'
    dbcon = database.connect(dbFile)
    dbcon.row_factory = lambda cursor, row: row[0]
    dbcur =  dbcon.cursor()
    idFile = 5
    posts = get_posts_from_bookmark(dbcur, idFile)
    dbcon.close()

def test_getIdFileInDb():
    dbFile = u'/home/kodi/.kodi/userdata/Database/MyVideos107.db'
    dbcon = database.connect(dbFile)
    dbcon.row_factory = lambda cursor, row: row[0]
    dbcur =  dbcon.cursor()

    fileName = u'back to the future.mp4'
    dirPath = u'/home/kodi/Videos/back to future/'

    idFile = getIdFileInDb(dbcur, fileName, dirPath)
    dbcon.close()
