

from django.urls import path


from .views import (
    SendSTKPUSH,
    MpesaCallbackApiView,
    FilterTransaction,
    C2BValidationApiView,
    C2BConfirmationApiView,
    MakeC2BPaymentApiView
)

app_name = "payments"

urlpatterns = [
    path("stk/",SendSTKPUSH.as_view()),
    path("callback/",MpesaCallbackApiView.as_view()),
    path("filter/",FilterTransaction.as_view()),
    path('validation_url/', C2BValidationApiView.as_view(), name='c2b_validation_url'),
    path('confirmation_url/', C2BConfirmationApiView.as_view(), name='c2b_confirmation_url'),
    path("c2b_simulate/",MakeC2BPaymentApiView.as_view())
]
