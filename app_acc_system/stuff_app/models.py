from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse_lazy
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

    username = models.CharField(verbose_name='Логин', max_length=255, unique=True, blank=False)
    password = models.CharField(verbose_name='Пароль', validators=[MinLengthValidator(8)],
                                max_length=255, unique=True, blank=False)
    first_name = models.CharField(verbose_name='Фамилия', max_length=255, blank=False)
    second_name = models.CharField(verbose_name='Имя', max_length=255, blank=False)
    last_name = models.CharField(verbose_name='Отчество', max_length=255, blank=True)
    role = models.CharField(verbose_name='Роль', choices=ROLES, max_length=10, blank=False)
    email = models.EmailField(verbose_name='Электронная почта', unique=True, null=True, blank=False)
    phone = PhoneNumberField(verbose_name='Номер телефона', region='RU', null=True, blank=False, unique=True)
    status = models.CharField(verbose_name='Статус', choices=STATUSES, max_length=10, default='Active')
    created_at = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)
    is_active = models.BooleanField(default=True)
    notifications_active = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['-status']

    def get_absolute_url(self):
        return reverse_lazy('stuff_detail', kwargs={'username': self.username})

    def get_full_name(self):
        if self.last_name:
            return f"{self.first_name} {self.second_name} {self.last_name}"
        return f"{self.first_name} {self.second_name}"

    def get_short_name(self):
        return f"{self.second_name}"

    @property
    def is_staff(self):
        return True if self.role == 'admin' else False

    def is_archive(self):
        return True if self.status == 'Archive' else False

    def __str__(self):
        return f"{self.username}: {self.role}"


class StuffUsersNotifications(models.Model):
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=StuffUsers,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notify_subject = models.CharField(
        verbose_name='Тема',
        max_length=255
    )
    notify_text = models.TextField(
        verbose_name='Содержание'
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Уведомление пользователя'
        verbose_name_plural = 'Уведомления пользователей'
        ordering = ['-user']

    def __str__(self):
        return f'Notify #{self.pk}'
