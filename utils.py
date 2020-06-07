import glob
import os
import re

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

def test_Latest_DB():
    #  USERDATA = xbmc.translatePath(os.path.join('special://home/userdata'))
    USERDATA = '/home/kodi/.kodi/userdata/'
    ret = Latest_DB(USERDATA, "MyVideos")
    assert "MyVideos" in ret
