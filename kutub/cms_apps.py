from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

from .cms_menus import KutubMenu

@apphook_pool.register
class KutubApphook(CMSApp):
    app_name = "kutub"
    name = "Kutub Application"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["kutub.urls"]

    def get_menus(self, page=None, language=None, **kwargs):
        return [KutubMenu]
