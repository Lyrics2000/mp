from django.contrib import admin

# Register your models here.

from .models import (
    MpesaRequest,
    MpesaCallbackMetaData,
    C2BPayments,
    
)


admin.site.register(MpesaRequest)
admin.site.register(MpesaCallbackMetaData)
admin.site.register(C2BPayments)
