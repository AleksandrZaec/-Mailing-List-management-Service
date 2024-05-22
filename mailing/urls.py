from django.urls import path

from mailing.apps import MailConfig
from mailing.views import HomePageListView, MailingListView, MailingCreateView, ClientCreateView, ClientListView, \
    ClientDeleteView, MailingDetailView, MailingDeleteView, MailingUpdateView, ClientDetailView, ClientUpdateView, \
    MessageCreateView, LogsListView, MessageListView, MessageDetailView, MessageUpdateView, MessageDeleteView

app_name = MailConfig.name

urlpatterns = [
    path('', HomePageListView.as_view(), name='index'),

    path('mailing/', MailingListView.as_view(), name='mailing'),
    path('mailing/create/', MailingCreateView.as_view(), name='create'),
    path('mailing/view/<int:pk>/', MailingDetailView.as_view(), name='view'),
    path('mailing/edit/<int:pk>/', MailingUpdateView.as_view(), name='edit'),
    path('mailing/delete/<int:pk>/', MailingDeleteView.as_view(), name='delete'),

    path('clients/', ClientListView.as_view(), name='clients'),
    path('clients/create', ClientCreateView.as_view(), name='clients_create'),
    path('clients/view/<int:pk>/', ClientDetailView.as_view(), name='clients_view'),
    path('clients/edit/<int:pk>/', ClientUpdateView.as_view(), name='clients_edit'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='clients_delete'),

    path('message/', MessageListView.as_view(), name='message'),
    path('message/create', MessageCreateView.as_view(), name='message_create'),
    path('message/view/<int:pk>/', MessageDetailView.as_view(), name='message_view'),
    path('message/edit/<int:pk>/', MessageUpdateView.as_view(), name='message_edit'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    path('logs_list/', LogsListView.as_view(), name='logs_list'),
    ]