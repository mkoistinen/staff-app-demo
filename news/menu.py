# -*- coding: utf-8 -*-

# from django.utils.translation import ugettext_lazy as _
# from django.utils.translation import get_language

# from menus.base import NavigationNode  # Modifier
# from menus.menu_pool import menu_pool
# from cms.menu_bases import CMSAttachMenu

# from models import Project


# class ProjectsSubMenu(CMSAttachMenu):

#     name = _("Projects Sub-Menu")

#     def get_nodes(self, request):
#         language = get_language()
#         nodes = []
#         for project in Project.objects.language(language).filter(published=True).order_by('order'):
#             node = NavigationNode(
#                 project.get_title(),
#                 project.get_absolute_url(),
#                 project.pk
#             )
#             nodes.append(node)

#         return nodes

# menu_pool.register_menu(ProjectsSubMenu)
