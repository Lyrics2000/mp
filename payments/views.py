from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from .Middleware import MicrosoftValidation
from config.settings.settings import (
    PAYMENTS_STK_PUSH,
    PAYMENT_QUERY_STK_PUSH,
    PAYMENT_GET_TRANSACTIONAL_STATUS
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
    OnlineCheckout
)

from django.views.decorators.csrf import csrf_exempt


from .serializers import (
   MpesaSerializers,
    MpesaCallbackMetaDataSerializers,
    C2BPaymentsValidationSerializer,
    C2BPaymentsConfirmationSerializer
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
    query_stk
)

from .mpesa import (
    Mpesa
)

import logging

logger = logging.getLogger(__name__)

from .models import (
    PayBillNumbers
)

from .serializers import (
    PayBillNumbersSerializers
)


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
            
            app =  query_stk(check_out_id,paybill)

            return Response(app['message'],status=app['code'])


        else:
            return Response({
                "status":"Failed",
                "message":"U have no rights for this request"
            },status =  400)


class AddPaybill(APIView):
    def post(self,request):
        # app =  MicrosoftValidation(request).verify()
            
        # if app.status_code == 401:
        #         return app

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

                return Response({
                    "status":"Success",
                    "message":"updated successfully",
                    "data": PayBillNumbersSerializers(f[0]).data
                },status=200)
            
            else:
                return Response({
                    "status":"Failed",
                    "message":"Paybill not found"
                },status =  200)





        
        return Response({
            "status":"Failed",
            "message":"An error occured"
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
                return Response({
                    "status":"Success",
                    "message":"Retrieved successfully",
                    "data":OnlineCheckoutResponseSerializer(obj,many =True).data
                })
            else:
                return Response({
                    "status":"Failed",
                    "message":"Data with checkout id not found!"
                },status =  400)
        else:
            return Response({
                "status": "Failed",
                "message": "You have no rights for this request"
            }, status=400)

            

        


class SendSTKPUSH(APIView):
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
                missing_fields['phone'] = "Phone number is missing"
            if accountReference is None:
                missing_fields['account_reference'] = "Account reference is missing"
            if amount is None:
                missing_fields['amount'] = "Amount is missing"
            if description is None:
                missing_fields['transaction_desc'] = "Transaction description is missing"
            if is_paybill is None:
                missing_fields['is_paybil'] = "Is_paybill flag is missing"
            if paybill is None:
                missing_fields['paybill'] = "Paybill number is missing"
            if call_back_url is None:
                missing_fields['call_back_url'] = "Callback URL is missing"

            if missing_fields:
                return Response({
                    "status": "Failed",
                    "message": "Missing required fields",
                    "details": missing_fields
                }, status=status.HTTP_400_BAD_REQUEST)

            if not is_numeric(amount):
                return Response({
                    "status": "Failed",
                    "message": "Incorrect amount format"
                })

            if not is_numeric(paybill):
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
                is_paybil=is_paybill
            )

            return Response(app['message'], status=app['code'])
        else:
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

        phone =  request.query_params.get("Phone",None)
        
        if None in [phone]:
            return Response({
                "status":"Failed",
                "message":"Fill all details"
            },status=status.HTTP_200_OK)
            
            
        
        
   
            
            
        filek = MpesaRequest.objects.filter(
            phoneNumber = phone
        )
        
        mpsac =  MpesaCallbackMetaData.objects.filter(rdb = filek[0])
        
        return Response({
            "status":"Success",
            "message":"Data found",
            "data":{
                "transaction":MpesaSerializers(filek[0]).data,
                "items":MpesaCallbackMetaDataSerializers(mpsac,many =   True).data
            }
        },status=status.HTTP_200_OK)
            



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
    
            
        
        
            
        
        
            
            
            
        


