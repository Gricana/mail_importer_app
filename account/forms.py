from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

from .models import Account


class AccountAuthForm(AuthenticationForm):
    username = forms.EmailField(label='Email', max_length=128,
                                widget=forms.EmailInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Введите email'
                                }))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Введите пароль'
                               }))

    def clean(self):
        """
        The overridden method is responsible for processing the creation of a new Account
        and its authentication

        Parameters:
        self (AccountAuthForm): The instance of the form being cleaned.

        Returns:
        dict: The cleaned and validated form data.
        """
        email = self.cleaned_data['username']
        password = self.cleaned_data['password']
        email_account, created = Account.objects.get_or_create(email=email)

        if created:
            email_account.set_password(password)
            email_account.save()

        self.user_cache = authenticate(self.request, username=email, password=password)
        if self.user_cache is not None:
            self.confirm_login_allowed(self.user_cache)
        else:
            raise self.get_invalid_login_error()

        return self.cleaned_data
