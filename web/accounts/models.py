from django.db import models
from authtools.models import AbstractBaseUser, UserManager, PermissionsMixin


class UserManager(UserManager):

    def _make_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('You must enter an email')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self._make_user(email, password, **kwargs)

    def create_user(self, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._make_user(email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def get_short_name(self):
        return '{}'.format(self.email.split('@')[0])

    def get_full_name(self):
        return '{}'.format(self.email)

    def __str__(self):
        return self.get_short_name()
