from django.test import TestCase
from ..models import ClientFiles, ContractFiles, EquipmentFiles, Clients


class ClientFilesModelTestCase(TestCase):
    def test_slug_field(self):
        field_meta = ClientFiles._meta.get_field('slug')
        self.assertEqual(field_meta.verbose_name, 'Слаг')
        self.assertEqual(field_meta.max_length, 255)

    def test_client_field(self):
        field_meta = ClientFiles._meta.get_field('client')
        self.assertEqual(field_meta.verbose_name, 'Клиент')
        self.assertFalse(field_meta.blank)

    def test_title_field(self):
        field_meta = ClientFiles._meta.get_field('title')
        self.assertEqual(field_meta.verbose_name, 'Название')
        self.assertEqual(field_meta.max_length, 255)
        self.assertEqual(field_meta.help_text, 'Введите название файла...')
        self.assertFalse(field_meta.blank)

    def test_description_field(self):
        field_meta = ClientFiles._meta.get_field('description')
        self.assertEqual(field_meta.verbose_name, 'Описание')
        self.assertEqual(field_meta.help_text, 'Введите описание файла...')
        self.assertFalse(field_meta.blank)

    def test_file_field(self):
        field_meta = ClientFiles._meta.get_field('file')
        self.assertEqual(field_meta.verbose_name, 'Файл')
        self.assertFalse(field_meta.blank)

    def test_created_at_field(self):
        field_meta = ClientFiles._meta.get_field('created_at')
        self.assertEqual(field_meta.verbose_name, 'Добавлен')
        self.assertTrue(field_meta.auto_now_add)

    def test_model_meta(self):
        model_meta = ClientFiles._meta
        self.assertEqual(model_meta.verbose_name, 'Файл клиента')
        self.assertEqual(model_meta.verbose_name_plural, 'Файлы клиентов')
        self.assertIn('-created_at', model_meta.ordering)

    def test_model_str(self):
        pass


class ContractFilesModelTestCase(TestCase):
    def test_slug_field(self):
        field_meta = ContractFiles._meta.get_field('slug')
        self.assertEqual(field_meta.verbose_name, 'Слаг')
        self.assertEqual(field_meta.max_length, 255)

    def test_contract_field(self):
        field_meta = ContractFiles._meta.get_field('contract')
        self.assertEqual(field_meta.verbose_name, 'Контракт')
        self.assertFalse(field_meta.blank)

    def test_title_field(self):
        field_meta = ContractFiles._meta.get_field('title')
        self.assertEqual(field_meta.verbose_name, 'Название')
        self.assertEqual(field_meta.max_length, 255)
        self.assertEqual(field_meta.help_text, 'Введите название файла...')
        self.assertFalse(field_meta.blank)

    def test_description_field(self):
        field_meta = ContractFiles._meta.get_field('description')
        self.assertEqual(field_meta.verbose_name, 'Описание')
        self.assertEqual(field_meta.help_text, 'Введите описание файла...')
        self.assertFalse(field_meta.blank)

    def test_file_field(self):
        field_meta = ContractFiles._meta.get_field('file')
        self.assertEqual(field_meta.verbose_name, 'Файл')
        self.assertFalse(field_meta.blank)

    def test_created_at_field(self):
        field_meta = ContractFiles._meta.get_field('created_at')
        self.assertEqual(field_meta.verbose_name, 'Добавлен')
        self.assertTrue(field_meta.auto_now_add)

    def test_model_meta(self):
        model_meta = ContractFiles._meta
        self.assertEqual(model_meta.verbose_name, 'Файл контракта')
        self.assertEqual(model_meta.verbose_name_plural, 'Файлы контрактов')
        self.assertIn('-created_at', model_meta.ordering)

    def test_model_str(self):
        pass


class EquipmentFilesModelTestCase(TestCase):
    def test_slug_field(self):
        field_meta = EquipmentFiles._meta.get_field('slug')
        self.assertEqual(field_meta.verbose_name, 'Слаг')
        self.assertEqual(field_meta.max_length, 255)

    def test_equipment_field(self):
        field_meta = EquipmentFiles._meta.get_field('equipment')
        self.assertEqual(field_meta.verbose_name, 'Оборудование')
        self.assertFalse(field_meta.blank)

    def test_title_field(self):
        field_meta = EquipmentFiles._meta.get_field('title')
        self.assertEqual(field_meta.verbose_name, 'Название')
        self.assertEqual(field_meta.max_length, 255)
        self.assertEqual(field_meta.help_text, 'Введите название файла...')
        self.assertFalse(field_meta.blank)

    def test_description_field(self):
        field_meta = EquipmentFiles._meta.get_field('description')
        self.assertEqual(field_meta.verbose_name, 'Описание')
        self.assertEqual(field_meta.help_text, 'Введите описание файла...')
        self.assertFalse(field_meta.blank)

    def test_file_field(self):
        field_meta = EquipmentFiles._meta.get_field('file')
        self.assertEqual(field_meta.verbose_name, 'Файл')
        self.assertFalse(field_meta.blank)

    def test_created_at_field(self):
        field_meta = EquipmentFiles._meta.get_field('created_at')
        self.assertEqual(field_meta.verbose_name, 'Добавлен')
        self.assertTrue(field_meta.auto_now_add)

    def test_model_meta(self):
        model_meta = EquipmentFiles._meta
        self.assertEqual(model_meta.verbose_name, 'Файл оборудования')
        self.assertEqual(model_meta.verbose_name_plural, 'Файлы оборудований')
        self.assertIn('-created_at', model_meta.ordering)

    def test_model_str(self):
        pass


class ClientsModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        data = dict(
            name='Client Corp 1',
            site='http://client.corp',
            email='client_corp_1@yandex.ru',
            phone='79103482470',
            office_address='Moscow-Pushkin-Kalatushkin-1',
            legal_address='Moscow-Pushkin-Kalatushkin-2',
            inn='1234567890',
            kpp='123456789',
            ogrn='1234567890123',
        )
        Clients.objects.create(**data)

    def test_slug_field(self):
        field_meta = Clients._meta.get_field('slug')
        self.assertEqual(field_meta.verbose_name, 'Слаг')
        self.assertEqual(field_meta.max_length, 255)

    def test_name_field(self):
        field_meta = Clients._meta.get_field('name')
        self.assertEqual(field_meta.verbose_name, 'Название')
        self.assertEqual(field_meta.max_length, 255)
        self.assertEqual(field_meta.help_text, 'Введите название клиента...')
        self.assertFalse(field_meta.blank)

    def test_second_name_field(self):
        field_meta = Clients._meta.get_field('second_name')
        self.assertEqual(field_meta.verbose_name, 'Дополнительное название')
        self.assertEqual(field_meta.max_length, 255)
        self.assertEqual(field_meta.help_text, 'Введите дополнительное название клиента...')
        self.assertTrue(field_meta.blank)

    def test_site_field(self):
        field_meta = Clients._meta.get_field('site')
        self.assertEqual(field_meta.verbose_name, 'Адрес сайта')
        self.assertEqual(field_meta.max_length, 255)
        self.assertEqual(field_meta.help_text, 'Введите адрес сайта клиента...')
        self.assertTrue(field_meta.blank)

    def test_email_field(self):
        field_meta = Clients._meta.get_field('email')
        self.assertEqual(field_meta.verbose_name, 'Адрес электронной почты')
        self.assertEqual(field_meta.help_text, 'Введите адрес электронной почты клиента...')
        self.assertFalse(field_meta.blank)
        self.assertTrue(field_meta.unique)

    def test_phone_field(self):
        field_meta = Clients._meta.get_field('phone')
        self.assertEqual(field_meta.verbose_name, 'Номер телефона')
        self.assertEqual(field_meta.region, 'RU')
        self.assertEqual(field_meta.help_text, 'Введите номер телефона клиента...')
        self.assertFalse(field_meta.blank)
        self.assertTrue(field_meta.unique)

    def test_office_address_field(self):
        field_meta = Clients._meta.get_field('office_address')
        self.assertEqual(field_meta.verbose_name, 'Адрес офиса')
        self.assertEqual(field_meta.help_text, 'Введите адрес офиса клиента...')
        self.assertFalse(field_meta.blank)

    def test_legal_address_field(self):
        field_meta = Clients._meta.get_field('legal_address')
        self.assertEqual(field_meta.verbose_name, 'Юридический адрес')
        self.assertEqual(field_meta.help_text, 'Введите юридический адрес клиента...')
        self.assertFalse(field_meta.blank)

    def test_inn_field(self):
        field_meta = Clients._meta.get_field('inn')
        self.assertEqual(field_meta.verbose_name, 'ИНН')
        self.assertEqual(field_meta.help_text, 'Пример: 0000000000')
        self.assertFalse(field_meta.blank)
        self.assertTrue(field_meta.unique)

    def test_kpp_field(self):
        field_meta = Clients._meta.get_field('kpp')
        self.assertEqual(field_meta.verbose_name, 'КПП')
        self.assertEqual(field_meta.help_text, 'Пример: 000000000')
        self.assertFalse(field_meta.blank)
        self.assertTrue(field_meta.unique)

    def test_ogrn_field(self):
        field_meta = Clients._meta.get_field('ogrn')
        self.assertEqual(field_meta.verbose_name, 'ОГРН')
        self.assertEqual(field_meta.help_text, 'Пример: 0000000000000')
        self.assertFalse(field_meta.blank)
        self.assertTrue(field_meta.unique)

    def test_note_field(self):
        field_meta = Clients._meta.get_field('note')
        self.assertEqual(field_meta.verbose_name, 'Заметки')
        self.assertEqual(field_meta.help_text, 'Введите заметки по клиенту...')
        self.assertTrue(field_meta.blank)

    def test_created_at_field(self):
        field_meta = Clients._meta.get_field('created_at')
        self.assertEqual(field_meta.verbose_name, 'Добавлен')
        self.assertTrue(field_meta.auto_now_add)

    def test_model_meta(self):
        model_meta = Clients._meta
        self.assertEqual(model_meta.verbose_name, 'Клиент')
        self.assertEqual(model_meta.verbose_name_plural, 'Клиенты')
        self.assertIn('-created_at', model_meta.ordering)

    def test_slug_generate(self):
        client = Clients.objects.get(pk=1)
        self.assertEqual(client.slug, 'client-corp-1')

    def test_model_str(self):
        client = Clients.objects.get(slug='client-corp-1')
        self.assertEqual(str(client), f"{client.slug}")
