# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone

from cms.models import CMSPlugin


class Contact(models.Model):

    #
    # NOTE: Everything in this section should be optional, fields are to be
    # made Required in the Forms.
    #

    name = models.CharField(u'Name',
        blank=True,
        default='',
        help_text=u'Your name',
        max_length=64,
    )

    company = models.CharField(u'Company or Organization',
        blank=True,
        default='',
        help_text=u'Your organization’s name',
        max_length=64,
    )

    email = models.EmailField(u'Email',
        blank=True,
        default='',
        error_messages={'invalid': 'Please enter a correctly formatted email address.'},
        help_text=u'Your email address',
        max_length=255,
    )

    telephone = models.CharField(u'Telephone Number',
        blank=True,
        default='',
        help_text=u'If you wish to be contacted by phone, please ensure you enter the correct number here.',
        max_length=32,
    )

    comments = models.TextField(u'Comment or Question',
        blank=True,
        default='',
        help_text=u'Please let us know what is on your mind.',
    )

    # Meta, non-form data
    contact_date = models.DateTimeField(u'contact date',
        blank=True,
        default=timezone.now,
        help_text=u'When this person completed the contact form.',
    )

    was_contacted = models.BooleanField(u'has been contacted?',
        default=False,
        help_text=u'Check this if someone has already reached out to this person.',
    )

    notes = models.TextField(u'contact notes',
        blank=True,
        default='',
        help_text=u'Internal notes relating to contacting this person.',
    )

    referer = models.CharField(u'referring page',
        blank=True,
        default='',
        help_text=u'This is the page the visitor was on before coming to the contact page.',
        max_length=2048,
    )


    def send_notification_email(self):
        """
        Sends a notification email to the list of recipients defined in
        settings.NOTIFICATIONS informing them that a new contact has arrived.
        
        SERVER_EMAIL is defined in settings and contacts the "from"
        address for email sent from the webserver.
        
        MANAGERS needs to be defined in settings and should be a list
        containing the email addresses of those that should receive
        notification of an incoming contact.
        """

        # Using a template is probably overkill for this but...
        email_subject = render_to_string('contacts/notification-subject.txt', {
            'contact': self,
        })

        email_body = render_to_string('contacts/notification-body.txt', {
            'contact': self,
        })
        
        try:
            send_mail(
                email_subject,
                email_body,
                settings.SERVER_EMAIL,
                settings.MANAGERS,
                fail_silently=(not settings.DEBUG)
            )

        except Exception:
            # If NOT in DEBUG (development) mode, we silently ignore any
            # exceptions to avoid interrupting capture of the submitter's
            # details. If in DEBUG mode, then raise the error so we can
            # troubleshoot.
            if (settings.DEBUG):
                raise


    def save(self, *args, **kwargs):

        if not self.pk:
            #
            # If using something like Celery, then this should be scheduled, not
            # executed in the request/response cycle.
            #
            try:
                self.send_notification_email()
            except:
                #
                # This is just a precaution, should there be an issue with the
                # emailing, we do not want this to prevent the new Contact
                # object from being saved.
                #
                pass

        super(Contact, self).save(*args, **kwargs)


    def __unicode__(self):
        return '%s (%s)' % (self.name, str(self.contact_date), )


class ContactPluginModel(CMSPlugin):

    title = models.CharField(u'title',
        blank=True,
        help_text=u'Optional. Title of the widget.',
        max_length=64,
    )
