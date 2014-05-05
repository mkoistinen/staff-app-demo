# -*- coding: utf-8 -*-

from django.conf import settings
from django.db.models import Count
from django.utils import timezone

from cms.models import CMSPlugin
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from .models import (
    NewsArchivePluginModel,
    NewsCategory,
    NewsItem,
    RecentNewsPluginModel,
)

class RecentNewsPlugin(CMSPluginBase):
    model = RecentNewsPluginModel
    name = u'Recent News'
    render_template = "news/_recent_news_plugin.html"
    text_enabled = False
    cache = False

    def render(self, context, instance, placeholder):
        request = context.get('request', None)
        toolbar = getattr(request, 'toolbar', False)

        if toolbar and toolbar.edit_mode:
            news_items = NewsItem.objects.order_by('-news_date')
        else:
            news_items = NewsItem.objects.filter(published=True, news_date__lte=timezone.now).order_by('-news_date')

        if instance.max_items:
            news_items = news_items[:instance.max_items]

        context['news_items'] = news_items
        context['instance'] = instance
        return context

plugin_pool.register_plugin(RecentNewsPlugin)


class NewsCategoriesListPlugin(CMSPluginBase):
    model = CMSPlugin
    name = u'News Categories List'
    render_template = "news/_news_categories_list_plugin.html"
    text_enabled = False
    cache = False

    def render(self, context, instance, placeholder):
        request = context.get('request', None)
        toolbar = getattr(request, 'toolbar', False)

        if toolbar and toolbar.edit_mode:
            categories = NewsCategory.objects.annotate(
                count=Count('news_items')
            ).filter(
                count__gt=0
            ).order_by('order')
        else:
            categories = NewsCategory.objects.filter(
                news_items__published=True,
                news_items__news_date__lte=timezone.now
            ).annotate(
                count=Count('news_items')
            ).filter(
                count__gt=0
            ).order_by('order')

        context['categories'] = categories
        context['instance'] = instance
        return context

plugin_pool.register_plugin(NewsCategoriesListPlugin)


class NewsArchivePlugin(CMSPluginBase):
    model = NewsArchivePluginModel
    name = u'News Archive'
    render_template = "news/_news_archive_plugin.html"
    text_enabled = False
    cache = False

    def render(self, context, instance, placeholder):
        request = context.get('request', None)
        toolbar = getattr(request, 'toolbar', False)

        category_slug = context.get('category_slug', None)
        context['show_months'] = instance.show_months
        context['dates'] = NewsItem.objects.get_months(category_slug, years_only=(not instance.show_months), edit_mode=(toolbar and toolbar.edit_mode))
        context['instance'] = instance
        return context

plugin_pool.register_plugin(NewsArchivePlugin)
