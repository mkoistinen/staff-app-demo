# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible, force_text
from django.utils.translation import ugettext_lazy as _, get_language

from cms.models.fields import PlaceholderField
from parler.models import TranslatableModel, TranslatedFields
from parler.utils.context import switch_language

@python_2_unicode_compatible
class Product(TranslatableModel):
    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    code = models.CharField(_('code'),
        blank=False,
        default='',
        help_text=_('Please supply the product code.'),
        max_length=16,
    )

    description = PlaceholderField('product_description')

    price = models.DecimalField(_('price'),
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text=('Please supply the current retail price of this product.'),
    )

    translations = TranslatedFields(
        name = models.CharField(_('name'),
            blank=False,
            default='',
            help_text=_('Please supply the product name.'),
            max_length=128,
        ),
        slug = models.SlugField(_('slug'),
            blank=False,
            default='',
            help_text=_('Please supply the product slug.'),
            max_length=128,
        )
    )


    def get_absolute_url(self):
        '''
        Returns the URL (relative to the server root) for this object in the
        current language.
        '''

        #
        # Despite what the parler docs say, we need to add the extra parameter here.
        #
        with switch_language(self, get_language()):
            return reverse('products:product_detail', kwargs={'slug': self.slug, })


    def __str__(self):
        return force_text(self.code)
