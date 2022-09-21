from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# class ClientFiles(models.Model):
#     client = models.ForeignKey()
#     title = models.CharField()
#     description = models.TextField()
#     file = models.FileField()
#
#     class Meta:
#         verbose_name = 'Файл клиента'
#         verbose_name_plural = 'Файлы клиентов'
#         ordering = ['']
#
#     def __str__(self):
#         return f""
#
#
# class ContractFiles(models.Model):
#     contract = models.ForeignKey()
#     title = models.CharField()
#     description = models.TextField()
#     file = models.FileField()
#
#     class Meta:
#         verbose_name = 'Файл контракта'
#         verbose_name_plural = 'Файлы контрактов'
#         ordering = ['']
#
#     def __str__(self):
#         return f""
#
#
# class EquipmentFiles(models.Model):
#     equipment = models.ForeignKey()
#     title = models.CharField()
#     description = models.TextField()
#     file = models.FileField()
#
#     class Meta:
#         verbose_name = 'Файл оборудования'
#         verbose_name_plural = 'Файлы оборудований'
#         ordering = ['']
#
#     def __str__(self):
#         return f""
#
#
# class ContactPersons(models.Model):
#     client = models.ForeignKey()
#     first_name = models.CharField()
#     second_name = models.CharField()
#     last_name = models.CharField()
#     post = models.CharField()
#     email = models.EmailField()
#     phone = PhoneNumberField()
#     note = models.TextField()
#
#     class Meta:
#         verbose_name = 'Контактное лицо'
#         verbose_name_plural = 'Контактные лица'
#         ordering = ['']
#
#     def __str__(self):
#         return f""
#
#
# class EquipmentType(models.Model):
#     code = models.PositiveSmallIntegerField()
#     name = models.CharField()
#
#     class Meta:
#         verbose_name = 'Тип оборудования'
#         verbose_name_plural = 'Типы оборудований'
#         ordering = ['']
#
#     def __str__(self):
#         return f""
#
#
# class EquipmentAttribute(models.Model):
#     code = models.PositiveSmallIntegerField()
#     name = models.CharField()
#     type_e = models.ForeignKey()
#     type_a = models.CharField(choices=['Строка', 'Дата', 'Множественный выбор', 'Единичный выбор'])
#
#     class Meta:
#         verbose_name = 'Атрибут оборудования'
#         verbose_name_plural = 'Атрибуты оборудований'
#         ordering = ['']
#
#     def __str__(self):
#         return f""
#
#
# class Equipments(models.Model):
#     client = models.ForeignKey()
#     name = models.CharField()
#     type = models.ForeignKey()
#     attribute = models.ManyToManyField()
#     note = models.TextField()
#
#     class Meta:
#         verbose_name = 'Оборудование'
#         verbose_name_plural = 'Оборудования'
#         ordering = ['']
#
#     def __str__(self):
#         return f""
#
#
# class Contracts(models.Model):
#     client = models.ForeignKey()
#     title = models.CharField()
#     price = models.PositiveBigIntegerField()
#     created_at = models.DateTimeField()
#     date_end = models.DateTimeField()
#     note = models.TextField()
#
#     class Meta:
#         verbose_name = 'Контракт клиента'
#         verbose_name_plural = 'Контракты клиентов'
#         ordering = ['']
#
#     def __str__(self):
#         return f""
#
#
# class Clients(models.Model):
#     name = models.CharField()
#     second_name = models.CharField()
#     site = models.CharField()
#     email = models.EmailField()
#     phone = PhoneNumberField()
#     office_address = models.CharField()
#     legal_address = models.CharField()
#     inn = models.IntegerField(max_length=10)
#     kpp = models.IntegerField(max_length=9)
#     ogrn = models.IntegerField(max_length=13)
#     note = models.TextField()
#
#     class Meta:
#         verbose_name = 'Клиент'
#         verbose_name_plural = 'Клиенты'
#         ordering = ['']
#
#     def __str__(self):
#         return f"{self.name} - {self.second_name}"
