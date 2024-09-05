from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):

    def create_user(self, email, password=None):
        """
        Создает и возвращает обычного пользователя с указанным email и паролем.
        """
        if not email:
            raise ValueError('Пользователь должен иметь адрес электронной почты')

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Создает и возвращает суперпользователя с указанным email и паролем.
        """
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):
        """
        Метод для поиска пользователя по естественному ключу (email).
        """
        return self.get(email=email)
