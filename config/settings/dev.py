

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.oracle',
        'NAME': 'dwh',
        'USER': 'tachongo[payment_UAT]',
        'PASSWORD': 'H#rd2_gu355',
        'HOST': '172.26.0.47',
        'PORT': '1521',
    },
    "validation":{
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'dwh',
        'USER': 'tachongo[VALIDATION]',
        'PASSWORD': 'H#rd2_gu355',
        'HOST': '172.26.0.47',
        'PORT': '1521',
    }
}


PAYMENTS_STK_PUSH = "PAYMENTS_STK_PUSH_UAT"
PAYMENTS_STK_PUSH_BUSINESS = "PAYMENTS_STK_PUSH_BUSINESS_UAT"
PAYMENT_QUERY_STK_PUSH = "PAYMENT_QUERY_STK_PUSH_UAT"
PAYMENT_GET_TRANSACTIONAL_STATUS = "PAYMENT_GET_TRANSACTIONAL_STATUS_UAT"
PAYMENT_ADD_PAYBILL = "PAYMENT_ADD_PAYBILL_UAT"
PAYMENT_C2B_REGISTER = "PAYMENT_C2B_REGISTER_UAT"
PAYMENT_C2B_SIMULATE = "PAYMENT_C2B_SIMULATE_UAT"
PAYMENT_GET_FILTER_MPESA = "PAYMENT_GET_FILTER_MPESA_UAT"
PAYMENT_REGISTER_URL = "PAYMENT_REGISTER_URL_UAT"
PAYMENT_ADD_BUSINESS = "PAYMENT_ADD_BUSINESS_UAT"
PAYMENT_VERIFY_CHECKOUT_ID = "PAYMENT_VERIFY_CHECKOUT_ID_UAT"
PAYMENT_ADD_USER = "PAYMENT_ADD_USER_UAT"
C2B_ADD_CALLBACK = "PAYMENT_C2B_ADD_CALLBACK_UAT"
PAYMENT_VERIFY_MANUAL_PAYMENT = "PAYMENT_VERIFY_MANUAL_PAYMENT_UAT"
C2B_ONLINE_CHECKOUT_CALLBACK_URL = 'https://brtgw.britam.com/mp/payment/uat'


C2B_CONFIRMATION_URL = "https://brtgw.britam.com/mp/payment/uat/api/v1/confirmation_url/"
C2B_VALIDATE_URL = "https://brtgw.britam.com/mp/payment/uat/api/v1/validation_url/"



AUDIENCE = "api://2551a6ae-039d-43bb-b05e-8d97d07f15e2"
ISSUER_ID = "e303f219-75ef-479a-b23c-35ac9479a8ce"


MTEK_KEY = "MTEK_UAT"

