
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
        'USER': 'tachongo[payments]',
        'PASSWORD': 'H#rd2_gu355',
        'HOST': '172.26.0.47',
        'PORT': '1521',
    }
}
PAYMENTS_STK_PUSH = "PAYMENTS_STK_PUSH"
PAYMENTS_STK_PUSH_BUSINESS = "PAYMENTS_STK_PUSH_BUSINESS_PROD"
PAYMENT_QUERY_STK_PUSH = "PAYMENT_QUERY_STK_PUSH"
PAYMENT_GET_TRANSACTIONAL_STATUS = "PAYMENT_GET_TRANSACTIONAL_STATUS"
PAYMENT_ADD_PAYBILL = "PAYMENT_ADD_PAYBILL"
PAYMENT_C2B_REGISTER = "PAYMENT_C2B_REGISTER_PROD"
PAYMENT_C2B_SIMULATE  = "PAYMENT_C2B_SIMULATE_PROD"
PAYMENT_GET_FILTER_MPESA = "PAYMENT_GET_FILTER_MPESA_PROD"
PAYMENT_REGISTER_URL = "PAYMENT_REGISTER_URL_PROD"
PAYMENT_ADD_BUSINESS = "PAYMENT_ADD_BUSINESS_PROD"
PAYMENT_ADD_USER = "PAYMENT_ADD_USER_PROD"
PAYMENT_VERIFY_CHECKOUT_ID = "PAYMENT_VERIFY_CHECKOUT_ID_PROD"
PAYMENT_VERIFY_MANUAL_PAYMENT = "PAYMENT_VERIFY_MANUAL_PAYMENT_PROD"
C2B_ONLINE_CHECKOUT_CALLBACK_URL = 'https://brtgw.britam.com/mp/payment'
C2B_CONFIRMATION_URL = "https://brtgw.britam.com/mp/payment/api/v1/confirmation_url/"
C2B_VALIDATE_URL = "https://brtgw.britam.com/mp/payment/api/v1/validation_url/"
MTEK_KEY = "MTEK_PROD"



AUDIENCE = "api://2551a6ae-039d-43bb-b05e-8d97d07f15e2"
ISSUER_ID = "e303f219-75ef-479a-b23c-35ac9479a8ce"


