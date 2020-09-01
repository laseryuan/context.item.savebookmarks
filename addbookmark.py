import os
import sys
import re
from sqlite3 import dbapi2 as database

import xbmc
import xbmcgui
import xbmcvfs

import utils
from kodidb import KodiDB
from bookmark import Bookmark

def get_positions():
    plot = sys.listitem.getVideoInfoTag().getPlot()
    return utils.retrieve_positions(plot)

def add_posts_to_bookmark(bookmark, positions):
    xbmcgui.Dialog().ok("positions", str(positions))
    for timeInSeconds in positions:
        bookmark.add_position(timeInSeconds)

def main():
    bookmark = Bookmark()

    positions = get_positions()
    add_posts_to_bookmark(bookmark, positions)

if __name__ == '__main__':
    main()
