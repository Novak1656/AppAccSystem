from django.test import TestCase
from ..forms import ClientForm
from ..models import Clients


class ClientFormTestCase(TestCase):
    def setUp(self):
        self.data = dict(
            name='Corp',
            site='https://ya.ru/',
            email='corp@mail.ru',
            phone_0='RU',
            phone_1='79102611111',
            office_address='orel dom 1',
            legal_address='orel dom 2',
            inn='0000000000',
            kpp='000000000',
            ogrn='0000000000000',
        )

    def test_form_fields(self):
        form = ClientForm()
        field_list = ['name', 'second_name', 'site', 'email', 'phone',
                      'office_address', 'legal_address', 'inn', 'kpp', 'ogrn', 'note']
        self.assertEqual(form._meta.fields, field_list)

    def test_form_model(self):
        form = ClientForm()
        self.assertEqual(form._meta.model, Clients)

    def test_form_validator_inn(self):
        self.data['inn'] = '0000inn000'
        form = ClientForm(data=self.data)
        form.is_valid()
        self.assertEqual(form.errors['inn'][0], 'ИНН должен состоять только из цифр')

    def test_form_validator_kpp(self):
        self.data['kpp'] = '000kpp000'
        form = ClientForm(data=self.data)
        form.is_valid()
        self.assertEqual(form.errors['kpp'][0], 'КПП должен состоять только из цифр')

    def test_form_validator_ogrn(self):
        self.data['ogrn'] = '00000ogrn0000'
        form = ClientForm(data=self.data)
        form.is_valid()
        self.assertEqual(form.errors['ogrn'][0], 'ОГРН должен состоять только из цифр')

    def test_form_validator_site(self):
        self.data['site'] = 'https://ya'
        form = ClientForm(data=self.data)
        form.is_valid()
        self.assertEqual(form.errors['site'][0], 'Указаный адрес сайта не действителен')
