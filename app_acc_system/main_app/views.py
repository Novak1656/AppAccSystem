import io
import os
import shutil
import xlsxwriter
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.core.files import File
from django.db.models import Q, Count, Case, When, Sum, F, IntegerField
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils import dateformat
from django.utils.timezone import now
from django.views.generic import ListView, CreateView
from .models import Applications, ApplicationComments, Reports
from client_app.models import Clients
from .forms import ApplicationsForms, ApplicationCommentsForms
from stuff_app.models import StuffUsers


class ApplicationsListView(AccessMixin, ListView):
    model = Applications
    template_name = 'main_app/applications_list.html'
    context_object_name = 'applications'
    login_url = reverse_lazy('stuff_user_auth')

    def get_queryset(self):
        return Applications.objects.select_related('client', 'contact_person').all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ApplicationsListView, self).get_context_data(**kwargs)
        context['clients'] = Clients.objects.values('pk', 'name').all()
        return context


class ApplicationCreateView(AccessMixin, CreateView):
    model = Applications
    template_name = 'main_app/applications_create.html'
    form_class = ApplicationsForms
    success_url = reverse_lazy('app_list')
    login_url = reverse_lazy('stuff_user_auth')

    def get_form_kwargs(self):
        kwargs = {
            'client_id': self.request.GET.get('client'),
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
            })
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.client = Clients.objects.get(pk=self.request.GET.get('client'))
        self.object.save()
        form.save_m2m()
        return super(ApplicationCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ApplicationCreateView, self).get_context_data(**kwargs)
        context['client'] = Clients.objects.get(pk=self.request.GET.get('client'))
        return context


class ApplicationDetailView(AccessMixin, CreateView):
    model = Applications
    template_name = 'main_app/applications_detail.html'
    login_url = reverse_lazy('stuff_user_auth')
    slug_url_kwarg = 'app_slug'
    form_class = ApplicationCommentsForms

    def get_success_url(self):
        return reverse('app_detail', kwargs={'app_slug': self.kwargs['app_slug']})
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.application = self.get_context_data().get('application')
        self.object.save()
        return super(ApplicationDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ApplicationDetailView, self).get_context_data(**kwargs)
        context['executors'] = StuffUsers.objects.filter(role='executor').all()
        context['application'] = Applications.objects.select_related(
            'client', 'contact_person', 'contract', 'executor'
        ).prefetch_related('equipment', 'comments').get(slug=self.kwargs['app_slug'])
        status_list = {
            'New': [('At work', 'В работе'), ('Postponed', 'Отложена')],
            'At work': [('Postponed', 'Отложена'), ('Solved', 'Решена')],
            'Postponed': [('At work', 'В работе'), ('Solved', 'Решена')],
            'Solved': [('At work', 'В работе'), ('Postponed', 'Отложена'), ('Closed', 'Закрыта')],
        }
        context['status_list'] = status_list.get(context['application'].status)
        return context


@login_required
def set_application_executor(request, app_slug):
    application = Applications.objects.get(slug=app_slug)
    executor = StuffUsers.objects.get(pk=request.GET.get('executor'))
    application.executor = executor
    application.save()
    return redirect('app_detail', app_slug=app_slug)


@login_required
def update_comment_body(request, comment_pk):
    ApplicationComments.objects.filter(pk=comment_pk).update(comment_body=request.POST[f'comment_body{comment_pk}'])
    return redirect(request.META['HTTP_REFERER'])


@login_required
def delete_comment(request, comment_pk):
    ApplicationComments.objects.get(pk=comment_pk).delete()
    return redirect(request.META['HTTP_REFERER'])


@login_required
def delete_application(request, app_slug):
    application = Applications.objects.prefetch_related('comments').get(slug=app_slug)
    if application.comments.all().filter(~Q(file=None)).exists():
        files_path = os.path.join(settings.BASE_DIR, f"media/Comment_files/{application.subject}/")
        shutil.rmtree(files_path)
    application.delete()
    return redirect('app_list')


@login_required
def change_application_status(request, app_slug):
    status = request.GET.get('status')
    if status == 'Closed':
        Applications.objects.filter(slug=app_slug).update(status=status, closing_date=now())
    else:
        Applications.objects.filter(slug=app_slug).update(status=status)
    return redirect('app_detail', app_slug=app_slug)


class ReportsListView(AccessMixin, ListView):
    model = Reports
    template_name = 'main_app/reports_list.html'
    context_object_name = 'reports'
    login_url = reverse_lazy('stuff_user_auth')

    def get_queryset(self):
        report_type = self.request.GET.get('report_type', None)
        if report_type:
            if report_type == 'clients':
                return Reports.objects.filter(type='Clients report').all()
            elif report_type == 'executors':
                return Reports.objects.filter(type='Executors report').all()
            else:
                client_pk = self.request.GET.get('client_pk')
                return Reports.objects.filter(client__pk=client_pk).all()
        return Reports.objects.all()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(ReportsListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ReportsListView, self).get_context_data(**kwargs)
        context['clients'] = Clients.objects.prefetch_related('reports').all()
        report_type = self.request.GET.get('report_type', None)
        if report_type:
            context['cur_report_type'] = report_type
        client_pk = self.request.GET.get('client_pk')
        if client_pk:
            context['cur_client'] = context['clients'].get(pk=client_pk)
        context['clients_with_reports'] = [(client.pk, client.name, client.reports.count()) for client in context.get('clients') if client.reports.all().exists()]
        context['all_reports_cnt'] = self.model.objects.all().count()

        rep_cnt_list = Reports.objects.all().values('type').annotate(
            cnt=Count(
                Case(
                    When(type='Client report', then=1),
                    When(type='Clients report', then=1),
                    When(type='Executors report', then=1),
                    output_field=IntegerField(),
                    default=0
                )
            )
        )
        for rep_cnt in rep_cnt_list:
            if rep_cnt.get('type') == 'Client report':
                context['client_rep_cnt'] = rep_cnt.get('cnt')
            elif rep_cnt.get('type') == 'Clients report':
                context['clients_rep_cnt'] = rep_cnt.get('cnt')
            else:
                context['executors_rep_cnt'] = rep_cnt.get('cnt')
        context['cur_date'] = dateformat.format(now().date(), 'Y-m-d')
        return context


@login_required
def report_client_create_view(request):
    client = Clients.objects.get(pk=request.GET.get('client'))
    detail = request.GET.get('detail')
    client_applications = Applications.objects.filter(Q(client=client) & Q(status='Closed'))

    output = io.BytesIO()

    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    if not detail:
        not_detail_report_data = client_applications.\
            annotate(
                plane=Count(Case(When(type='Planned', then=1), output_field=IntegerField())),
                unplane=Count(Case(When(type='Unplanned', then=1), output_field=IntegerField())))\
            .aggregate(
                plane_cnt=Sum('plane'),
                unplane_cnt=Sum('unplane'),
                sum=Sum('plane')+Sum('unplane')
            )

        exel_data = list(zip(['Плановая', 'Внеплановая', 'Все заявки:'], not_detail_report_data))

        worksheet.write('A1', 'Тип заявки')
        worksheet.write('B1', 'Количество')

        for row, (row_name, value) in enumerate(exel_data, start=1):
            worksheet.write(row, 0, row_name)
            worksheet.write(row, 1, not_detail_report_data.get(value, 0))
    else:
        types = {'Planned': 'Плановая', 'Unplanned': 'Внеплановая', 'All': 'Все заявки'}
        detail_report_data = {'Плановая': '', 'Внеплановая': '', 'Все заявки': ''}

        for type_app, label in types.items():
            if type_app == 'All':
                applications = client_applications
            else:
                applications = client_applications.filter(type=type_app)

            queryset = applications\
                .annotate(
                    accident=Count(
                        Case(When(priority='Accident', then=1), output_field=IntegerField())
                    ),
                    urgent=Count(
                        Case(When(priority='Urgent', then=1), output_field=IntegerField())
                    ),
                    planned=Count(
                        Case(When(priority='Planned', then=1), output_field=IntegerField())
                    )
                ).aggregate(
                    acc_cnt=Sum('accident'),
                    urg_cnt=Sum('urgent'),
                    plan_cnt=Sum('planned'),
                    sum=Sum('accident') + Sum('urgent') + Sum('planned')
                )
            detail_report_data[label] = list(
                zip(['Авария', 'Срочно', 'Планово', 'Все приоритеты: '], queryset.values())
            )

        worksheet.write('A1', 'Тип заявки')
        worksheet.write('B1', 'Приоритет')
        worksheet.write('C1', 'Количество')

        worksheet.merge_range('A2:A5', 'Плановая')
        worksheet.merge_range('A6:A9', 'Внеплановая')
        worksheet.merge_range('A10:A13', 'Все заявки:')

        start_row = 1
        for data in detail_report_data.values():
            for row_name, row_value in data:
                worksheet.write(start_row, 1, row_name)
                if row_value:
                    worksheet.write(start_row, 2, row_value)
                else:
                    worksheet.write(start_row, 2, 0)
                start_row += 1

    workbook.close()
    output.seek(0)

    Reports.objects.create(
        type='Client report',
        client=client,
        file=File(output, name=f'report_{client.name.lower()}_{dateformat.format(now(), "dbY_H_i_s")}.xlsx')
    )
    output.close()
    return redirect(f"{reverse('reports_list')}?report_type=client&client_pk={client.pk}")


@login_required
def report_clients_create_view(request):
    date1, date2 = request.GET.get('date1'), request.GET.get('date2')
    apps = Applications.objects.select_related('client').filter(created_at__date__range=(date1, date2))\
        .values(name=F('client__name'))\
        .annotate(
            created_apps=Count('client'),
            close_apps=Count(Case(When(status='Closed', then=1), output_field=IntegerField())),
            failed_apps=Count(Case(When(deadline__lt=F('closing_date'), then=1), output_field=IntegerField()))
    )

    output = io.BytesIO()

    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    my_format = workbook.add_format()
    my_format.set_align('vcenter')

    worksheet.merge_range('A1:A2', 'Клиент', my_format)
    worksheet.merge_range('B1:B2', 'Создано за период', my_format)
    worksheet.merge_range('C1:D1', 'Решено за период', my_format)
    worksheet.write('C2', 'Решено', my_format)
    worksheet.write('D2', 'Из них просрочено', my_format)

    for row, data in enumerate(apps, start=2):
        for col, value in enumerate(data.values()):
            worksheet.write(row, col, value)

    workbook.close()
    output.seek(0)

    Reports.objects.create(
        type='Clients report',
        file=File(output, name=f'report_clients_{dateformat.format(now(), "dbY_H_i_s")}.xlsx')
    )

    output.close()
    return redirect(f"{reverse('reports_list')}?report_type=clients")


@login_required
def report_executors_create_view(request):
    date1, date2 = request.GET.get('date1'), request.GET.get('date2')
    executors_res = Applications.objects.select_related('executor')\
        .filter(Q(closing_date__date__range=(date1, date2)) & ~Q(executor=None))\
        .values(name=F('executor__username'))\
        .annotate(
            close_apps=Count(Case(When(status='Closed', then=1), output_field=IntegerField())),
            failed_apps=Count(Case(When(deadline__lt=F('closing_date'), then=1), output_field=IntegerField()))
    )
    final_results = executors_res.aggregate(
        close_apps_sum=Sum('close_apps'),
        failed_apps_sum=Sum('failed_apps')
    )

    output = io.BytesIO()

    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    worksheet.write('A1', 'Сотрудник')
    worksheet.write('B1', 'Решено')
    worksheet.write('C1', 'Из них просрочено')

    last_row = 0
    print(executors_res)
    for row, data in enumerate(executors_res, start=1):
        for col, value in enumerate(data.values()):
            worksheet.write(row, col, value)
        last_row = row
    last_row += 1

    worksheet.write(last_row, 0, 'Итого: ')
    worksheet.write(last_row, 1, final_results.get('close_apps_sum'))
    worksheet.write(last_row, 2, final_results.get('failed_apps_sum'))

    workbook.close()
    output.seek(0)

    Reports.objects.create(
        type='Executors report',
        file=File(output, name=f'report_executors_{dateformat.format(now(), "dbY_H_i_s")}.xlsx')
    )

    output.close()

    return redirect(request.META['HTTP_REFERER'])


@login_required
def delete_report_view(request):
    rep_pk = request.GET.get('rep_pk')
    Reports.objects.get(pk=rep_pk).delete()
    return redirect(request.META['HTTP_REFERER'])
