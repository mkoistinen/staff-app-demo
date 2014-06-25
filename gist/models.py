# -*- coding: utf-8 -*-

from django.db import models

from cms.models import CMSPlugin


class GistPluginModel(CMSPlugin):

	gist_user = models.CharField('GitHub User',
		blank=False,
		default='',
		help_text=u'Please supply the username of the GitHub user',
		max_length=32,
	)

	gist_id = models.CharField('Gist ID',
		blank=False,
		default='',
		help_text=u'Please supply the ID of the gist',
		max_length=32,
	)

	filename = models.CharField('Filename',
		blank=True,
		default='',
		help_text=u'Optional. Supply a filename',
		max_length=64,
	)

	def __unicode__(self):
		return u'%s:%s:%s' % (self.gist_user, self.gist_id, self.filename, )
