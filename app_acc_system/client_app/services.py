from django.http import Http404


def chek_is_staff(user) -> None:
    if not user.is_staff:
        raise Http404
    return None
