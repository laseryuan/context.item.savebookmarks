import xbmcaddon

class Setting():
    @staticmethod
    def get_addon_setting(setting_id):
        addon = xbmcaddon.Addon()
        setting = addon.getSettingString(setting_id)
        del addon
        return setting

    @staticmethod
    def set_addon_setting(setting_id, value):
        addon = xbmcaddon.Addon()
        setting = addon.setSettingString(setting_id, value)
        del addon
        return setting
