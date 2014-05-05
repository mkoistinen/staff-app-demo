# -*- coding: utf-8 -*-

from django import template
from django.utils.text import Truncator

register = template.Library()


@register.simple_tag(takes_context=True)
def placeholder_truncate_words(context, placeholderfield, words=20):

    from cms.plugin_rendering import render_placeholder

    if not 'request' in context:
        return '<!-- missing request -->'

    html = render_placeholder(placeholderfield, context)

    return Truncator(html).words(words, html=True, truncate='...')
