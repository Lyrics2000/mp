from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from .Middleware import MicrosoftValidation
import json
import json
from django.utils.dateparse import parse_datetime
from .models import CardPaymentsTransactions

from utils.app import (
      OracleDB
)
from config.settings.settings import (
    PAYMENTS_STK_PUSH,
    PAYMENT_QUERY_STK_PUSH,
    PAYMENT_GET_TRANSACTIONAL_STATUS,
    PAYMENT_ADD_PAYBILL,
    PAYMENT_C2B_SIMULATE,
    PAYMENT_GET_FILTER_MPESA,
    PAYMENT_REGISTER_URL,
    PAYMENT_ADD_BUSINESS,
    PAYMENTS_STK_PUSH_BUSINESS,
    PAYMENT_VERIFY_CHECKOUT_ID,
    PAYMENT_ADD_USER,
    PAYMENT_VERIFY_MANUAL_PAYMENT
)

from config.util.c2butils import (
      process_online_checkout
)

from .important.ImportantClasses import (
    LipaNaMpesa,
    format_phone_number
)


from .models import OnlineCheckoutResponse

from .models import (
    MpesaRequest,
    MpesaCallbackMetaData,
    C2BPaymentsValidation,
    C2BPaymentsConfirmation,
    AuthToken,
    OnlineCheckout,
    UserRequestsModel
)

from django.views.decorators.csrf import csrf_exempt


from .serializers import (
   MpesaSerializers,
    MpesaCallbackMetaDataSerializers,
    C2BPaymentsValidationSerializer,
    C2BPaymentsConfirmationSerializer,
    StoreBusinessCodeSerializer,
    UserRequestsModelSerializer
)
import threading
from rest_framework.generics import CreateAPIView
from datetime import datetime
import pytz
from config.util.c2butils import handleCallback_m
from .tasks import (
    process_b2c_result_response_task,
    process_c2b_confirmation_task,
    process_c2b_validation_task,
    handle_online_checkout_callback_task,
    call_online_checkout_task
)

from config.util.c2butils import (
    process_online_checkout,
    query_stk,
    register_c2b_url,
    simulate_c2b_transaction
)

from .mpesa import (
    Mpesa
)

import logging

logger = logging.getLogger(__name__)

from .models import (
    PayBillNumbers,
    StoreBusinessCode
)

from .serializers import (
    PayBillNumbersSerializers
)

from utils.logs import (
     make_api_request_log_request
)


class UserRequestsModelApiView(APIView):
      def post(self,request):
        app =  MicrosoftValidation(request).verify()
            
        if app.status_code == 401:
                return app

        if PAYMENT_ADD_USER in app.json()['data']['roles']:
            business_id =  request.data.get("business_id",None)
            name =  request.data.get("name",None)
            key =  request.data.get("key",None)

            if None in [business_id,name,key]:
                    dddata = {
                            "role": PAYMENT_ADD_USER,
                            "successfull": False,
                            "message": f"add all required fields",
                            "endpoint": "api/v1/add/user/"
                        }
                    kk = make_api_request_log_request(request,dddata)

                    if kk['code'] > 204:
                                    return Response(kk['message'],status = kk['code'])
                    
                    return Response({
                          "status":"Failed",
                          "message":"Fill all required details"
                    },status=400)
              
            else:
                try:
                        int(business_id)
                except:
                    dddata = {
                            "role": PAYMENT_ADD_USER,
                            "successfull": False,
                            "message": f"Invalid Business id",
                            "endpoint": "api/v1/add/user/"
                        }
                    kk = make_api_request_log_request(request,dddata)

                    if kk['code'] > 204:
                                    return Response(kk['message'],status = kk['code'])
                      

                    return Response({
                          "status":"Failed",
                          "message":"Invalid business id"
                    },status=400)
                

                check_biz = StoreBusinessCode.objects.filter(id  =  int(business_id))

                if len(check_biz) > 0:
                      obj,update =  UserRequestsModel.objects.update_or_create(
                            business = check_biz[0],
                            name =  name,
                            key =  key

                      )

                      if obj:
                        dddata = {
                            "role": PAYMENT_ADD_USER,
                            "successfull": True,
                            "message": f"Created the user successfully",
                            "endpoint": "api/v1/add/user/"
                        }
                        kk = make_api_request_log_request(request,dddata)

                        if kk['code'] > 204:
                                        return Response(kk['message'],status = kk['code'])

                        return Response({
                              "status":"Failed",
                              "message":"Created successfully",
                              "data":UserRequestsModelSerializer(obj).data
                        },status=201)
                      else:
                        dddata = {
                            "role": PAYMENT_ADD_USER,
                            "successfull": False,
                            "message": f"Internal Error creating user",
                            "endpoint": "api/v1/add/user/"
                        }
                        kk = make_api_request_log_request(request,dddata)

                        if kk['code'] > 204:
                                        return Response(kk['message'],status = kk['code'])

                        return Response({
                              "status":"Failed",
                              "message":"Internal Error creating user"
                        },status=500)
                else:
                    dddata = {
                            "role": PAYMENT_ADD_USER,
                            "successfull": False,
                            "message": f"Business with id {business_id} is not found",
                            "endpoint": "api/v1/add/user/"
                        }
                    kk = make_api_request_log_request(request,dddata)

                    if kk['code'] > 204:
                                    return Response(kk['message'],status = kk['code'])

                    return Response(
                          {
                                "status":"Failed",
                                "message":f"Business with id {business_id} is not found"
                          },status=400
                    ) 
  

        else:
            dddata = {
                            "role": PAYMENT_ADD_USER,
                            "successfull": False,
                            "message": f"You have no right",
                            "endpoint": "api/v1/add/user/"
                        }
            kk = make_api_request_log_request(request,dddata)

            if kk['code'] > 204:
                            return Response(kk['message'],status = kk['code'])
            return Response({
                "status":"Failed",
                "message":"You have no rights for this request"
            },status =  400)
              
              
            
class QueryMpesaStatement(APIView):
    def post(self,request):

        app =  MicrosoftValidation(request).verify()
            
        if app.status_code == 401:
                return app

        if PAYMENT_QUERY_STK_PUSH in app.json()['data']['roles']:
            check_out_id =  request.data.get("check_out_id",None)
            paybill  = request.data.get("paybill",None)

            if None in [check_out_id,paybill]:
                return Response({
                    "status":"Failed",
                    "message":"Fill all details"
                },status=400)
            
            # check_if checkout_id_exist

            k = MpesaRequest.objects.filter(
                  CheckoutRequestID = check_out_id
            )

            if len(k) > 0:
                app =  query_stk(check_out_id,paybill,PAYMENT_QUERY_STK_PUSH,request,"api/v1/stk/query/")

                return Response(app['message'],status=app['code'])
            else:
                dddata = {
                            "role": PAYMENT_QUERY_STK_PUSH,
                            "successfull": False,
                            "message": f"Checkout id not found in our system {check_out_id} for paybill {paybill}",
                            "endpoint": "api/v1/stk/"
                        }
                kk = make_api_request_log_request(request,dddata)

                if kk['code'] > 204:
                                return Response(kk['message'],status = kk['code'])
                
                return Response({
                      "status":"Failed",
                      "message":f"checkout id {check_out_id} is not found in our system!"
                },status=400)


        else:
            dddata = {
                            "role": PAYMENT_QUERY_STK_PUSH,
                            "successfull": False,
                            "message": f"User doesnt have rights",
                            "endpoint": "api/v1/stk/"
                        }
            kk = make_api_request_log_request(request,dddata)

            if kk['code'] > 204:
                            return Response(kk['message'],status = kk['code'])
            return Response({
                "status":"Failed",
                "message":"You have no rights for this request"
            },status =  400)


class VerifyManualApiView(APIView):
      def post(self,request):
        app =  MicrosoftValidation(request).verify()
            
        if app.status_code == 401:
                return app

        if PAYMENT_VERIFY_MANUAL_PAYMENT in app.json()['data']['roles']: 
              transId =  request.data.get("transId",None)
              payBill =  request.data.get("payBill",None)
              BillRefNumber  =  request.data.get("billRefNumber",None)

              if None in [transId,payBill,BillRefNumber]:
                    dddata = {
                            "role": PAYMENT_VERIFY_MANUAL_PAYMENT,
                            "successfull": False,
                            "message": f"Verification Successfully!",
                            "endpoint": "verify/manual/"
                        }
                    
                    kk = make_api_request_log_request(request,dddata)
                    if kk['code'] > 204:
                            return Response(kk['message'],status = kk['code'])
                    return Response({
                          "status":"Failed",
                          "message":"Fill required details"
                    },status =  400)
              else:
    
                c2bmodel_data = C2BPaymentsConfirmation.objects.filter(
                    TransID = str(transId),
                    BusinessShortCode = payBill,
                    BillRefNumber = BillRefNumber,
                
                ) 

                if len(c2bmodel_data) > 0:

                    dddata = {
                                    "role": PAYMENT_VERIFY_MANUAL_PAYMENT,
                                    "successfull": True,
                                    "message": f"Successfully retrieved data {c2bmodel_data[0].TransID}!",
                                    "endpoint": "verify/manual/"
                                }
                            
                    kk = make_api_request_log_request(request,dddata)
                    if kk['code'] > 204:
                                    return Response(kk['message'],status = kk['code'])
                    return Response({
                        "status":"Success",
                        "message":"Retrived successfully",
                        "data":C2BPaymentsConfirmationSerializer(c2bmodel_data,many = True).data
                    })
                else:
                    dddata = {
                                    "role": PAYMENT_VERIFY_MANUAL_PAYMENT,
                                    "successfull": False,
                                    "message": f"No data found for {transId} {payBill} {BillRefNumber}!",
                                    "endpoint": "verify/manual/"
                                }
                            
                    kk = make_api_request_log_request(request,dddata)
                    if kk['code'] > 204:
                        return Response(kk['message'],status = kk['code'])
                    return Response({
                            "status":"Failed",
                            "message":"No data found",
                            "data":[]
                    },status=400)

        else:
              
            dddata = {
                        "role": PAYMENT_VERIFY_MANUAL_PAYMENT,
                        "successfull": False,
                        "message": f"User Doesnt have rights to insert paybill endpoint",
                        "endpoint": "api/v1/add/paybill/"
                    }
            kk = make_api_request_log_request(request,dddata)
            if kk['code'] > 204:
                return Response(kk['message'],status = kk['code'])
            
            return Response({
                "status":"Failed",
                "message":"You have no rights for this request"
            },status =  400)      
                    

class AddPaybill(APIView):
    def post(self,request):
        app =  MicrosoftValidation(request).verify()
            
        if app.status_code == 401:
                return app

        if PAYMENT_ADD_PAYBILL in app.json()['data']['roles']:
            paybill =  request.data.get("paybill",None)
            client_ref =  request.data.get("client_ref",None)
            client_secret =  request.data.get("client_secret",None)
            developmet =  request.data.get("developmet",None)
            password = request.data.get("password",None)
            tyee = request.data.get("type",None)

            if None in [paybill,client_ref,client_secret,developmet,tyee,password]:
                return Response({
                    "status":"Success",
                    "message":"Fill all details"
                },status =  400)
            
            if tyee == "CREATE":
            
                obj = PayBillNumbers.objects.create(
                    paybill = int(paybill),
                    client_ref =  client_ref,
                    client_secret =  client_secret,
                    developmet =  developmet,
                    password = password
                )

                if obj:
                    dddata = {
                            "role": PAYMENT_ADD_PAYBILL,
                            "successfull": True,
                            "message": f"Paybill Created successfully!",
                            "endpoint": "api/v1/add/paybill/"
                        }
                    
                    kk = make_api_request_log_request(request,dddata)
                    if kk['code'] > 204:
                            return Response(kk['message'],status = kk['code'])
                    return Response({
                        "status":"Success",
                        "message":"Data created",
                        "data": PayBillNumbersSerializers(obj).data
                    },status=201)
                
            elif tyee  == "UPDATE":
                f = PayBillNumbers.objects.filter(
                    paybill =  int(paybill)
                )

                if len(f) > 0:
                    f[0].client_ref =  client_ref
                    f[0].client_secret =  client_secret
                    f[0].developmet =  developmet
                    f[0].password = password
                    f[0].save()
                    dddata = {
                            "role": PAYMENT_ADD_PAYBILL,
                            "successfull": True,
                            "message": f"Paybill Updated successfully!",
                            "endpoint": "api/v1/add/paybill/"
                        }
                    kk = make_api_request_log_request(request,dddata)
                    if kk['code'] > 204:
                            return Response(kk['message'],status = kk['code'])
                    return Response({
                        "status":"Success",
                        "message":"updated successfully",
                        "data": PayBillNumbersSerializers(f[0]).data
                    },status=200)
                
                else:
                    dddata = {
                            "role": PAYMENT_ADD_PAYBILL,
                            "successfull": False,
                            "message": f"Paybill {paybill} not found in db",
                            "endpoint": "api/v1/add/paybill/"
                        }
                    kk = make_api_request_log_request(request,dddata)
                    if kk['code'] > 204:
                            return Response(kk['message'],status = kk['code'])
                    return Response({
                        "status":"Failed",
                        "message":"Paybill not found"
                    },status =  200)





            dddata = {
                        "role": PAYMENT_ADD_PAYBILL,
                        "successfull": False,
                        "message": f"An errror occured while inserting Paybill",
                        "endpoint": "api/v1/add/paybill/"
                    }
            kk = make_api_request_log_request(request,dddata)
            if kk['code'] > 204:
                return Response(kk['message'],status = kk['code'])
            
            return Response({
                "status":"Failed",
                "message":"An error occured"
            },status =  400)

        else:
            dddata = {
                        "role": PAYMENT_ADD_PAYBILL,
                        "successfull": False,
                        "message": f"User Doesnt have rights to insert paybill endpoint",
                        "endpoint": "api/v1/add/paybill/"
                    }
            kk = make_api_request_log_request(request,dddata)
            if kk['code'] > 204:
                return Response(kk['message'],status = kk['code'])
            
            return Response({
                "status":"Failed",
                "message":"You have no rights for this request"
            },status =  400)


class CreateBusinessApiView(APIView):
    def post(self,request):
        app =  MicrosoftValidation(request).verify()
            
        if app.status_code == 401:
                return app

        if PAYMENT_ADD_BUSINESS in app.json()['data']['roles']:
            name =  request.data.get("name",None)
            key =  request.data.get("key",None)
            
        
            if None in [key]:
                return Response({
                    "status":"Success",
                    "message":"Fill all details"
                },status =  400)

            
            obj,updated = StoreBusinessCode.objects.update_or_create(
                    name = name,
                    key = key
                )

            if obj:
                    dddata = {
                            "role": PAYMENT_ADD_BUSINESS,
                            "successfull": True,
                            "message": f"Updated Successfully!",
                            "endpoint": "api/v1/add/business/"
                        }
                    
                    kk = make_api_request_log_request(request,dddata)
                    if kk['code'] > 204:
                            return Response(kk['message'],status = kk['code'])
                    return Response({
                        "status":"Success",
                        "message":"Data created",
                        "data": StoreBusinessCodeSerializer(obj).data
                    },status=201)
            
            else:
                dddata = {
                            "role": PAYMENT_ADD_BUSINESS,
                            "successfull": True,
                            "message": f"Could not update successfully!",
                            "endpoint": "api/v1/add/business/"
                        }
                    
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                            return Response(kk['message'],status = kk['code']) 
                
                return Response({
                        "status":"Failed",
                        "message":"Data created",
                    },status=400)

        else:
            dddata = {
                        "role": PAYMENT_ADD_BUSINESS,
                        "successfull": False,
                        "message": f"User Doesnt have rights to insert paybill endpoint",
                        "endpoint": "api/v1/add/paybill/"
                    }
            kk = make_api_request_log_request(request,dddata)
            if kk['code'] > 204:
                return Response(kk['message'],status = kk['code'])
            
            return Response({
                "status":"Failed",
                "message":"You have no rights for this request"
            },status =  400)






class B2cResult(APIView):
    """
    Handle b2c result
    """

    @csrf_exempt
    def post(self, request, format=None):
        """
        process the timeout
        :param request:
        :param format:
        :return:
        """
        data = request.data
        process_b2c_result_response_task.apply_async(
            args=(data,), queue="b2c_result"
        )
        return Response(dict(value="ok", key="status", detail="success"))


def insert_payment_transaction(data):
    # Parse date fields explicitly
    auth_time = parse_datetime(data.get("auth_time").replace("T", "").replace("Z", "")) if data.get("auth_time") else None
    signed_date_time = parse_datetime(data.get("signed_date_time")) if data.get("signed_date_time") else None

    # Convert amounts to Decimal if needed
    auth_amount = data.get("auth_amount")
    req_amount = data.get("req_amount")
    try:
        auth_amount = float(auth_amount)
    except (TypeError, ValueError):
        auth_amount = 0.0
    try:
        req_amount = float(req_amount)
    except (TypeError, ValueError):
        req_amount = 0.0

    transaction = CardPaymentsTransactions.objects.create(
        req_locale = data.get("req_locale"),
        req_payer_authentication_indicator = data.get("req_payer_authentication_indicator"),
        payer_authentication_acs_transaction_id = data.get("payer_authentication_acs_transaction_id"),
        req_card_type_selection_indicator = data.get("req_card_type_selection_indicator"),
        auth_trans_ref_no = data.get("auth_trans_ref_no"),
        payer_authentication_enroll_veres_enrolled = data.get("payer_authentication_enroll_veres_enrolled"),
        req_bill_to_surname = data.get("req_bill_to_surname"),
        req_card_expiry_date = data.get("req_card_expiry_date"),
        merchant_advice_code = data.get("merchant_advice_code"),
        req_bill_to_phone = data.get("req_bill_to_phone"),
        card_type_name = data.get("card_type_name"),
        auth_amount = auth_amount,
        auth_response = data.get("auth_response"),
        bill_trans_ref_no = data.get("bill_trans_ref_no"),
        req_payment_method = data.get("req_payment_method"),
        req_payer_authentication_merchant_name = data.get("req_payer_authentication_merchant_name"),
        auth_time = auth_time,
        transaction_id = data.get("transaction_id"),
        req_card_type = data.get("req_card_type"),
        payer_authentication_transaction_id = data.get("payer_authentication_transaction_id"),
        payer_authentication_pares_status = data.get("payer_authentication_pares_status"),
        payer_authentication_cavv = data.get("payer_authentication_cavv"),
        auth_avs_code = data.get("auth_avs_code"),
        auth_code = data.get("auth_code"),
        payment_token_instrument_identifier_new = data.get("payment_token_instrument_identifier_new"),
        payer_authentication_specification_version = data.get("payer_authentication_specification_version"),
        req_bill_to_address_country = data.get("req_bill_to_address_country"),
        req_profile_id = data.get("req_profile_id"),
        signed_date_time = signed_date_time,
        req_bill_to_address_line1 = data.get("req_bill_to_address_line1"),
        payer_authentication_validate_e_commerce_indicator = data.get("payer_authentication_validate_e_commerce_indicator"),
        req_card_number = data.get("req_card_number"),
        signature = data.get("signature"),
        payment_token = data.get("payment_token"),
        payment_token_instrument_identifier_id = data.get("payment_token_instrument_identifier_id"),
        req_bill_to_address_city = data.get("req_bill_to_address_city"),
        auth_cavv_result = data.get("auth_cavv_result"),
        reason_code = data.get("reason_code"),
        req_bill_to_forename = data.get("req_bill_to_forename"),
        req_payer_authentication_acs_window_size = data.get("req_payer_authentication_acs_window_size"),
        payment_account_reference = data.get("payment_account_reference"),
        request_token = data.get("request_token"),
        req_device_fingerprint_id = data.get("req_device_fingerprint_id"),
        auth_cavv_result_raw = data.get("auth_cavv_result_raw"),
        req_amount = req_amount,
        req_bill_to_email = data.get("req_bill_to_email"),
        payer_authentication_reason_code = data.get("payer_authentication_reason_code"),
        auth_avs_code_raw = data.get("auth_avs_code_raw"),
        req_currency = data.get("req_currency"),
        decision = data.get("decision"),
        message = data.get("message"),
        req_transaction_uuid = data.get("req_transaction_uuid"),
        payer_authentication_eci = data.get("payer_authentication_eci"),
        req_transaction_type = data.get("req_transaction_type"),
        payer_authentication_xid = data.get("payer_authentication_xid"),
        req_access_key = data.get("req_access_key"),
        req_reference_number = data.get("req_reference_number"),
        payer_authentication_validate_result = data.get("payer_authentication_validate_result"),
        payment_token_instrument_identifier_status = data.get("payment_token_instrument_identifier_status"),
        auth_reconciliation_reference_number = data.get("auth_reconciliation_reference_number"),
        signed_field_names = data.get("signed_field_names")
    )

    return transaction


class RecurringCardsView(APIView):
    """
    Handle c2b Confirmation
    """

    @csrf_exempt
    def post(self, request, format=None):
        """
        process the confirmation
        :param request:
        :param format:
        :return:
        """
        data = request.data
        print("The data is :",data)
        logger.info(f"The data is {data}")
        data_dict = dict(line.split("=", 1) for line in data.strip().split("\n"))

        # Convert to JSON
        json_output = json.dumps(data_dict, indent=2)
        loaded_json =  json.loads(json_output)
        inserted_transaction = insert_payment_transaction(json_data)
        return Response(dict(value="ok", key="status", detail="success"))



class C2bConfirmation(APIView):
    """
    Handle c2b Confirmation
    """

    @csrf_exempt
    def post(self, request, format=None):
        """
        process the confirmation
        :param request:
        :param format:
        :return:
        """
        data = request.data
        process_c2b_confirmation_task.apply_async(
            args=(data,), queue="c2b_confirmation"
        )
        return Response(dict(value="ok", key="status", detail="success"))



class C2bValidation(APIView):
    """
    Handle c2b Validation
    """

    @csrf_exempt
    def post(self, request, format=None):
        """
        process the c2b Validation
        :param request:
        :param format:
        :return:
        """
        data = request.data
        process_c2b_validation_task.apply_async(
            args=(data,), queue="c2b_validation"
        )
        return Response(dict(value="ok", key="status", detail="success"))



class OnlineCheckoutCallback(APIView):
    """
    Handle online checkout callback
    """

    @csrf_exempt
    def post(self, request, format=None):
        """
        process the confirmation
        :param request:
        :param format:
        :return:
        """
        data = request.data
        print("the callback has started...")
        logger.info(dict(update_info=f"the data is {data}"))

        handle_online_checkout_callback_task(
            data
        )

        # background_thread = threading.Thread(target=handleCallback_m, args=(response,all_m[0]))

        #     # Start the thread
        # background_thread.start()
        return Response(dict(value="ok", key="status", detail="success"))


class B2cTimeOut(APIView):
    """
    Handle b2c time out
    """

    @csrf_exempt
    def post(self, request, format=None):
        """
        process the timeout
        :param request:
        :param format:
        :return:
        """
        data = request.data
        return Response(dict(value="ok", key="status", detail="success"))



class C2BConfirmationApiView(CreateAPIView):
    queryset = C2BPaymentsConfirmation.objects.all()
    serializer_class = C2BPaymentsConfirmationSerializer
    permission_classes = [AllowAny]


    def create(self, request):
        logger.info(f"the mpesa Confirmation endpoint is  : {request.data}")
        print(request.data, ': Data from Confirmation')  
        transaction_time = request.data['TransTime']
        str_transaction_date = str(transaction_time)
        transaction_date = datetime.strptime(str_transaction_date, '%Y%m%d%H%M%S')

        #Sync Safaricoms response time with server time
        aware_transaction_date = pytz.utc.localize(transaction_date)
        print(aware_transaction_date)

        transaction_type = request.data['TransactionType']
        transaction_id = request.data['TransID']
        transaction_time = aware_transaction_date
        transaction_amount = request.data['TransAmount']
        business_short_code = request.data['BusinessShortCode']
        bill_ref_number = request.data['BillRefNumber']
        invoice_number = request.data['InvoiceNumber']
        org_account_balance = request.data['OrgAccountBalance']
        third_party_transaction_id = request.data['ThirdPartyTransID']
        phone_number = request.data['MSISDN']
        first_name = request.data['FirstName']
        middle_name = request.data['MiddleName']
        last_name = request.data['LastName']

        c2bmodel_data = C2BPaymentsConfirmation.objects.create(
            TransactionType = transaction_type,
            TransID = transaction_id,
            TransTime = transaction_time,
            TransAmount = transaction_amount,
            BusinessShortCode = business_short_code,
            BillRefNumber = bill_ref_number,
            InvoiceNumber = invoice_number,
            OrgAccountBalance = org_account_balance,
            ThirdPartyTransID = third_party_transaction_id,
            MSISDN = phone_number,
            FirstName = first_name,
            MiddleName = middle_name,
            LastName = last_name,
        )

        c2bmodel_data.save()
        c2b_data = C2BPaymentsConfirmation.objects.all()
        data = C2BPaymentsConfirmationSerializer(c2b_data, many=True)
        c2b_context = {
            "Result Code": 0,
            "Data": data.data
        }

        return Response(c2b_context)


class SimulateApiView(APIView):
    def post(self,request):
        app =  MicrosoftValidation(request).verify()
            
        if app.status_code == 401:
                return app
        
        if PAYMENT_C2B_SIMULATE in app.json()['data']['roles']:
            paybill = request.data.get("paybill",None)
            is_paybill =  request.data.get("is_paybill",None),
            amount =  request.data.get("amount",None)
            phoneNumber =  request.data.get("phoneNumber",None)
            bill_reference =  request.data.get("billReference",None)

            def is_numeric(value):
                        return isinstance(value, (int, float, complex))


            if None in [paybill,is_paybill,amount,phoneNumber,bill_reference]:
                dddata = {
                            "role": PAYMENT_C2B_SIMULATE,
                            "successfull": False,
                            "message": f"Fill all details data needed is ,paybill,is_paybill,amount,phoneNumber,billReference, but data send is {request.data} !",
                            "endpoint": "api/v1/c2b/simulate/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                            return Response(kk['message'],status = kk['code'])
                return Response({
                    "status":"Failed",
                    "message":"Fill all details"
                },status=400)
            
            if not is_numeric(paybill):
                        dddata = {
                            "role": PAYMENT_C2B_SIMULATE,
                            "successfull": False,
                            "message": f"Invalid Paybill format, paybill should be numeric, paybill supplied is {paybill}!",
                            "endpoint": "api/v1/c2b/simulate/"
                        }
                        kk = make_api_request_log_request(request,dddata)
                        if kk['code'] > 204:
                                    return Response(kk['message'],status = kk['code'])
                        return Response({
                            "status": "Failed",
                            "message": "Incorrect Paybill format"
                        })
            
            if not is_numeric(amount):
                        dddata = {
                            "role": PAYMENT_C2B_SIMULATE,
                            "successfull": False,
                            "message": f"Invalid amount format, amount should be numeric, amount supplied is {amount}!",
                            "endpoint": "api/v1/c2b/simulate/"
                        }
                        kk = make_api_request_log_request(request,dddata)
                        if kk['code'] > 204:
                                    return Response(kk['message'],status = kk['code'])
                        return Response({
                            "status": "Failed",
                            "message": "Incorrect Amount format"
                        })
            app = simulate_c2b_transaction(paybill,is_paybill,amount,phoneNumber,bill_reference,PAYMENT_C2B_SIMULATE,request,"api/v1/c2b/simulate/")

            return Response({
                    "status":app['status'],
                    "message":app['message'],
                    "data":app['data']
                },status =  app['status_code'])

        else:
            return Response({
                "status":"Failed",
                "message":"You have no rights for this request"
            },status =  400)


class RegisterURL(APIView):
    def post(self,request):
        app =  MicrosoftValidation(request).verify()
            
        if app.status_code == 401:
                return app
        
        if PAYMENT_REGISTER_URL in app.json()['data']['roles']:
            paybill = request.data.get("paybill",None)
            responseType = request.data.get("responseType",None)
            
            def is_numeric(value):
                    return isinstance(value, (int, float, complex))

            if None in [paybill,responseType]:
                return Response({
                    "status":"Failed",
                    "message":"Fill all required details"
                },status =  400)
            
            if not is_numeric(paybill):
                    return Response({
                        "status": "Failed",
                        "message": "Incorrect Paybill format"
                    })

            # check_paybill = PayBillNumbers.objects.filter(paybill = paybill).first()
            app = register_c2b_url(paybill,responseType,PAYMENT_REGISTER_URL,request,"api/v1/c2b/register/url/")

            return Response({
                "status":app['status'],
                "message":app['message'],
                "data":app['data']
            },status =  app['status_code'])

        else:
            return Response({
                "status":"Failed",
                "message":"You have no rights for this request"
            },status =  400)




class MakeC2BPaymentApiView(APIView):
    def post(self,request):
        phone_number =  request.data.get("phone_number",None)
        amount =  request.data.get("amount",None)
        billRef =  request.data.get("billRef",None)
        
        if None in [phone_number,amount,billRef]:
            return Response({
                "status":"Failed",
                "message":"Fill all details"
            },status=status.HTTP_400_BAD_REQUEST)
            
        app =  LipaNaMpesa(phone_number,billRef,f"{amount}",f"Payment for {billRef} and {amount} and phone {phone_number} ")
        register_url =  app.register_url()
        
        print("to register is ", register_url)
        
        simulate = app.simulate_c2b_transaction()
        print("the simulated is ", simulate)
        
        return Response({
            "status":"Success",
            "message":"The data is simulated successfully",
            "data":simulate
        })
            
        
class C2BValidationApiView(CreateAPIView):
    queryset = C2BPaymentsValidation.objects.all()
    serializer_class = C2BPaymentsValidationSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        logger.info(f"the mpesa validation endpoint is  : {request.data}")
        print(request.data, ': Data from Validation')
            
        transaction_time = request.data['TransTime']
        str_transaction_date = str(transaction_time)
        transaction_date = datetime.strptime(str_transaction_date, '%Y%m%d%H%M%S')

        #Sync Safaricoms response time with server time
        aware_transaction_date = pytz.utc.localize(transaction_date)
        print(aware_transaction_date)

        transaction_type = request.data['TransactionType']
        transaction_id = request.data['TransID']
        transaction_time = aware_transaction_date
        transaction_amount = request.data['TransAmount']
        business_short_code = request.data['BusinessShortCode']
        bill_ref_number = request.data['BillRefNumber']
        invoice_number = request.data['InvoiceNumber']
        org_account_balance = request.data['OrgAccountBalance']
        third_party_transaction_id = request.data['ThirdPartyTransID']
        phone_number = request.data['MSISDN']
        first_name = request.data['FirstName']
        middle_name = request.data['MiddleName']
        last_name = request.data['LastName']

        c2bmodel_data = C2BPaymentsValidation.objects.create(
            TransactionType = transaction_type,
            TransID = transaction_id,
            TransTime = transaction_time,
            TransAmount = transaction_amount,
            BusinessShortCode = business_short_code,
            BillRefNumber = bill_ref_number,
            InvoiceNumber = invoice_number,
            OrgAccountBalance = org_account_balance,
            ThirdPartyTransID = third_party_transaction_id,
            MSISDN = phone_number,
            FirstName = first_name,
            MiddleName = middle_name,
            LastName = last_name,
        )

        c2bmodel_data.save()
        c2b_data = C2BPaymentsValidation.objects.all()
        data = C2BPaymentsValidationSerializer(c2b_data, many=True)
        c2b_context = {
            "Result Code": 0,
            "Data": data.data
        }

        return Response(c2b_context)



from .serializers import OnlineCheckoutResponseSerializer

class CheckTransactionStatus(APIView):
    def get(self,request):
        app = MicrosoftValidation(request).verify()

        if app.status_code != 200:
            return app

        if PAYMENT_GET_TRANSACTIONAL_STATUS in app.json()['data']['roles']:
            checkout_id =  request.query_params.get("checkout_id",None)
            if None in [checkout_id]:
                return Response({
                    "status":"Failed",
                    "message":"Submit correct checkout id"
                },status =  400)
            
            obj =  OnlineCheckoutResponse.objects.filter(checkout_request_id =  checkout_id)

            if len(obj) > 0:
                dddata = {
                            "role": PAYMENT_GET_TRANSACTIONAL_STATUS,
                            "successfull": True,
                            "message": f"Retrived successfully!",
                            "endpoint": "api/v1/check/transaction/status/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                            return Response(kk['message'],status = kk['code'])
                return Response({
                    "status":"Success",
                    "message":"Retrieved successfully",
                    "data":OnlineCheckoutResponseSerializer(obj,many =True).data
                })
            else:
                dddata = {
                            "role": PAYMENT_GET_TRANSACTIONAL_STATUS,
                            "successfull": False,
                            "message": f"The data with {checkout_id} not found",
                            "endpoint": "api/v1/check/transaction/status/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                            return Response(kk['message'],status = kk['code'])
                return Response({
                    "status":"Failed",
                    "message":"Data with checkout id not found!"
                },status =  400)
        else:
            dddata = {
                            "role": PAYMENT_GET_TRANSACTIONAL_STATUS,
                            "successfull": False,
                            "message": "You have no rights for this request",
                            "endpoint": "api/v1/check/transaction/status/"
                        }
            kk = make_api_request_log_request(request,dddata)
            if kk['code'] > 204:
                            return Response(kk['message'],status = kk['code'])
            return Response({
                "status": "Failed",
                "message": "You have no rights for this request"
            }, status=400)

            


class SendSTKPUSHBusinessProcess(APIView):
    def post(self, request):
        app = MicrosoftValidation(request).verify()

        if app.status_code != 200:
            # logger.info("the jjs" , app.text)
            return app

        # logger.info("the jjs2" , app.text)
        if PAYMENTS_STK_PUSH_BUSINESS in app.json()['data']['roles']:
            user_key = request.data.get("user_key",None)
            phoneNumber = request.data.get("phone", None)
            accountReference = request.data.get("account_reference", None)
            amount = request.data.get("amount", None)
            description = request.data.get("transaction_desc", None)
            is_paybill = request.data.get("is_paybil", None)
            paybill = request.data.get("paybill", None)
            call_back_url = request.data.get("call_back_url", None)

            def is_numeric(value):
                return isinstance(value, (int, float, complex))

            missing_fields = {}
            
            if user_key is None:
                dddata = {
                            "role": PAYMENTS_STK_PUSH_BUSINESS,
                            "successfull": False,
                            "message": f"User key is missing in body",
                            "endpoint": "api/v1/stk/business/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                        return Response(kk['message'],status = kk['code'])
                missing_fields['user_key'] = "User key is missing"

            if phoneNumber is None:
                dddata = {
                            "role": PAYMENTS_STK_PUSH_BUSINESS,
                            "successfull": False,
                            "message": f"Phone number is missing in body",
                            "endpoint": "api/v1/stk/business/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                        return Response(kk['message'],status = kk['code'])
                missing_fields['phone'] = "Phone number is missing"
            if accountReference is None:
                dddata = {
                            "role": PAYMENTS_STK_PUSH_BUSINESS,
                            "successfull": False,
                            "message": f"Account reference is missing in body",
                            "endpoint": "api/v1/stk/business/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                        return Response(kk['message'],status = kk['code'])
                missing_fields['account_reference'] = "Account reference is missing"
            if amount is None:
                dddata = {
                            "role": PAYMENTS_STK_PUSH_BUSINESS,
                            "successfull": False,
                            "message": f"Amount is missing in body",
                            "endpoint": "api/v1/stk/business/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                        return Response(kk['message'],status = kk['code'])
                missing_fields['amount'] = "Amount is missing"
            if description is None:
                dddata = {
                            "role": PAYMENTS_STK_PUSH_BUSINESS,
                            "successfull": False,
                            "message": f"Transaction description is missing",
                            "endpoint": "api/v1/stk/business/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                        return Response(kk['message'],status = kk['code'])
                missing_fields['transaction_desc'] = "Transaction description is missing"
            if is_paybill is None:
                dddata = {
                            "role": PAYMENTS_STK_PUSH_BUSINESS,
                            "successfull": False,
                            "message": f"Is_paybill flag  is missing",
                            "endpoint": "api/v1/stk/business/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                        return Response(kk['message'],status = kk['code'])
                missing_fields['is_paybil'] = "Is_paybill flag is missing"
            if paybill is None:
                dddata = {
                            "role": PAYMENTS_STK_PUSH_BUSINESS,
                            "successfull": False,
                            "message": f"Paybill number  is missing",
                            "endpoint": "api/v1/stk/business/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                        return Response(kk['message'],status = kk['code'])
                missing_fields['paybill'] = "Paybill number is missing"
            if call_back_url is None:
                dddata = {
                            "role": PAYMENTS_STK_PUSH_BUSINESS,
                            "successfull": False,
                            "message": f"Callback URL is missing",
                            "endpoint": "api/v1/stk/business/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                        return Response(kk['message'],status = kk['code'])
                missing_fields['call_back_url'] = "Callback URL is missing"

            if missing_fields:
                return Response({
                    "status": "Failed",
                    "message": "Missing required fields",
                    "details": missing_fields
                }, status=status.HTTP_400_BAD_REQUEST)


            if not is_numeric(amount):
                dddata = {
                            "role": PAYMENTS_STK_PUSH_BUSINESS,
                            "successfull": False,
                            "message": f"Incorrect amount format",
                            "endpoint": "api/v1/stk/business/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                        return Response(kk['message'],status = kk['code'])
                return Response({
                    "status": "Failed",
                    "message": "Incorrect amount format"
                })

            if not is_numeric(paybill):
                dddata = {
                            "role": PAYMENTS_STK_PUSH_BUSINESS,
                            "successfull": False,
                            "message": f"Incorrect paybill format",
                            "endpoint": "api/v1/stk/business/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                        return Response(kk['message'],status = kk['code'])
                return Response({
                    "status": "Failed",
                    "message": "Incorrect paybill format"
                })

            print("the start iss")
            dt = request.data

            logger.info("there is a test coming")

            check_bis =  UserRequestsModel.objects.filter(
                key =  user_key  
            )

            if len(check_bis) > 0:
                ap =  MpesaRequest.objects.create(
                        user_key = check_bis[0],
                        phoneNumber = phoneNumber,
                        accountReference = accountReference,
                        amount  = amount,
                        description = description,
                        MerchantRequestID = "MerchantRequestID",
                        CheckoutRequestID = "CheckoutRequestID",
                        ResponseCode = "1",
                        ResponseDescription = "ResponseDescription",
                        CustomerMessage = "CustomerMessage",
                        callback_url = call_back_url
                    ) 
                dddata = {
                            "role": PAYMENTS_STK_PUSH_BUSINESS,
                            "successfull": False,
                            "message": f"Mpesa payment request for {request.data} created successfully",
                            "endpoint": "api/v1/stk/business/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                        return Response(kk['message'],status = kk['code'])  



                # check_business

                if check_bis[0].business.key == "IGAS":
                    # validate payment 
                    db_commissions = OracleDB()  # Adjust as necessary for your OracleDB class setup


                    # try:
                    db_commissions.connect()
                    logger.info("Connected to the database successfully.")

                    headers_query = f"""
                            SELECT POLICY_NO, POL_STAT, NX_EXP_PR_DT, PREM_STOP_DATE, PLANNO, PLAN_DESCN, NI_NUMBER, FIRST_NAME, SURNAME
                            FROM VALIDATION.IGAS_MPESA_VALIDATIONS WHERE POLICY_NO  = '{accountReference}'"""
                    
                    headers = db_commissions.execute_query(headers_query)
                    if headers:
                        headers_data = json.loads(headers)

                        if len(headers_data) > 0:
                            dddata = {
                            "role": PAYMENTS_STK_PUSH_BUSINESS,
                            "successfull": True,
                            "message": f"Fetched {headers_data} headers to process.",
                            "endpoint": "api/v1/stk/business/"
                                    }
                            kk = make_api_request_log_request(request,dddata)
                            if kk['code'] > 204:
                                    return Response(kk['message'],status = kk['code'])  

                            check_policy_status =  headers_data[0]['POL_STAT']

                            if "A" in [check_policy_status]:
                                
                                app  =  process_online_checkout(
                                  phoneNumber,amount,paybill,accountReference,description,PAYMENTS_STK_PUSH_BUSINESS,request,"api/v1/stk/business/",is_paybill,ap
                                )

                                dddata = {
                                "role": PAYMENTS_STK_PUSH_BUSINESS,
                                "successfull": True,
                                "message": f"Processed request successfully, The response {app['message']}",
                                "endpoint": "api/v1/stk/business/"
                                        }
                                kk = make_api_request_log_request(request,dddata)
                                if kk['code'] > 204:
                                        return Response(kk['message'],status = kk['code'])
                                return Response(app['message'], status=app['code'])
                            else:
                                return Response({
                                      "status":"Failed",
                                      "message":"Policy can not accept payment",
                                      "data":headers_data
                                },status=400)  
                            
                        else:
                            dddata = {
                            "role": PAYMENTS_STK_PUSH_BUSINESS,
                            "successfull": False,
                            "message": f"User with account ref {accountReference} does not exist",
                            "endpoint": "api/v1/stk/business/"
                                    }
                            kk = make_api_request_log_request(request,dddata)
                            if kk['code'] > 204:
                                    return Response(kk['message'],status = kk['code'])  

                            logger.info(f"Fetched {headers_data} headers to process.")
                        
                            return Response({
                                  "status":"False",
                                  "message":f"User with account ref {accountReference} does not exist"
                            },status=400)

                    
            
                else:
                    dddata = {
                            "role": PAYMENTS_STK_PUSH_BUSINESS,
                            "successfull": False,
                            "message": f"Business with key {check_bis[0].business.key} not configured yet",
                            "endpoint": "api/v1/stk/business/"
                        }
                    kk = make_api_request_log_request(request,dddata)
                    if kk['code'] > 204:
                            return Response(kk['message'],status = kk['code'])  

                    return Response({
                          "status":"Failed",
                          "message":f"Business with key {check_bis[0].business.key} not configured yet"
                    },status=400)
                
            else:
                dddata = {
                            "role": PAYMENTS_STK_PUSH_BUSINESS,
                            "successfull": False,
                            "message": f"No user key Found",
                            "endpoint": "api/v1/stk/business/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                        return Response(kk['message'],status = kk['code'])  

                return Response({
                      "status":"Failed",
                      "message":f"No user key Found"
                }) 
                  

            # app = call_online_checkout_task(
            #     phone=phoneNumber,
            #     amount=f'{amount}',
            #     paybill=paybill,
            #     account_reference=accountReference,
            #     transaction_desc=description,
            #     call_back_url=call_back_url,
            #     is_paybil=is_paybill,
            #     role=PAYMENTS_STK_PUSH,
            #     request=request,
            #     endpoint="api/v1/stk/"

            # )

            # return Response(app['message'], status=app['code'])
        else:
            dddata = {
                            "role": PAYMENTS_STK_PUSH,
                            "successfull": False,
                            "message": f"User doesnt have rights",
                            "endpoint": "api/v1/stk/"
                        }
            kk = make_api_request_log_request(request,dddata)
            return Response({
                "status": "Failed",
                "message": "You have no rights for this request"
            }, status=400)




class SendSTKPUSH(APIView):
    def get(self,request):
        app = MicrosoftValidation(request).verify()

        if app.status_code != 200:
            # logger.info("the jjs" , app.text)
            return app

        # logger.info("the jjs2" , app.text)
        if PAYMENT_VERIFY_CHECKOUT_ID in app.json()['data']['roles']:
            checkout_id  = request.query_params.get("checkout_id",None)
            phone_number =  request.query_params.get("phone_number",None)

            if None in [checkout_id,phone_number]:
                dddata = {
                            "role": PAYMENT_VERIFY_CHECKOUT_ID,
                            "successfull": False,
                            "message": f"User doesnt have rights",
                            "endpoint": "api/v1/stk/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                            return Response(kk['message'],status = kk['code'])
                return Response({
                      "status":"Failed",
                      "message":"Fill the phone number and checkout id"
                },status=400)
          
            else:
                ap =  MpesaRequest.objects.filter(
                        phoneNumber = phone_number,
                        CheckoutRequestID = checkout_id,
                    
                    )
                dddata = {
                            "role": PAYMENT_VERIFY_CHECKOUT_ID,
                            "successfull": True,
                            "message": f"Successfully retrieved a record",
                            "endpoint": "api/v1/stk/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                            return Response(kk['message'],status = kk['code'])
                return Response({
                      "status":"Success",
                      "message":"Retrived Successfully!!",
                      "data":MpesaSerializers(
                            ap,many = True
                      ).data
                })
                
        
        else:
            dddata = {
                            "role": PAYMENT_VERIFY_CHECKOUT_ID,
                            "successfull": False,
                            "message": f"User doesnt have rights",
                            "endpoint": "api/v1/stk/"
                        }
            kk = make_api_request_log_request(request,dddata)
            if kk['code'] > 204:
                        return Response(kk['message'],status = kk['code'])
            return Response({
                "status": "Failed",
                "message": "You have no rights for this request"
            }, status=400)
              
    def post(self, request):
        app = MicrosoftValidation(request).verify()

        if app.status_code != 200:
            # logger.info("the jjs" , app.text)
            return app

        # logger.info("the jjs2" , app.text)
        if PAYMENTS_STK_PUSH in app.json()['data']['roles']:
            phoneNumber = request.data.get("phone", None)
            accountReference = request.data.get("account_reference", None)
            amount = request.data.get("amount", None)
            description = request.data.get("transaction_desc", None)
            is_paybill = request.data.get("is_paybil", None)
            paybill = request.data.get("paybill", None)
            call_back_url = request.data.get("call_back_url", None)

            def is_numeric(value):
                return isinstance(value, (int, float, complex))

            missing_fields = {}
            
            if phoneNumber is None:
                dddata = {
                            "role": PAYMENT_ADD_PAYBILL,
                            "successfull": False,
                            "message": f"Phone number is missing in body",
                            "endpoint": "api/v1/add/paybill/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                        return Response(kk['message'],status = kk['code'])
                missing_fields['phone'] = "Phone number is missing"
            if accountReference is None:
                dddata = {
                            "role": PAYMENT_ADD_PAYBILL,
                            "successfull": False,
                            "message": f"Account reference is missing in body",
                            "endpoint": "api/v1/add/paybill/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                        return Response(kk['message'],status = kk['code'])
                missing_fields['account_reference'] = "Account reference is missing"
            if amount is None:
                dddata = {
                            "role": PAYMENT_ADD_PAYBILL,
                            "successfull": False,
                            "message": f"Amount is missing in body",
                            "endpoint": "api/v1/add/paybill/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                        return Response(kk['message'],status = kk['code'])
                missing_fields['amount'] = "Amount is missing"
            if description is None:
                dddata = {
                            "role": PAYMENT_ADD_PAYBILL,
                            "successfull": False,
                            "message": f"Transaction description is missing",
                            "endpoint": "api/v1/add/paybill/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                        return Response(kk['message'],status = kk['code'])
                missing_fields['transaction_desc'] = "Transaction description is missing"
            if is_paybill is None:
                dddata = {
                            "role": PAYMENT_ADD_PAYBILL,
                            "successfull": False,
                            "message": f"Is_paybill flag  is missing",
                            "endpoint": "api/v1/add/paybill/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                        return Response(kk['message'],status = kk['code'])
                missing_fields['is_paybil'] = "Is_paybill flag is missing"
            if paybill is None:
                dddata = {
                            "role": PAYMENT_ADD_PAYBILL,
                            "successfull": False,
                            "message": f"Paybill number  is missing",
                            "endpoint": "api/v1/add/paybill/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                        return Response(kk['message'],status = kk['code'])
                missing_fields['paybill'] = "Paybill number is missing"
            if call_back_url is None:
                dddata = {
                            "role": PAYMENT_ADD_PAYBILL,
                            "successfull": False,
                            "message": f"Callback URL is missing",
                            "endpoint": "api/v1/add/paybill/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                        return Response(kk['message'],status = kk['code'])
                missing_fields['call_back_url'] = "Callback URL is missing"

            if missing_fields:
                return Response({
                    "status": "Failed",
                    "message": "Missing required fields",
                    "details": missing_fields
                }, status=status.HTTP_400_BAD_REQUEST)

            if not is_numeric(amount):
                dddata = {
                            "role": PAYMENT_ADD_PAYBILL,
                            "successfull": False,
                            "message": f"Incorrect amount format",
                            "endpoint": "api/v1/add/paybill/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                        return Response(kk['message'],status = kk['code'])
                return Response({
                    "status": "Failed",
                    "message": "Incorrect amount format"
                })

            if not is_numeric(paybill):
                dddata = {
                            "role": PAYMENT_ADD_PAYBILL,
                            "successfull": False,
                            "message": f"Incorrect paybill format",
                            "endpoint": "api/v1/add/paybill/"
                        }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                        return Response(kk['message'],status = kk['code'])
                return Response({
                    "status": "Failed",
                    "message": "Incorrect paybill format"
                })

            print("the start iss")
            dt = request.data

            logger.info("there is a test coming")

            app = call_online_checkout_task(
                phone=phoneNumber,
                amount=f'{amount}',
                paybill=paybill,
                account_reference=accountReference,
                transaction_desc=description,
                call_back_url=call_back_url,
                is_paybil=is_paybill,
                role=PAYMENTS_STK_PUSH,
                request=request,
                endpoint="api/v1/stk/"

            )

            return Response(app['message'], status=app['code'])
        else:
            dddata = {
                            "role": PAYMENTS_STK_PUSH,
                            "successfull": False,
                            "message": f"User doesnt have rights",
                            "endpoint": "api/v1/stk/"
                        }
            kk = make_api_request_log_request(request,dddata)
            return Response({
                "status": "Failed",
                "message": "You have no rights for this request"
            }, status=400)



# class SendSTKPUSH(APIView):
#     def post(self,request):
#         app =  MicrosoftValidation(request).verify()
            
#         if app.status_code == 401:
#                 return app

#         if PAYMENTS_STK_PUSH in app.json()['data']['roles']:
#             phoneNumber =  request.data.get("phone",None)
#             accountReference =  request.data.get("account_reference",None)
#             amount =  request.data.get("amount",None)
#             description =   request.data.get("transaction_desc",None)
#             is_paybill = request.data.get("is_paybil",None)
#             paybill =  request.data.get("paybill",None)
#             call_back_url =  request.data.get("call_back_url",None)
            
#             def is_numeric(value):
#                 return isinstance(value, (int, float, complex))
            
            
            
            
        
#             if None in [phoneNumber,accountReference,amount,description,is_paybill,paybill,call_back_url]:
                
#                 return Response({
#                     "status":"Failed",
#                     "message":"Fill all details"
#                 },status=status.HTTP_400_BAD_REQUEST)
                
                
            
#             if not is_numeric(amount):
                
#                 return Response({
#                     "status":"Failed",
#                     "message":"Incorrect amount format"
#                 })
            
            
#             if not is_numeric(paybill):
#                 return Response({
#                     "status":"Failed",
#                     "message":"Incorrect paybill format"
#                 })
            
            
#             print("the start iss")
#             dt =  request.data
            
        
    
#             logger.info("there is a test coming")
            
#             app =   call_online_checkout_task(
                
#                     phone=phoneNumber,
#                     amount=f'{amount}' ,
#                     paybill=paybill,
#                     account_reference=accountReference,
#                     transaction_desc=description,
#                     call_back_url=call_back_url,
#                     is_paybil=is_paybill
            
            
#             )
        
        
     
#             return Response(app['message'],status=app['code'])
#         else:
#             return Response({
#                 "status":"Failed",
#                 "message":"U have no rights for this request"
#             },status =  400)
      
        
        
      
            
        
      
        

        
      



class FilterTransaction(APIView):
    def get(self,request):
        app =  MicrosoftValidation(request).verify()
            
        if app.status_code == 401:
                return app

        if PAYMENTS_STK_PUSH in app.json()['data']['roles']:
            phone =  request.query_params.get("Phone",None)
            
            if None in [phone]:
                dddata = {
                                "role": PAYMENT_GET_TRANSACTIONAL_STATUS,
                                "successfull": False,
                                "message": f"Fill {phone} parameters",
                                "endpoint": "api/v1/filter/"
                            }
                kk = make_api_request_log_request(request,dddata)
                if kk['code'] > 204:
                                return Response(kk['message'],status = kk['code'])
                return Response({
                    "status":"Failed",
                    "message":"Fill all details"
                },status=status.HTTP_200_OK)

            filek = MpesaRequest.objects.filter(
                    phoneNumber = phone
                )
                
            mpsac =  MpesaCallbackMetaData.objects.filter(rdb = filek[0])
            dddata = {
                                "role": PAYMENT_GET_TRANSACTIONAL_STATUS,
                                "successfull": True,
                                "message": f"Data was found and sent",
                                "endpoint": "api/v1/filter/"
                            }
            kk = make_api_request_log_request(request,dddata)
            if kk['code'] > 204:
                                return Response(kk['message'],status = kk['code'])
            return Response({
                "status":"Success",
                "message":"Data found",
                "data":{
                    "transaction":MpesaSerializers(filek[0]).data,
                    "items":MpesaCallbackMetaDataSerializers(mpsac,many =   True).data
                }
            },status=status.HTTP_200_OK)

        else:
            dddata = {
                                "role": PAYMENT_GET_FILTER_MPESA,
                                "successfull": False,
                                "message": "You have no rights for this request",
                                "endpoint": "api/v1/filter/"
                            }
            kk = make_api_request_log_request(request,dddata)
            if kk['code'] > 204:
                                return Response(kk['message'],status = kk['code'])
            return Response({
                "status":"Failed",
                "message":"You have no rights for this request"
            },status =  400)    



class MpesaCallbackApiView(APIView):
    @csrf_exempt
    def post(self, request):
        # Your POST logic here
        data = request.data  # This contains the POST data sent to the view
        print("the data is ", data)
        ss =  data['Body']['stkCallback']
        print("the res",ss)
        merchant = ss['MerchantRequestID']
        checkout =  ss['CheckoutRequestID']
        
        result_code = ss['ResultCode']
        
        check = MpesaRequest.objects.filter(
            MerchantRequestID = merchant,
            CheckoutRequestID = checkout
        )
        
        if int(result_code) > 0:
            
            check[0].paid = "CANCELLED"
            check[0].save()
            
            return Response({
                "status":"Failed",
                "message":"Transaction failed"
            })
            
        
            
            
            
            
        items =  ss['CallbackMetadata']['Item']
        description =  ss['ResultDesc']
        # ss =  data['Body']['stkCallback']['CallbackMetadata']['Item']
        # merchantId = data['Body']['stkCallback']['MerchantRequestID']
        # checkout =  data['Body']['stkCallback']['CheckoutRequestID']
        # description =  data['Body']['stkCallback']['ResultDesc']
        
        
        
        if len(check) > 0:
            print("found ",check)
            check[0].paid = "PAID"
            check[0].save()
            for i in items:
                try:
                    obj =  MpesaCallbackMetaData.objects.create(
                        rdb = check[0],
                        name = i['Name'],
                        value = i['Value'],
                        description = description
                        
                    )
                except:
                    pass
                
                
        # Your processing logic here

        return Response({'message': 
            'Post request received successfully'},
                        status=status.HTTP_200_OK)
        
        
        

class B2cTimeOut(APIView):
    """
    Handle b2c time out
    """

    @csrf_exempt
    def post(self, request, format=None):
        """
        process the timeout
        :param request:
        :param format:
        :return:
        """
        data = request.data
        return Response(dict(value="ok", key="status", detail="success"))



class B2cResult(APIView):
    """
    Handle b2c result
    """

    @csrf_exempt
    def post(self, request, format=None):
        """
        process the timeout
        :param request:
        :param format:
        :return:
        """
        data = request.data
        process_b2c_result_response_task.apply_async(
            args=(data,), queue="b2c_result"
        )
        return Response(dict(value="ok", key="status", detail="success"))
    
            
        
        
            
        
        
            
            
            
        


