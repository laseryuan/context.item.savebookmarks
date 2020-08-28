import utils
import xbmcgui
import xbmcvfs
from addbookmark import AddBookmark

params = utils.parameters_string_to_dict(sys.argv[2])

mode = params.get('mode')
item_label = params.get('item_label')
image_name = params.get('image_name')

position = utils.retrieve_position_from_thumb(image_name)
if position != 0:
    file = xbmc.translatePath('special://temp') + image_name
    list_item = xbmcgui.ListItem(item_label)
    import ipdb; ipdb.set_trace()
    from IPython import embed; embed(colors="neutral")
    addbookmark = AddBookmark()
    addbookmark.add_thumb(file, position)
