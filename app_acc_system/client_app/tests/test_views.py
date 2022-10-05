from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Count
from django.test import TestCase
from django.urls import reverse_lazy
from stuff_app.models import StuffUsers
from ..models import Clients, ClientFiles, ContactPersons
from ..forms import ClientForm, ClientFilesForms, ContactPersonsForms
from ..views import ClientCreateView, ClientDetailView, ClientUpdateView, ClientFilesCreateView, \
    ContactPersonsListView, ContactPersonCreateView, ContactPersonDetailView


class ClientsListViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        for _ in range(3):
            Clients.objects.create(
                email=f"corp{_}@mail.ru",
                phone=f"7910261111{_}",
                inn=f"000000000{_}",
                kpp=f"00000000{_}",
                ogrn=f"000000000000{_}",
                name='Corp',
                site='https://ya.ru/',
                office_address='orel dom 1',
                legal_address='orel dom 2',
            )

    def setUp(self):
        StuffUsers.objects.create_superuser(username='admin', password='admin')
        self.client.login(username='admin', password='admin')

    def test_url(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_url_name(self):
        resp = self.client.get(reverse_lazy('clients_list'))
        self.assertEqual(resp.status_code, 200)

    def test_view_template(self):
        resp = self.client.get(reverse_lazy('clients_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'client_app/clients_page.html')

    def test_user_not_login(self):
        self.client.logout()
        resp = self.client.get(reverse_lazy('clients_list'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/stuff/user/login/?next=/')

    def test_view_context_object_name(self):
        resp = self.client.get(reverse_lazy('clients_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('clients', resp.context)

    def test_view_queryset(self):
        resp = self.client.get(reverse_lazy('clients_list'))
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
    def setUp(self):
        StuffUsers.objects.create_superuser(username='admin', password='admin')
        self.client.login(username='admin', password='admin')
        self.client_obj = Clients.objects.create(
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

    def test_url(self):
        resp = self.client.get(f'/clients/update/{self.client_obj.slug}/')
        self.assertEqual(resp.status_code, 200)

    def test_url_name(self):
        resp = self.client.get(reverse_lazy('client_update', kwargs={'client_slug': self.client_obj.slug}))
        self.assertEqual(resp.status_code, 200)

    def test_view_template(self):
        resp = self.client.get(f'/clients/update/{self.client_obj.slug}/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'client_app/client_update.html')

    def test_user_not_login(self):
        self.client.logout()
        resp = self.client.get(f'/clients/update/{self.client_obj.slug}/')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, f'/stuff/user/login/?next=%2Fclients%2Fupdate%2F{self.client_obj.slug}%2F')

    def test_view_kwargs_name(self):
        slug_kwargs_name = ClientUpdateView.slug_url_kwarg
        self.assertEqual(slug_kwargs_name, 'client_slug')

    def test_view_model(self):
        view_model = ClientUpdateView.model
        self.assertEqual(view_model, Clients)

    def test_view_form_class(self):
        form_class = ClientUpdateView.form_class
        self.assertEqual(form_class, ClientForm)

    def test_view_context_objects(self):
        resp = self.client.get(f'/clients/update/{self.client_obj.slug}/')
        context_list = ['form', 'client_name']
        for cont in context_list:
            self.assertIn(cont, resp.context)
        self.assertEqual(resp.context['client_name'], self.client_obj.name)


class ClientFilesCreateViewTestCase(TestCase):
    def setUp(self):
        StuffUsers.objects.create_superuser(username='admin', password='admin')
        self.client.login(username='admin', password='admin')
        self.client_obj = Clients.objects.create(
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

    def test_url(self):
        resp = self.client.get(f'/clients/detail/{self.client_obj.slug}/add/file/')
        self.assertEqual(resp.status_code, 200)

    def test_url_name(self):
        resp = self.client.get(reverse_lazy('client_create_file', kwargs={'client_slug': self.client_obj.slug}))
        self.assertEqual(resp.status_code, 200)

    def test_view_template(self):
        resp = self.client.get(f'/clients/detail/{self.client_obj.slug}/add/file/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'client_app/add_client_file.html')

    def test_user_not_login(self):
        self.client.logout()
        resp = self.client.get(f'/clients/detail/{self.client_obj.slug}/add/file/')
        self.assertEqual(resp.status_code, 302)
        redirect_url = f'/stuff/user/login/?next=%2Fclients%2Fdetail%2F{self.client_obj.slug}%2Fadd%2Ffile%2F'
        self.assertRedirects(resp, redirect_url)

    def test_view_kwargs_name(self):
        slug_kwargs_name = ClientFilesCreateView.slug_url_kwarg
        self.assertEqual(slug_kwargs_name, 'client_slug')

    def test_view_model(self):
        view_model = ClientFilesCreateView.model
        self.assertEqual(view_model, ClientFiles)

    def test_view_form_class(self):
        form_class = ClientFilesCreateView.form_class
        self.assertEqual(form_class, ClientFilesForms)

    def test_view_form_valid(self):
        file = SimpleUploadedFile("file.pdf", b"file_content")
        data = {'title': 'text', 'description': 'text', 'file': file}
        resp = self.client.post(f'/clients/detail/{self.client_obj.slug}/add/file/', data=data)
        self.assertEqual(resp.status_code, 302)
        redirect_url = reverse_lazy('client_detail', kwargs={'client_slug': self.client_obj.slug})
        self.assertRedirects(resp, redirect_url)
        self.assertTrue(self.client_obj.files.exists())


class DeleteClientFileViewTestCase(TestCase):
    def setUp(self):
        StuffUsers.objects.create_superuser(username='admin', password='admin')
        self.client.login(username='admin', password='admin')
        self.client_obj = Clients.objects.create(
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
        file = SimpleUploadedFile("file.pdf", b"file_content")
        data = {'title': 'text', 'description': 'text', 'file': file, 'client': self.client_obj}
        self.file_obj = ClientFiles.objects.create(**data)

    def test_user_not_login(self):
        self.client.logout()
        resp = self.client.get(f'/clients/files/delete/{self.file_obj.slug}/')
        self.assertEqual(resp.status_code, 302)
        redirect_url = f'/stuff/user/login/?next=%2Fclients%2Ffiles%2Fdelete%2F{self.file_obj.slug}%2F'
        self.assertRedirects(resp, redirect_url)


class ContactPersonsListViewTestCase(TestCase):
    def setUp(self):
        StuffUsers.objects.create_superuser(username='admin', password='admin')
        self.client.login(username='admin', password='admin')
        self.client_obj = Clients.objects.create(
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
        ContactPersons.objects.create(
            client=self.client_obj,
            first_name='t',
            second_name='e',
            post='s',
            email='t@mail.ru',
            phone='79123647542'
        )

    def test_url(self):
        resp = self.client.get(f'/clients/detail/{self.client_obj.slug}/contact_persons/')
        self.assertEqual(resp.status_code, 200)

    def test_url_name(self):
        resp = self.client.get(reverse_lazy('cp_list', kwargs={'client_slug': self.client_obj.slug}))
        self.assertEqual(resp.status_code, 200)

    def test_view_template(self):
        resp = self.client.get(f'/clients/detail/{self.client_obj.slug}/contact_persons/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'client_app/contact_persons_list.html')

    def test_user_not_login(self):
        self.client.logout()
        resp = self.client.get(f'/clients/detail/{self.client_obj.slug}/contact_persons/')
        self.assertEqual(resp.status_code, 302)
        redirect_url = f'/stuff/user/login/?next=%2Fclients%2Fdetail%2F{self.client_obj.slug}%2Fcontact_persons%2F'
        self.assertRedirects(resp, redirect_url)

    def test_view_model(self):
        view_model = ContactPersonsListView.model
        self.assertEqual(view_model, ContactPersons)

    def test_view_context_objects(self):
        resp = self.client.get(f'/clients/detail/{self.client_obj.slug}/contact_persons/')
        cont = Clients.objects.get(slug=self.client_obj.slug)
        self.assertIn('client', resp.context)
        self.assertIn('contact_persons', resp.context)
        self.assertEqual(resp.context['client'], cont)

    def test_view_queryset(self):
        resp = self.client.get(f'/clients/detail/{self.client_obj.slug}/contact_persons/')
        queryset = ContactPersons.objects.select_related('client').filter(client__slug=self.client_obj.slug).all()
        self.assertEqual(resp.status_code, 200)
        self.assertQuerysetEqual(resp.context['contact_persons'], queryset)


class ContactPersonCreateViewTestCase(TestCase):
    def setUp(self):
        StuffUsers.objects.create_superuser(username='admin', password='admin')
        self.client.login(username='admin', password='admin')
        self.client_obj = Clients.objects.create(
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

    def test_url(self):
        resp = self.client.get(f'/clients/detail/{self.client_obj.slug}/contact_persons/add')
        self.assertEqual(resp.status_code, 200)

    def test_url_name(self):
        resp = self.client.get(reverse_lazy('cp_create', kwargs={'client_slug': self.client_obj.slug}))
        self.assertEqual(resp.status_code, 200)

    def test_view_template(self):
        resp = self.client.get(f'/clients/detail/{self.client_obj.slug}/contact_persons/add')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'client_app/contact_persons_create.html')

    def test_user_not_login(self):
        self.client.logout()
        resp = self.client.get(f'/clients/detail/{self.client_obj.slug}/contact_persons/add')
        self.assertEqual(resp.status_code, 302)
        redirect_url = f'/stuff/user/login/?next=%2Fclients%2Fdetail%2F{self.client_obj.slug}%2Fcontact_persons%2Fadd'
        self.assertRedirects(resp, redirect_url)

    def test_view_model(self):
        view_model = ContactPersonCreateView.model
        self.assertEqual(view_model, ContactPersons)

    def test_view_form_class(self):
        form_class = ContactPersonCreateView.form_class
        self.assertEqual(form_class, ContactPersonsForms)

    def test_view_form_valid(self):
        data = dict(
            first_name='name',
            second_name='sec_name',
            post='post',
            email='cp@mail.ru',
            phone_0='RU',
            phone_1='79123647542'
        )
        url = reverse_lazy('cp_create', kwargs={'client_slug': self.client_obj.slug})
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 302)
        redirect_url = reverse_lazy('cp_list', kwargs={'client_slug': self.client_obj.slug})
        self.assertRedirects(resp, redirect_url)
        self.assertTrue(self.client_obj.contact_persons.exists())


class ContactPersonDetailViewTestCase(TestCase):
    def setUp(self):
        StuffUsers.objects.create_superuser(username='admin', password='admin')
        self.client.login(username='admin', password='admin')
        self.client_obj = Clients.objects.create(
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
        self.c_person = ContactPersons.objects.create(
            client=self.client_obj,
            first_name='t',
            second_name='e',
            post='s',
            email='t@mail.ru',
            phone='79123647542'
        )

    def test_url(self):
        resp = self.client.get(f'/contact_persons/detail/{self.c_person.pk}/')
        self.assertEqual(resp.status_code, 200)

    def test_url_name(self):
        resp = self.client.get(reverse_lazy('cp_detail', kwargs={'pk': self.c_person.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_view_template(self):
        resp = self.client.get(f'/contact_persons/detail/{self.c_person.pk}/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'client_app/contact_persons_detail.html')

    def test_user_not_login(self):
        self.client.logout()
        resp = self.client.get(f'/contact_persons/detail/{self.c_person.pk}/')
        self.assertEqual(resp.status_code, 302)
        redirect_url = f'/stuff/user/login/?next=%2Fcontact_persons%2Fdetail%2F{self.c_person.pk}%2F'
        self.assertRedirects(resp, redirect_url)

    def test_view_model(self):
        view_model = ContactPersonDetailView.model
        self.assertEqual(view_model, ContactPersons)

    def test_view_context_objects(self):
        resp = self.client.get(f'/contact_persons/detail/{self.c_person.pk}/')
        cont = self.c_person
        self.assertIn('contact_person', resp.context)
        self.assertEqual(resp.context['contact_person'], cont)


class ContactPersonUpdateViewTestCase(TestCase):
    pass


class ContactPersonDeleteViewTestCase(TestCase):
    pass
