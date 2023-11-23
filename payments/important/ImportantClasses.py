from datetime import datetime
from .keys import *
import base64
import requests
from requests.auth import HTTPBasicAuth

from .exceptions import *


def format_phone_number(phone_number):

	if len(phone_number) < 9:
		return {
            "status":"Failed",
            "message":"invalid Phone number"
        }
	else:
		return {
            "status":"Success",
            "message":'254' + phone_number[-9:]
        }

class DateFormated:
    unformated_time = datetime.now()
    formated_time = unformated_time.strftime("%Y%m%d%H%M%S")
    
class Base64Pass:
    data_to_encode = BusinessShortCode + lipa_na_mpesa_passkey + DateFormated.formated_time
    encoded_string = base64.b64encode(data_to_encode.encode())
    decoded_password =  encoded_string.decode('utf-8')
    
class AccessToken:
    def __init__(self,consumer_key,consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        
    def access_token(self):
        consumer_key = self.consumer_key
        consumer_secret = self.consumer_secret
        api_URL = f"{BASEURL}/oauth/v1/generate?grant_type=client_credentials"
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        json_reponse = r.json()
        accetoken = json_reponse["access_token"]
        return accetoken

class LipaNaMpesa:
    def __init__(self,phoneNumber,accountReference,amount,description):
        self.phoneNumber = phoneNumber
        self.accountReference = accountReference
        self.amount = amount
        self.description =  description
        
        
    def lipa_na_mpesa(self):
        access_token_class = AccessToken(Consumer_key,Consumer_secret)
        access_token = access_token_class.access_token()
        api_url = f"{BASEURL}/mpesa/stkpush/v1/processrequest"
        headers = { "Authorization": "Bearer %s" % access_token }
        request = {
        "BusinessShortCode": BusinessShortCode,
        "Password": Base64Pass.decoded_password,
        "Timestamp": DateFormated.formated_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": str(self.amount),
        "PartyA": str(self.phoneNumber),
        "PartyB": BusinessShortCode,
        "PhoneNumber": str(self.phoneNumber),
        "CallBackURL": f"{CALLBACK_URL}/api/v1/callback/",
        "AccountReference": str(self.accountReference),
        "TransactionDesc": self.description
        }
        
        response = requests.post(api_url, json = request, headers=headers)

        return response.json()
    
    def register_url(self):
            access_token_class = AccessToken(Consumer_key,Consumer_secret)
            access_token = access_token_class.access_token()
            api_url = f"{BASEURL}/mpesa/c2b/v1/registerurl"
            headers = {"Authorization": "Bearer %s" % access_token}
            request = {"ShortCode": C2B_SHORTCODE,
                        "ResponseType": "Cancelled",
                        "ConfirmationURL": f"{CALLBACK_URL}//api/v1/validation_url/",
                        "ValidationURL": f"{CALLBACK_URL}//api/v1/confirmation_url/"
                        }

            response = requests.post(api_url, json=request, headers=headers)

            return response.json()
        
    def simulate_c2b_transaction(self):
        access_token_class = AccessToken(Consumer_key,Consumer_secret)
        access_token = access_token_class.access_token()
        api_url = f"{BASEURL}/mpesa/c2b/v1/simulate"
        headers = {"Authorization": "Bearer %s" % access_token}

        request = {"ShortCode": C2B_SHORTCODE,
                "CommandID": "CustomerPayBillOnline",
                "Amount": self.amount,
                "Msisdn": self.phoneNumber,
                "BillRefNumber": self.accountReference}

        response = requests.post(api_url, json=request, headers=headers)

        return response.json()
    

# lipa_na_mpesa = LipaNaMpesa(254704157038,33380005,1)
# print(lipa_na_mpesa.lipa_na_mpesa())
        
        
        
        