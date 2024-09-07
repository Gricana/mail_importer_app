from django.contrib.auth.views import LoginView, LogoutView

from .forms import AccountAuthForm


class AccountLoginView(LoginView):
    """
    A Django view for handling user login.

    Attributes:
    template_name: The name of the HTML template to render for the login page.
    authentication_form: The form class to use for user authentication.
    next_page: The URL name to redirect to after successful login.
    """

    template_name = 'account/login.html'
    authentication_form = AccountAuthForm
    next_page = 'mails'


class AccountLogoutView(LogoutView):
    next_page = 'acc_login'
