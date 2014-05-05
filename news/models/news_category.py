# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.db import models

from adminsortable.models import Sortable


class NewsCategory(Sortable):
    class Meta:
        app_label = 'news'
        verbose_name_plural = 'news categories'

    taints_cache = True

    name = models.CharField('category name',
        blank=False,
        default='',
        help_text=u'Please provide a unique name for this news category.',
        max_length=64,
    )

    slug = models.SlugField('slug',
        blank=False,
        default='',
        help_text=u'Please ensure there is a unique “slug” for this news category.',
        max_length=255,
    )

    def get_absolute_url(self):
        return reverse('news:archive', kwargs={'category_slug': self.slug})

    def __unicode__(self):
        return self.name


