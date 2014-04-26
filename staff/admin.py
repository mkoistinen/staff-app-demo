# -*- coding: utf-8 -*-

from django.contrib import admin
from cms.admin.placeholderadmin import PlaceholderAdminMixin

from .models import Seniority, StaffMember


class SeniorityAdmin(admin.ModelAdmin):
	pass

admin.site.register(Seniority, SeniorityAdmin)


class StaffMemberAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    pass

admin.site.register(StaffMember, StaffMemberAdmin)