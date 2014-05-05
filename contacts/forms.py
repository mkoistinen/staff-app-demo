# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm

from .models import Contact


class ContactBaseForm(ModelForm):
    class Meta:
        abstract = True

    required_css_class = 'required'

    #
    # To help prevent people sending a typo’ed email address, then wondering
    # why we never got back to them, we'll require them to provide their email
    # twice.
    #
    verify_email = forms.EmailField(
        label=u'Verify email',
        help_text=u'Please retype your email address here.',
        max_length=255,
        required=True,
    )

    required_fields = []

    def __init__(self, *args, **kwargs):
        super(ContactBaseForm, self).__init__(*args, **kwargs)

        # We wish for some fields to be mandatory on THIS form
        for field in self.required_fields:
            self.fields[field].required = True

    def clean(self):
        ''' Want to ensure that the user type their email address in correctly twice.'''

        cleaned_data = super(ContactBaseForm, self).clean()

        #
        # Ensure that both of the email addresses match one another.
        #
        email = cleaned_data.get('email')
        verify_email = cleaned_data.get('verify_email')

        if email != verify_email:
            raise forms.ValidationError(u'Please ensure that you enter the correct email address twice.')

        return cleaned_data


class ContactForm(ContactBaseForm):
    class Meta:
        model = Contact
        fields = [
            'name', 'company', 'email', 'verify_email', 'telephone',
            'comments', 'referer',
        ]
        widgets = {
            'referer': forms.HiddenInput(),
        }

    required_fields = ['name', 'email', 'verify_email', ]


class ContactAjaxForm(ContactBaseForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'verify_email', 'telephone', 'referer', ]
        widgets = { 'referer': forms.HiddenInput(), }

    required_fields = ['email', 'verify_email', ]
