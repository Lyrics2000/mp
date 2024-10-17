from rest_framework import serializers

from .models import (
    MpesaRequest,
    MpesaCallbackMetaData,
    C2BPayments,
    PayBillNumbers,
    OnlineCheckoutResponse
)


class OnlineCheckoutResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model =  OnlineCheckoutResponse
        fields = '__all__'

class PayBillNumbersSerializers(serializers.ModelSerializer):
    class Meta:
        model =  PayBillNumbers
        fields = '__all__'

class MpesaSerializers(serializers.ModelSerializer):
    class Meta:
        model =  MpesaRequest
        fields = ('phoneNumber','accountReference','amount','description','callback_url','paid')
        
class MpesaCallbackMetaDataSerializers(serializers.ModelSerializer):
    class Meta:
        model = MpesaCallbackMetaData
        fields = '__all__'
        
        

class C2BPaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = C2BPayments
        fields = (
            'id',
            'TransactionType',
            'TransID',
            'TransTime',
            'TransAmount',
            'BusinessShortCode',
            'BillRefNumber',
            'InvoiceNumber',
            'OrgAccountBalance',
            'ThirdPartyTransID',
            'MSISDN',
            'FirstName',
            'MiddleName',
            'LastName',
            )
        