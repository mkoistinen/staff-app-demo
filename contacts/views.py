# -*- coding: utf-8 -*-
# Django 1.6

import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import FormView

from cms.models.pagemodel import Page

from .forms import ContactForm, ContactAjaxForm


#
# This is used from the contact page, so, no AJAX is required. Its a normal
# POST submission.
#
class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'contacts/contact_form.html'

    def get_initial(self):
        """
        We wish to record where the visitor was BEFORE arriving at the contact
        page. We'll ultimately record this in the 'referer' field in our
        model. But for now, we'll initialize our form object to include this
        here, but only when creating the original form object. This way, no
        matter how many times the visitor has validation errors, etc., we'll
        still preserve this original HTTP_REFERER.
        """
        initial = super(ContactFormView, self).get_initial()
        initial['referer'] = self.request.META.get('HTTP_REFERER', ''),
        return initial
        
    def get_success_url(self):
        page = get_object_or_404(
            Page,
            reverse_id='contact_form_submission',
            publisher_is_draft=False
        )
        return page.get_absolute_url()

    def form_valid(self, form):
        self.object = form.save()
        return super(ContactFormView, self).form_valid(form)

#
# From: https://docs.djangoproject.com/en/1.6/topics/class-based-views/generic-editing/#ajax-example
#
class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors)  # , status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return self.render_to_json_response(data)
        else:
            return response


#
# This is used from the ContactPlugin, so could be anywhere on the site. It is
# submitted via AJAX and shouldn't take the user off the page.
#
class ContactFormAjaxView(AjaxableResponseMixin, FormView):
    form_class = ContactAjaxForm
    http_method_names = [u'post']  # Not interested in any GETs here...
    template_name = 'contacts/_contact_widget.html'

    #
    # NOTE: Even though this will never be used, the FormView requires that
    # either the success_url property or the get_success_url() method is
    # defined. So, let use the sensible thing and set it to the page where
    # this plugin is coming from.
    #
    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        # AjaxableResponseMixin expects our contact object to be 'self.object'.
        self.object = form.save(commit=True)
        return super(ContactFormAjaxView, self).form_valid(form)
