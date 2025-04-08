import base64
from datetime import datetime
import time
import traceback
import threading
import requests
from config.settings.settings import (
    C2B_CONFIRMATION_URL,
    C2B_VALIDATE_URL,
    C2B_ONLINE_CHECKOUT_CALLBACK_URL
)
from payments.models import AuthToken
from config.util.http import post
from django.http import JsonResponse
from rest_framework import status
from utils.logs import (
     make_api_request_log_request
)
from payments.models import (
     MpesaRequest,
     OnlineCheckoutResponse,
     MpesaCallbackMetaData
)

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
import json


def register_c2b_url(paybill,response_type,role,request,endpoint):
    """
    Register the c2b_url
    :return:
    """
    filter_paybill = PayBillNumbers.objects.filter(paybill = paybill)
    
    if len(filter_paybill) > 0:
        client_ref_ss =  filter_paybill[0].client_ref
        client_sec_ss = filter_paybill[0].client_secret
        development_ss = filter_paybill[0].developmet
        password  = filter_paybill[0].password
        basee_url = getBaseUrl(paybill)
        url = f"{basee_url}/mpesa/c2b/v1/registerurl"
        logger.info(dict(updated_data=f"Began registering token for url {url}"))

        try:
            token =  get_token(client_ref_ss,client_sec_ss,development_ss)
            
            headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
            logger.info(dict(updated_data=f"Began registering header  for url {headers}"))
            body = dict(
                ShortCode=paybill,
                ResponseType=response_type,
                ConfirmationURL=C2B_CONFIRMATION_URL,
                ValidationURL=C2B_VALIDATE_URL,
            )

            logger.info(dict(updated_data=f"Began registering token for url {body}"))
            response = post(url=url, headers=headers, data=body)
            jj = response.json()
            dddata = {
                            "role": role,
                            "successfull": True,
                            "message": f"Successfully registed the {C2B_CONFIRMATION_URL} and {C2B_VALIDATE_URL} response is {jj}!",
                            "endpoint": endpoint
                        }
            kk = make_api_request_log_request(request,dddata)
            return {
                 "status":"Success",
                 "status_code":response.status_code,
                 "message":"Connected to register Endpoint",
                 "data":jj
            }
        
        except Exception as e:
            error_message = traceback.format_exc()
            dddata = {
                            "role": role,
                            "successfull": False,
                            "message": f"Error connecting to register url {url} error is {error_message} !",
                            "endpoint": endpoint
                        }
            kk = make_api_request_log_request(request,dddata)
            return {
                  "status":"Failed",
                  "status_code":500,
                  "message":"Error connecting to register",
                  "data":{}
             }

    else:

        dddata = {
                            "role": role,
                            "successfull": False,
                            "message": f"Paybill {paybill} does not exist",
                            "endpoint": endpoint
                        }
        kk = make_api_request_log_request(request,dddata)
        return {
              "status":"Failed",
              "status_code":400,
              "message":"Paybill does not exist",
              "data":{}
         }

def handleCallback_m(message,db):
  
        try:
            get_mm =  MpesaCallbackMetaData.objects.filter(rdb = db)
            if len(get_mm) > 0:
                 
                logger.info(dict(updated_data=f"sending response in {message}"))
                payload =  json.dumps(json.loads(get_mm[0].description))
                headers = {
                'Content-Type': 'application/json',
              
                }
                res =  requests.post(db.callback_url,data = payload,headers=headers
                )  
                db.callback_sent =  True
                db.save()
            else:
                 logger.info(dict(updated_data=f"issue sending data {message}"))
                 
        except:
            pass

    


        

def simulate_c2b_transaction(paybill,is_paybill,amount,phoneNumber,billReference,role,request,endpoint):
        filter_paybill = PayBillNumbers.objects.filter(paybill = paybill)
    
        if len(filter_paybill) > 0:
            client_ref_ss =  filter_paybill[0].client_ref
            client_sec_ss = filter_paybill[0].client_secret
            development_ss = filter_paybill[0].developmet
            password  = filter_paybill[0].password
            basee_url = getBaseUrl(paybill)
            api_url = f"{basee_url}/mpesa/c2b/v1/simulate"

            try:
                token =  get_token(client_ref_ss,client_sec_ss,development_ss)
            
                headers = {
                    "Authorization": "Bearer {}".format(token),
                    "Content-Type": "application/json"
                }
                transaction_type = "CustomerPayBillOnline"
                if not is_paybill:
                        transaction_type = "CustomerBuyGoodsOnline"

                request = {"ShortCode": paybill,
                        "CommandID": transaction_type,
                        "Amount": amount,
                        "Msisdn": phoneNumber,
                        "BillRefNumber": billReference}

                response = requests.post(api_url, json=request, headers=headers)
                jj = response.json()
                dddata = {
                            "role": role,
                            "successfull": True,
                            "message": f"Simulation was successful, the response is {jj}",
                            "endpoint": endpoint
                        }
                kk = make_api_request_log_request(request,dddata)

                return {
                 "status":"Success",
                    "status_code":response.status_code,
                    "message":"Connected to simulate Endpoint",
                    "data":jj
                }
            except Exception as e:
                error_message = traceback.format_exc()

                dddata = {
                            "role": role,
                            "successfull": False,
                            "message": f"Error generating simulation response,error is {error_message} ",
                            "endpoint": endpoint
                        }
                kk = make_api_request_log_request(request,dddata)

                return {
                  "status":"Failed",
                  "status_code":500,
                  "message":"Error connecting to register",
                  "data":{}
             }
        
        else:
            dddata = {
                                "role": role,
                                "successfull": False,
                                "message": f"Paybill {paybill} does not exist",
                                "endpoint": endpoint
                            }
            kk = make_api_request_log_request(request,dddata)

            return {
                "status":"Failed",
                "status_code":400,
                "message":"Paybill does not exist",
                "data":{}
            }

def process_online_checkout(
    msisdn: int,
    amount: int,
    paybill : int,
    account_reference: str,
    transaction_desc: str,
    role: str,
    request,
    endpoint,
    is_paybil=True,
    db  =  None,
    
    
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
                            password,
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
                    CallBackURL=f"{C2B_ONLINE_CHECKOUT_CALLBACK_URL}/api/v1/c2b/online_checkout/callback/",
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
                    CallBackURL=f"{C2B_ONLINE_CHECKOUT_CALLBACK_URL}/api/v1/c2b/online_checkout/callback/",
                    AccountReference=account_reference,
                    TransactionDesc=transaction_desc,
                ))
            response = post(url=url, headers=headers, data=body)
                
            
            js = response.json()
            dddata = {
                            "role": role,
                            "successfull": True,
                            "message": f"Initiates stk push successfully {js}",
                            "endpoint": endpoint
                        }
            kk = make_api_request_log_request(request,dddata)
            

            try:

                dddata = {
                            "role": role,
                            "successfull": True,
                            "message": f"Saved Response to db Successfully",
                            "endpoint": endpoint
                        }
                kk = make_api_request_log_request(request,dddata)
                
                db.MerchantRequestID = js['MerchantRequestID']
                db.CheckoutRequestID =  js['CheckoutRequestID']
                db.ResponseCode =  js['ResponseCode']
                db.ResponseDescription = js['ResponseDescription']
                db.CustomerMessage = js['CustomerMessage']
                db.save()

            except:
                 pass

            
        

            # background_thread = threading.Thread(target=handleCallback_m, args=(paybill, db,True))

            # # Start the thread
            # background_thread.start()
            
            # handleCallback_m(paybill,db)
            return  {"code":response.status_code,"message":response.json()}
        
        except  Exception as e:
            error_message = traceback.format_exc()
            dddata = {
                            "role": role,
                            "successfull": False,
                            "message": f"Error conencting to {url} error {error_message}",
                            "endpoint": endpoint
                        }
            kk = make_api_request_log_request(request,dddata)
            
            return {"code":500,"message": {
                "status":"Failed",
                "message":"Error connecting"
            }}
        #     return JsonResponse(token, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
    
    else:
        logger.info(dict(updated_data=f"The paybill is not found here {paybill}"))
        dddata = {
                            "role": role,
                            "successfull": False,
                            "message": f"Paybill {paybill} not found",
                            "endpoint": endpoint
                        }
        kk = make_api_request_log_request(request,dddata)
        return {"code":500,"message": {
                "status":"Failed",
                "message":"paybill is not found"
            }}
    

       
    

def query_stk(check_out_id,paybill,role,request,endpoint):
    logger.info(dict(updated = f"initiated stk query for {check_out_id} {paybill} "))
        
    filter_paybill = PayBillNumbers.objects.filter(paybill = paybill)
    
    if len(filter_paybill) > 0:
        
        client_ref_ss =  filter_paybill[0].client_ref
        client_sec_ss = filter_paybill[0].client_secret
        development_ss = filter_paybill[0].developmet
        password  = filter_paybill[0].password
        basee_url = getBaseUrl(paybill)
            
        
        try:
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
                            password,
                            timestamp,
                        ),
                        "utf-8",
                    )
                ).decode("utf-8")
            token =  get_token(client_ref_ss,client_sec_ss,development_ss)
            
            
            headers = {
                    'Content-Type': 'application/json',
                    "Authorization": "Bearer {}".format(token)
                }
            
            logger.info(dict(updated = f"the sent headers is {headers}"))
     
            payload = {
                    "BusinessShortCode": paybill,
                    "Password":password,
                    "Timestamp": timestamp,
                    "CheckoutRequestID": check_out_id,
                }
            
           
            
            logger.info(dict(updated = f"The request payload is {payload}"))
            response = requests.post(f'{basee_url}/mpesa/stkpushquery/v1/query', headers = headers, json = payload)

            js_ =  response.json()
            dddata = {
                            "role": role,
                            "successfull": True,
                            "message": f"Received response {js_} for {check_out_id} {paybill}",
                            "endpoint": endpoint
                        }
            kk = make_api_request_log_request(request,dddata)


            logger.info(dict(updated= f"Received response {js_} for {check_out_id} {paybill}"))
            try:
                if int(js_['ResultCode']) == 0:
                    obj =  MpesaRequest.objects.filter(CheckoutRequestID = check_out_id ) 
                    if len(obj) > 0:
                         obj[0].paid = "PAID"
                         obj[0].save()
                         mm =  OnlineCheckoutResponse.objects.create(
                             rdb =  obj[0],
                             merchant_request_id = obj[0].MerchantRequestID,
                             checkout_request_id = obj[0].CheckoutRequestID,
                             result_code = js_['ResultCode'],
                             result_description = js_['ResultDesc'],
                             amount = obj[0].amount
                         )
                         background_thread = threading.Thread(target=handleCallback_m, args=(js_['ResultDesc'],obj[0]))

                        # Start the thread
                         background_thread.start()

                else:
                    obj =  MpesaRequest.objects.filter(CheckoutRequestID = check_out_id ) 
                    if len(obj) > 0:
                         obj[0].paid = "CANCELLED"
                         obj[0].save()
                         obj[0].paid = "PAID"
                         obj[0].save()
                         mm =  OnlineCheckoutResponse.objects.create(
                             rdb =  obj[0],
                             merchant_request_id = obj[0].MerchantRequestID,
                             checkout_request_id = obj[0].CheckoutRequestID,
                             result_code = js_['ResultCode'],
                             result_description = js_['ResultDesc'],
                             amount = obj[0].amount
                         )

                         background_thread = threading.Thread(target=handleCallback_m, args=(js_['ResultDesc'],obj[0]))

                        # Start the thread
                         background_thread.start()



            except:
                dddata = {
                            "role": role,
                            "successfull": True,
                            "message": f"Could not save  {js_} for {check_out_id} {paybill} to db ",
                            "endpoint": endpoint
                        }
                kk = make_api_request_log_request(request,dddata)
                pass

                         
           
            js_['BillRefNumber'] = obj.accountReference
            js_['TRANSID'] =  mm.mpesa_receipt_number
            return {
                    "code": response.status_code,
                    "message": js_
                }
            

        except Exception as e:
            error_message = traceback.format_exc()
            dddata = {
                            "role": role,
                            "successfull": True,
                            "message": f"Could not get The stk query response error is {error_message}",
                            "endpoint": endpoint
                        }
            kk = make_api_request_log_request(request,dddata)

            return {
                  "code":500,
                  "message":{
                       "status":"Failed",
                       "message":"Error getting data"
                  }
             }