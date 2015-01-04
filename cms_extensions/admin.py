
from django.contrib import admin
from cms.extensions import PageExtensionAdmin

from .models import ColorExtension


class ColorExtensionAdmin(PageExtensionAdmin):
    pass

admin.site.register(ColorExtension, ColorExtensionAdmin)