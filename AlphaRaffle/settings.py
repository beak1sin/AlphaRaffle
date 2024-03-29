"""
Django settings for AlphaRaffle project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
# import my_settings
import dj_database_url
import pymysql
pymysql.install_as_MySQLdb()

# env = os.environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# reading .env file 
# 로컬에서는 주석처리해제, 서버로는 주석처리

# DEBUG = False
# DEBUG = bool(os.environ.get('DJANGO_DEBUG', True))


# if DEBUG == True:
#     import environ
#     environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))

# DEBUG = True
import environ
environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))

DEBUG = bool(1 if os.environ.get('DJANGO_DEBUG') == 'True' else 0)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = my_settings.SECRET
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
# DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1','132.145.85.241', 'alpharaffle.com', 'www.alpharaffle.com', 'shoeneakers.com', 'www.shoeneakers.com', 'localhost']


# Application definition

INSTALLED_APPS = [
    'draw.apps.DrawConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'django_crontab',
    'django.contrib.sitemaps',
    'django.contrib.syndication',
    'pwa',
    # 'channels',
]

# import sys
# import django

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# sys.path.insert(0, os.path.join(BASE_DIR, 'AlphaRaffle'))
# django.setup()
# from cron import crawl
# from AlphaRaffle.cron import crawl

cronPath = os.path.join(BASE_DIR, 'cron.log')
cronPath2 = os.path.join(BASE_DIR, 'cron2.log')
cronPath3 = os.path.join(BASE_DIR, 'cron3.log')
cronPath4 = os.path.join(BASE_DIR, 'cron4.log')
cronPath5 = os.path.join(BASE_DIR, 'cron5.log')
CRONJOBS = [
    # ('10 9,21 * * *', 'crawl', '>> ' + cronPath2),
    # ('*/1 * * * *', 'AlphaRaffle.cron.hello', '>> ' + cronPath),
    ('10 3,9,15,21 * * *', 'AlphaRaffle.cron.crawl', '>> ' + cronPath2),
    ('0 15 * * *', 'AlphaRaffle.cron.daily_verification_delete_crontab', '>> ' + cronPath3),
    ('0 15 * * *', 'AlphaRaffle.cron.mijungCheck', '>> ' + cronPath4),
    ('0 15 * * *', 'AlphaRaffle.cron.nullCheck', '>> ' + cronPath5),
]

# The Debug Toolbar is shown only if your IP is listed in the INTERNAL_IPS setting.
INTERNAL_IPS = ['127.0.0.1']

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
]

ROOT_URLCONF = 'AlphaRaffle.urls'

# BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'AlphaRaffle.wsgi.application'


# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             # Redis 주소 및 포트 정보
#             'hosts': [('127.0.0.1', 6379)],
#         },
#     },
# }

ASGI_APPLICATION = 'AlphaRaffle.asgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
# DATABASES = my_settings.DATABASES

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# DATABASES = {
#   'default' : {
#       'ENGINE': 'django.db.backends.mysql',
#       'NAME': env('JAWSDB_NAME'),
#       'USER': env('JAWSDB_USER'), #주로 'root'
#       'PASSWORD': env('JAWSDB_PASSWORD'),
#       'HOST': env('JAWSDB_HOST'),
#       'PORT': env('JAWSDB_PORT'),
#       'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
#         },
#   }
# }

DATABASES = {
  'default' : {
      'ENGINE': 'django.db.backends.mysql',
      'NAME': os.environ.get('JAWSDB_NAME'),
      'USER': os.environ.get('JAWSDB_USER'), #주로 'root'
      'PASSWORD': os.environ.get('JAWSDB_PASSWORD'),
      'HOST': os.environ.get('JAWSDB_HOST'),
      'PORT': os.environ.get('JAWSDB_PORT'),
      'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        },
  }
}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = False
LOGIN_REDIRECT_URL = '/'
# AUTH_USER_MODEL = 'draw.Userdata'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# 로컬에서 진행할거면 주석처리하고 서버로 배포하는거면 주석해제 후 collectstatic 진행 후 배포
# STATICFILES_DIRS = [
#     # os.path.join(BASE_DIR, "static"),
#     # os.path.join(BASE_DIR, "staticfiles"),
#     os.path.join(BASE_DIR, 'static2'),
# ]

if DEBUG == False:
    STATICFILES_DIRS = []
    PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static/draw/js', 'serviceworker.js')
else:
    # STATIC_ROOT = os.path.join(BASE_DIR, 'draw/static')
    STATICFILES_DIRS = [BASE_DIR / "draw/static"]
    PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'draw/static/draw/js', 'serviceworker.js')

# if DEBUG:
#     STATIC_ROOT = os.path.join(BASE_DIR, 'draw', 'static')
#     STATICFILES_DIRS = []
    
# else:
#     STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # collectstatic할때의 경로 설정
#     STATICFILES_DIRS = []


# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

EMAIL_BACKEND: 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD2')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

# rss
FEEDS = {
    'latest': {
        'title': 'Latest Shoes',
        'link': '/rss/',
        'description': 'Updates on the latest shoes.',
        'feed_url': '/rss/',
    },
}
# 로그인 세션 지속시간
SESSION_COOKIE_AGE = 60 * 60 * 24




PWA_APP_NAME = 'shoeneakers'
PWA_APP_DESCRIPTION = "한정판 신발을 자동응모해주는 플랫폼입니다."
PWA_APP_THEME_COLOR = '#000000'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': '/static/draw/necessary/shoeneakers_favicon.svg',
        'sizes': '152x152'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/draw/necessary/shoeneakers_favicon.svg',
        'sizes': '152x152'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/images/icons/splash-640x1136.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'
PWA_APP_SHORTCUTS = [
    {
        'name': 'Shortcut',
        'url': '/target',
        'description': 'Shortcut to a page in my application'
    }
]
PWA_APP_SCREENSHOTS = [
    {
      'src': '/static/images/icons/splash-750x1334.png',
      'sizes': '750x1334',
      "type": "image/png"
    }
]