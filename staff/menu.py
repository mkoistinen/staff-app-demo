# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu

from .models import StaffMember


class StaffSubMenu(CMSAttachMenu):

    name = _("Staff Sub-Menu")

    def get_nodes(self, request):
        nodes = []

        for staff in StaffMember.objects.order_by('full_name').all():

            node = NavigationNode(
                mark_safe(staff.full_name),
                staff.get_absolute_url(),
                staff.id,
            )

            nodes.append(node)

        return nodes

menu_pool.register_menu(StaffSubMenu)
