from django.http import Http404


def chek_access_rights(user) -> None:
    if user.role not in ['dispatcher', 'admin']:
        raise Http404
    return None


def chek_is_staff(user):
    if not user.is_staff:
        raise Http404
    return None
