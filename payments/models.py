from django.db import models



from config.util.managers import AuthTokenManager



class PayBillNumbers(models.Model):
    """stores paybll to use and client secrets"""
    paybill =  models.PositiveBigIntegerField(default = 0)
    client_ref =  models.TextField()
    client_secret =  models.TextField()
    password =  models.TextField(blank=True,null=True)
    developmet =   models.BooleanField(default = True)
    date_added = models.DateTimeField(auto_now_add=True)

    
    def __str__(self) -> str:
        return str(self.paybill)


class AuthToken(models.Model):
    """Handles AuthTokens"""

    access_token = models.CharField(max_length=40)
    type = models.CharField(max_length=3)
    expires_in = models.BigIntegerField()
    objects = AuthTokenManager()

    def __str__(self):
        return self.access_token

    class Meta:
        db_table = "tbl_access_token"


class B2CRequest(models.Model):
    """
    Handles B2C requests
    """

    id = models.BigAutoField(primary_key=True)
    phone = models.BigIntegerField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    conversation_id = models.CharField(max_length=40, blank=True, null=True)
    originator_conversation_id = models.CharField(
        max_length=40, blank=True, null=True
    )
    response_code = models.CharField(max_length=5, blank=True, null=True)
    response_description = models.TextField(blank=True, null=True)
    request_id = models.CharField(max_length=20, blank=True, null=True)
    error_code = models.CharField(max_length=20, blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.phone)

    class Meta:
        db_table = "tbl_b2c_requests"
        verbose_name_plural = "B2C Requests"


class B2CResponse(models.Model):
    """
    Handles B2C Response
    """

    id = models.BigAutoField(primary_key=True)
    phone = models.BigIntegerField(blank=True, null=True)
    amount = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    conversation_id = models.CharField(max_length=40, blank=True, null=True)
    originator_conversation_id = models.CharField(
        max_length=40, blank=True, null=True
    )
    result_type = models.CharField(max_length=5, blank=True, null=True)
    result_code = models.CharField(max_length=5, blank=True, null=True)
    result_description = models.TextField(blank=True, null=True)
    transaction_id = models.CharField(max_length=20, blank=True, null=True)
    transaction_receipt = models.CharField(
        max_length=20, blank=True, null=True
    )
    transaction_amount = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    working_funds = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    utility_funds = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    paid_account_funds = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    transaction_date = models.DateTimeField(blank=True, null=True)
    mpesa_user_name = models.CharField(max_length=100, blank=True, null=True)
    is_registered_customer = models.CharField(
        max_length=1, blank=True, null=True
    )

    def __str__(self):
        return str(self.phone)

    class Meta:
        db_table = "tbl_b2c_response"
        verbose_name_plural = "B2C Responses"


class C2BRequest(models.Model):
    """
    Handles C2B Requests
    """

    id = models.BigAutoField(primary_key=True)
    transaction_type = models.CharField(max_length=20, blank=True, null=True)
    transaction_id = models.CharField(max_length=20, unique=True)
    transaction_date = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    business_short_code = models.CharField(
        max_length=20, blank=True, null=True
    )
    bill_ref_number = models.CharField(max_length=50, blank=True, null=True)
    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    org_account_balance = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True, default=0.0
    )
    third_party_trans_id = models.CharField(
        max_length=50, blank=True, null=True
    )
    phone = models.BigIntegerField(blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    is_validated = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {} {}".format(
            self.first_name, self.middle_name, self.last_name
        )

    class Meta:
        db_table = "tbl_c2b_requests"
        verbose_name_plural = "C2B Requests"

    @property
    def name(self):
        return "{} {} {}".format(
            self.first_name, self.middle_name, self.last_name
        )


class OnlineCheckout(models.Model):
    """
    Handles Online Checkout
    """

    id = models.BigAutoField(primary_key=True)
    phone = models.BigIntegerField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    is_paybill = models.BooleanField(default=True)
    checkout_request_id = models.TextField(default="")
    account_reference = models.CharField(max_length=50, default="")
    transaction_description = models.TextField(
        blank=True, null=True
    )
    call_back_url =  models.URLField(blank = True,null = True)
    customer_message = models.TextField(blank=True, null=True)
    merchant_request_id = models.TextField(
       blank=True, null=True
    )
    response_code = models.CharField(max_length=5, blank=True, null=True)
    response_description = models.TextField(
       blank=True, null=True
    )
    error_id   =  models.TextField(blank = True)
    error_code = models.TextField(blank = True,null = True)
    error_messsage =  models.TextField(blank = True,null =True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.phone)

    class Meta:
        db_table = "tbl_online_checkout_requests"
        verbose_name_plural = "Online Checkout Requests"



class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Company(TimestampedModel):
    name = models.CharField(max_length=255)
    company_code =  models.CharField(max_length=255)


    def __str__(self):
        return self.name
# Your other models can now inherit from TimestampedModel

class C2BPaymentsConfirmation(models.Model):
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
    
    created_on = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)


    send_sms = models.BooleanField(default=False)
    p_flag =  models.PositiveBigIntegerField(default=0)
    imarika_flag = models.BooleanField(default=False)
    igas_flag =  models.BooleanField(default=False)
    sirius_status = models.BooleanField(default=False)
    intergration_status =  models.CharField(max_length=255,blank=True,null=True)
    integration_date =  models.DateTimeField(blank=True,null=True)
    sirius_error_description = models.TextField(blank=True,null=True)
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE,blank=True,null=True)
    user_id  =  models.CharField(max_length=255,blank=True,null=True)
    user_name =  models.CharField(max_length=255,blank=True,null=True)
    is_from_reconcilliation =  models.BooleanField(default=False)
    fetch_id = models.CharField(max_length=255,blank=True,null=True)
    group_id =  models.CharField(max_length=255,blank=True,null=True)
    pollkava =  models.CharField(max_length=255,blank=True,null=True)
    kavaflag =  models.CharField(max_length=255,blank=True,null=True)
    kavaresult =  models.TextField(blank=True,null=True)
    p_kava =  models.CharField(max_length=255,blank=True,null=True)
    p_kava_result =  models.TextField(blank=True,null=True)
    fa_updated_date =  models.DateTimeField(blank=True,null=True)
    lob_policyNumber =  models.CharField(max_length=255,blank=True,null=True)
    recon_comment =  models.TextField(blank=True,null=True)
    is_valid_trans =  models.BooleanField(default=False)
    p_aims =  models.TextField(blank=True,null=True)
    aims_result =  models.CharField(max_length=255,blank=True,null=True)
    cellulant_flag = models.CharField(max_length=255,blank=True,null=True)
    column2 =  models.TextField(blank=True,null=True)
    newappflag =  models.BooleanField(default=False)
    confirmation_status = models.BooleanField(default=False)


    def __repr__(self):
        return f'{self.InvoiceNumber}'


class C2BPaymentsValidation(models.Model):
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
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __repr__(self):
        return f'{self.InvoiceNumber}'
class StoreBusinessCode(TimestampedModel):
    name  =  models.CharField(max_length=255)
    key =  models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class UserRequestsModel(TimestampedModel):
    business =  models.ForeignKey(StoreBusinessCode,on_delete=models.CASCADE)
    name =  models.CharField(max_length=255)
    key =  models.CharField(max_length=255)


    def __str__(self):
        return self.name

class MpesaRequest(TimestampedModel):
    STATUS_CHOICES = (
        ('PENDING', 'PENDING'),
        ('PAID', 'PAID'),
        ('CANCELLED', 'CANCELLED'),
      
    )
    user_key =  models.ForeignKey(UserRequestsModel,on_delete=models.CASCADE,blank=True,null=True)
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
    callback_sent =  models.BooleanField(default=False)
    paid =  models.CharField(max_length =  255, choices = STATUS_CHOICES , default = "PENDING" )
    
    
    def __str__(self) -> str:
        return self.phoneNumber
    
    
class MpesaCallbackMetaData(TimestampedModel):
    rdb =  models.ForeignKey(MpesaRequest,on_delete =  models.CASCADE,blank=True,null=True)
    name =  models.CharField(max_length =  255)
    value =  models.CharField(max_length = 255)
    description =  models.TextField(blank  =  True,null =True)

    def __str__(self) -> str:
        return self.name
    

class OnlineCheckoutResponse(models.Model):
    rdb =  models.ForeignKey(MpesaRequest,on_delete =  models.CASCADE,blank=True,null=True)
    merchant_request_id = models.CharField(
        max_length=50, blank=True, null=True
    )
    checkout_request_id = models.CharField(max_length=50, default="")
    result_code = models.CharField(max_length=5, blank=True, null=True)
    result_description = models.CharField(
        max_length=100, blank=True, null=True
    )
    mpesa_receipt_number = models.CharField(
        max_length=50, blank=True, null=True
    )
    transaction_date = models.DateTimeField(blank=True, null=True)
    phone = models.BigIntegerField(blank=True, null=True)
    amount = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.phone)

    class Meta:
        db_table = "tbl_online_checkout_responses"
        verbose_name_plural = "Online Checkout Responses"




