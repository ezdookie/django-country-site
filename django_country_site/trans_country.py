from threading import local
from django.conf import settings
from .utils import COUNTRY_SESSION_KEY

_active = local()


def activate_country(country):
    if not country: return
    _active.value = country

def get_country():
    t = getattr(_active, "value", None)
    return t if not None else settings.COUNTRY_CODE

def set_country(country_code, request):
    if hasattr(request, 'session'):
        request.session[COUNTRY_SESSION_KEY] = country_code