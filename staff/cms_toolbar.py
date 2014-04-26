# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.toolbar.items import Break, SubMenu
from cms.cms_toolbar import ADMIN_MENU_IDENTIFIER, ADMINISTRATION_BREAK


@toolbar_pool.register
class StaffToolbar(CMSToolbar):

    def populate(self):
        admin_menu = self.toolbar.get_or_create_menu(ADMIN_MENU_IDENTIFIER, _('Apps'))

        position = admin_menu.get_alphabetical_insert_position(
            _('Staff'),
            SubMenu
        )

        if not position:
            position = admin_menu.find_first(Break, identifier=ADMINISTRATION_BREAK) + 1
            admin_menu.add_break('custom-break', position=position)

        menu = admin_menu.get_or_create_menu('staff-menu', _('Staff ...'), position=position)

        url = reverse('admin:staff_staffmember_changelist')
        menu.add_sideframe_item(_('Staff List'), url=url)

        url = reverse('admin:staff_staffmember_add')
        menu.add_modal_item(_('Add New Staff Member'), url=url)

