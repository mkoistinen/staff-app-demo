# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.toolbar.items import Break, SubMenu
from cms.cms_toolbar import ADMIN_MENU_IDENTIFIER, ADMINISTRATION_BREAK


@toolbar_pool.register
class NewsToolbar(CMSToolbar):

    def populate(self):
        #
        # 'Apps' is the spot on the existing djang-cms toolbar admin_menu
        # 'where we'll insert all of our applications' menus.
        #
        admin_menu = self.toolbar.get_or_create_menu(ADMIN_MENU_IDENTIFIER, _('Apps'))

        #
        # Let's check to see where we would insert an 'Offices' menu in the
        # admin_menu.
        #
        position = admin_menu.get_alphabetical_insert_position(
            _('News'),
            SubMenu
        )

        #
        # If zero was returned, then we know we're the first of our
        # applications' menus to be inserted into the admin_menu, so, here
        # we'll compute that we need to go after the first
        # ADMINISTRATION_BREAK and, we'll insert our own break after our
        # section.
        #
        if not position:
            # OK, use the ADMINISTRATION_BREAK location + 1
            position = admin_menu.find_first(Break, identifier=ADMINISTRATION_BREAK) + 1
            # Insert our own menu-break, at this new position. We'll insert
            # all subsequent menus before this, so it will ultimately come
            # after all of our applications' menus.
            admin_menu.add_break('custom-break', position=position)

        # OK, create our newsitem menu here.
        newsitem_menu = admin_menu.get_or_create_menu('news-menu', _('News ...'), position=position)

        # Let's add some sub-menus to our newsitem menu that help our users
        # manage newsitem-related things.
        url = reverse('admin:news_newscategory_changelist')
        newsitem_menu.add_sideframe_item(_('News Category List'), url=url)

        url = reverse('admin:news_newscategory_add')
        newsitem_menu.add_modal_item(_('Add New News Category'), url=url)

        newsitem_menu.add_break()

        url = reverse('admin:news_newsitem_changelist')
        newsitem_menu.add_sideframe_item(_('News Item List'), url=url)

        url = reverse('admin:news_newsitem_add')
        newsitem_menu.add_modal_item(_('Add New News Item'), url=url)


