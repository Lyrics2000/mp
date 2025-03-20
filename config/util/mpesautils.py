from django.conf import settings
import base64
from config.util.http import get
import requests
import logging
logger = logging.getLogger(__name__)


def get_token(client_ref,client_secret,development):
    """
    fetch a new token
    :param: type: whether we are fetching token for B2C or C2B
    :return: JSON
    """
    
    
    # TODO : input real mpesa live url
    main_url  = "https://sandbox.safaricom.co.ke" if development else "https://api.safaricom.co.ke"
    url = f"{main_url}/oauth/v1/generate?grant_type=client_credentials"
    credentials = f"{client_ref}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }
    response = requests.get(url, headers=headers)
    
    logger.info(dict(updated_data=f"Began generating token"))
    
    try:
        tok = response.json()['access_token']
        logger.info(dict(updated_data=f"The access token is {tok}"))
        return tok
    except:

        res = response.text
        logger.info(dict(updated_data=f"Error generating access toke so response is {res}"))
        return res
        
    

# def getAuthToken():
#         # Set the client credentials


#         url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"


#         response = requests.request("GET", url, auth=('oGrbf3zHUFzPhrxLT94acL2UQmCQLwq2','lMQYWvur09ADAZSk'))

#         if response.status_code == 200:
#             return response.json()['access_token']
        
#         else:
#             return None

def encode_str_to_base_64(str_to_encode):
    """
    Encodes the a given string to base64
    :param str_to_encode: str to encode
    :return: base64 encoded str
    """
    return base64.urlsafe_b64encode(str_to_encode.encode("UTF-8")).decode(
        "ascii"
    )
