# -*- coding: utf-8 -*-

import os.path

from django.db import models
from django.db.models import F
from django.db.models.signals import m2m_changed

from filer.fields.file import FilerFileField
from adminsortable.models import Sortable

from project.apps.news.models import NewsItem


class Clipping(Sortable):
    class Meta(Sortable.Meta):
        app_label = 'clippings'

    taints_cache = True

    staff = models.ForeignKey('staff.StaffMember',
        blank=False,
        default=None,
        help_text=u'Required. To whom is this clipping connected?',
        null=False,
        related_name='clippings',
    )

    title = models.CharField('title',
        blank=True,
        default='',
        help_text=u'Please provide a title for this clipping.',
        max_length=255,
    )

    download = FilerFileField(
        blank=True,
        null=True,
        help_text=u'Provide a file download. This overrides news items and external links.',
    )

    news_item = models.ForeignKey('news.NewsItem',
        blank=True,
        default=None,
        help_text=u'Select a News Item. This overrides external links.',
        null=True,
    )

    external_link = models.CharField(u'external link',
        blank=True,
        default='',
        help_text=u'Provide an external link.',
        max_length=2048,
    )

    def get_type(self):
        '''Returns the type of clipping this is'''
        if self.download:
            return 'file download'
        elif self.news_item:
            return 'news post'
        elif self.external_link:
            return 'external link'
        else:
            return 'unknown'

    def get_absolute_url(self):
        if self.download:
            return self.download.url
        elif self.news_item:
            return self.news_item.get_absolute_url()
        elif self.external_link:
            return self.external_link
        return None

    def get_target(self):
        if self.download:
            return '_blank'
        elif self.news_item:
            return ''
        elif self.external_link:
            return '_blank'
        return None

    get_type.short_description = 'clipping type'


    def save(self, **kwargs):
        from django.utils.text import Truncator
        '''
        Automatically set an appropriate title, depending on the type of media
        selected. Also, new items are at the top of the clippings list.
        '''

        is_new = (not self.id)

        if not self.title:
            if self.download:
                self.title = os.path.basename(self.download.file.name)
            elif self.news_item:
                self.title = self.news_item.headline
            elif self.external_link:
                self.title = self.external_link
            else:
                self.title = 'Untitled Clipping'

        self.title = Truncator(self.title).chars(252, truncate='...')

        super(Clipping, self).save(**kwargs)

        if is_new:
            # We need to push all the other clippings "down" one...
            Clipping.objects.exclude(id=self.id).update(order=F('order') + 1)
            # OK, there is now 'room' for this entry at an order of 2.
            Clipping.objects.filter(id=self.id).update(order=2)


    def __unicode__(self):
        return self.title


#
# NOTE: A news item can "point to" any number of staff members, but we'd like
# the staff members to decide whether that news item will appear on their
# pages. To facilitate this, when we point to a staff member from a news item,
# we'll automatically create a separate, but reciprocal relationship from the
# Staff member to the News Item (via a Clipping object), but it is not the
# same relationship, and one or the other can then be deleted without
# affecting the other.
#
# The signal sender is located in apps.news.models.news_item
# If this note is updated, please update the same note there.
#
def link_staff_to_news_item(sender, instance, action, pk_set, **kwargs):
    from project.apps.staff.models import StaffMember

    if action == 'post_add':
        for staff in StaffMember.objects.filter(pk__in=pk_set):
            if Clipping.objects.filter(staff=staff, external_link='', news_item=instance).count() == 0:
                #
                # OK, looks like staff doesn't already have this as a
                # clipping, so create one.
                #

                # print('Creating Clipping for %s ...' % staff.full_name)
                clipping = Clipping()
                clipping.staff = staff
                clipping.news_item = instance
                clipping.save()

# Listen for signals from NewsItem.related_staff M2M changes
m2m_changed.connect(link_staff_to_news_item, sender=NewsItem.related_staff.through)
