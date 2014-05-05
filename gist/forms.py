# -*- coding: utf-8 -*-

from django.forms.models import ModelForm
from easy_select2.widgets import Select2TextInput

from .models import GistPluginModel


class GistPluginAdminForm(ModelForm):

    """Provides some smarts to the gist_user field; specifically, it allows
    the user to merely choose from one of the existing values while still
    allowing her to type a new one in.
    """

    class Meta:
        model = GistPluginModel

    def __init__(self, *args, **kwargs):
        super(GistPluginAdminForm, self).__init__(*args, **kwargs)

        def get_choices():
            values = GistPluginModel.objects.values_list('gist_user', flat=True).distinct().order_by('gist_user')
            return [{'id': str(x), 'text': str(x)} for x in values]

        self.fields['gist_user'].widget = Select2TextInput(
            select2attrs={
                'data': get_choices()
            },
        )


