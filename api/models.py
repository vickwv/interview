from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from api.helper import generate_random_string


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **kwargs):
        if not password:
            raise ValueError("请传入密码！")
        if not email:
            raise ValueError("请传入邮箱地址！")
        user = self.model(nickname="面试者" + generate_random_string(10), email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs['is_superuser'] = True
        return self._create_user(email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    nickname = models.CharField(max_length=20, verbose_name="昵称")
    email = models.CharField(max_length=64, unique=True, verbose_name="邮箱")
    password = models.CharField(max_length=128, verbose_name="密码")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="创建时间", blank=True)
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="更新时间", blank=True)

    class Meta:
        db_table = 'user'
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.nickname

    def get_short_name(self):
        return self.nickname

