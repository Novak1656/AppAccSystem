from django.test import TestCase
from ..models import StuffUsers
from ..forms import StuffUserCreateForm, StuffUserInfoForm, StuffUserLoginChangeForm, StuffUserLoginForm


class StuffUserCreateFormTestCase(TestCase):
    def test_username_field(self):
        form = StuffUserCreateForm()
        self.assertEqual(form.fields['username'].label, 'Логин')

    def test_first_name_field(self):
        form = StuffUserCreateForm()
        self.assertEqual(form.fields['first_name'].label, 'Фамилия')

    def test_second_name_field(self):
        form = StuffUserCreateForm()
        self.assertEqual(form.fields['second_name'].label, 'Имя')

    def test_last_name_field(self):
        form = StuffUserCreateForm()
        self.assertEqual(form.fields['last_name'].label, 'Отчество')

    def test_role_field(self):
        form = StuffUserCreateForm()
        self.assertEqual(form.fields['role'].label, 'Роль')
        roles = [('', '---------'), ('admin', 'Администратор'), ('dispatcher', 'Диспетчер'), ('executor', 'Исполнитель')]
        self.assertEqual(roles, form.fields['role'].widget.choices)

    def test_email_field(self):
        form = StuffUserCreateForm()
        self.assertEqual(form.fields['email'].label, 'Электронная почта')

    def test_phone_field(self):
        form = StuffUserCreateForm()
        self.assertEqual(form.fields['phone'].label, 'Номер телефона')

    def test_password1_field(self):
        form = StuffUserCreateForm()
        self.assertEqual(form.fields['password1'].label, 'Пароль')

    def test_password2_field(self):
        form = StuffUserCreateForm()
        self.assertEqual(form.fields['password2'].label, 'Подтверждение пароля')

    def test_form_meta(self):
        form = StuffUserCreateForm()
        self.assertEqual(form._meta.model, StuffUsers)
        fields_list = [
            'username', 'first_name', 'second_name', 'last_name',
            'role', 'email', 'phone', 'password1', 'password2'
        ]
        self.assertEqual(form._meta.fields, fields_list)

    def test_clean_password2(self):
        data = {
            'username': 'DefaultUser',
            'first_name': 'Novikov',
            'second_name': 'Andrey',
            'role': StuffUsers.ROLES[1][0],
            'email': 'Andrey1234@yandex.ru',
            'phone_0': 'RU',
            'phone_1': '79102611111',
            'password1': 'default_some_password_12345',
            'password2': 'default_some_',
        }
        form1 = StuffUserCreateForm(data=data)
        self.assertFalse(form1.is_valid())
        data['password2'] = data['password1']
        form2 = StuffUserCreateForm(data=data)
        self.assertTrue(form2.is_valid())

    def test_save(self):
        data = {
            'username': 'DefaultUser',
            'password1': 'default_some_password_12345',
            'password2': 'default_some_password_12345',
            'first_name': 'Novikov',
            'second_name': 'Andrey',
            'last_name': 'Andreevich',
            'role': StuffUsers.ROLES[1][0],
            'email': 'Andrey1234@yandex.ru',
            'phone_0': 'RU',
            'phone_1': '79102611111',
        }
        form = StuffUserCreateForm(data=data)
        form.is_valid()
        user = form.save()
        self.assertTrue(StuffUsers.objects.get(pk=1) == user)


class StuffUserInfoFormTestCase(TestCase):
    def test_first_name_field(self):
        form = StuffUserInfoForm()
        self.assertEqual(form.fields['first_name'].label, 'Фамилия')

    def test_second_name_field(self):
        form = StuffUserInfoForm()
        self.assertEqual(form.fields['second_name'].label, 'Имя')

    def test_last_name_field(self):
        form = StuffUserInfoForm()
        self.assertEqual(form.fields['last_name'].label, 'Отчество')

    def test_role_field(self):
        form = StuffUserInfoForm()
        self.assertEqual(form.fields['role'].label, 'Роль')
        roles = [('', '---------'), ('admin', 'Администратор'), ('dispatcher', 'Диспетчер'),
                 ('executor', 'Исполнитель')]
        self.assertEqual(roles, form.fields['role'].widget.choices)

    def test_email_field(self):
        form = StuffUserInfoForm()
        self.assertEqual(form.fields['email'].label, 'Электронная почта')

    def test_phone_field(self):
        form = StuffUserInfoForm()
        self.assertEqual(form.fields['phone'].label, 'Номер телефона')

    def test_form_meta(self):
        form = StuffUserInfoForm()
        self.assertEqual(form._meta.model, StuffUsers)
        fields_list = ('first_name', 'second_name', 'last_name', 'role', 'email', 'phone',)
        self.assertEqual(form._meta.fields, fields_list)


class StuffUserLoginChangeFormTestCase(TestCase):
    def test_username_label(self):
        form = StuffUserLoginChangeForm()
        self.assertEqual(form.fields['username'].label, 'Логин')

    def test_username_placeholder(self):
        form = StuffUserLoginChangeForm()
        self.assertEqual(form.fields['username'].widget.attrs['placeholder'], 'Введите новый логин...')

    def test_form_meta(self):
        form = StuffUserLoginChangeForm()
        self.assertEqual(form._meta.model, StuffUsers)
        self.assertEqual(form._meta.fields, ('username',))


class StuffUserLoginFormTestCase(TestCase):
    def test_username_field(self):
        form = StuffUserLoginForm()
        self.assertEqual(form.fields['username'].label, 'Логин')
        self.assertEqual(form.fields['username'].widget.attrs['placeholder'], 'Введите логин...')

    def test_password_field(self):
        form = StuffUserLoginForm()
        self.assertEqual(form.fields['password'].label, 'Пароль')
        self.assertEqual(form.fields['password'].widget.attrs['placeholder'], 'Введите пароль...')
