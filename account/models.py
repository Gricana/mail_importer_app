from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from .managers import AccountManager


cipher_suite = Fernet(settings.PASSWORD_KEY.encode())


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email', max_length=128, unique=True)
    password = models.BinaryField()
    last_login = None

    # For “simplicity” of logging into the admin panel
    is_staff = True
    is_active = True
    is_superuser = True

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        """
        Encrypts the raw password using the cipher suite and sets it as the account's password.

        Parameters:
        raw_password (str): The raw password to be encrypted.

        Returns:
        None
        """
        password = cipher_suite.encrypt(raw_password.encode())
        self.password = password

    def get_password(self):
        """
        Decrypts the account's password and returns it as a string.

        Returns:
        str: The decrypted password.
        """
        decrypted_password = cipher_suite.decrypt(self.password).decode()
        return decrypted_password

    def check_password(self, raw_password):
        """
        Decrypts the account's password and checks if it matches the raw password.

        Parameters:
        raw_password (str): The raw password to be checked.

        Returns:
        bool: True if the raw password matches the decrypted password, False otherwise.
        """
        decrypted_password = cipher_suite.decrypt(self.password).decode()
        return decrypted_password == raw_password

    def has_perm(self, perm, obj=None):
        """
        Checking for access rights
        (Optional functionality!) To simplify the development process
        """
        return True

    def has_module_perms(self, app_label):
        """
        Checking access rights to modules.
        (Optional functionality!) To simplify the development process
        """
        return True

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
