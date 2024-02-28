
import os
from dotenv import load_dotenv
from pathlib import Path
from django.utils.translation import gettext_lazy as _

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# print("base dir path: ", BASE_DIR)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-#_bi-zg0*_41=#%z)0l64z6ol#_!8@=rs$cu122kae&3!pp@8e'
SECRET_KEY = os.environ.get('SECRET_KEY')

SECURE_CROSS_ORIGIN_OPENER_POLICY = None
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG')
# DEBUG = True
# SECURE_SSL_REDIRECT = False

ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = [
#                  '0.0.0.0'
#                 #  '192.168.1.3',
#                  ]
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = [
#     'http://localhost:8000',
#     'http://127.0.0.1:8000',
#     'http://192.168.1.3:8000',
#     'http://192.168.140.17:8000',
#     'http://0.0.0.0:8000',

# ]
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Other Apps
    # 'google_translate',
    # 'geoip2',

    # My Apps
    'products',
    'base',
    'api',
    'members',
    'cart',
    'shop',
    'blog',
    'financial',
]

AUTH_USER_MODEL = "members.Member"

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    
]

ROOT_URLCONF = 'toystore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'toystore.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':'devDB',
        'USER':'postgres',
        'PASSWORD':'admin',
        'HOST':'localhost',
        'PORT':'5432',
    }
}
#zarinpal config
MERCHANT = os.environ.get('MERCHANT')
SANDBOX = False
if DEBUG:
    BASE_URL = 'localhost'
else:
    BASE_URL = 'https://numera.ir'

#Crypto payment config
CRYPTO_SECRET_KEY = os.environ.get('CRYPTO_SECRET_KEY')


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'fa'
# LANGUAGE_CODE = 'en-us'
LANGUAGES = (
    ('fa', _('Farsi')),
    ('en-us', _('English')),
)
TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
# STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"
LOCALE_PATHS = [BASE_DIR / "locale"]
# GEOIP_PATH = [BASE_DIR / 'geoip']
# GEOIP_PATH = os.path.join('geoip')
# GEOIP_PATH =os.path.join(BASE_DIR, 'geoip')


DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_SCALE = 0.5
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = "JPEG"
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {"JPEG": ".jpg"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True



# Emailing settings
CRYPTO_SECRET_KEY = os.environ.get('CRYPTO_SECRET_KEY')
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_FROM = os.environ.get('EMAIL_FROM')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL')

PASSWORD_RESET_TIMEOUT = 7300

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


