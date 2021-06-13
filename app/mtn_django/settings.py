import os
import dj_database_url
import uuid
import django_heroku

DEPLOYMENT = os.getenv('DEPLOYMENT')
USE_S3 = os.getenv('USE_S3') == "TRUE"
USE_WHITENOISE = os.getenv('USE_WHITENOISE') == "TRUE"
DATABASE_URL = os.environ.get('DATABASE_URL')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


if DEPLOYMENT == 'DEV':

    import dotenv

    DJANGO_READ_DOT_ENV_FILE = True

    dotenv_file = os.path.join(BASE_DIR, '../.env.dev')

    if os.path.isfile(dotenv_file):
        dotenv.load_dotenv(dotenv_file)


SECRET_KEY = os.getenv('SECRET_KEY', default='superSecret123!')

DEBUG = int(os.environ.get("DEBUG", default=0))


ALLOWED_HOSTS = ['map-the-news.herokuapp.com', 'localhost', '127.0.0.1']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'mtn_web.apps.MtnWebConfig',
    'mtn_sifter.apps.MtnSifterConfig',
    'storages',
    'simple_history',
]

if DEPLOYMENT == 'DEV':
    INSTALLED_APPS.insert(0, 'whitenoise.runserver_nostatic')

if 'ON_HEROKU' in os.environ:
    INSTALLED_APPS.insert(0, 'scout_apm.django')


AUTH_USER_MODEL = 'mtn_web.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

if USE_WHITENOISE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

ROOT_URLCONF = 'mtn_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
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

WSGI_APPLICATION = 'mtn_django.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("DB_DATABASE"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

db_from_env = dj_database_url.config(default=DATABASE_URL, conn_max_age=500, ssl_require=True)
DATABASES['default'].update(db_from_env)

if 'ENABLE_SERVER_SIDE_CURSORS' in os.environ:
    DISABLE_SERVER_SIDE_CURSORS = False


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 86400
    }
}

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# local static
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# local media
MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')


# =========================================================== #
#  -------   STATIC FILES   -------   MEDIA FILES   --------  #
# =========================================================== #

if USE_S3:

    # Amazon s3 bucket
    AWS_DEFAULT_ACL = "public-read"
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.us-east-2.amazonaws.com"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

    # Amazon s3 static
    STATIC_LOCATION = "static"
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/"
    STATICFILES_STORAGE = "mtn_django.storage_backends.StaticStorage"

    # Amazon s3 media
    MEDIA_LOCATION = "media"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/"
    DEFAULT_FILE_STORAGE = "mtn_django.storage_backends.MediaStorage"

if USE_WHITENOISE:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATIC_URL = '/staticfiles/'
    WHITENOISE_AUTOREFRESH = True
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
    MEDIA_URL = '/mediafiles/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')


STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

ADMIN_MEDIA_PREFIX = f"{STATIC_URL}admin/"

CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = ["*"]

LOGIN_URL = "login"
LOGOUT_REDIRECT_URL = "index"

# 3rd Party Geo Library Locations
GDAL_LIBRARY_PATH = os.getenv('GDAL_LIBRARY_PATH')
GEOS_LIBRARY_PATH = os.getenv('GEOS_LIBRARY_PATH')


if 'ON_HEROKU' in os.environ:
    SCOUT_MONITOR = os.environ.get('SCOUT_MONITOR')
    SCOUT_KEY = os.environ.get('SCOUT_KEY')
    SCOUT_NAME = 'Map the News'
    # DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
    # django_heroku.settings(locals())

# LOGGING = {
#     'loggers': {
#         'django.db.backends': {
#             'level': 'DEBUG',
#         },
#     },
# }


if DEBUG == 1:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    BETTER_EXCEPTIONS = 1
    # INTERNAL_IPS = ("127.0.0.1", "localhost", os.getenv('MTN_WEB_1_IP'))
    INTERNAL_IPS = type(str('c'), (), {'__contains__': lambda *a: True})()
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
        "debug_toolbar.panels.profiling.ProfilingPanel",
    ]

    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CONFIG": show_toolbar,
        "SHOW_COLLAPSED": False,
        "SQL_WARNING_THRESHOLD": 500,
    }
