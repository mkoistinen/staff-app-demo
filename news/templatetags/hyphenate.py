# -*- coding: utf-8 -*-

from hyphen import Hyphenator, dictools

from django import template
from django.conf import settings
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

#
# This whole file started with: http://djangosnippets.org/snippets/1446/
#

@register.filter
def hyphenate(value, arg=None, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    
    minlen = 7

    if arg:
        args = arg.split(u',')
        code = args[0]
        if len(args) > 1:
            minlen = int(args[1])
    else:
        code = settings.LANGUAGE_CODE

    #
    # Looks like this is assuming that the language code will arrive as 'xx-
    # YY'. In our case, it will arrive as simply 'en', so we MUST expand this
    # into a locale in order to work with PyHyphen.
    #

    # TODO: This should probably be a lookup against a dict in settings?

    s = code.split(u'-')

    if len(s) == 1:
        if s[0] == 'en':
            s.append(u'US')
        elif s[0] == 'bg':
            s.append(u'BG')

    lang = s[0].lower() + u'_' + s[1].upper()
    
    if not dictools.is_installed(lang): 
        dictools.install(lang)
        
    h = Hyphenator(lang)

    new = []

    for word in value.split(u' '):
        if len(word) > minlen and word.isalpha():
            new.append(u'&shy;'.join(h.syllables(word)))
        else:
            new.append(word)
    
    result = u' '.join(new)
    return mark_safe(result)

hyphenate.needs_autoescape = True
