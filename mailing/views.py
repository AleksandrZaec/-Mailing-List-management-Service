from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import random

from blog.models import Blog
from mailing.forms import MailingForm, ClientForm, MessageForm, MailingModeratorForm
from mailing.models import Mailing, Client, Message, Logs
from mailing.services import get_cache_mailing_count, get_cache_mailing_active


class HomePageListView(ListView):
    model = Mailing
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mailings_count'] = get_cache_mailing_count()
        context_data['active_mailings_count'] = get_cache_mailing_active()
        context_data['clients_count'] = len(Client.objects.all())
        blog_list = list(Blog.objects.all())
        random.shuffle(blog_list)
        context_data['blog_list'] = blog_list[:3]
        return context_data


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing')

    def form_valid(self, form, *args, **kwargs):
        new_mailing = form.save(commit=False)
        new_mailing.owner = self.request.user
        new_mailing.save()
        return super().form_valid(form)


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'


class MailingUpdateView(PermissionRequiredMixin, UpdateView):
    model = Mailing
    permission_required = 'mailing.change_mailing'
    success_url = reverse_lazy('mailing:mailing')

    def get_form_class(self):
        if self.request.user == self.get_object().owner:
            return MailingForm
        elif self.request.user.has_perm('mailing.set_is_activated'):
            return MailingModeratorForm

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs["user"] = self.request.user
    #     return kwargs


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing')


class ClientListView(ListView):
    model = Client
    template_name = 'mailing/client_list.html'


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients')

    def form_valid(self, form, *args, **kwargs):
        new_client = form.save()
        new_client.owner = self.request.user
        new_client.save()
        return super().form_valid(form)


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailing/client_detail.html'


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:clients')


class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message_list.html'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:create')

    def form_valid(self, form, *args, **kwargs):
        new_message = form.save()
        new_message.owner = self.request.user
        new_message.save()
        return super().form_valid(form)


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message')


class LogsListView(ListView):
    model = Logs
    template_name = 'mailing/logs_list.html'