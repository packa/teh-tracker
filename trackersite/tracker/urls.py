# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView, DetailView, RedirectView

from tracker.models import Ticket, Topic

urlpatterns = patterns('',
    url(r'^tickets/$', ListView.as_view(model=Ticket), name='ticket_list'),
    url(r'^ticket/(?P<pk>\d+)/$', 'tracker.views.ticket_detail', name='ticket_detail'),
    url(r'^ticket/(?P<pk>\d+)/edit/$', 'tracker.views.edit_ticket', name='edit_ticket'),
    url(r'^ticket/new/$', 'tracker.views.create_ticket', name='create_ticket'),
    url(r'^topics/$', ListView.as_view(model=Topic), name='topic_list'),
    url(r'^topic/(?P<pk>\d+)/$', DetailView.as_view(model=Topic), name='topic_detail'),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^old/(?P<url>(?:tickets?/|topics?/|)(?:\d+/|new/)?)$', RedirectView.as_view(url='/%(url)s')),
)
