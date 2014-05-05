# -*- coding: utf-8 -*-

from django.db import models

from cms.models import CMSPlugin

class RecentNewsPluginModel(CMSPlugin):
    class Meta:
        app_label = 'news'

    taints_cache = True

    max_items = models.PositiveIntegerField('max. number',
        blank=False,
        default=5,
        help_text=u'Please provide the maximum number of items to display (0 means unlimited)',
    )


class NewsArchivePluginModel(CMSPlugin):
    class Meta:
        app_label = 'news'

    taints_cache = True

    show_months = models.BooleanField('show months?',
        default=False,
        help_text=u'Check this option to break the archive down into years and months.',
    )
