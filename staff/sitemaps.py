# -*- coding: utf-8 -*-

from django.contrib.sitemaps import Sitemap
from .models import StaffMember


class StaffSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.75

    def items(self):
        return StaffMember.objects.all()
