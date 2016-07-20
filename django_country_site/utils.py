import re

from collections import OrderedDict
from django.contrib.gis.geoip2 import GeoIP2
from django.conf import settings
from django.utils import lru_cache

COUNTRY_SESSION_KEY = '_country'

country_code_prefix_re = re.compile(r'^/([\w]{2})(/|$)')


@lru_cache.lru_cache()
def get_countries_and_language():
    return OrderedDict(settings.COUNTRIES_LANGUAGE)

def get_country_from_request(request):
    country_code = get_country_from_path(request.path_info)
    if country_code is not None:
        return country_code

    supported_country_codes = get_countries_and_language()

    if hasattr(request, 'session'):
        country_code = request.session.get(COUNTRY_SESSION_KEY)
        if country_code in supported_country_codes and country_code is not None:
            return country_code

    return get_country_from_ip(request)

def get_country_from_path(path):
    regex_match = country_code_prefix_re.match(path)
    if not regex_match:
        return None
    country_code = regex_match.group(1)
    try:
        return country_code
    except LookupError:
        return None

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_country_from_ip(request):
    supported_country_codes = get_countries_and_language()

    try:
        g = GeoIP2()
        country_code = settings.COUNTRY_CODE
        res_country_code = g.country_code(get_client_ip(request)).lower()
        if res_country_code in supported_country_codes and res_country_code is not None:
            country_code = res_country_code
        return country_code
    except:
        return settings.COUNTRY_CODE