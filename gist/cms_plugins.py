# -*- coding: utf-8 -*-

from django.conf import settings

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import GistPluginModel
from .forms import GistPluginAdminForm

class GistPlugin(CMSPluginBase):
	form = GistPluginAdminForm
	name = u'Gist'
	model = GistPluginModel
	render_template = "gist/_gist_plugin.html"
	text_enabled = True

	def render(self, context, instance, placeholder):

		context['instance'] = instance

		return context

	def icon_src(self, instance):
		return settings.STATIC_URL + 'gist/images/gist_plugin_icon.png'

	def icon_alt(self, instance):
		return u'Gist: %s' % instance

plugin_pool.register_plugin(GistPlugin)