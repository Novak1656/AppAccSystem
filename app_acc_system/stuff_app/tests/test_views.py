import random
from django.test import TestCase
from ..models import StuffUsers
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
            data['role'] = StuffUsers.ROLES[random.randint(0, 1)][0]
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
        self.user_admin = StuffUsers.objects.create_superuser(username='admin', password='admin')
        self.user = StuffUsers.objects.create_user(
            username='DefaultUser',
            password='default_some_password_12345',
            first_name='Novikov',
            second_name='Andrey',
            last_name='',
            role=StuffUsers.ROLES[1][0],
            email='Andrey1234@yandex.ru',
            phone='79102611111',
            status=StuffUsers.STATUSES[0][0],
        )
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
        form_data = dict(
            first_name='Novikov',
            second_name='Andrey',
            last_name='',
            role=StuffUsers.ROLES[1][0],
            email='Andrey1234@yandex.ru',
            phone_0='RU',
            phone_1='79102611111'
            )
        form_data['last_name'] = 'Andreevich'
        resp = self.client.post(f'/stuff/{self.user.username}/detail/', data=form_data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.user.last_name, '')
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, 'Andreevich')
        self.assertRedirects(resp, self.user.get_absolute_url())


class ChangeUserStatusViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        StuffUsers.objects.create_superuser(username='admin', password='admin')

    def setUp(self):
        self.user = StuffUsers.objects.create_user(
            username='DefaultUser',
            password='default_some_password_12345',
            first_name='Novikov',
            second_name='Andrey',
            last_name='',
            role=StuffUsers.ROLES[1][0],
            email='Andrey1234@yandex.ru',
            phone='79102611111',
            status=StuffUsers.STATUSES[0][0],
        )
        self.client.login(username='admin', password='admin')

    def test_user_not_login(self):
        self.client.logout()
        resp = self.client.get(f"/stuff/change_user_status/{self.user.pk}/")
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, f'/stuff/user/login/?next=%2Fstuff%2Fchange_user_status%2F{self.user.pk}%2F')

    def test_url(self):
        resp = self.client.get(f"/stuff/change_user_status/{self.user.pk}/")
        self.assertEqual(resp.status_code, 302)

    def test_url_name(self):
        resp = self.client.get(reverse('change_user_status', kwargs={'user_pk': self.user.pk}))
        self.assertEqual(resp.status_code, 302)

    def test_view_redirect(self):
        resp = self.client.get(f"/stuff/change_user_status/{self.user.pk}/")
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.user.get_absolute_url())

    def test_view_status_active_to_archive(self):
        self.assertEqual(self.user.status, 'Active')
        resp = self.client.get(f"/stuff/change_user_status/{self.user.pk}/")
        self.assertEqual(resp.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.status, 'Archive')

    def test_view_status_archive_to_active(self):
        user = StuffUsers.objects.create_user(
            username='DefaultUser2',
            password='default_some_password_12346',
            first_name='Novikov2',
            second_name='Andrey2',
            role=StuffUsers.ROLES[1][0],
            email='Andrey5678@yandex.ru',
            phone='79102622222',
            status=StuffUsers.STATUSES[1][0],
        )
        self.assertEqual(user.status, 'Archive')
        resp = self.client.get(f"/stuff/change_user_status/{user.pk}/")
        self.assertEqual(resp.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.status, 'Active')


class StuffUserChangeLoginViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        StuffUsers.objects.create_superuser(username='admin', password='admin')

    def setUp(self):
        self.user = StuffUsers.objects.create_user(
            username='DefaultUser',
            password='default_some_password_12345',
            first_name='Novikov',
            second_name='Andrey',
            last_name='',
            role=StuffUsers.ROLES[1][0],
            email='Andrey1234@yandex.ru',
            phone='79102611111',
            status=StuffUsers.STATUSES[0][0],
        )
        self.client.login(username='admin', password='admin')

    def test_user_not_login(self):
        self.client.logout()
        resp = self.client.get(f'/stuff/user/config/new_login/{self.user.pk}/')
        self.assertEqual(resp.status_code, 302)
        redirect_url = f'/stuff/user/login/?next=%2Fstuff%2Fuser%2Fconfig%2Fnew_login%2F{self.user.pk}%2F'
        self.assertRedirects(resp, redirect_url)

    def test_url(self):
        resp = self.client.get(f'/stuff/user/config/new_login/{self.user.pk}/')
        self.assertEqual(resp.status_code, 200)

    def test_url_name(self):
        resp = self.client.get(reverse('stuff_user_change_login', kwargs={'user_pk': self.user.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_view_template(self):
        resp = self.client.get(f'/stuff/user/config/new_login/{self.user.pk}/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'stuff_app/change_login.html')

    def test_view_post_user_login_update(self):
        resp = self.client.post(f'/stuff/user/config/new_login/{self.user.pk}/', data={'username': 'User'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.user.username, 'DefaultUser')
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'User')
        self.assertRedirects(resp, self.user.get_absolute_url())


class StuffUserChangePasswordViewTestCase(TestCase):
    def setUp(self):
        self.admin = StuffUsers.objects.create_superuser(username='admin', password='admin')
        self.client.login(username='admin', password='admin')

    def test_user_not_login(self):
        self.client.logout()
        resp = self.client.get(f'/stuff/user/config/new_password/{self.admin.pk}/')
        self.assertEqual(resp.status_code, 302)
        redirect_url = f'/stuff/user/login/?next=%2Fstuff%2Fuser%2Fconfig%2Fnew_password%2F{self.admin.pk}%2F'
        self.assertRedirects(resp, redirect_url)

    def test_url(self):
        resp = self.client.get(f'/stuff/user/config/new_password/{self.admin.pk}/')
        self.assertEqual(resp.status_code, 200)

    def test_url_name(self):
        resp = self.client.get(reverse('stuff_user_change_password', kwargs={'user_pk': self.admin.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_view_template(self):
        resp = self.client.get(f'/stuff/user/config/new_password/{self.admin.pk}/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'stuff_app/change_password.html')

    def test_view_post_user_password_update(self):
        data = {
            'old_password': 'admin',
            'new_password1': 'VeRy_VeRy_Hard_PaSsWoRd_12345',
            'new_password2': 'VeRy_VeRy_Hard_PaSsWoRd_12345'
        }
        resp = self.client.post(f'/stuff/user/config/new_password/{self.admin.pk}/', data=data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.admin.refresh_from_db()
        self.client.logout()
        self.client.login(username='admin', password='VeRy_VeRy_Hard_PaSsWoRd_12345')


class StuffUserDeleteViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        StuffUsers.objects.create_superuser(username='admin', password='admin')

    def setUp(self):
        self.user = StuffUsers.objects.create_user(
            username='DefaultUser',
            password='default_some_password_12345',
            first_name='Novikov',
            second_name='Andrey',
            last_name='',
            role=StuffUsers.ROLES[1][0],
            email='Andrey1234@yandex.ru',
            phone='79102611111',
            status=StuffUsers.STATUSES[0][0],
        )
        self.client.login(username='admin', password='admin')

    def test_user_not_login(self):
        self.client.logout()
        resp = self.client.get(f'/stuff/user/delete/{self.user.pk}/')
        self.assertEqual(resp.status_code, 302)
        redirect_url = f'/stuff/user/login/?next=%2Fstuff%2Fuser%2Fdelete%2F{self.user.pk}%2F'
        self.assertRedirects(resp, redirect_url)

    def test_url(self):
        resp = self.client.get(f'/stuff/user/delete/{self.user.pk}/')
        self.assertEqual(resp.status_code, 302)

    def test_url_name(self):
        resp = self.client.get(reverse('stuff_user_delete', kwargs={'user_pk': self.user.pk}))
        self.assertEqual(resp.status_code, 302)

    def test_view_redirect(self):
        resp = self.client.get(f'/stuff/user/delete/{self.user.pk}/')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('stuff_list'))

    def test_view_user_delete(self):
        resp = self.client.get(f'/stuff/user/delete/{self.user.pk}/')
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(StuffUsers.objects.filter(pk=self.user.pk).exists())


class StuffUserAuthViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        StuffUsers.objects.create_superuser(username='admin', password='admin')
        StuffUsers.objects.create_user(
            username='DefaultUser',
            password='default_some_password_12345',
            first_name='Novikov',
            second_name='Andrey',
            last_name='',
            role=StuffUsers.ROLES[1][0],
            email='Andrey1234@yandex.ru',
            phone='79102611111',
            status=StuffUsers.STATUSES[1][0],
        )

    def test_user_login(self):
        self.client.login(username='admin', password='admin')
        resp = self.client.get('/stuff/user/login/')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('stuff_list'))

    def test_url(self):
        resp = self.client.get('/stuff/user/login/')
        self.assertEqual(resp.status_code, 200)

    def test_url_name(self):
        resp = self.client.get(reverse('stuff_user_auth'))
        self.assertEqual(resp.status_code, 200)

    def test_view_template(self):
        resp = self.client.get('/stuff/user/login/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'stuff_app/login_page.html')

    def test_view_post_user_auth_active(self):
        resp = self.client.post('/stuff/user/login/', data={'username': 'admin', 'password': 'admin'})
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('stuff_list'))
        user = StuffUsers.objects.get(username='admin')
        self.assertTrue(user.is_authenticated)

    def test_view_post_user_auth_archive(self):
        data = {'username': 'DefaultUser', 'password': 'default_some_password_12345'}
        resp = self.client.post('/stuff/user/login/', data=data)
        messages = [mes.message for mes in resp.context['messages']]
        self.assertIn('Ваша учетная запись заблокирована, обратитесь к администратору системы', messages)
        self.assertEqual(resp.status_code, 200)


class StuffUserLogoutViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        StuffUsers.objects.create_superuser(username='admin', password='admin')

    def setUp(self):
        self.client.login(username='admin', password='admin')

    def test_url(self):
        resp = self.client.get('/stuff/user/logout/')
        self.assertEqual(resp.status_code, 302)

    def test_url_name(self):
        resp = self.client.get(reverse('stuff_user_logout'))
        self.assertEqual(resp.status_code, 302)

    def test_view_redirect(self):
        resp = self.client.get(reverse('stuff_user_logout'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('stuff_user_auth'))


class UsersPermissionsViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        StuffUsers.objects.create_superuser(username='admin', password='admin')
        StuffUsers.objects.create_user(
            username='UserDispatcher',
            password='default_some_password_12345',
            first_name='Novikov',
            second_name='Andrey',
            role=StuffUsers.ROLES[1][0],
            email='Andrey1234@yandex.ru',
            phone='79102611111',
        )
        StuffUsers.objects.create_user(
            username='UserExecutor',
            password='default_some_password_67890',
            first_name='Kim',
            second_name='Alex',
            role=StuffUsers.ROLES[2][0],
            email='Andrey5678@yandex.ru',
            phone='79102622222',
        )

    def test_admin_permissions(self):
        user = StuffUsers.objects.get(username='admin')
        self.client.login(username='admin', password='admin')
        resp_user_create = self.client.get(reverse('stuff_create'))
        self.assertEqual(resp_user_create.status_code, 200)
        resp_users_list = self.client.get(reverse('stuff_list'))
        self.assertEqual(resp_users_list.status_code, 200)
        resp_user_detail = self.client.get(reverse('stuff_detail', kwargs={'username': user.username}))
        self.assertEqual(resp_user_detail.status_code, 200)
        resp_user_status = self.client.get(reverse('change_user_status', kwargs={'user_pk': user.pk}))
        self.assertEqual(resp_user_status.status_code, 302)
        resp_user_new_login = self.client.get(reverse('stuff_user_change_login', kwargs={'user_pk': user.pk}))
        self.assertEqual(resp_user_new_login.status_code, 200)
        resp_user_new_password = self.client.get(reverse('stuff_user_change_password', kwargs={'user_pk': user.pk}))
        self.assertEqual(resp_user_new_password.status_code, 200)
        resp_user_delete = self.client.get(reverse('stuff_user_delete', kwargs={'user_pk': user.pk}))
        self.assertEqual(resp_user_delete.status_code, 302)
        resp_user_logout = self.client.get(reverse('stuff_user_logout'))
        self.assertEqual(resp_user_logout.status_code, 302)
        self.client.logout()
        resp_user_login = self.client.get(reverse('stuff_user_auth'))
        self.assertEqual(resp_user_login.status_code, 200)

    def test_dispatcher_permissions(self):
        user = StuffUsers.objects.get(username='UserDispatcher')
        self.client.login(username='UserDispatcher', password='default_some_password_12345')
        resp_user_create = self.client.get(reverse('stuff_create'))
        self.assertEqual(resp_user_create.status_code, 404)
        resp_users_list = self.client.get(reverse('stuff_list'))
        self.assertEqual(resp_users_list.status_code, 200)
        resp_user_detail = self.client.get(reverse('stuff_detail', kwargs={'username': user.username}))
        self.assertEqual(resp_user_detail.status_code, 404)
        resp_user_status = self.client.get(reverse('change_user_status', kwargs={'user_pk': user.pk}))
        self.assertEqual(resp_user_status.status_code, 404)
        resp_user_new_login = self.client.get(reverse('stuff_user_change_login', kwargs={'user_pk': user.pk}))
        self.assertEqual(resp_user_new_login.status_code, 404)
        resp_user_new_password = self.client.get(reverse('stuff_user_change_password', kwargs={'user_pk': user.pk}))
        self.assertEqual(resp_user_new_password.status_code, 404)
        resp_user_delete = self.client.get(reverse('stuff_user_delete', kwargs={'user_pk': user.pk}))
        self.assertEqual(resp_user_delete.status_code, 404)
        resp_user_logout = self.client.get(reverse('stuff_user_logout'))
        self.assertEqual(resp_user_logout.status_code, 302)
        self.client.logout()
        resp_user_login = self.client.get(reverse('stuff_user_auth'))
        self.assertEqual(resp_user_login.status_code, 200)

    def test_executor_permissions(self):
        user = StuffUsers.objects.get(username='UserExecutor')
        self.client.login(username='UserExecutor', password='default_some_password_67890')
        resp_user_create = self.client.get(reverse('stuff_create'))
        self.assertEqual(resp_user_create.status_code, 404)
        resp_users_list = self.client.get(reverse('stuff_list'))
        self.assertEqual(resp_users_list.status_code, 404)
        resp_user_detail = self.client.get(reverse('stuff_detail', kwargs={'username': user.username}))
        self.assertEqual(resp_user_detail.status_code, 404)
        resp_user_status = self.client.get(reverse('change_user_status', kwargs={'user_pk': user.pk}))
        self.assertEqual(resp_user_status.status_code, 404)
        resp_user_new_login = self.client.get(reverse('stuff_user_change_login', kwargs={'user_pk': user.pk}))
        self.assertEqual(resp_user_new_login.status_code, 404)
        resp_user_new_password = self.client.get(reverse('stuff_user_change_password', kwargs={'user_pk': user.pk}))
        self.assertEqual(resp_user_new_password.status_code, 404)
        resp_user_delete = self.client.get(reverse('stuff_user_delete', kwargs={'user_pk': user.pk}))
        self.assertEqual(resp_user_delete.status_code, 404)
        resp_user_logout = self.client.get(reverse('stuff_user_logout'))
        self.assertEqual(resp_user_logout.status_code, 302)
        self.client.logout()
        resp_user_login = self.client.get(reverse('stuff_user_auth'))
        self.assertEqual(resp_user_login.status_code, 200)
