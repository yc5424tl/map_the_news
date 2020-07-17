"""
Django settings for mtn_core project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import dj_database_url
import django_heroku
import dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DJANGO_READ_DOT_ENV_FILE = True
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", default=False) == "TRUE"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.gis",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admindocs",
    "mtn_web.apps.MtnWebConfig",
    "mtn_sifter.apps.MtnSifterConfig",
    "django_apscheduler",
    "storages",
]

AUTH_USER_MODEL = "mtn_web.User"

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mtn_core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "mtn_core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("MTN_DB_NAME"),
        "USER": os.getenv("MTN_DB_USER"),
        "PASSWORD": os.getenv("MTN_DB_PW"),
        "HOST": os.getenv("MTN_DB_HOST"),
        "PORT": os.getenv("MTN_DB_PORT"),
    }
}
DOCKER_POSTGRES = os.getenv("DOCKER_POSTGRES") == "TRUE"

if DOCKER_POSTGRES:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "postgres",
            "USER": "postgres",
            "HOST": "db",
            "PORT": 5432,
            "PASSWORD": "sqlAdmin1234!",
        }
    }

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

USE_S3 = os.getenv("USE_S3") == "TRUE"

if USE_S3:

    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_DEFAULT_ACL = "public-read"
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.us-east-2.amazonaws.com"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

    # s3 static settings
    STATIC_LOCATION = "static"
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/"
    STATICFILES_STORAGE = "mtn_core.storage_backends.StaticStorage"

    # s3 media settings
    MEDIA_LOCATION = "media"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/"
    DEFAULT_FILE_STORAGE = "mtn_core.storage_backends.MediaStorage"

else:
    STATIC_URL = "/static/"
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    # STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    STATIC_ROOT = "./static"
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "staticfiles")]



PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))



ADMIN_MEDIA_PREFIX = f"{STATIC_URL}admin/"

CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = ["*"]

LOGIN_URL = "login"
LOGOUT_REDIRECT_URL = "index"

BETTER_EXCEPTIONS = 1

GDAL_LIBRARY_PATH = os.getenv("GDAL_LIBRARY_PATH")
GEOS_LIBRARY_PATH = os.getenv("GEOS_LIBRARY_PATH")

if "ON_HEROKU" in os.environ:
    ALLOWED_HOSTS = ["map_the_news.herokuapp.com"]
    DATABASES["default"] = dj_database_url.config(conn_max_age=600, ssl_require=True)
    django_heroku.settings(locals(), staticfiles=False)

if os.getenv("DEBUG") == "TRUE":
    INTERNAL_IPS = ["127.0.0.1", "localhost"]
    # MIDDLEWARE.append('debug_toolbar.middleware.DebugToolBarMiddleware')
    INSTALLED_APPS.append("debug_toolbar")
    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
    ]
    DEBUG_TOOLBAR_CONFIG = {
        "INTERCEPT REDIRECTS": False,
        "SHOW_COLLAPSED": True,
        "SQL_WARNING_THRESHOLD": 100,
    }

from mtn_core.logger import LOGGING
