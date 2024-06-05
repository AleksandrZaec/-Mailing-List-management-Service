from django.views.decorators.cache import cache_page
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

    def dispatch(self, *args, **kwargs):
        # Кэшировать результат представления на 15 минут
        return cache_page(60 * 15)(super().dispatch)(*args, **kwargs)

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
    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing')

    def form_valid(self, form, *args, **kwargs):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingUpdateView(PermissionRequiredMixin, UpdateView):
    model = Mailing
    permission_required = 'mailing.change_mailing'
    success_url = reverse_lazy('mailing:mailing')

    def get_form_class(self):
        if self.request.user == self.get_object().owner:
            return MailingForm
        elif self.request.user.has_perm('mailing.set_is_activated'):
            return MailingModeratorForm

    def get_queryset(self):
        if self.request.user.has_perm('mailing.set_is_activated'):
            return Mailing.objects.all()  # Пользователь с разрешением set_is_activated имеет доступ ко всем рассылкам
        else:
            return Mailing.objects.filter(owner=self.request.user)  # Остальные пользователи могут видеть только свои рассылки
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs["user"] = self.request.user
    #     return kwargs


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing')
    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)

class ClientListView(ListView):
    model = Client
    template_name = 'mailing/client_list.html'
    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients')
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailing/client_detail.html'
    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients')
    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)

class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:clients')
    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)

class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    def get_queryset(self):
        # Фильтруем сообщения по владельцу (текущему пользователю)
        return Message.objects.filter(owner=self.request.user)


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:create')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'



class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message')
    def test_func(self):
        # Проверяем, что пользователь является владельцем сообщения
        message = self.get_object()
        return self.request.user == message.owner


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message')

    def test_func(self):
        # Проверяем, что пользователь является владельцем сообщения
        message = self.get_object()
        return self.request.user == message.owner


class LogsListView(ListView):
    model = Logs
    template_name = 'mailing/logs_list.html'

    def get_queryset(self):
        # Фильтруем журналы по владельцу
        return Logs.objects.filter(mailing__owner=self.request.user)