# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _, get_language
from django.utils.safestring import mark_safe

from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu

from .models import Product


class ProductSubMenu(CMSAttachMenu):

    name = _("Product Sub-Menu")

    def get_nodes(self, request):
        nodes = []

        for product in Product.objects.filter(translations__language_code=get_language()).order_by('code').all():

            node = NavigationNode(
                mark_safe(product.name),
                product.get_absolute_url(),
                product.id,
            )

            nodes.append(node)

        return nodes

menu_pool.register_menu(ProductSubMenu)
