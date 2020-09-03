import utils
import xbmcvfs
from bookmark import Bookmark

def add_thumb(bookmark, thumb, position):
    bookmark.add_position(position, thumb)

def import_gdrive_image(file_name, item_path):
    position = utils.retrieve_position_from_thumb(file_name)
    if position != 0:
        file = xbmc.translatePath('special://temp') + file_name
        bookmark = Bookmark(item_path)
        add_thumb(bookmark, file, position)

def main(mode):
    if mode == 'import_image':
        import_gdrive_image(params['image_name'], utils.translateItemPath(params['item_path']))

if __name__ == '__main__':
    params = utils.parameters_string_to_dict(sys.argv[2])
    mode = params.get('mode', 'test')

    if mode == 'test':
        from bookmark_test import TestBookmark
        TestBookmark.test_save_positions()
        TestBookmark.test_get_bookmarks()
    else:
        main(mode)
