import os

from django.db import models
from django.urls import reverse
from django_unique_slugify import unique_slugify, slugify
from unidecode import unidecode


def get_application_file_path(instance, filename):
    return f'Application_files/{instance.client.name}/{instance.subject}/{filename}'


def get_comment_file_path(instance, filename):
    return f'Comment_files/{instance.comment.application.subject}/{filename}'


class ApplicationFiles(models.Model):
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=255
    )
    application = models.ForeignKey(
        verbose_name='Заявка',
        to='Applications',
        on_delete=models.CASCADE,
        related_name='files',
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=255,
        help_text='Введите название файла...'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        help_text='Введите описание файла...'
    )
    file = models.FileField(
        verbose_name='Файл',
        upload_to=get_application_file_path,
    )

    class Meta:
        verbose_name = 'Файл заявки'
        verbose_name_plural = 'Файлы заявок'
        ordering = ['-application']

    def save(self, *args, **kwargs):
        if not self.pk:
            unique_slugify(self, slugify(unidecode(self.title)))
        super(ApplicationFiles, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        os.remove(self.file.path)
        super(ApplicationFiles, self).delete(*args, **kwargs)

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return f"{self.application}: {self.title}"


class CommentsFiles(models.Model):
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=255
    )
    comment = models.ForeignKey(
        verbose_name='Комментарий',
        to='ApplicationComments',
        on_delete=models.CASCADE,
        related_name='files'
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=255,
        help_text='Введите название файла...'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        help_text='Введите описание файла...'
    )
    file = models.FileField(
        verbose_name='Файл',
        upload_to=get_comment_file_path
    )

    class Meta:
        verbose_name = 'Файл комментария'
        verbose_name_plural = 'Файлы комментариев'
        ordering = ['-comment']

    def save(self, *args, **kwargs):
        if not self.pk:
            unique_slugify(self, slugify(unidecode(self.title)))
        super(CommentsFiles, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        os.remove(self.file.path)
        super(CommentsFiles, self).delete(*args, **kwargs)

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return f"{self.comment}: {self.title}"


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

    def __str__(self):
        return f"{self.application}: comment #{self.pk}"


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
