# -*- coding: utf-8 -*-

from django.contrib import admin

from easy_select2 import select2_modelform
from adminsortable.admin import SortableAdmin

from ..models import Clipping

class ClippingAdmin(SortableAdmin):
    form = select2_modelform(Clipping, attrs={'width': '250px'})
    list_display = ('staff', 'title', 'get_type', )
    list_display_links = ('staff', 'title', )
    readonly_fields= ('get_type', )

    fieldsets = (
        (None, {
            'fields': (
                'staff',
                'title',
                'download',
                'news_item',
                'external_link',
            ),
        }),
    )

admin.site.register(Clipping, ClippingAdmin)
