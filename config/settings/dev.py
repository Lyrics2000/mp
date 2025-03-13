

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
    'payments.Middleware.AzureADAuthenticationMiddleware',
]

DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.oracle',
        'NAME': 'dwh',
        'USER': 'tachongo[payment_UAT]',
        'PASSWORD': 'H#rd2_gu355',
        'HOST': '172.26.0.47',
        'PORT': '1521',
    }
}

RegisterClient_ID  = "RegisterClient"
VerifyIdNo_ID = "VerifyClientByIdNumber"
VerifyClientByTaxPin_ID = "VerifyClientByKraPin"
VerifyAgent_ID = "VerifyAgent"
CheckAimsClientNo_ID = "CheckAimsClientNo"
GeneratePolicy_ID = "GeneratePolicy"
GET_PRODUCT_CLASSES =  'VerifyAgent'
GET_BANK_CODES = 'VerifyAgent'
GET_BANK_BRANCH_CODES = 'VerifyAgent'
GET_TITLE = 'VerifyAgent'
GET_BRANCH_CODE = 'VerifyAgent'
GET_IDENTITY_TYPE = 'VerifyAgent' # dont share 
GET_SECTION_GROUP = 'VerifyAgent'
GET_SECTION_CODES = 'VerifyAgent'
GET_EXTENTION_CODES = 'VerifyAgent'
GET_CURRENCY_CODES = 'VerifyAgent'
GET_CURRENCY_RATES = 'VerifyAgent'
GET_OCCUPATION_CODES = 'VerifyAgent'
GET_COUNTRY_CODES = 'VerifyAgent'
GET_LIMITS_CODES = 'VerifyAgent'
GET_CLAUSES_CODES = 'VerifyAgent'
GET_EXCESS_CODES = 'VerifyAgent'
GET_PERILS_CODES = 'VerifyAgent'
GET_CAUSE_CODES = 'VerifyAgent'
GET_TAXES_CODES = 'VerifyAgent'
GET_ACCESSORY_CODES = 'VerifyAgent'
GET_ACCESSORY_MAKE_CODES = 'VerifyAgent'
REINSURANCE = 'VerifyAgent'
DEBITING = 'VerifyAgent'
NILL_ENDORSEMENT = 'VerifyAgent'
RECEIPTING = 'VerifyAgent'
GET_ALL_AGEENTS = 'VerifyAgent'
VERIFY_AGENT_BY_PIN = 'VerifyAgent'
GET_ALL_PORTS = 'VerifyAgent'
GET_ALL_PARCKET_TYPES = 'VerifyAgent'
GET_ALL_MARINE_GROUPS = 'VerifyAgent'



AUDIENCE = "api://2551a6ae-039d-43bb-b05e-8d97d07f15e2"
ISSUER_ID = "e303f219-75ef-479a-b23c-35ac9479a8ce"


