from django.test import TestCase
from django.urls import reverse_lazy
from stuff_app.models import StuffUsers
from ..models import Clients
from ..forms import ClientForm
from ..views import ClientCreateView


class ClientsListViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        data = dict(
            name='Corp',
            site='https://ya.ru/',
            office_address='orel dom 1',
            legal_address='orel dom 2',
        )

        clients = [
            Clients(
                email=f"corp{_}@mail.ru",
                phone=f"7910261111{_}",
                inn=f"000000000{_}",
                kpp=f"00000000{_}",
                ogrn=f"000000000000{_}",
                **data
            ) for _ in range(3)
        ]
        Clients.objects.bulk_create(clients)

    def setUp(self):
        StuffUsers.objects.create_superuser(username='admin', password='admin')
        self.client.login(username='admin', password='admin')

    def test_url(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    def test_url_name(self):
        resp = self.client.get(reverse_lazy('clients_list'))
        self.assertEqual(resp.status_code, 200)

    def test_view_template(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'client_app/clients_page.html')

    def test_user_not_login(self):
        self.client.logout()
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/stuff/user/login/?next=/')

    def test_view_context_object_name(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('clients', resp.context)

    def test_view_queryset(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)
        clients = Clients.objects.all()
        self.assertQuerysetEqual(resp.context['clients'], clients)


class ClientCreateViewTestCase(TestCase):
    def setUp(self):
        StuffUsers.objects.create_superuser(username='admin', password='admin')
        self.client.login(username='admin', password='admin')

    def test_url(self):
        resp = self.client.get('/clients/add/')
        self.assertEqual(resp.status_code, 200)

    def test_url_name(self):
        resp = self.client.get(reverse_lazy('client_create'))
        self.assertEqual(resp.status_code, 200)

    def test_view_template(self):
        resp = self.client.get('/clients/add/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'client_app/add_client.html')

    def test_user_not_login(self):
        self.client.logout()
        resp = self.client.get('/clients/add/')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/stuff/user/login/?next=%2Fclients%2Fadd%2F')

    def test_view_form_class(self):
        form = ClientCreateView.form_class
        self.assertEqual(form, ClientForm)

    def test_view_model(self):
        model = ClientCreateView.model
        self.assertEqual(model, Clients)

    def test_view_redirect(self):
        data = dict(
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
        resp = self.client.post('/clients/add/', data=data)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/')
