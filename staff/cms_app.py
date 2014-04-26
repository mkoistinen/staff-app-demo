# -*- coding: utf-8 -*-

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

from .menu import StaffSubMenu


class StaffApp(CMSApp):
    name = _('Staff')
    urls = ['project.apps.staff.urls', ]
    app_name = 'staff'
    menus = [StaffSubMenu, ]

apphook_pool.register(StaffApp)
