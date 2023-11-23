from django.db import models

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Your other models can now inherit from TimestampedModel


class C2BPayments(models.Model):
    TransactionType = models.CharField(max_length=50, blank=True, null=True)
    TransID = models.CharField(max_length=30, blank=True, null=True)
    TransTime = models.CharField(max_length=50, blank=True, null=True)
    TransAmount = models.CharField(max_length=120, blank=True, null=True)
    BusinessShortCode = models.CharField(max_length=50, blank=True, null=True)
    BillRefNumber = models.CharField(max_length=120, blank=True, null=True)
    InvoiceNumber = models.CharField(max_length=120, blank=True, null=True)
    OrgAccountBalance = models.CharField(max_length=120, blank=True, null=True)
    ThirdPartyTransID = models.CharField(max_length=120, blank=True, null=True)
    MSISDN = models.CharField(max_length=25, blank=True, null=True)
    FirstName = models.CharField(max_length=50, blank=True, null=True)
    MiddleName = models.CharField(max_length=50, blank=True, null=True)
    LastName = models.CharField(max_length=50, blank=True, null=True)

    def __repr__(self):
        return f'{self.InvoiceNumber}'


class MpesaRequest(TimestampedModel):
    STATUS_CHOICES = (
        ('PENDING', 'PENDING'),
        ('PAID', 'PAID'),
        ('CANCELLED', 'CANCELLED'),
    )
    phoneNumber =  models.CharField(max_length =  255)
    accountReference =  models.TextField()
    amount =  models.DecimalField(max_digits = 20, decimal_places = 2)
    description =  models.TextField()
    MerchantRequestID =  models.TextField()
    CheckoutRequestID =  models.TextField()
    ResponseCode =  models.TextField()
    ResponseDescription =  models.TextField()
    CustomerMessage =  models.TextField()
    callback_url =  models.URLField(blank =  True,null = True)
    paid =  models.CharField(max_length =  255, choices = STATUS_CHOICES , default = "PENDING" )
    
    
    def __str__(self) -> str:
        return self.phoneNumber
    
    
class MpesaCallbackMetaData(TimestampedModel):
    rdb =  models.ForeignKey(MpesaRequest,on_delete =  models.CASCADE)
    name =  models.CharField(max_length =  255)
    value =  models.CharField(max_length = 255)
    description =  models.TextField(blank  =  True,null =True)
    
    
    
    def __str__(self) -> str:
        return self.name
    