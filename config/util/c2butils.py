import base64
from datetime import datetime
import time
import threading
import requests
from config.settings.settings import (
    C2B_ONLINE_PASSKEY,
    C2B_SHORT_CODE,
    C2B_RESPONSE_TYPE,
    C2B_CONFIRMATION_URL,
    C2B_VALIDATE_URL,
    C2B_ONLINE_CHECKOUT_CALLBACK_URL
)
from payments.models import AuthToken
from config.util.http import post
from django.http import JsonResponse
from rest_framework import status

from payments.models import (
    PayBillNumbers
)

import logging

logger = logging.getLogger(__name__)

from payments.mpesa import(
    Mpesa
)


from .configs import (
    getBaseUrl
)

from .mpesautils import (
    get_token
)


def register_c2b_url(client_ref,client_secret,development):
    """
    Register the c2b_url
    :return:
    """
    url = f"{MPESA_URL}/mpesa/c2b/v1/registerurl"
    headers = {
        "Authorization": "Bearer {}".format(AuthToken.objects.get_token("c2b",client_ref,client_secret,development))
    }
    body = dict(
        ShortCode=C2B_SHORT_CODE,
        ResponseType=C2B_RESPONSE_TYPE,
        ConfirmationURL=C2B_CONFIRMATION_URL,
        ValidationURL=C2B_VALIDATE_URL,
    )
    response = post(url=url, headers=headers, data=body)
    return response.json()


def handleCallback_m(paybill,db,typee):
    if (int(paybill) == 174379) and typee:
        time.sleep(30)
        try:
            res =  requests.post(db.callback_url,data = {
            "Body": 
            {
                "stkCallback": 
                {
                    "MerchantRequestID": db.MerchantRequestID,
                    "CheckoutRequestID": db.CheckoutRequestID,
                    "ResultCode": db.ResponseCode,
                    "ResultDesc": "The service request is processed successfully.",
                    "CallbackMetadata": 
                    {
                        "Item": 
                        [
                            {
                                "Name": "Amount",
                                "Value": db.amount
                            },
                            {
                                "Name": "MpesaReceiptNumber",
                                "Value": "LK451H35OP"
                            },
                            {
                                "Name": "Balance"
                            },
                            {
                                "Name": "TransactionDate",
                                "Value": 20171104184944
                            },
                            {
                                "Name": "PhoneNumber",
                                "Value": 254706506361
                            }
                        ]
                    }
                }
            }
            } )  
            db.callback_sent =  True
            db.save()
        except:
            pass

    else:
        res =  requests.post(db.callback_url,data={})


        



def process_online_checkout(
    msisdn: int,
    amount: int,
    paybill : int,
    account_reference: str,
    transaction_desc: str,
    is_paybil=True,
    db  =  None
    
):
    """
    Handle the online checkout
    :param msisdn:
    :param amount:
    :param account_reference:
    :param transaction_desc:
    :param is_paybil: If set to False it means we are make a till transaction
    :return:
    """
    
    filter_paybill = PayBillNumbers.objects.filter(paybill = paybill)
    
    if len(filter_paybill) > 0:
        
        client_ref_ss =  filter_paybill[0].client_ref
        client_sec_ss = filter_paybill[0].client_secret
        development_ss = filter_paybill[0].developmet
        password  = filter_paybill[0].password
        basee_url = getBaseUrl(paybill)
        
        logger.info(dict(updated_data="The paybill is found"))
    
        
        # print("thee keys ",client_ref_ss,client_sec_ss,development_ss)
        logger.info(dict(updated_data= f" thee keys {client_ref_ss} , {client_sec_ss} , {development_ss} , {basee_url} "))
      
     
        transaction_type = "CustomerPayBillOnline"
        if not is_paybil:
            transaction_type = "CustomerBuyGoodsOnline"

        url = f"{basee_url}/mpesa/stkpush/v1/processrequest"
        token = None
        
        try:
            token =  get_token(client_ref_ss,client_sec_ss,development_ss)
            
            
            headers = {
                    "Authorization": "Bearer {}".format(token)
                }
        
            logger.info(dict(updated_data= f"The header is {headers}"))
        
            timestamp = (
                    str(datetime.now())[:-7]
                    .replace("-", "")
                    .replace(" ", "")
                    .replace(":", "")
                )
            password = base64.b64encode(
                    bytes(
                        "{}{}{}".format(
                            paybill,
                            C2B_ONLINE_PASSKEY,
                            timestamp,
                        ),
                        "utf-8",
                    )
                ).decode("utf-8")
            body = dict(
                    BusinessShortCode=paybill,
                    Password=password,
                    Timestamp=timestamp,
                    TransactionType=transaction_type,
                    Amount=str(amount),
                    PartyA=str(msisdn),
                    PartyB=paybill,
                    
                    PhoneNumber=str(msisdn),
                    CallBackURL=f"{C2B_ONLINE_CHECKOUT_CALLBACK_URL}/api/v1/c2b/online_checkout/callback",
                    AccountReference=account_reference,
                    TransactionDesc=transaction_desc,
                )
                
            logger.info(
                                dict(
                    BusinessShortCode=paybill,
                    Password=password,
                    Timestamp=timestamp,
                    TransactionType=transaction_type,
                    Amount=str(amount),
                    PartyA=str(msisdn),
                    PartyB=paybill,
                    
                    PhoneNumber=str(msisdn),
                    CallBackURL=f"{C2B_ONLINE_CHECKOUT_CALLBACK_URL}/api/v1/c2b/online_checkout/callback",
                    AccountReference=account_reference,
                    TransactionDesc=transaction_desc,
                ))
            response = post(url=url, headers=headers, data=body)
                
                
            js = response.json()

            db.MerchantRequestID = js['MerchantRequestID']
            db.CheckoutRequestID =  js['CheckoutRequestID']
            db.ResponseCode =  js['ResponseCode']
            db.ResponseDescription = js['ResponseDescription']
            db.CustomerMessage = js['CustomerMessage']
            db.save()

            
        

            # background_thread = threading.Thread(target=handleCallback_m, args=(paybill, db,True))

            # # Start the thread
            # background_thread.start()
            
            # handleCallback_m(paybill,db)
            return response.json()
        
        except:
            return {
                "status":"Failed",
                "message":"Error connecting"
            }
        #     return JsonResponse(token, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
    
    else:
        logger.info(dict(updated_data=f"The paybill is not found here {paybill}"))
    

        return {"status":"Failed",
                "message":"paybill is not found"}