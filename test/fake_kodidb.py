class FakeKodiDB():
    def idFiles(self, *args):
        return [{'idFile': 3}]

    def bookmarks(self, *args):
        return \
            [{'idBookmark': 25,
              'idFile': 2,
              'player': u'VideoPlayer',
              'playerState': None,
              'thumbNailImage': None,
              'timeInSeconds': 10.0,
              'totalTimeInSeconds': None,
              'type': 0},
             {'idBookmark': 26,
              'idFile': 2,
              'player': u'VideoPlayer',
              'playerState': None,
              'thumbNailImage': None,
              'timeInSeconds': 20.0,
              'totalTimeInSeconds': None,
              'type': 0},
             {'idBookmark': 26,
              'idFile': 2,
              'player': u'VideoPlayer',
              'playerState': None,
              'thumbNailImage': None,
              'timeInSeconds': 40.0,
              'totalTimeInSeconds': None,
              'type': 0},
             {'idBookmark': 26,
              'idFile': 2,
              'player': u'VideoPlayer',
              'playerState': None,
              'thumbNailImage': None,
              'timeInSeconds': 20.0,
              'totalTimeInSeconds': None,
              'type': 0},
             {'idBookmark': 27,
              'idFile': 2,
              'player': u'VideoPlayer',
              'playerState': None,
              'thumbNailImage': None,
              'timeInSeconds': 30.0,
              'totalTimeInSeconds': None,
              'type': 0}]


