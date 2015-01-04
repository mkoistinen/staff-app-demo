# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import NoReverseMatch
from django.contrib.sitemaps import Sitemap
from django.utils import translation

from .models import Product


class I18NSitemap(Sitemap):

    def __init__(self, language=None):
        if language:
            self.language = language
        else:
            self.language = settings.LANGUAGES[0][0]

    def location(self, item):
        with translation.override(self.language):
            try:
                return item.get_absolute_url()
            except NoReverseMatch:
                # Note, if we did our job right in items(), this
                # shouldn't happen at all.
                return ''


class ProductsSitemap(I18NSitemap):
    changefreq = "weekly"
    priority = 0.75

    def items(self):
        return Product.objects.translated(self.language).all()
