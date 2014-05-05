# -*- coding: utf-8 -*-

from django.contrib.sitemaps import Sitemap
from django.utils import timezone

from .models import NewsItem

class NewsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.75

    def items(self):
        return NewsItem.objects.filter(published=True, news_date__lte=timezone.now)
