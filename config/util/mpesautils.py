from django.conf import settings
import base64
from config.util.http import get


def get_token(type,client_ref,client_secret,development):
    """
    fetch a new token
    :param: type: whether we are fetching token for B2C or C2B
    :return: JSON
    """
    
    # TODO : input real mpesa live url
    main_url  = "https://sandbox.safaricom.co.ke" if development else ""
    url = f"{main_url}/oauth/v1/generate?grant_type=client_credentials"
    concat_str = "{}:{}".format(
        client_ref, client_secret
    )
    auth_token = encode_str_to_base_64(concat_str)
    if type.lower() == "b2c":
        concat_str = "{}:{}".format(
            client_ref, client_secret
        )
        auth_token = encode_str_to_base_64(concat_str)
    headers = {"Authorization": "Basic {}".format(auth_token)}
    response = get(url, headers)
    return response.json()


def encode_str_to_base_64(str_to_encode):
    """
    Encodes the a given string to base64
    :param str_to_encode: str to encode
    :return: base64 encoded str
    """
    return base64.urlsafe_b64encode(str_to_encode.encode("UTF-8")).decode(
        "ascii"
    )
