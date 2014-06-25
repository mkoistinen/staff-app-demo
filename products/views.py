# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.utils.translation import get_language
from django.views.generic import DetailView, ListView

from parler.views import TranslatableSlugMixin

from .models import Product


#
# Not very interesting, here...
#
class ProductListView(ListView):
    model = Product


#
# Products are translated, so, we need to add this Mixin, provided by
# django-parler.
#
class ProductDetailView(TranslatableSlugMixin, DetailView):
    model = Product

    #
    # This is needed to allow the language changer on the toolbar to work
    # properly with app_hooked objects.
    #
    def get(self, *args, **kwargs):
        self.object = self.get_object()
        if hasattr(self.request, 'toolbar'):
            self.request.toolbar.set_object(self.object)

        response = super(ProductDetailView, self).get(*args, **kwargs)
        return response

    #
    # A slight change required on the queryset to get the translated object.
    #
    def get_queryset(self):
        language = get_language()
        return super(ProductDetailView, self).get_queryset().filter(
            translations__language_code=language
        )
