# -*- coding: utf-8 -*-

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class NewsApp(CMSApp):
    name = _('News')
    urls = ['project.apps.news.urls']
    app_name = 'news'

apphook_pool.register(NewsApp)
