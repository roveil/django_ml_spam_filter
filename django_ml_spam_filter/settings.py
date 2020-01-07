"""
Django settings for django_ml_spam_filter project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import datetime
import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from . import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getattr(config, 'SECRET_KEY', '')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getattr(config, 'DEBUG', False)

ALLOWED_HOSTS = [
    '*'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'rest_framework',
    'spam_filter',
    'cacheops'
]

ROOT_URLCONF = 'django_ml_spam_filter.urls'

WSGI_APPLICATION = 'django_ml_spam_filter.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser'
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'spam_filter.permissions.AccessPermission',
    ),
    'EXCEPTION_HANDLER': 'django_ml_spam_filter.utils.rest_framework_exception_handler'
}

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

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

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Parallel threads number
PARALLEL_THREADS = getattr(config, 'PARALLEL_THREADS', 8)

# Logging
DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'default': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    }
}

LOGGING = getattr(config, 'LOGGING', DEFAULT_LOGGING)

# Celery
CELERY_QUEUE = getattr(config, 'CELERY_QUEUE', 'spam_filter_main')
BROKER_URL = getattr(config, 'BROKER_URL', 'amqp://')

CELERYBEAT_SCHEDULE = {
    'process_auto_learning': {
        'task': 'spam_filter.tasks.process_auto_learning',
        'schedule': datetime.timedelta(minutes=30),
    }
}

# SECURE TOKEN
SECURE_TOKEN = getattr(config, 'SECURE_TOKEN', '')

# STATSD
# Важно определять это до первого импорта statsd. Иначе он возьмет настройки по умолчанию.
# https://statsd.readthedocs.io/en/latest/configure.html#in-django
STATSD_HOST = getattr(config, 'STATSD_HOST', '127.0.0.1')
STATSD_PORT = getattr(config, 'STATSD_PORT', 8125)
STATSD_PREFIX = getattr(config, 'STATSD_PREFIX', None)

# Настройка sentry
SENTRY_SDK_DSN_URL = getattr(config, 'SENTRY_SDK_DSN_URL', '')

if SENTRY_SDK_DSN_URL:
    sentry_sdk.init(
        dsn=SENTRY_SDK_DSN_URL,
        integrations=[DjangoIntegration()]
    )
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = getattr(config, 'DATABASES', {})

# CACHEOPS
CACHEOPS_ENABLED = getattr(config, 'CACHEOPS_ENABLED', True)
CACHEOPS_REDIS = getattr(config, 'CACHEOPS_REDIS', {})

CACHEOPS = {
    'spam_filter.BayesDictionary': {'ops': 'all', 'timeout': 60 * 60 * 24}
}

# Прочее
AUTO_LEARNING_ENABLED = getattr(config, 'AUTO_LEARNING_ENABLED', False)

NUM_CPU_CORES = getattr(config, 'NUM_CPU_CORES', 4)
