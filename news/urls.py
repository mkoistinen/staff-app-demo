# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import (
    NewsArchiveView,
    NewsItemDetailView,
)

urlpatterns = patterns('',

    #
    # News Archive List Views
    #
    url(r'^$', NewsArchiveView.as_view(), name='archive'),
    url(r'^(?P<year>\d{4})/$', NewsArchiveView.as_view(), name='archive'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', NewsArchiveView.as_view(), name='archive'),

    url(r'^category/(?P<category_slug>[^/]+)/$', NewsArchiveView.as_view(), name='archive'),
    url(r'^category/(?P<category_slug>[^/]+)/(?P<year>\d{4})/$', NewsArchiveView.as_view(), name='archive'),
    url(r'^category/(?P<category_slug>[^/]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/$', NewsArchiveView.as_view(), name='archive'),

    #
    # News Item Detail
    #
    url(r'^(?P<slug>[^/]+)/$', NewsItemDetailView.as_view(), name='news_item_detail'),
)
