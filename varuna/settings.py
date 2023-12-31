"""
Django settings for Varuna project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import datetime
import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r9%byhi6f!2yn15$pmbnr#7_(*go*wkfr_t3vl43ty$+fd16k5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'NO') == 'YES'
DEBUG_PROPAGATE_EXCEPTIONS = os.getenv('DEBUG_PROPAGATE_EXCEPTIONS', 'NO') == 'YES'
DEBUG_PRINT_LOGGER = os.getenv('DEBUG_PRINT_LOGGER', 'NO') == 'YES'
GOOGLE_GEOCODE_API_KEY = os.getenv('GOOGLE_GEOCODE_API_KEY')
PARTICLE_API_KEY = os.getenv('PARTICLE_API_KEY')
SENSOR_DATA_INTERVAL = os.getenv('SENSOR_DATA_INTERVAL', 15)

ALLOWED_HOSTS = [
    'localhost',
    'api.varunaiot.com',
    'console.varunaiot.com',
    'varunaplatform.uc.r.appspot.com',
    'djangobackendapp.uc.r.appspot.com',
    'qwinix.varunaiot.com',
    'api.varunaview.io',
    'www.varunaview.io',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_cleanup.apps.CleanupConfig',
    'rest_framework',
    'corsheaders',
    'scrapy',
    'zipcodes',
    'drf_yasg',
    'geo',
    'iccr',
    'user',
    'pump',
    'utility',
    'download',
    'cron',
    'varuna',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'varuna.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'varuna.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # RDS_DB_NAME, RDS_HOSTNAME, RDS_USERNAME, RDS_PORT, RDS_PASSWORD if we are using AWS RDS
        # GCP_DB_NAME, GCP_DB_HOSTNAME, GCP_DB_USERNAME, GCP_DB_PORT, BCP_DB_PASSWORD if we are using GCP SQL
        'NAME': os.environ.get('GCP_DB_NAME', 'varuna_db'),
        'HOST': os.environ.get('GCP_DB_HOSTNAME', 'localhost'),
        'USER': os.environ.get('GCP_DB_USERNAME', 'varuna'),
        'PORT': os.environ.get('GCP_DB_PORT', '5432'),
        'PASSWORD': os.environ.get('GCP_DB_PASSWORD', 'password'),
        'TEST': {
            'NAME': 'varuna_test'
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Auth user model
AUTH_USER_MODEL = 'user.User'


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'common.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    )
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'https://www.varunaview.io',
    'http://www.varunaview.io',
    'https://www.varunacl.com',
    'http://www.varunacl.com',
    'https://console.varunaiot.com',
    'http://console.varunaiot.com',
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/


if os.getenv('GAE_INSTANCE'):
    STATIC_URL = 'https://storage.googleapis.com/static.varunaiot.com/'
else:
    STATIC_URL = '/static/'

STATIC_ROOT = 'static'


# Documentation
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'description': 'Bearer JWT authorization',
            'name': 'Authorization',
            'in': 'header',
        }
    }
}

# domain config

HOST_NAME = 'https://api.varunaview.io'

APP_NAME = 'https://www.varunacl.com'

# django-storages

DEFAULT_FILE_STORAGE = 'common.storages.PrivateStorage'

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')

AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')



GS_BUCKET_NAME = os.getenv('GS_BUCKET_NAME')

GS_PROJECT_ID = os.getenv('GS_PROJECT_ID')

# mail config

EMAIL_HOST = os.getenv('EMAIL_HOST')

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = 'masao@varunaiot.com'

EMAIL_USE_TLS = True
