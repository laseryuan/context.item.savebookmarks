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

def test_import_gdrive_image():
    params = {'item_label': 'Back.to.the.Future.1985.1080p.BluRay.x264-NODLABS.mkv', 'item_path': 'plugin%3A%2F%2Fplugin.googledrive%2F%3Fitem_id%3D18cvSs9r93ysjiyt7YG6AoNWUzaUksBUnnA%26driveid%3D10773356246826176512%26item_driveid%3D00075374721629811014%26action%3Dplay%26content_type%3Dvideo', 'mode': 'import_image', 'image_name': 'Back.to.the.Future.1985.1080p.BluRay.x264-NODLABS-thumb-120.jpg'}
    import_gdrive_image(params['image_name'], utils.translateItemPath(params['item_path']))

def main(mode):
    if mode == 'import_image':
        import_gdrive_image(params['image_name'], utils.translateItemPath(params['item_path']))

if __name__ == '__main__':
    if False:
    #  if True:
        test_import_gdrive_image()

        from savebookmark import TestSaveBookmark
        TestSaveBookmark.test_export_gdrive_image()
    else:
        params = utils.parameters_string_to_dict(sys.argv[2])
        mode = params.get('mode', '')
        main(mode)
