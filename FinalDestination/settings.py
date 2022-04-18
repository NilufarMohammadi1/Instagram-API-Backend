from datetime import timedelta
from pathlib import Path
import os

from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-e12suwz@)ux^4f(qc73r!2dtnf(g13d#*(0i$gd!g6g2#2a2_!'

DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Accounts',
    'Posts',
    'Comments',
    'Likes',
    'rest_framework'
]







# Choices are: "semantic", "bootstrap"
MARTOR_THEME = getattr(settings, "MARTOR_THEME", "bootstrap")

# Global martor settings
# Input: string boolean, `true/false`
MARTOR_ENABLE_CONFIGS = getattr(
    settings,
    "MARTOR_ENABLE_CONFIGS",
    {
        "emoji": "true",  # enable/disable emoji icons.
        "imgur": "true",  # enable/disable imgur/custom uploader.
        "mention": "false",  # enable/disable mention
        "jquery": "true",  # include/revoke jquery (require for admin django)
        "living": "false",  # enable/disable live updates in preview
        "spellcheck": "false",  # enable/disable spellcheck in form textareas
        "hljs": "true",  # enable/disable hljs highlighting in preview
    },
)


MARTOR_MARKDOWN_BASE_MENTION_URL = getattr(
    settings,
    "MARTOR_MARKDOWN_BASE_MENTION_URL",
    "https://python.web.id/author/",
)





MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ratelimit.middleware.RatelimitMiddleware'
]

RATELIMIT_VIEW = 'Accounts.views.rate_limit'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,



}




ROOT_URLCONF = 'FinalDestination.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'FinalDestination.wsgi.application'
AUTH_USER_MODEL = 'Accounts.Users'
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'FinalDestinationDB3',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}




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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

