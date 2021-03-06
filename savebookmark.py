import os
import sys
import re
from sqlite3 import dbapi2 as database

import xbmc
import xbmcgui
import xbmcvfs

from kodidb import KodiDB
from bookmark import Bookmark
import utils

def main():
    bookmark = Bookmark()
    bookmark.save_positions()
    bookmark.save_thumbnails()

if __name__ == '__main__':
    main()
