"""
Django settings for MyLineBot project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6rnzlml8*ys1gmm7#q0ey!@g1(_ie$&zexxvv6@yb#gatgcv2e'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# test
# ALLOWED_HOSTS = [
#     '32e6ab80d1ff.ngrok.io', #允許的網域名稱
# ]

# heroku
ALLOWED_HOSTS = [
    'linebotchallenge.herokuapp.com', #允許的網域名稱
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'selfpromotelinebot',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MyLineBot.urls'

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

WSGI_APPLICATION = 'MyLineBot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# bobi
# LINE_CHANNEL_ACCESS_TOKEN = '1VgBCdRa3TyfPx5OBwrRjuiPXK7LWCPv0s7BX5S7idxa8854ELfwoKn6VHshxgAKjan+can6+A0q6Wz4BBgvtjOrIpfLJ0lrOyF4tvBOicMxgwtaclG+7YlgVhXeyh8cGdUWsDnptCRUWa1JwgwnywdB04t89/1O/w1cDnyilFU='
# LINE_CHANNEL_SECRET = 'b501d0f45de043473a9d0be6968d3742'

# test
LINE_CHANNEL_ACCESS_TOKEN = '/sZCPcz0jlqC4zuFfS9wZfu2QmxuzQ84vihUMfnN6ezpZS+eMM2+WYUzzL2pxpRl6BQovQ0zRA1QPlQbsL65h/dsdgmVPMkKJ4TK+08mz6yDkIE0wi+GqqL+Pcv8d+Ssd8bZ2oRCbpQlYsJuhqLHBgdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '740a4d3d75483bef5303513c2599ae10'

import os

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
