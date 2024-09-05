from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from .managers import AccountManager


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email', max_length=128, unique=True)
    last_login = None

    # Для "простоты" входа в админку
    is_staff = True
    is_admin = True
    is_superuser = True

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Проверка наличия прав доступа"""
        return True

    def has_module_perms(self, app_label):
        """Проверка прав доступа к модулям"""
        return True

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
