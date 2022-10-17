import os

from django.db import models
from django.urls import reverse
from django.utils import dateformat
from django.utils.timezone import now
from django_unique_slugify import unique_slugify, slugify
from unidecode import unidecode


def get_comment_file_path(instance, filename):
    return f'Comment_files/{instance.application.subject}/{filename}'

# Удалить это после завершения проекта
def get_application_file_path(instance, filename):
    return f'Comment_files/{instance.application.subject}/{filename}'


def get_report_file_path(instance, filename):
    if instance.type == 'Client report':
        return f'Reports/Client reports/{instance.client.name}/{filename}'
    elif instance.type == 'Clients report':
        return f'Reports/Clients reports/{filename}'
    else:
        return f'Reports/Executors reports/{filename}'


class Reports(models.Model):
    TYPE_LIST = [
        ('Client report', 'Отчет о выполненных заявках по клиенту'),
        ('Clients report', 'Отчет о заявках клиентов'),
        ('Executors report', 'Отчет о выполненных заявках исполнителей')
    ]

    title = models.CharField(
        verbose_name='Название',
        max_length=255,
        blank=True
    )
    type = models.CharField(
        verbose_name='Тип',
        max_length=255,
        choices=TYPE_LIST
    )
    client = models.ForeignKey(
        verbose_name='Клиент',
        to='client_app.Clients',
        on_delete=models.CASCADE,
        related_name='reports',
        blank=True,
        null=True,
        help_text='Выберите клиента по которому хотите составить отчёт...'
    )
    file = models.FileField(
        verbose_name='Файл',
        upload_to=get_report_file_path
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отчёт'
        verbose_name_plural = 'Отчёты'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        cur_date = dateformat.format(now(), "d.b.Y H:i:s")
        if self.type == 'Client report':
            self.title = f'Отчет о выполненных заявках по клиенту {self.client.name} от {cur_date}'
        elif self.type == 'Clients report':
            self.title = f'Отчет о заявках клиентов от {cur_date}'
        else:
            self.title = f'Отчет о выполненных заявках исполнителей от {cur_date}'
        super(Reports, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        os.remove(self.file.path)
        super(Reports, self).delete(*args, **kwargs)

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return f'{self.title}'


class ApplicationComments(models.Model):
    application = models.ForeignKey(
        verbose_name='Заявка',
        to='Applications',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    comment_body = models.TextField(
        verbose_name='Комментарий',
        max_length=2000
    )
    is_private = models.BooleanField(
        verbose_name='Приватный',
        default=False
    )
    is_public = models.BooleanField(
        verbose_name='Публичный',
        default=True
    )
    file = models.FileField(
        verbose_name='Файл',
        upload_to=get_comment_file_path,
        blank=True
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий заявки'
        verbose_name_plural = 'Комментарии заявок'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.is_public:
            self.is_private = True
        super(ApplicationComments, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.file:
            os.remove(self.file.path)
        super(ApplicationComments, self).delete(*args, **kwargs)

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return f"comment #{self.pk}"


class Applications(models.Model):
    STATUS_LIST = [
        ('New', 'Новая'),
        ('At work', 'В работе'),
        ('Postponed', 'Отложена'),
        ('Solved', 'Решена'),
        ('Closed', 'Закрыта')
    ]

    PRIORITY_LIST = [
        ('Accident', 'Авария'),
        ('Urgent', 'Срочно'),
        ('Planned', 'Планово')
    ]

    TYPE_LIST = [
        ('Planned', 'Плановая'),
        ('Unplanned', 'Внеплановая')
    ]

    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=255
    )
    client = models.ForeignKey(
        verbose_name='Клиент',
        to='client_app.Clients',
        on_delete=models.CASCADE,
        related_name='applications',
        help_text='Выберите клиента...'
    )
    contact_person = models.ForeignKey(
        verbose_name='Котактное лицо',
        to='client_app.ContactPersons',
        on_delete=models.CASCADE,
        related_name='applications',
        help_text='Выберите котактное лицо...'
    )
    contract = models.ForeignKey(
        verbose_name='Договор',
        to='client_app.Contracts',
        on_delete=models.CASCADE,
        related_name='applications',
        help_text='Выберите договор...'
    )
    equipment = models.ManyToManyField(
        verbose_name='Оборудование',
        to='client_app.Equipments',
        related_name='applications',
        help_text='Выберите оборудование...'
    )
    subject = models.CharField(
        verbose_name='Тема',
        max_length=255,
        help_text='Введите тему зявки...'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        help_text='Введите описание заявки...'
    )
    priority = models.CharField(
        verbose_name='Приоритет',
        choices=PRIORITY_LIST,
        max_length=10,
        help_text='Выберите приоритет заявки...'
    )
    type = models.CharField(
        verbose_name='Тип',
        choices=TYPE_LIST,
        max_length=15,
        help_text='Выберите тип заявки...'
    )
    status = models.CharField(
        verbose_name='Статус',
        choices=STATUS_LIST,
        max_length=25,
        default='New',
        help_text='Выберите статус заявки...'
    )
    deadline = models.DateTimeField(
        verbose_name='Дедлайн',
        blank=True,
        null=True
    )
    closing_date = models.DateTimeField(
        verbose_name='Дата закрытия',
        blank=True,
        null=True
    )
    executor = models.ForeignKey(
        verbose_name='Исполнитель',
        to='stuff_app.StuffUsers',
        on_delete=models.PROTECT,
        related_name='applications',
        help_text='Выберите исполнителя...',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.pk:
            unique_slugify(self, slugify(unidecode(self.subject)))
        super(Applications, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('app_detail', kwargs={'app_slug': self.slug})

    def __str__(self):
        return f"{self.client}: {self.subject}"
