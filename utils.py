import glob
import os
import re
import urllib
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
    ret = urllib.unquote(itemPath)
    if "PlayMedia" in itemPath:
        ret = re.findall('"([^"]*)"', ret).pop()
    return ret

def retrieve_positions(string):
    inBrackets = re.search(r"\[(.+?)\]", string).group(1)
    numbers = []
    if re.match(r"^[0-9]+$", inBrackets):
        numbers.append(int(inBrackets))
    else:
        if not re.match(r"([0-9]+, )+[0-9]+", inBrackets):
            print "No positions found"
            return numbers
        else:
            numbers = map(int, inBrackets.split(","))
    return numbers

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

def test_translateItemPath():
    itemPath = 'favourites://PlayMedia(%22plugin%3a%2f%2fplugin.googledrive%2f%3fitem_id%3d1pj-j1YkzjKX8vyggsJiMeJr7k1-vEfwc%26driveid%3d12202755082028000981%26item_driveid%3d12202755082028000981%26action%3dplay%26content_type%3dvideo%22)/'
    translateItemPath(itemPath)

def test_retrieve_positions():
    plot = '[1, 2, 3]'
    ret  = retrieve_positions(plot)
    assert ret == [1, 2, 3]

    plot = '[star] [test]'
    ret  = retrieve_positions(plot)
    assert ret == []

    plot = '[123]'
    ret  = retrieve_positions(plot)
    assert ret == [123]
