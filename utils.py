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

def test_make_filename():
    string = 'ab|c?d/e.txt'
    ret = make_filename(string)
    assert ret == 'ab_c_d_e.txt'

def get_export_bookmarks_file_name(title):
    file = make_filename(title) + '.bmk'
    return file

def test_get_export_bookmarks_file_name():
    string = 'videofilename'
    ret = get_export_bookmarks_file_name(string)
    assert ret == 'videofilename.bmk'

def get_export_bookmarks_image_name(title, seconds):
    file = make_filename(title) + '-thumb-' + str(int(seconds)) + '.jpg'
    return file

def test_get_export_bookmarks_image_name():
    title = 'videofilename'
    seconds = 120
    ret = get_export_bookmarks_image_name(title, seconds)
    assert ret == 'videofilename-thumb-120.jpg'

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

def retrieve_position_from_thumb(string):
    res = re.search(r"thumb-(\d+)\.\w", string)
    ret = 0
    if (res):
        num = res.group(1)
        ret = int(num)
    else:
        print "No position found in thumb file name"
    return ret

def test_retrieve_position_from_thumb():
    string = 'videofilename-thumb-120.jpg'
    ret = retrieve_position_from_thumb(string)
    assert ret == 120

    string = 'videofilename-120.jpg'
    ret = retrieve_position_from_thumb(string)
    assert ret == 0

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
    ret = translateItemPath(itemPath)
    assert ret == 'plugin://plugin.googledrive/?item_id=1pj-j1YkzjKX8vyggsJiMeJr7k1-vEfwc&driveid=12202755082028000981&item_driveid=12202755082028000981&action=play&content_type=video'

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

def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

class BookmarkUtils:
    @staticmethod
    def get_file_name(itemPath):
        if not "plugin://" in itemPath:
            itemPath = os.path.basename(itemPath)
        return itemPath.decode('utf-8')

    @staticmethod
    def get_file_dir(itemPath):
        dirPath = os.path.dirname(itemPath) + os.sep
        return dirPath.decode('utf-8')

def test_get_file_name():
    itemPath = u'plugin://plugin.googledrive/?item_id=18cvSs9r93ysjiyt7YG6AoNWUzaUksBUnnA&driveid=10773356246826176512&item_driveid=00075374721629811014&action=play&content_type=video'
    ret = BookmarkUtils.get_file_name(itemPath)
    assert ret == u'plugin://plugin.googledrive/?item_id=18cvSs9r93ysjiyt7YG6AoNWUzaUksBUnnA&driveid=10773356246826176512&item_driveid=00075374721629811014&action=play&content_type=video'

    itemPath = '/home/kodi/Videos/back to future/back to the future.mp4'
    ret = BookmarkUtils.get_file_name(itemPath)
    assert ret == u'back to the future.mp4'

def test_get_file_dir():
    itemPath = 'plugin://plugin.googledrive/?item_id=18cvSs9r93ysjiyt7YG6AoNWUzaUksBUnnA&driveid=10773356246826176512&item_driveid=00075374721629811014&action=play&content_type=video'
    ret = BookmarkUtils.get_file_dir(itemPath)
    assert ret == u'plugin://plugin.googledrive/'
