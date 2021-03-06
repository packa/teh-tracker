# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django import forms
from tracker import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils import simplejson
from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.template import RequestContext
from django.template.loader import get_template

class MediaInfoAdmin(admin.TabularInline):
    model = models.MediaInfo

class ExpeditureAdmin(admin.TabularInline):
    model = models.Expediture

class AddAckForm(forms.Form):
    ack_type = forms.ChoiceField(choices=models.ACK_TYPES, label=_('Type'))
    comment = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'size':'40'}))

class TicketAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(TicketAdmin, self).queryset(request)
        if request.user.has_perm('tracker.supervisor'):
            return qs
        else:
            return qs.extra(where=['topic_id in (select topic_id from tracker_topic_admin where user_id = %s)'], params=[request.user.id])
    
    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        ticket = self.get_object(request, object_id)
        extra_context['user_can_edit_documents'] = ticket.can_edit_documents(request.user)
        extra_context['user_can_see_documents'] = ticket.can_see_documents(request.user)
        extra_context['add_ack_form'] = AddAckForm()
        return super(TicketAdmin, self).change_view(request, object_id, extra_context=extra_context)
    
    exclude = ('updated', 'sort_date', 'cluster')
    readonly_fields = ('state_str', 'payment_status', 'requested_user_details')
    list_display = ('sort_date', 'id', 'summary', 'topic', 'requested_by', 'state_str', 'payment_status')
    list_display_links = ('summary',)
    list_filter = ('topic', 'payment_status')
    date_hierarchy = 'sort_date'
    search_fields = ['id', 'requested_user__username', 'requested_text', 'summary']
    inlines = [MediaInfoAdmin, ExpeditureAdmin]
    
    @staticmethod
    def _render(request, template_name, context_data):
        c = RequestContext(request, context_data)
        return get_template(template_name).render(c)
    
    def add_ack(self, request, object_id):
        ticket = models.Ticket.objects.get(id=object_id)
        if (request.method == 'POST'):
            form = AddAckForm(request.POST)
            if form.is_valid():
                ack = ticket.ticketack_set.create(ack_type=form.cleaned_data['ack_type'], added_by=request.user, comment=form.cleaned_data['comment'])
                return HttpResponse(simplejson.dumps({
                    'form':self._render(request, 'admin/tracker/ticket/ack_line.html', {'ack':ack}),
                    'id':ack.id,
                    'success':True,
                }))
        else:
            form = AddAckForm()
        form_html = self._render(request, 'admin/tracker/ticket/add_ack.html', {'form':form})
        return HttpResponse(simplejson.dumps({'form':form_html}))
    
    def remove_ack(self, request, object_id):
        ticket = models.Ticket.objects.get(id=object_id)
        if (request.method != 'POST'):
            return HttpResponseNotAllowed(['POST'])
        try:
            ack = ticket.ticketack_set.get(id=request.POST.get('id', None))
        except models.TicketAck.DoesNotExist:
            raise Http404
        ack.delete()
        return HttpResponse(simplejson.dumps({
            'success':True,
        }))
    
    def get_urls(self):
        return patterns('',
            url(r'^(?P<object_id>\d+)/acks/add/$', self.add_ack),
            url(r'^(?P<object_id>\d+)/acks/remove/$', self.remove_ack),
        ) + super(TicketAdmin, self).get_urls()
admin.site.register(models.Ticket, TicketAdmin)

class TopicAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if request.user.has_perm('tracker.supervisor'):
            return ()
        else:
            return ('admin', 'grant')
    
    def queryset(self, request):
        if request.user.has_perm('tracker.supervisor'):
            return super(TopicAdmin, self).queryset(request)
        else:
            return request.user.topic_set.all()
    
    list_display = ('name', 'grant', 'open_for_tickets', 'ticket_media', 'ticket_expenses')
    list_filter = ('grant', )
    filter_horizontal = ('admin', )
admin.site.register(models.Topic, TopicAdmin)

class GrantAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('short_name',)}
admin.site.register(models.Grant, GrantAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'other_party', 'amount', 'description', 'ticket_ids', 'accounting_info')
    list_display_links = ('amount', 'description')
    filter_vertical = ('tickets', )
    exclude = ('cluster', )
admin.site.register(models.Transaction, TransactionAdmin)

# piggypatch admin site to display our own index template with some bonus links
admin.site.index_template = 'tracker/admin_index_override.html'
