# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import ContactFormView, ContactFormAjaxView


urlpatterns = patterns('',
    url(r'^multi_form/$', ContactFormAjaxView.as_view(), name='multi_form'),
    url(r'^$', ContactFormView.as_view(), name='contact_form'),
)
