import jwt
from datetime import datetime
from urllib.request import urlopen
import json
import requests
from jose import jwk, jwt
from jose.backends import RSAKey
from datetime import datetime
import requests
from django.http import JsonResponse
from rest_framework import status

import logging

logger = logging.getLogger(__name__)



class ValidateToken:
    def __init__(self,token,audience,tenant_id):
        self.token = token 
        self.audience =  audience
        self.tenant_id =  tenant_id
        self.jwks_uri = f"https://login.microsoftonline.com/{self.tenant_id}/discovery/v2.0/keys"
        self.issuer = f"https://sts.windows.net/{self.tenant_id}/"

    def decode_and_verify_token(self):
        # Fetching Azure AD signing keys
        try:
            keys_response = requests.get(self.jwks_uri)
            keys_response.raise_for_status()
            keys_data = keys_response.json()
        except Exception as err:
            logger.error(f"error during auth {err} ")
            return  JsonResponse({
                 "code":500,
                 "message":f"An Error occured during validation"
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
        # Decode the token to get the kid (key ID)
        unverified_header = jwt.get_unverified_header(self.token)
        kid = unverified_header.get("kid")
        if not kid:
             return JsonResponse({"code": 401 ,"message" : "Key ID (kid) not found in token header"},status=status.HTTP_401_UNAUTHORIZED
                    )
           
            
        rsa_key = {}
        for key in keys_data["keys"]:
                if key["kid"] == kid:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }
                    
        try:
            

            decoded_token = jwt.decode(
                self.token,
                algorithms=["RS256"],
                audience=self.audience,
                issuer=self.issuer,
                options={"verify_signature": True},
                key= rsa_key
            )
            
            logger.info(f"ssuccess generating token {decoded_token}")
            
            return decoded_token

        except Exception as e:
            logger.error(f"error during auth {str(e)}")
            return JsonResponse(
                        {"code": "Unauthorized", "description": f"Authentication Erro occured","roles":[]},
                        
                        status=status.HTTP_401_UNAUTHORIZED
                    )
        
     


        
        
