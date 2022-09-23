import random

from django.test import TestCase
from ..models import StuffUsers
# Тесты всех вьюшек по отдельности и тест доступа пользователей
from django.urls import reverse


class StuffUserCreateViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        StuffUsers.objects.create_superuser(username='Some_username', password='some_password_123')

    def setUp(self):
        self.client.login(username='Some_username', password='some_password_123')

    def test_url(self):
        resp = self.client.get('/stuff/create/')
        self.assertEqual(resp.status_code, 200)

    def test_url_name(self):
        resp = self.client.get(reverse('stuff_create'))
        self.assertEqual(resp.status_code, 200)

    def test_view_template(self):
        resp = self.client.get(reverse('stuff_create'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'stuff_app/add_executor.html')

    def test_user_not_login(self):
        self.client.logout()
        resp = self.client.get('/stuff/create/')
        self.assertRedirects(resp, '/stuff/user/login/?next=%2Fstuff%2Fcreate%2F')


class StuffUsersListViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        usernames = [f'user{i}' for i in range(10)]
        passwords = [f'default_some_password_{i}' for i in range(10)]
        emails = [f'mail{i}@mail.ru' for i in range(10)]
        data = {
            'first_name': 'Name',
            'second_name': 'Sec_name',
        }
        for i in range(10):
            data['role'] = StuffUsers.ROLES[random.randint(0, 2)][0]
            data['phone'] = f"7910{''.join(str(random.randint(0, 9)) for _ in range(7))}"
            StuffUsers.objects.create_user(username=usernames[i], password=passwords[i], email=emails[i], **data)

    def test_user_not_login(self):
        resp = self.client.get('/stuff/')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/stuff/user/login/?next=%2Fstuff%2F')

    def test_url(self):
        self.client.login(username='user1', password='default_some_password_1')
        resp = self.client.get('/stuff/')
        self.assertEqual(resp.status_code, 200)

    def test_url_name(self):
        self.client.login(username='user1', password='default_some_password_1')
        resp = self.client.get(reverse('stuff_list'))
        self.assertEqual(resp.status_code, 200)

    def test_view_template(self):
        self.client.login(username='user1', password='default_some_password_1')
        resp = self.client.get('/stuff/')
        self.assertTemplateUsed(resp, 'stuff_app/executors_page.html')

    def test_view_query_set_list(self):
        self.client.login(username='user1', password='default_some_password_1')
        resp = self.client.get('/stuff/')
        self.assertQuerysetEqual(resp.context['executors'], StuffUsers.objects.all())


class StuffUserDetailViewTestCase(TestCase):
    def setUp(self):
        StuffUsers.objects.create_superuser(username='admin', password='admin')
        self.client.login(username='admin', password='admin')

    def test_user_not_login(self):
        self.client.logout()
        resp = self.client.get('/stuff/admin/detail/')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/stuff/user/login/?next=%2Fstuff%2Fadmin%2Fdetail%2F')

    def test_url(self):
        resp = self.client.get('/stuff/admin/detail/')
        self.assertEqual(resp.status_code, 200)

    def test_url_name(self):
        resp = self.client.get(reverse('stuff_detail', kwargs={'username': 'admin'}))
        self.assertEqual(resp.status_code, 200)

    def test_view_template(self):
        resp = self.client.get('/stuff/admin/detail/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'stuff_app/detail_executor.html')

    def test_view_query_set(self):
        resp = self.client.get('/stuff/admin/detail/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(str(resp.context['executor']), 'admin: admin')

    def test_view_post_user_info_data_update(self):
        resp = self.client.post('/stuff/admin/detail/', data={'first_name': 'Andrey'}, follow=True)
        user = StuffUsers.objects.get(username='admin')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(user.username, 'admin')
        self.assertEqual(user.first_name, 'Andrey')
        self.assertRedirects(resp, user.get_absolute_url())


