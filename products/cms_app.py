# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

from .menu import ProductSubMenu

class ProductApp(CMSApp):
    name = _('Products')
    urls = ['project.apps.products.urls']
    app_name = 'products'
    menus = [ProductSubMenu, ]

apphook_pool.register(ProductApp)
