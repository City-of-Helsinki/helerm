"""
Django settings for helerm project.
"""

import environ
import logging
import os

from django.utils.translation import ugettext_lazy as _

CONFIG_FILE_NAME = "config_dev.env"

# This will get default settings, as Django has not yet initialized
# logging when importing this file
logger = logging.getLogger(__name__)

root = environ.Path(__file__) - 2  # two levels back in hierarchy
env = environ.Env(
    DEBUG=(bool, False),
    DJANGO_LOG_LEVEL=(str, 'INFO'),
    CONN_MAX_AGE=(int, 0),
    DATABASE_URL=(str, 'postgres:///helerm'),
    HEL_SITE_TYPE=(str, 'dev'),
    TOKEN_AUTH_ACCEPTED_AUDIENCE=(str, ''),
    TOKEN_AUTH_SHARED_SECRET=(str, ''),
    SECRET_KEY=(str, ''),
    ALLOWED_HOSTS=(list, []),
    ADMINS=(list, []),
    SECURE_PROXY_SSL_HEADER=(tuple, None),
    MEDIA_ROOT=(environ.Path(), root('media')),
    STATIC_ROOT=(environ.Path(), root('static')),
    MEDIA_URL=(str, '/media/'),
    STATIC_URL=(str, '/static/'),
    TRUST_X_FORWARDED_HOST=(bool, False),
    SENTRY_DSN=(str, ''),
    SENTRY_ENVIRONMENT=(str, 'development'),
    COOKIE_SECURE=(bool, True),
    COOKIE_PREFIX=(str, 'helerm'),
    PATH_PREFIX=(str, '/'),
    INTERNAL_IPS=(list, []),
    HELERM_JHS191_EXPORT_DESCRIPTION=(str, 'exported from undefined environment'),
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = root()

# Helsinki specific setting specifying whether the site
# is in ('dev','test' or 'production'). Only sets the background
# color in admin for HelERM
SITE_TYPE=env('HEL_SITE_TYPE')

# Django environ has a nasty habit of complanining at level
# WARN about env file not being preset. Here we pre-empt it.
env_file_path = os.path.join(BASE_DIR, CONFIG_FILE_NAME)
if os.path.exists(env_file_path):
    # Logging configuration is not available at this point
    print(f'Reading config from {env_file_path}')
    environ.Env.read_env(env_file_path)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')
ADMINS = env('ADMINS')

INTERNAL_IPS = env('INTERNAL_IPS',
                   default=(['127.0.0.1'] if DEBUG else []))

# Application definition

INSTALLED_APPS = [
    'helusers.apps.HelusersConfig',
    'helusers.apps.HelusersAdminConfig',
    'django.contrib.postgres',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'helusers.providers.helsinki',
    'adminsortable2',
    'django_filters',

    'metarecord',
    'users',
]

if env('SENTRY_DSN'):
    import raven

    RAVEN_CONFIG = {
        'dsn': env('SENTRY_DSN'),
        # Needs to change if settings.py is not in an immediate child of the project
        'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
        'environment': env('SENTRY_ENVIRONMENT'),
    }
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'helerm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'helerm.wsgi.application'

DATABASES = {
    'default': env.db()
}

# Persistent connections
# https://docs.djangoproject.com/en/3.1/ref/settings/#conn-max-age
DATABASES['default']['CONN_MAX_AGE'] = env('CONN_MAX_AGE')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'timestamped_named': {
            'format': '%(asctime)s %(name)s %(levelname)s: %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'timestamped_named',
        },
        # Just for reference, not used
        'blackhole': {
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('fi', _('Finnish')),
    ('en', _('English')),
)

TIME_ZONE = 'Europe/Helsinki'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


STATIC_URL = env('STATIC_URL')
MEDIA_URL = env('MEDIA_URL')
STATIC_ROOT = env('STATIC_ROOT')
MEDIA_ROOT = env('MEDIA_ROOT')

# Whether to trust X-Forwarded-Host headers for all purposes
# where Django would need to make use of its own hostname
# fe. generating absolute URLs pointing to itself
# Most often used in reverse proxy setups
USE_X_FORWARDED_HOST = env('TRUST_X_FORWARDED_HOST')

# HelERM is a very public API
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True

CSRF_COOKIE_NAME = '{}-csrftoken'.format(env('COOKIE_PREFIX'))
CSRF_COOKIE_PATH = env('PATH_PREFIX')
CSRF_COOKIE_SECURE = env('COOKIE_SECURE')
SESSION_COOKIE_NAME = '{}-sessionid'.format(env('COOKIE_PREFIX'))
SESSION_COOKIE_PATH = env('PATH_PREFIX')
SESSION_COOKIE_SECURE = env('COOKIE_SECURE')

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SOCIALACCOUNT_PROVIDERS = {
    'helsinki': {
        'VERIFIED_EMAIL': True
    }
}
SOCIALACCOUNT_ADAPTER = 'helusers.adapter.SocialAccountAdapter'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_ON_GET = True

SITE_ID = 1

JWT_AUTH = {
    'JWT_PAYLOAD_GET_USER_ID_HANDLER': 'helusers.jwt.get_user_id_from_payload_handler',
    'JWT_AUDIENCE': env('TOKEN_AUTH_ACCEPTED_AUDIENCE'),
    'JWT_SECRET_KEY': env('TOKEN_AUTH_SHARED_SECRET'),
}

# Used for descriptive comment in the headers of JHS191 XML export
XML_EXPORT_DESCRIPTION = env('HELERM_JHS191_EXPORT_DESCRIPTION')

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'helusers.jwt.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'metarecord.pagination.MetaRecordPagination',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',

    'DEFAULT_PARSER_CLASSES': (
        # Django REST framework's default parser settings
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',

        # Parser settings for djangorestframework-xml
        'rest_framework_xml.parsers.XMLParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        # Django REST framework's default renderer settings
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',

        # Renderer settings for djangorestframework-xml
        'rest_framework_xml.renderers.XMLRenderer',
    ),
}

# Django SECRET_KEY setting, used for password reset links and such
SECRET_KEY = env('SECRET_KEY')
# If a secret key was not supplied elsewhere, generate a random one and log
# a warning (note that logging is not configured yet). This means that any
# functionality expecting SECRET_KEY to stay same will break upon restart.
# Should not be a problem for development.
if not SECRET_KEY:
    logger.warn("SECRET_KEY was not defined in configuration. Generating an ephemeral key.")
    import random
    system_random = random.SystemRandom()
    SECRET_KEY = ''.join([system_random.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
                         for i in range(64)])

# local_settings.py is useful for overriding settings not available
# through environment and when developing new stuff
local_settings_path = os.path.join(BASE_DIR, "local_settings.py")
if os.path.exists(local_settings_path):
    with open(local_settings_path) as fp:
        code = compile(fp.read(), local_settings_path, 'exec')
    exec(code, globals(), locals())
