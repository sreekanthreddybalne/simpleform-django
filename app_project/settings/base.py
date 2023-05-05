"""
Django settings for app_project project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import datetime
from decouple import config, Csv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

SITE_ID = 2
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

APPEND_SLASH = True
# Application definition

INSTALLED_APPS = [
    'app',
    'api',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'corsheaders',
	'rest_framework',
	'rest_framework.authtoken',
    'sorl.thumbnail',
    'django.contrib.sitemaps',
    'django_filters',
    'guardian',
]

AUTH_USER_MODEL = 'app.User'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login'

#Authentication backends
AUTHENTICATION_BACKENDS = (
        'app.backends.EmailOrUsernameModelBackend',
        'django.contrib.auth.backends.ModelBackend',
        'guardian.backends.ObjectPermissionBackend',
    )

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        #'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'api.jwt_utils.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
       'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'COERCE_DECIMAL_TO_STRING': False,
    "DATE_INPUT_FORMATS": ["%m-%d-%Y"],
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

X_FRAME_OPTIONS = 'ALLOWALL'

CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = []

from corsheaders.defaults import default_headers

CORS_ALLOW_HEADERS = default_headers + (
    'HTTP_AUTHORIZATION',
)

ROOT_URLCONF = 'app_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
            'app_tags': 'app.templatetags.app_tags',
            },
        },
    },
]

WSGI_APPLICATION = 'app_project.wsgi.application'

ASGI_APPLICATION = "app_project.routing.application"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

HIVE_DATABASE = {
    'name': 'wealth_management',
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'api.jwt_utils.jwt_response_payload_handler',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

DATE_FORMAT = "m-d-Y"

LANGUAGE_CODE = 'en-us'


TIME_ZONE =  'Asia/Kolkata'

USE_I18N = True

USE_L10N = False

USE_TZ = True

EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT', cast=int)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': '',                      # Set to empty string for default.
    }
}

from app.settings import COMPANY_SHORT_NAME as ds
DEFAULT_FROM_EMAIL = ds + ' <support@bankplusone.com>'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR,'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
IMAGE_UPLOAD_PATH =  'media/images/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
)
THUMBNAIL_FORMAT = 'PNG'


from celery.schedules import crontab
from django.utils import timezone
from datetime import timedelta

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
#CELERY_BROKER_URL = 'amqp://sree:D.t9676768131@0.0.0.0:5672/bidbuzz_vhost'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_IGNORE_RESULT = True
CELERY_ACKS_LATE = True
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'fanout_prefix': True,
    'fanout_patterns': True
}
CELERY_BEAT_SCHEDULE = {
}