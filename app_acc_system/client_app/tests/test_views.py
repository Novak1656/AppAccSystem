from django.db.models import Count
from django.test import TestCase
from django.urls import reverse_lazy
from stuff_app.models import StuffUsers
from ..models import Clients
from ..forms import ClientForm
from ..views import ClientCreateView, ClientDetailView


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


class ClientDetailViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Clients.objects.create(
            name='Corp',
            site='https://ya.ru/',
            office_address='orel dom 1',
            legal_address='orel dom 2',
            email="corp1@mail.ru",
            phone="79102611111",
            inn="0000000000",
            kpp="000000000",
            ogrn="0000000000000",
        )

    def setUp(self):
        self.client_slug = Clients.objects.first().slug
        StuffUsers.objects.create_superuser(username='admin', password='admin')
        self.client.login(username='admin', password='admin')

    def test_url(self):
        resp = self.client.get(f'/clients/detail/{self.client_slug}/')
        self.assertEqual(resp.status_code, 200)

    def test_url_name(self):
        resp = self.client.get(reverse_lazy('client_detail', kwargs={'client_slug': self.client_slug}))
        self.assertEqual(resp.status_code, 200)

    def test_view_template(self):
        resp = self.client.get(f'/clients/detail/{self.client_slug}/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'client_app/client_detail.html')

    def test_user_not_login(self):
        self.client.logout()
        resp = self.client.get(f'/clients/detail/{self.client_slug}/')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, f'/stuff/user/login/?next=%2Fclients%2Fdetail%2F{self.client_slug}%2F')

    def test_view_kwargs_name(self):
        slug_kwargs_name = ClientDetailView.slug_url_kwarg
        self.assertEqual(slug_kwargs_name, 'client_slug')

    def test_view_model(self):
        view_model = ClientDetailView.model
        self.assertEqual(view_model, Clients)

    def test_view_context_objects(self):
        resp = self.client.get(f'/clients/detail/{self.client_slug}/')
        context_list = ['client', 'client_files']
        for cont in context_list:
            self.assertIn(cont, resp.context)

    def test_view_queryset(self):
        resp = self.client.get(f'/clients/detail/{self.client_slug}/')
        client = Clients.objects.filter(slug=self.client_slug).annotate(
            cp_count=Count('contact_persons'),
            eq_count=Count('equipments'),
            ct_count=Count('contracts'),
        ).first()
        self.assertEqual(resp.context['client'], client)


class ClientUpdateViewTestCase(TestCase):
    pass


class ClientFilesCreateViewTestCase(TestCase):
    pass


class DeleteClientFileViewTestCase(TestCase):
    pass


class ContactPersonsListViewTestCase(TestCase):
    pass


class ContactPersonCreateViewTestCase(TestCase):
    pass


class ContactPersonDetailViewTestCase(TestCase):
    pass
