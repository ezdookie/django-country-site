import re

from django.core.urlresolvers import RegexURLResolver
from .trans_country import get_country


class CountryRegexURLResolver(RegexURLResolver):
    def __init__(self, urlconf_name, default_kwargs=None, app_name=None, namespace=None):
        super(CountryRegexURLResolver, self).__init__(
            None, urlconf_name, default_kwargs, app_name, namespace)

    @property
    def regex(self):
        country_code = get_country()
        if country_code not in self._regex_dict:
            regex_compiled = re.compile('^%s/' % country_code, re.UNICODE)
            self._regex_dict[country_code] = regex_compiled
        return self._regex_dict[country_code]

def country_patterns(prefix, *args):
    pattern_list = [prefix] + list(args)
    return [CountryRegexURLResolver(pattern_list)]