from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny

from .important.ImportantClasses import (
    LipaNaMpesa,
    format_phone_number
)


from .models import (
    MpesaRequest,
    MpesaCallbackMetaData,
    C2BPayments,
    AuthToken,
    OnlineCheckout
)

from django.views.decorators.csrf import csrf_exempt


from .serializers import (
   MpesaSerializers,
    MpesaCallbackMetaDataSerializers,
    C2BPaymentsSerializer
)
from rest_framework.generics import CreateAPIView
from datetime import datetime
import pytz

from .tasks import (
    process_b2c_result_response_task,
    process_c2b_confirmation_task,
    process_c2b_validation_task,
    handle_online_checkout_callback_task,
    call_online_checkout_task
)

from config.util.c2butils import (
    process_online_checkout
)

from .mpesa import (
    Mpesa
)

import logging

logger = logging.getLogger(__name__)



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
        handle_online_checkout_callback_task.apply_async(
            args=(data,), queue="online_checkout_callback"
        )
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
    queryset = C2BPayments.objects.all()
    serializer_class = C2BPaymentsSerializer
    permission_classes = [AllowAny]

    def create(self, request):
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

        c2bmodel_data = C2BPayments.objects.create(
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
        c2b_data = C2BPayments.objects.all()
        data = C2BPaymentsSerializer(c2b_data, many=True)
        c2b_context = {
            "Result Code": 0,
            "Data": data
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
    queryset = C2BPayments.objects.all()
    serializer_class = C2BPaymentsSerializer
    permission_classes = [AllowAny]

    def create(self, request):
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

        c2bmodel_data = C2BPayments.objects.create(
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
        c2b_data = C2BPayments.objects.all()
        data = C2BPaymentsSerializer(c2b_data, many=True)
        c2b_context = {
            "Result Code": 0,
            "Data": data
        }

        return Response(c2b_context)





class SendSTKPUSH(APIView):
    def post(self,request):
        phoneNumber =  request.data.get("phone",None)
        accountReference =  request.data.get("account_reference",None)
        amount =  request.data.get("amount",None)
        description =   request.data.get("transaction_desc",None)
        is_paybill = request.data.get("is_paybil",None)
        paybill =  request.data.get("paybill",None)
        call_back_url =  request.data.get("call_back_url",None)
        
        def is_numeric(value):
            return isinstance(value, (int, float, complex))
        
        
        if None in [phoneNumber,accountReference,amount,description,is_paybill,paybill,call_back_url]:
            
            return Response({
                "status":"Failed",
                "message":"Fill all details"
            },status=status.HTTP_400_BAD_REQUEST)
            
            
            
        if not is_numeric(amount):
            
            return Response({
                "status":"Failed",
                "message":"Incorrect amount format"
            })
            
            
        if not is_numeric(paybill):
            return Response({
                "status":"Failed",
                "message":"Incorrect paybill format"
            })
            
            
        print("the start iss")
        dt =  request.data
        
     
    
        logger.info("there is a test coming")
        
        call_online_checkout_task.apply_async(
               kwargs={
                'phone':phoneNumber,
                'amount':f'{amount}' ,
                'paybill':paybill,
                'account_reference': accountReference,
                'transaction_desc' : description,
                'call_back_url':call_back_url,
                'is_paybil' : is_paybill}
           ,
            queue="online_checkout_request",
        )
        
        # app =  Mpesa().stk_push(
        #         phone=phoneNumber,
                
                
        #     )
        
        return Response({
                "status":"Success",
                "message":"Mpesa is initiated check your phone for payment",
                
            },status=status.HTTP_201_CREATED)
        
        # app = process_online_checkout(
        #     phoneNumber,
        #     f'{amount}',
        #     accountReference,
        #     description
            
        # )
        
        
        
        
        # if app['ResponseCode'] == "0":
            
        #     print("the data is ", app)
        #     app =  Mpesa().stk_push(
        #         phone=phoneNumber,
        #         amount=amount,
        #         account_reference=accountReference,
        #         merchant_request_id=app['MerchantRequestID'],
        #         response_code=app['ResponseCode'],
        #         checkout_request_id=app['CheckoutRequestID'],
        #         is_paybill=is_paybill
                
        #     )
            
        
      
        

        
        return Response({
            "status":"Failed",
            "message":"Error occured while creating mpesa"
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # app =  LipaNaMpesa(phoneNumber,accountReference,f"{amount}",description)
        # app1 =  app.lipa_na_mpesa()
        
        # print("the ss", app1)
        
        
        # if app1['ResponseCode'] == "0":
        #     obj =  MpesaRequest.objects.create(
        #         phoneNumber =  phoneNumber,
        #         accountReference = accountReference,
        #         amount =  amount,
        #         description =  description,
        #         MerchantRequestID =  app1['MerchantRequestID'],
        #         CheckoutRequestID =  app1['CheckoutRequestID'],
        #         ResponseCode =  app1['ResponseCode'],
        #         ResponseDescription =  app1['ResponseDescription'],
        #         CustomerMessage =  app1['CustomerMessage']
        #     )
        
        #     print("the app1 ", app1)
            
        #     return Response({
        #         "status":"Success",
        #         "message":"The payment is initiated"
        #     },status=status.HTTP_201_CREATED)
            
        # return Response({
        #     "status":"Failed",
        #     "message":"Failed to initiate mpesa"
        # },status=status.HTTP_400_BAD_REQUEST)
        
        


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
    
            
        
        
            
        
        
            
            
            
        


