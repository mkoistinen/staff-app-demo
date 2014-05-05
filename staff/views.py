# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView

from .models import StaffMember


class StaffListView(ListView):
    model = StaffMember
    queryset = StaffMember.objects.order_by('order').all()

    def render_to_response(self, context, **response_kwargs):
        # Shim to affect the CMS Toolbar only
        if self.request.toolbar and self.request.toolbar.edit_mode:
            menu = self.request.toolbar.get_or_create_menu('staff-list-menu', 'Leadership')
            menu.add_sideframe_item(u'Seniority List', url=reverse('admin:staff_seniority_changelist'))
            menu.add_modal_item('Add new Seniority', url="%s" % (reverse('admin:staff_seniority_add'), ))
            menu.add_break()
            menu.add_sideframe_item(u'Staff List', url=reverse('admin:staff_staffmember_changelist'))
            menu.add_modal_item('Add new Staff Member', url="%s" % (reverse('admin:staff_staffmember_add'), ))

        return super(StaffListView, self).render_to_response(context, **response_kwargs)


class StaffDetailView(DetailView):
    model = StaffMember
    context_object_name = 'staff'

    def render_to_response(self, context, **response_kwargs):
        # Shim to affect the CMS Toolbar only
        if self.request.toolbar and self.request.toolbar.edit_mode:
            menu = self.request.toolbar.get_or_create_menu('staff-member-menu', self.object.full_name)
            menu.add_modal_item('Edit %s' % self.object.full_name, url=reverse('admin:staff_staffmember_change', args=[self.object.id]), )

            menu.add_break()

            # Ho hum...
            # menu.add_modal_item('Attach New Clipping',
            #     url="%s" % (reverse('admin:clippings_clipping_add'), )
            # )

            # Coolness...
            menu.add_modal_item('Attach New Clipping',
                url="%s?staff=%d" % (
                    reverse('admin:clippings_clipping_add'),
                    self.object.id,
                )
            )


        return super(StaffDetailView, self).render_to_response(context, **response_kwargs)
