from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse

from .forms import AccountAuthForm


class AccountLoginView(LoginView):
    template_name = 'account/login.html'
    authentication_form = AccountAuthForm

    def get_success_url(self):
        return reverse('mails')


class AccountLogoutView(LogoutView):
    next_page = 'acc_login'
