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

def make_filename(title):
    filename = title.replace("|", "_").replace("?", "_").replace("/", "_")
    return filename

def round_positions(positions):
    return map(lambda x: int(x), positions)

def translateItemPath(itemPath):
    ret = itemPath
    if "PlayMedia" in itemPath:
        ret = re.findall('"([^"]*)"', ret).pop()
    return ret

def test_Latest_DB():
    #  USERDATA = xbmc.translatePath(os.path.join('special://home/userdata'))
    USERDATA = '/home/kodi/.kodi/userdata/'
    ret = Latest_DB(USERDATA, "MyVideos")
    assert "MyVideos" in ret

def test_getHash():
    string = "Thumbnail-Name"
    hash = getHash(string)
    assert hash == 'ed7bca40'

def test_round_positions():
    ret = round_positions([1.0, 2.1])
    assert ret == [1, 2]
