from bookmark import Bookmark

import mock
from mock import patch

class TestBookmark():

    @staticmethod
    def test_add_position():
        item_path = 'plugin://plugin.googledrive/?item_id=18cvSs9r93ysjiyt7YG6AoNWUzaUksBUnnA&driveid=10773356246826176512&item_driveid=00075374721629811014&action=play&content_type=video'
        thumb = '/home/kodi/.kodi/temp/Back.to.the.Future.1985.1080p.BluRay.x264-NODLABS-thumb-120.jpg'
        position = 120
        bookmark = Bookmark(item_path)
        with patch('bookmark.Bookmark.add_position', return_value=None) as pmock:
            bookmark.add_position(position, thumb)
            pmock.assert_called_once()

    @staticmethod
    def test_save_positions():
        item_path = 'plugin://plugin.googledrive/?item_id=18cvSs9r93ysjiyt7YG6AoNWUzaUksBUnnA&driveid=10773356246826176512&item_driveid=00075374721629811014&action=play&content_type=video'
        bookmark = Bookmark(item_path)
        with patch.object(bookmark, '_Bookmark__save_bmk_posts_to_file', return_value=None):
            with patch.object(bookmark, '_Bookmark__get_save_dir', return_value='/tmp'):
                with patch('bookmark.xbmcgui', mock.MagicMock()):
                    ret = bookmark.save_positions()
