
from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-u2fmh@sepulv17d390rm@ryn&7^p5_h-nfl@t(2e&6zot=pon1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rangefilter',
     'rest_framework',
     'payments'
]



ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'
UAT_ENV  =  True



if DEBUG:
    from .dev import *
    
else:
    from .prod import *
    
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases




# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
#         },
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# # development
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_project_file'),
]

# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR,'static_cdn')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join('media_cdn')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



#Consumer Key
MPESA_B2C_ACCESS_KEY = config('MPESA_B2C_ACCESS_KEY', default='')
#Consumer Secret
MPESA_B2C_CONSUMER_SECRET = config('MPESA_B2C_CONSUMER_SECRET', default='')
# This is the encryption of the scurity Credentials I used the Developer site to encrypt it.
B2C_SECURITY_TOKEN =  config('B2C_SECURITY_TOKEN', default='')
#InitiatorName
B2C_INITIATOR_NAME = config('B2C_INITIATOR_NAME', default='')
# CommandID
B2C_COMMAND_ID = config('B2C_COMMAND_ID', default='')
#PartyA
B2C_SHORTCODE = config('B2C_SHORTCODE', default='')
# this is the url where Mpesa  will post in case of a time out. Replace http://mpesa.ngrok.io/  with your url ow here this app is running
B2C_QUEUE_TIMEOUT_URL = config('B2C_QUEUE_TIMEOUT_URL', default='')
# this is the url where Mpesa will post the result. Replace http://mpesa.ngrok.io/  with your url ow here this app is running
B2C_RESULT_URL = config('B2C_RESULT_URL', default='')
# this is the url where we post the B2C request to Mpesa. Replace this with the url you get from safaricom after you have passed the UATS
MPESA_URL = config('MPESA_URL', default='')

# C2B (Paybill) Configs
# See https://developer.safaricom.co.ke/c2b/apis/post/registerurl

#Consumer Secret
MPESA_C2B_ACCESS_KEY = config('MPESA_C2B_ACCESS_KEY', default='')
# Consumer Key
MPESA_C2B_CONSUMER_SECRET = config('MPESA_C2B_CONSUMER_SECRET', default='')
# Url for registering your paybill replace it the url you get from safaricom after you have passed the UATS
C2B_REGISTER_URL = config('C2B_REGISTER_URL', default='')
#ValidationURL
# replace http://mpesa.ngrok.io/ with your url ow here this app is running
C2B_VALIDATE_URL = config('C2B_VALIDATE_URL', default='')
#ConfirmationURL
# replace http://mpesa.ngrok.io/ with your url ow here this app is running
C2B_CONFIRMATION_URL = config('C2B_CONFIRMATION_URL', default='')
#ShortCode (Paybill)
C2B_SHORT_CODE = config('C2B_SHORT_CODE', default='')
#ResponseType
C2B_RESPONSE_TYPE = config('C2B_RESPONSE_TYPE', default='')

# C2B (STK PUSH) Configs
# https://developer.safaricom.co.ke/lipa-na-m-pesa-online/apis/post/stkpush/v1/processrequest

#replace http://mpesa.ngrok.io/ with your url ow here this app is running

C2B_ONLINE_CHECKOUT_CALLBACK_URL = 'https://brtgw.britam.com/mpesa/payment/uat'
# C2B_ONLINE_CHECKOUT_CALLBACK_URL = 'https://7fc3-105-163-157-249.ngrok-free.app'
# The Pass Key provided by Safaricom when you pass UAT's
# See https://developer.safaricom.co.ke/test_credentials
C2B_ONLINE_PASSKEY = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
# Your Short code
C2B_ONLINE_SHORT_CODE = config('C2B_ONLINE_SHORT_CODE', default='')
# your paybill or till number
C2B_ONLINE_PARTY_B = config('C2B_ONLINE_PARTY_B', default='')
# number of seconds from the expiry we consider the token expired the token expires after an hour
# so if the token is 600 sec (10 minutes) to expiry we consider the token expired.
TOKEN_THRESHOLD = config('TOKEN_THRESHOLD', default=600, cast=int)

CELERY_BROKER_URL = config('CELERY_BROKER', default="redis://redis:6379/0", cast=str)
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default="redis://redis:6379/0", cast=str)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'


PAYMENTS_STK_PUSH = "PAYMENTS_STK_PUSH"
PAYMENT_QUERY_STK_PUSH = "PAYMENT_QUERY_STK_PUSH"
PAYMENT_GET_TRANSACTIONAL_STATUS = "PAYMENT_GET_TRANSACTIONAL_STATUS"


