# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from cms.admin.placeholderadmin import PlaceholderAdminMixin
from parler.admin import TranslatableAdmin

from .models import Product

class ProductAdmin(PlaceholderAdminMixin, TranslatableAdmin):

    list_display = ('code', 'price', 'language_column',)

    fieldsets = (
        (None, {
            'fields': (
                'code',
                'price',
            ),
        }),
        (_('Translated Fields'), {
            'fields': (
                'name',
                'slug',
            ),
        }),
    )

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)
