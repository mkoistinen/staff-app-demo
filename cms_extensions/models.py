from django.db import models

from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool


class ColorExtension(PageExtension):
    color = models.CharField('color',
    	default=None,
    	help_text='Please provide an HTML color code.',
    	max_length=8,
    )

extension_pool.register(ColorExtension)