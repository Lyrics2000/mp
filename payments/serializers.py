from rest_framework import serializers

from .models import (
    MpesaRequest,
    MpesaCallbackMetaData,
    C2BPaymentsConfirmation,
    PayBillNumbers,
    OnlineCheckoutResponse,
    C2BPaymentsValidation
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
        
        

class C2BPaymentsConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = C2BPaymentsConfirmation
        fields = '__all__'

class C2BPaymentsValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = C2BPaymentsValidation
        fields = '__all__'