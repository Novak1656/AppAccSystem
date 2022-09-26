from django.core.validators import MinLengthValidator
from django.test import TestCase
from ..models import StuffUsers


class StuffUsersModelTestCase(TestCase):
    def setUp(self):
        self.user = StuffUsers.objects.create_user(
            username='DefaultUser',
            password='default_some_password_12345',
            first_name='Novikov',
            second_name='Andrey',
            last_name='Andreevich',
            role=StuffUsers.ROLES[1][0],
            email='Andrey1234@yandex.ru',
            phone='79102611111',
            status=StuffUsers.STATUSES[0][0],
        )

    def test_username_field(self):
        user_meta = self.user._meta.get_field('username')
        field_label = user_meta.verbose_name
        self.assertEqual(field_label, 'Логин')
        field_length = user_meta.max_length
        self.assertEqual(field_length, 255)
        field_unique = user_meta.unique
        self.assertTrue(field_unique)
        field_blank = user_meta.blank
        self.assertFalse(field_blank)

    def test_password_field(self):
        user_meta = self.user._meta.get_field('password')
        field_label = user_meta.verbose_name
        self.assertEqual(field_label, 'Пароль')
        field_validators = user_meta.validators
        self.assertIn(MinLengthValidator(8), field_validators)
        field_length = user_meta.max_length
        self.assertEqual(field_length, 255)
        field_unique = user_meta.unique
        self.assertTrue(field_unique)
        field_blank = user_meta.blank
        self.assertFalse(field_blank)

    def test_first_name_field(self):
        user_meta = self.user._meta.get_field('first_name')
        field_label = user_meta.verbose_name
        self.assertEqual(field_label, 'Фамилия')
        field_length = user_meta.max_length
        self.assertEqual(field_length, 255)
        field_blank = user_meta.blank
        self.assertFalse(field_blank)

    def test_second_name_field(self):
        user_meta = self.user._meta.get_field('second_name')
        field_label = user_meta.verbose_name
        self.assertEqual(field_label, 'Имя')
        field_length = user_meta.max_length
        self.assertEqual(field_length, 255)
        field_blank = user_meta.blank
        self.assertFalse(field_blank)

    def test_last_name_field(self):
        user_meta = self.user._meta.get_field('last_name')
        field_label = user_meta.verbose_name
        self.assertEqual(field_label, 'Отчество')
        field_length = user_meta.max_length
        self.assertEqual(field_length, 255)
        field_blank = user_meta.blank
        self.assertTrue(field_blank)

    def test_role_field(self):
        user_meta = self.user._meta.get_field('role')
        field_label = user_meta.verbose_name
        self.assertEqual(field_label, 'Роль')
        field_length = user_meta.max_length
        self.assertEqual(field_length, 10)
        field_blank = user_meta.blank
        self.assertFalse(field_blank)
        field_choices = user_meta.choices
        choices_list = [('admin', 'Администратор'), ('dispatcher', 'Диспетчер'), ('executor', 'Исполнитель')]
        self.assertEqual(field_choices, choices_list)

    def test_email_field(self):
        user_meta = self.user._meta.get_field('email')
        field_label = user_meta.verbose_name
        self.assertEqual(field_label, 'Электронная почта')
        field_unique = user_meta.unique
        self.assertTrue(field_unique)
        field_null = user_meta.null
        self.assertTrue(field_null)
        field_blank = user_meta.blank
        self.assertFalse(field_blank)

    def test_phone_field(self):
        user_meta = self.user._meta.get_field('phone')
        field_label = user_meta.verbose_name
        self.assertEqual(field_label, 'Номер телефона')
        field_region = user_meta.region
        self.assertEqual(field_region, 'RU')
        field_null = user_meta.null
        self.assertTrue(field_null)
        field_blank = user_meta.blank
        self.assertFalse(field_blank)
        field_unique = user_meta.unique
        self.assertTrue(field_unique)

    def test_status_field(self):
        user_meta = self.user._meta.get_field('status')
        field_label = user_meta.verbose_name
        self.assertEqual(field_label, 'Статус')
        field_choices = user_meta.choices
        choices_list = [('Active', 'Активный'), ('Archive', 'Архивный')]
        self.assertEqual(field_choices, choices_list)
        field_length = user_meta.max_length
        self.assertEqual(field_length, 10)
        field_default = user_meta.default
        self.assertEqual(field_default, 'Active')

    def test_created_at_field(self):
        user_meta = self.user._meta.get_field('created_at')
        field_label = user_meta.verbose_name
        self.assertEqual(field_label, 'Дата добавления')
        field_auto_now_add = user_meta.auto_now_add
        self.assertTrue(field_auto_now_add)

    def test_updated_at_field(self):
        user_meta = self.user._meta.get_field('updated_at')
        field_label = user_meta.verbose_name
        self.assertEqual(field_label, 'Дата изменения')
        field_auto_now = user_meta.auto_now
        self.assertTrue(field_auto_now)

    def test_model_meta_attrs(self):
        model_meta = self.user._meta
        field_label = model_meta.verbose_name
        self.assertEqual(field_label, 'Сотрудник')
        field_label_plural = model_meta.verbose_name_plural
        self.assertEqual(field_label_plural, 'Сотрудники')
        field_ordering = model_meta.ordering
        ordering_list = ['-status']
        self.assertEqual(field_ordering, ordering_list)

    def test_user_get_absolute_url(self):
        absolute_url = f"/stuff/{self.user.username}/detail/"
        self.assertEqual(self.user.get_absolute_url(), absolute_url)

    def test_user_get_full_name(self):
        full_name = f"{self.user.first_name} {self.user.second_name} {self.user.last_name}"
        self.assertEqual(self.user.get_full_name(), full_name)
        user2 = StuffUsers.objects.create_superuser(
            username='admin1', password='admin1',
            first_name='Volkov', second_name='Alex'
        )
        full_name_without_last_name = f"{user2.first_name} {user2.second_name}"
        self.assertEqual(user2.get_full_name(), full_name_without_last_name)

    def test_user_get_short_name(self):
        short_name = f"{self.user.second_name}"
        self.assertEqual(self.user.get_short_name(), short_name)

    def test_user_is_staff(self):
        self.assertFalse(self.user.is_staff)

    def test_user_is_archive(self):
        self.assertFalse(self.user.is_archive())

    def test_user_str(self):
        true_str = f'{self.user.username}: {self.user.role}'
        self.assertEqual(str(self.user), true_str)

    def test_create_super_user(self):
        user = StuffUsers.objects.create_superuser(username='admin', password='admin')
        self.assertTrue(user.is_superuser)
