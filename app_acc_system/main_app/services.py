from stuff_app.models import StuffUsers, StuffUsersNotifications


def get_base_notification_text(application_obj) -> str:
    priorities = {'Accident': 'Авария', 'Urgent': 'Срочно', 'Planned': 'Планово'}
    types = {'Planned': 'Плановая', 'Unplanned': 'Внеплановая'}

    base_text = f'<strong>Номер заявки:</strong> {application_obj.pk}.<br>' \
        f'<strong>Тема</strong>: {application_obj.subject}<br>' \
        f'<strong>Описание:</strong> {application_obj.description}<br>' \
        f'<strong>Тип:</strong> {types.get(application_obj.type)}<br>' \
        f'<strong>Приоритет:</strong> {priorities.get(application_obj.priority)}<br>' \
        f'<strong>Клиент:</strong> {application_obj.client.name}<br>' \
        f'<strong>Оборудование:</strong> {", ".join(equip.name for equip in application_obj.equipment.all())}<br>' \
        f'<strong>Контактное лицо:</strong> {application_obj.contact_person.get_full_name}'
    return base_text


def new_application_notification(application_obj) -> None:
    users = StuffUsers.objects.filter(notifications_active=True)
    subject = 'Новая заявка'
    text = get_base_notification_text(application_obj)
    notifications = [StuffUsersNotifications(user=user, notify_subject=subject, notify_text=text) for user in users]
    StuffUsersNotifications.objects.bulk_create(notifications)


def new_comment_notification(application_obj, comment_body, is_public) -> None:
    user = application_obj.executor
    if user:
        subjects = {True: 'Новый публичный комментарии к заявке', False: 'Новый приватный комментарии к заявке'}
        subject = subjects.get(is_public)
        text = f'<strong>Комментарий:</strong> {comment_body}<br>' + get_base_notification_text(application_obj)
        StuffUsersNotifications.objects.create(user=user, notify_subject=subject, notify_text=text)
    return


def application_status_change_notification(application_obj) -> None:
    user = application_obj.executor
    if user:
        statuses = {
            'New': 'Новая',
            'At work': 'В работе',
            'Postponed': 'Отложена',
            'Solved': 'Решена',
            'Closed': 'Закрыта'
        }
        subject = 'Смена статуса заявки'
        new_status = statuses.get(application_obj.status)
        text = f'<strong>Новый статус:</strong> {new_status} <br>' + get_base_notification_text(application_obj)
        StuffUsersNotifications.objects.create(user=user, notify_subject=subject, notify_text=text)
    return


def new_executor_application_notification(application_obj) -> None:
    user = application_obj.executor
    if user:
        subject = 'Вас назначили ответственным за заявку'
        text = get_base_notification_text(application_obj)
        StuffUsersNotifications.objects.create(user=user, notify_subject=subject, notify_text=text)
    return
