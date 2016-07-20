# Django Country Site

## Getting Started

Add the middleware just before `LocaleMiddleware`
```
# settings.py

MIDDLEWARE_CLASSES = (
    ...
    'django_country_site.middleware.CountryLocaleMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    ...
)
```

Add a list of tuples indicating available countries and their languages by default or None if you want to detect it
```
# settings.py

COUNTRIES_LANGUAGE = [
    ('us', 'en'),
    ('pe', 'es'),
    ('ru', 'ru'),
    ('br', None),
]
```

Choose a country by default in case it was unable to detect it
```
# settings.py

COUNTRY_CODE = 'us'
```
