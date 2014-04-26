# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import StaffListView, StaffDetailView


urlpatterns = patterns('',

    # List View
    url(r'^$', StaffListView.as_view(), name="staffmember_list"),

    # Detail View
    url(r'^(?P<slug>[^/]+)/$', StaffDetailView.as_view(), name='staffmember_detail'),
)
