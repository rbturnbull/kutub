from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from cms.menu_bases import CMSAttachMenu
from menus.base import NavigationNode
from menus.menu_pool import menu_pool

from . import models

class Increment():
    def __init__(self):
        self.value = 0

    def __call__(self):
        self.value +=1
        return self.value

increment = Increment()


class KutubMenu(CMSAttachMenu):
    name = _("Kutub Menu")  # give the menu a name this is required.

    def get_nodes(self, request):
        """
        This method is used to build the menu tree.
        """
        nodes = [
            NavigationNode(
                title="Manuscripts",
                url=reverse("kutub:manuscript-list"),
                id=increment(),
                visible=True,
            ),
            NavigationNode(
                title="Repositories",
                url=reverse("kutub:repository-list"),
                id=increment(),
                visible=True,
            ),
            # NavigationNode(
            #     title="Tags",
            #     url=reverse("kutub:documenttag-list"),
            #     id=1,
            #     visible=True,
            # ),
            # NavigationNode(
            #     title="Scripts",
            #     url=reverse("kutub:script-list"),
            #     id=2,
            #     visible=True,
            # ),
            # NavigationNode(
            #     title="Languages",
            #     url=reverse("kutub:language-list"),
            #     id=3,
            #     visible=True,
            # ),
            # NavigationNode(
            #     title="Materials",
            #     url=reverse("kutub:material-list"),
            #     id=4,
            #     visible=True,
            # ),
        ]            
        return nodes

menu_pool.register_menu(KutubMenu)
