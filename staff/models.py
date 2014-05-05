# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.db import models

from adminsortable.models import Sortable
from cms.models.fields import PlaceholderField
from filer.fields.image import FilerImageField

class Seniority(models.Model):
    class Meta:
        app_label = 'staff'
        verbose_name_plural = 'seniorities'

    label = models.CharField(u'label',
        blank=False,
        default='',
        help_text=u'Please provide a label for this seniority',
        max_length=64,
        unique=True,
    )

    def __unicode__(self):
        return self.label


class StaffMember(Sortable):
    class Meta:
        app_label = 'staff'


    full_name = models.CharField(u'full name',
        blank=False,
        default='',
        help_text=u'Please enter a full name for this staff member',
        max_length=64,
        unique=True,
    )

    slug = models.SlugField(u'slug',
        blank=False,
        default='',
        help_text=u'Provide a unique slug for this staff member',
        max_length=64,
    )

    seniority = models.ForeignKey('staff.Seniority',
        blank=True,
        default=None,
        help_text=u'Please specify a seniority level for this staff member',
        null=True
    )

    photo = FilerImageField(
        blank=True,
        help_text=u'Optional. Please supply a photo of this staff member.',
        null=True,
        on_delete=models.SET_NULL, # Important
    )

    bio = PlaceholderField('staff_bio')

    def absolute_url(self):
        return reverse('staff:staffmember_detail', kwargs={'slug': self.slug, })

    def __unicode__(self):
        return self.full_name
