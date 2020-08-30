import utils
import xbmcgui
import xbmcvfs
from addbookmark import AddBookmark

params = utils.parameters_string_to_dict(sys.argv[2])
mode = params['mode']

position = utils.retrieve_position_from_thumb(params['image_name'])
if position != 0:
    file = xbmc.translatePath('special://temp') + params['image_name']
    item_path = utils.translateItemPath(params['item_path'])
    addbookmark = AddBookmark(item_path)
    addbookmark.add_thumb(file, position)
