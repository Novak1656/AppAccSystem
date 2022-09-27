from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_unique_slugify import unique_slugify, slugify
from unidecode import unidecode


def user_files_directory_path(instance, filename):
    return f'User_files/{instance.client.username}/{filename}'


def contract_files_directory_path(instance, filename):
    return f'Contract_files/{instance.contract.title}/{filename}'


def equipment_files_directory_path(instance, filename):
    return f'Equipment_files/{instance.equipment.title}/{filename}'


class ClientFiles(models.Model):
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=255
    )
    client = models.ForeignKey(
        verbose_name='Клиент',
        to='Clients',
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
        help_text='Введите описание файла...'
    )
    file = models.FileField(
        verbose_name='Файл',
        upload_to=user_files_directory_path
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлен',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Файл клиента'
        verbose_name_plural = 'Файлы клиентов'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.pk:
            unique_slugify(self, slugify(unidecode(self.title)))
        super(ClientFiles, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.slug}"


class ContractFiles(models.Model):
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=255
    )
    contract = models.ForeignKey(
        verbose_name='Контракт',
        to='Contracts',
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
        help_text='Введите описание файла...'
    )
    file = models.FileField(
        verbose_name='Файл',
        upload_to=contract_files_directory_path
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлен',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Файл контракта'
        verbose_name_plural = 'Файлы контрактов'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.pk:
            unique_slugify(self, slugify(unidecode(self.title)))
        super(ContractFiles, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.slug}"


class EquipmentFiles(models.Model):
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=255
    )
    equipment = models.ForeignKey(
        verbose_name='Оборудование',
        to='Equipments',
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
        help_text='Введите описание файла...'
    )
    file = models.FileField(
        verbose_name='Файл',
        upload_to=equipment_files_directory_path
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлен',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Файл оборудования'
        verbose_name_plural = 'Файлы оборудований'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.pk:
            unique_slugify(self, slugify(unidecode(self.title)))
        super(EquipmentFiles, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.slug}"


class ContactPersons(models.Model):
    client = models.ForeignKey(
        verbose_name='Клиент',
        to='Clients',
        on_delete=models.CASCADE,
        related_name='contact_persons'
    )
    first_name = models.CharField(
        verbose_name='Фамилия',
        max_length=255,
        help_text='Введите фамилию лица...',
    )
    second_name = models.CharField(
        verbose_name='Имя',
        max_length=255,
        help_text='Введите имя лица...',
    )
    last_name = models.CharField(
        verbose_name='Отчество',
        max_length=255,
        help_text='Введите отчество лица...',
        blank=True
    )
    post = models.CharField(
        verbose_name='Должность',
        max_length=255,
        help_text='Введите должность лица...',
    )
    email = models.EmailField(
        verbose_name='Email',
        help_text='Введите email адрес лица...',
        unique=True
    )
    phone = PhoneNumberField(
        verbose_name='Номер телефона',
        region='RU',
        unique=True
    )
    note = models.TextField(
        verbose_name='Заметки',
        help_text='Введите заметки по контактному лицу...',
        blank=True
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлен',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Обновлён',
        auto_now=True
    )

    class Meta:
        verbose_name = 'Контактное лицо'
        verbose_name_plural = 'Контактные лица'
        ordering = ['-created_at']

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.second_name} {self.last_name}"

    def __str__(self):
        return self.get_full_name


class EquipmentType(models.Model):
    code = models.PositiveSmallIntegerField(
        verbose_name='Код',
        help_text='Введите код типа...',
        unique=True
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=255,
        help_text='Введите название типа...',
        unique=True
    )

    class Meta:
        verbose_name = 'Тип оборудования'
        verbose_name_plural = 'Типы оборудований'
        ordering = ['-name']

    def __str__(self):
        return f"{self.name}"


class EquipmentAttribute(models.Model):
    ATTRS_TYPES = [
        ('string_attr', 'Строка'),
        ('date_attr', 'Дата'),
        ('many_attrs', 'Множественный выбор'),
        ('solo_attr', 'Единичный выбор')
    ]

    code = models.PositiveSmallIntegerField(
        verbose_name='Код',
        help_text='Введите код атрибута...',
        unique=True
    )
    name = models.CharField(
        verbose_name='Название',
        help_text='Введите название атрибута...',
        max_length=255,
        unique=True
    )
    type_e = models.ManyToManyField(
        verbose_name='Типы оборудования',
        to=EquipmentType,
        related_name='equipment_attrs'
    )
    type_a = models.CharField(
        verbose_name='Тип атрибута',
        choices=ATTRS_TYPES,
        max_length=25
    )

    class Meta:
        verbose_name = 'Атрибут оборудования'
        verbose_name_plural = 'Атрибуты оборудований'
        ordering = ['-name']

    def __str__(self):
        return f"{self.name}"


class Equipments(models.Model):
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=255
    )
    client = models.ForeignKey(
        verbose_name='Клиент',
        to='Clients',
        on_delete=models.CASCADE,
        related_name='equipments'
    )
    name = models.CharField(
        verbose_name='Название',
        help_text='Введите название оборудования...',
        max_length=255,
    )
    type = models.ForeignKey(
        verbose_name='Тип',
        to=EquipmentType,
        on_delete=models.PROTECT,
        related_name='equipments'
    )
    attribute = models.ManyToManyField(
        verbose_name='Атрибуты',
        to=EquipmentAttribute,
        related_name='equipments'
    )
    note = models.TextField(
        verbose_name='Заметки',
        blank=True
    )

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудования'
        ordering = ['-name']

    def save(self, *args, **kwargs):
        if not self.pk:
            unique_slugify(self, slugify(unidecode(self.name)))
        super(Equipments, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.slug}"


class Contracts(models.Model):
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=255
    )
    client = models.ForeignKey(
        verbose_name='Клиент',
        to='Clients',
        on_delete=models.CASCADE,
        related_name='contracts'
    )
    title = models.CharField(
        verbose_name='Название',
        help_text='Введите название контракта...',
        max_length=255,
    )
    price = models.PositiveBigIntegerField(
        verbose_name='Цена',
        help_text='Введите цену контракта...',
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания контракта',
        auto_now_add=True
    )
    is_end = models.BooleanField(
        verbose_name='Контракт закрыт',
        default=False
    )
    date_end = models.DateTimeField(
        verbose_name='Дата закрытия контракта',
        null=True,
        blank=True
    )
    note = models.TextField(
        verbose_name='Заметки',
        blank=True
    )

    class Meta:
        verbose_name = 'Контракт клиента'
        verbose_name_plural = 'Контракты клиентов'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.pk:
            unique_slugify(self, slugify(unidecode(self.title)))
        super(Contracts, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.slug}"


class Clients(models.Model):
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=255
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=255,
        help_text='Введите название клиента...',
    )
    second_name = models.CharField(
        verbose_name='Дополнительное название',
        max_length=255,
        help_text='Введите дополнительное название клиента...',
        blank=True
    )
    site = models.CharField(
        verbose_name='Адрес сайта',
        max_length=255,
        help_text='Введите адрес сайта клиента...',
        blank=True
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        help_text='Введите адрес электронной почты клиента...',
        unique=True
    )
    phone = PhoneNumberField(
        verbose_name='Номер телефона',
        region='RU',
        unique=True,
        help_text='Введите номер телефона клиента...',
    )
    office_address = models.CharField(
        verbose_name='Адрес офиса',
        max_length=255,
        help_text='Введите адрес офиса клиента...',
    )
    legal_address = models.CharField(
        verbose_name='Юридический адрес',
        max_length=255,
        help_text='Введите юридический адрес клиента...',
    )
    inn = models.CharField(
        verbose_name='ИНН',
        unique=True,
        max_length=10,
        help_text='Пример: 0000000000',
    )
    kpp = models.CharField(
        verbose_name='КПП',
        unique=True,
        max_length=9,
        help_text='Пример: 000000000',
    )
    ogrn = models.CharField(
        verbose_name='ОГРН',
        unique=True,
        max_length=13,
        help_text='Пример: 0000000000000',
    )
    note = models.TextField(
        verbose_name='Заметки',
        help_text='Введите заметки по клиенту...',
        blank=True
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлен',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.pk:
            unique_slugify(self, slugify(unidecode(self.name)))
        super(Clients, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.slug}"
