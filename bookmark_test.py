from test.fake_kodidb import FakeKodiDB
from test.fake_xbmc import mock_xbmc, mock_xbmcgui, mock_xbmcvfs, mock_sys
import sys
sys.modules['xbmc'] = mock_xbmc
sys.modules['xbmcgui'] = mock_xbmcgui
sys.modules['xbmcvfs'] = mock_xbmcvfs
import mock
from mock import patch

from bookmark import Bookmark

class TestBookmark():

    @staticmethod
    def test_bookmark():
        mock_sys.listitem.getPath.return_value = \
            'plugin://plugin.googledrive/?item_id=18cvS&driveid=10773&item_driveid=000753&action=play&content_type=video'

        with patch('bookmark.sys', mock_sys):
            with patch('bookmark.KodiDB', FakeKodiDB):
                bookmark = Bookmark()

    @staticmethod
    def test_add_position():
        item_path = \
            'plugin://plugin.googledrive/?item_id=18cvS&driveid=10773&item_driveid=000753&action=play&content_type=video'
        thumb = '/home/kodi/.kodi/temp/A-thumb-120.jpg'
        position = 120

        with patch('bookmark.sys', mock_sys):
            with patch('bookmark.KodiDB', FakeKodiDB):
                with patch('bookmark.Bookmark.add_position', return_value=None) as pmock:
                    bookmark = Bookmark(item_path)
                    bookmark.add_position(position, thumb)
                    pmock.assert_called_once()

    @staticmethod
    def test_save_positions():
        item_path = \
            'plugin://plugin.googledrive/?item_id=18cvS&driveid=10773&item_driveid=000753&action=play&content_type=video'
        with patch('bookmark.sys', mock_sys):
            with patch('bookmark.KodiDB', FakeKodiDB):
                with patch('bookmark.Bookmark._get_save_dir', return_value='/tmp'):
                    bookmark = Bookmark(item_path)
                    bookmark.save_positions()
