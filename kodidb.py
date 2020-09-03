import glob
import os
import re
from sqlite3 import dbapi2 as database

class KodiDB:
    def __init__(self, dbFile):
        self.dbcon = database.connect(dbFile)
        self.dbcon.row_factory = database.Row
        self.dbcur =  self.dbcon.cursor()

    def __del__(self):
        self.dbcon.close()
