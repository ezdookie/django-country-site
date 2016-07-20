from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.utils.functional import cached_property
from django.core.urlresolvers import (
    get_resolver, get_script_prefix, is_valid_path
)
from .trans_country import (
    activate_country, get_country, set_country
)
from .utils import (
    get_countries_and_language, get_country_from_path, get_country_from_request
)
from .urls import CountryRegexURLResolver


class CountryLocaleMiddleware(object):
    response_redirect_class = HttpResponseRedirect

    def process_request(self, request):
        supported_country_codes = get_countries_and_language()
        country_code = get_country_from_request(request)

        if country_code in supported_country_codes and country_code is not None:
            activate_country(country_code)
            set_country(country_code, request)
            request.COUNTRY_CODE = country_code

            lang_code = supported_country_codes[country_code]
            if lang_code is not None:
                request.session[LANGUAGE_SESSION_KEY] = lang_code

    def process_response(self, request, response):
        country_code = get_country()
        country_from_path = get_country_from_path(request.path_info)
        if (response.status_code == 404 and not country_from_path
                and self.is_language_prefix_patterns_used):
            urlconf = getattr(request, 'urlconf', None)
            country_path = '/%s%s' % (country_code, request.path_info)
            path_valid = is_valid_path(country_path, urlconf)
            path_needs_slash = (
                not path_valid and (
                    settings.APPEND_SLASH and not country_path.endswith('/')
                    and is_valid_path('%s/' % country_path, urlconf)
                )
            )

            if path_valid or path_needs_slash:
                script_prefix = get_script_prefix()
                language_url = request.get_full_path(force_append_slash=path_needs_slash).replace(
                    script_prefix,
                    '%s%s/' % (script_prefix, country_code),
                    1
                )
                return self.response_redirect_class(language_url)

        return response

    @cached_property
    def is_language_prefix_patterns_used(self):
        for url_pattern in get_resolver(None).url_patterns:
            if isinstance(url_pattern, CountryRegexURLResolver):
                return True
        return False