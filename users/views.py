from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save()
        token = get_random_string(length=10)
        new_user.verification_token = token
        new_user.save()
        current_site = get_current_site(self.request)

        send_mail(
            subject='Подтверждение аккаунта',
            message=f'Поздравляем, Вы зарегистрировались на нашем портале!\n'
            f'Для завершения регистрации и подтверждения вашей электронной почты, '
            f'пожалуйста, кликните по следующей ссылке:\n'
            f'http://{current_site.domain}{reverse("users:verify_email", kwargs={"uid": new_user.pk, "token": token})}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )

        return super().form_valid(form)


class VerifyEmailView(View):
    def get(self, request, uid, token):
        try:
            user = get_object_or_404(User, pk=uid, verification_token=token)
            user.is_active = True
            user.save()
            return render(request, 'users/register_success.html')  # Покажем сообщение о регистрации
        except User.DoesNotExist:
            return render(request, 'users/register_failed.html')  # Покажем сообщение об ошибке


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(LoginRequiredMixin, ListView):
    model = User
    extra_context = {'title': 'Пользователи',}

    # def test_func(self):
    #     _user = self.request.user
    #     if _user.has_perms(['users.set_is_active',]):
    #         return True
    #     return self.handle_no_permission()