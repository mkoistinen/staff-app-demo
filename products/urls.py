# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import patterns, url

from .views import (
    ProductListView,
    ProductDetailView,
)

urlpatterns = patterns('',

    #
    # Product List View
    #
    url(r'^$', ProductListView.as_view(), name='product_list'),

    #
    # Product Detail View
    #
    url(r'^(?P<slug>.*)/$', ProductDetailView.as_view(), name='product_detail'),
)
