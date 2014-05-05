# -*- coding: utf-8 -*-

from django.contrib import admin

from adminsortable.admin import SortableAdmin, SortableTabularInline
from cms.admin.placeholderadmin import PlaceholderAdminMixin
from easy_select2 import select2_modelform
from project.apps.clippings.models import Clipping
from .models import Seniority, StaffMember


class SeniorityAdmin(admin.ModelAdmin):
	pass

admin.site.register(Seniority, SeniorityAdmin)


class ClippingInline(SortableTabularInline):    
    extra = 1
    form = select2_modelform(Clipping, attrs={'width': '250px'})
    model = Clipping


class StaffMemberAdmin(PlaceholderAdminMixin, SortableAdmin):
	form = select2_modelform(StaffMember, attrs={'width': '250px'})
	inlines = [ ClippingInline, ]

admin.site.register(StaffMember, StaffMemberAdmin)