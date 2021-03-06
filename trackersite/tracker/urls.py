# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView, RedirectView

from tracker.models import Ticket, Topic, Grant
from tracker.feeds import LatestTicketsFeed, TopicTicketsFeed, TransactionsFeed

urlpatterns = patterns('',
    url(r'^tickets/$', ListView.as_view(model=Ticket), name='ticket_list'),
    url(r'^tickets/feed/$', LatestTicketsFeed(), name='ticket_list_feed'),
    url(r'^ticket/(?P<pk>\d+)/$', 'tracker.views.ticket_detail', name='ticket_detail'),
    url(r'^ticket/(?P<pk>\d+)/edit/$', 'tracker.views.edit_ticket', name='edit_ticket'),
    url(r'^ticket/(?P<pk>\d+)/edit/docs/$', 'tracker.views.edit_ticket_docs', name='edit_ticket_docs'),
    url(r'^ticket/(?P<pk>\d+)/edit/docs/new/$', 'tracker.views.upload_ticket_doc', name='upload_ticket_doc'),
    url(r'^ticket/(?P<pk>\d+)/edit/acks/(?P<ack_id>\d+)/delete/$', 'tracker.views.ticket_ack_delete', name='ticket_ack_delete'),
    url(r'^ticket/(?P<ticket_id>\d+)/docs/(?P<filename>[-_\.A-Za-z0-9]+\.[A-Za-z0-9]+)$', 'tracker.views.download_document', name='download_document'),
    url(r'^ticket/new/$', 'tracker.views.create_ticket', name='create_ticket'),
    url(r'^topics/$', ListView.as_view(model=Topic), name='topic_list'),
    url(r'^topics/finance/$', 'tracker.views.topic_finance', name='topic_finance'),
    url(r'^topic/(?P<pk>\d+)/$', 'tracker.views.topic_detail', name='topic_detail'),
    url(r'^topic/(?P<pk>\d+)/feed/$', TopicTicketsFeed(), name='topic_ticket_feed'),
    url(r'^grant/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Grant), name='grant_detail'),
    url(r'^users/$', 'tracker.views.user_list', name='user_list'),
    url(r'^users/(?P<username>[^/]+)/$', 'tracker.views.user_detail', name='user_detail'),
    url(r'^my/details/$', 'tracker.views.user_details_change', name='user_details_change'),
    url(r'^transactions/$', 'tracker.views.transaction_list', name='transaction_list'),
    url(r'^transactions/feed/$', TransactionsFeed(), name='transactions_feed'),
    url(r'^transactions/transactions\.csv$', 'tracker.views.transactions_csv', name='transactions_csv'),
    url(r'^cluster/(?P<pk>\d+)/$', 'tracker.views.cluster_detail', name='cluster_detail'),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^old/(?P<url>(?:tickets?/|topics?/|)(?:\d+/|new/)?)$', RedirectView.as_view(url='/%(url)s')),
    url(r'^js/topics\.js$', 'tracker.views.topics_js', name='topics_js'),
    url(r'^admin/users/$', 'tracker.views.admin_user_list', name='admin_user_list'),
)
