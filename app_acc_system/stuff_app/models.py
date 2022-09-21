from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        elif not password:
            raise ValueError('The given password must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields['role'] = 'admin'
        return self._create_user(username, password, **extra_fields)


class StuffUsers(AbstractBaseUser, PermissionsMixin):
    STATUSES = [('Active', 'Активный'), ('Archive', 'Архивный')]
    ROLES = [('admin', 'Администратор'), ('dispatcher', 'Диспетчер'), ('executor', 'Исполнитель')]

    username = models.CharField(verbose_name='Логин', max_length=255, unique=True, null=False, blank=False)
    password = models.CharField(verbose_name='Пароль', validators=[MinLengthValidator(8)],
                                max_length=255, unique=True, blank=False, null=False)
    first_name = models.CharField(verbose_name='Фамилия', max_length=255, null=True, blank=False)
    second_name = models.CharField(verbose_name='Имя', max_length=255, null=True, blank=False)
    last_name = models.CharField(verbose_name='Отчество', max_length=255, blank=True)
    role = models.CharField(verbose_name='Роль', choices=ROLES, max_length=10, null=False, blank=False)
    email = models.EmailField(verbose_name='Электронная почта', unique=True, null=True, blank=False)
    phone = PhoneNumberField(verbose_name='Номер телефона', null=True, blank=False, unique=True)
    status = models.CharField(verbose_name='Статус', choices=STATUSES, max_length=10, default='Active')
    created_at = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['-status']

    def get_full_name(self):
        return f"{self.first_name} {self.second_name}"

    def get_short_name(self):
        return f"{self.second_name}"

    @property
    def is_staff(self):
        return True if self.role == 'admin' else False

    @property
    def is_active(self):
        return True if self.status == 'Active' else False

    def __str__(self):
        return f"{self.get_full_name()}: {self.role}"
