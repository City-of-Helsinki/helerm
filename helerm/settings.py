"""
Django settings for helerm project.
"""

import logging
import os
import subprocess

import environ
import sentry_sdk
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.django import DjangoIntegration

CONFIG_FILE_NAME = "config_dev.env"

# This will get default settings, as Django has not yet initialized
# logging when importing this file
logger = logging.getLogger(__name__)


def get_git_revision_hash() -> str:
    """
    Retrieve the git hash for the underlying git repository or die trying

    We need a way to retrieve git revision hash for sentry reports
    I assume that if we have a git repository available we will
    have git-the-comamand as well
    """
    try:
        # We are not interested in gits complaints
        git_hash = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL, encoding="utf8"
        )
    # ie. "git" was not found
    # should we return a more generic meta hash here?
    # like "undefined"?
    except FileNotFoundError:
        git_hash = "git_not_available"
    except subprocess.CalledProcessError:
        # Ditto
        git_hash = "no_repository"
    return git_hash.rstrip()


root = environ.Path(__file__) - 2  # two levels back in hierarchy
env = environ.Env(
    DEBUG=(bool, False),
    DJANGO_LOG_LEVEL=(str, "INFO"),
    CONN_MAX_AGE=(int, 0),
    DATABASE_URL=(str, "postgres:///helerm"),
    HEL_SITE_TYPE=(str, "dev"),
    TOKEN_AUTH_ACCEPTED_AUDIENCE=(str, ""),
    TOKEN_AUTH_SHARED_SECRET=(str, ""),
    SECRET_KEY=(str, ""),
    ALLOWED_HOSTS=(list, []),
    ADMINS=(list, []),
    SECURE_PROXY_SSL_HEADER=(tuple, None),
    MEDIA_ROOT=(environ.Path(), root("media")),
    STATIC_ROOT=(environ.Path(), root("static")),
    MEDIA_URL=(str, "/media/"),
    STATIC_URL=(str, "/static/"),
    TRUST_X_FORWARDED_HOST=(bool, False),
    SENTRY_DSN=(str, ""),
    SENTRY_ENVIRONMENT=(str, "development"),
    COOKIE_SECURE=(bool, True),
    COOKIE_PREFIX=(str, "helerm"),
    PATH_PREFIX=(str, "/"),
    INTERNAL_IPS=(list, []),
    HELERM_JHS191_EXPORT_DESCRIPTION=(str, "exported from undefined environment"),
    ELASTICSEARCH_HOST=(str, "helerm_elasticsearch:9200"),
    ELASTICSEARCH_USERNAME=(str, ""),
    ELASTICSEARCH_PASSWORD=(str, ""),
    ELASTICSEARCH_ANALYZER_MODE=(str, "probe"),
    SOCIAL_AUTH_TUNNISTAMO_KEY=(str, ""),
    SOCIAL_AUTH_TUNNISTAMO_SECRET=(str, ""),
    SOCIAL_AUTH_TUNNISTAMO_OIDC_ENDPOINT=(str, "https://api.hel.fi/sso/openid"),
    OIDC_API_TOKEN_AUTH_AUDIENCE=(str, ""),
    OIDC_API_TOKEN_AUTH_ISSUER=(str, "https://api.hel.fi/sso"),
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = root()

# Helsinki specific setting specifying whether the site
# is in ('dev','test' or 'production'). Only sets the background
# color in admin for HelERM
SITE_TYPE = env("HEL_SITE_TYPE")

# Django environ has a nasty habit of complanining at level
# WARN about env file not being preset. Here we pre-empt it.
env_file_path = os.path.join(BASE_DIR, CONFIG_FILE_NAME)
if os.path.exists(env_file_path):
    # Logging configuration is not available at this point
    print(f"Reading config from {env_file_path}")
    environ.Env.read_env(env_file_path)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")
ADMINS = env("ADMINS")

INTERNAL_IPS = env("INTERNAL_IPS", default=(["127.0.0.1"] if DEBUG else []))

# Application definition

INSTALLED_APPS = [
    "helusers.apps.HelusersConfig",
    "helusers.apps.HelusersAdminConfig",
    "django.contrib.postgres",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "rest_framework",
    "corsheaders",
    "social_django",
    "adminsortable2",
    "django_filters",
    "django_elasticsearch_dsl",
    "django_elasticsearch_dsl_drf",
    "django_admin_json_editor",
    "metarecord",
    "search_indices",
    "users",
]

if env("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=env("SENTRY_DSN"),
        environment=env("SENTRY_ENVIRONMENT"),
        release=get_git_revision_hash(),
        integrations=[DjangoIntegration()],
    )


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "helerm.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "helerm.wsgi.application"

DATABASES = {"default": env.db()}

# Persistent connections
# https://docs.djangoproject.com/en/3.1/ref/settings/#conn-max-age
DATABASES["default"]["CONN_MAX_AGE"] = env("CONN_MAX_AGE")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "timestamped_named": {
            "format": "%(asctime)s %(name)s %(levelname)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "timestamped_named",
        },
        # Just for reference, not used
        "blackhole": {
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = "en"

LANGUAGES = (
    ("fi", _("Finnish")),
    ("en", _("English")),
)

TIME_ZONE = "Europe/Helsinki"

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)


STATIC_URL = env("STATIC_URL")
MEDIA_URL = env("MEDIA_URL")
STATIC_ROOT = env("STATIC_ROOT")
MEDIA_ROOT = env("MEDIA_ROOT")

# Whether to trust X-Forwarded-Host headers for all purposes
# where Django would need to make use of its own hostname
# fe. generating absolute URLs pointing to itself
# Most often used in reverse proxy setups
USE_X_FORWARDED_HOST = env("TRUST_X_FORWARDED_HOST")

# HelERM is a very public API
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True

CSRF_COOKIE_NAME = "{}-csrftoken".format(env("COOKIE_PREFIX"))
CSRF_COOKIE_PATH = env("PATH_PREFIX")
CSRF_COOKIE_SECURE = env("COOKIE_SECURE")
SESSION_COOKIE_NAME = "{}-sessionid".format(env("COOKIE_PREFIX"))
SESSION_COOKIE_PATH = env("PATH_PREFIX")
SESSION_COOKIE_SECURE = env("COOKIE_SECURE")

AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "helusers.tunnistamo_oidc.TunnistamoOIDCAuth",
)

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_ON_GET = True

SITE_ID = 1

JWT_AUTH = {
    "JWT_PAYLOAD_GET_USER_ID_HANDLER": "helusers.jwt.get_user_id_from_payload_handler",
    "JWT_AUDIENCE": env("TOKEN_AUTH_ACCEPTED_AUDIENCE"),
    "JWT_SECRET_KEY": env("TOKEN_AUTH_SHARED_SECRET"),
}

# Used for descriptive comment in the headers of JHS191 XML export
XML_EXPORT_DESCRIPTION = env("HELERM_JHS191_EXPORT_DESCRIPTION")

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": ("helusers.oidc.ApiTokenAuthentication",),
    "DEFAULT_PAGINATION_CLASS": "metarecord.pagination.MetaRecordPagination",
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_PARSER_CLASSES": (
        # Django REST framework's default parser settings
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        # Parser settings for djangorestframework-xml
        "rest_framework_xml.parsers.XMLParser",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        # Django REST framework's default renderer settings
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        # Renderer settings for djangorestframework-xml
        "rest_framework_xml.renderers.XMLRenderer",
    ),
}

SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"

SOCIAL_AUTH_TUNNISTAMO_KEY = env("SOCIAL_AUTH_TUNNISTAMO_KEY")
SOCIAL_AUTH_TUNNISTAMO_SECRET = env("SOCIAL_AUTH_TUNNISTAMO_SECRET")
SOCIAL_AUTH_TUNNISTAMO_OIDC_ENDPOINT = env("SOCIAL_AUTH_TUNNISTAMO_OIDC_ENDPOINT")

OIDC_API_TOKEN_AUTH = {
    # Audience that must be present in the token for the request to be
    # accepted. Value must be agreed between your SSO service and your
    # application instance. Essentially this allows your application to
    # know that the token in meant to be used with it.
    "AUDIENCE": env("OIDC_API_TOKEN_AUTH_AUDIENCE"),
    # Who we trust to sign the tokens. The library will request the
    # public signature keys from standard locations below this URL
    "ISSUER": env("OIDC_API_TOKEN_AUTH_ISSUER"),
}

# by default drf-oidc-auth allows tokens to be at most 10 minutes old
# extend that to one hour. Likely the behaviour of the underlying
# drf-oidc-auth library will change at some point:
# https://github.com/ByteInternet/drf-oidc-auth/issues/49
OIDC_AUTH = {"OIDC_LEEWAY": 60 * 60}

# Elasticsearch configuration
ELASTICSEARCH_DSL = {
    "default": {
        "hosts": env("ELASTICSEARCH_HOST"),
        "http_auth": (
            env("ELASTICSEARCH_USERNAME"),
            env("ELASTICSEARCH_PASSWORD"),
        )
        if env("ELASTICSEARCH_USERNAME") and env("ELASTICSEARCH_PASSWORD")
        else None,
    },
}

# Name of the Elasticsearch index
ELASTICSEARCH_INDEX_NAMES = {
    "search_indices.documents.action": "action",
    "search_indices.documents.function": "function",
    "search_indices.documents.classification": "classification",
    "search_indices.documents.phase": "phase",
    "search_indices.documents.record": "record",
}

# Which analyzer will be used by elasticsearch. Default is to check if raudikko
# plugin is available and use standard as a fallback. Probing can be skipped by setting
# a specific analyzer.
# Possible values are: probe, raudikko, standard
ELASTICSEARCH_ANALYZER_MODE = env("ELASTICSEARCH_ANALYZER_MODE")

JHS_XSD_PATH = os.path.join(BASE_DIR, "data", "Skeema_TOS_kooste_HKI_custom.xsd")


# Django SECRET_KEY setting, used for password reset links and such
SECRET_KEY = env("SECRET_KEY")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# If a secret key was not supplied elsewhere, generate a random one and log
# a warning (note that logging is not configured yet). This means that any
# functionality expecting SECRET_KEY to stay same will break upon restart.
# Should not be a problem for development.
if not SECRET_KEY:
    logger.warning(
        "SECRET_KEY was not defined in configuration. Generating an ephemeral key."
    )
    import random

    system_random = random.SystemRandom()
    SECRET_KEY = "".join(
        [
            system_random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)")
            for _ in range(64)
        ]
    )

# local_settings.py is useful for overriding settings not available
# through environment and when developing new stuff
local_settings_path = os.path.join(BASE_DIR, "local_settings.py")
if os.path.exists(local_settings_path):
    with open(local_settings_path) as fp:
        code = compile(fp.read(), local_settings_path, "exec")
    exec(code, globals(), locals())
