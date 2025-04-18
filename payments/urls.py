

from django.urls import path


from .views import (
    SendSTKPUSH,
    MpesaCallbackApiView,
    FilterTransaction,
    C2BValidationApiView,
    C2BConfirmationApiView,
    MakeC2BPaymentApiView,
    B2cResult,
    B2cTimeOut,
    C2bConfirmation,
    C2bValidation,
    OnlineCheckoutCallback,
    AddPaybill,
    QueryMpesaStatement,
    CheckTransactionStatus,
    RegisterURL,
    SimulateApiView,
    RecurringCardsView,
    CreateBusinessApiView,
    SendSTKPUSHBusinessProcess,
    UserRequestsModelApiView,
    VerifyManualApiView
    
)

app_name = "payments"


urlpatterns = [
    path("add/paybill/",AddPaybill.as_view()),
    path("add/user/",UserRequestsModelApiView.as_view()),
    path("add/business/",CreateBusinessApiView.as_view()),
    path("stk/",SendSTKPUSH.as_view()),
    path("stk/business/",SendSTKPUSHBusinessProcess.as_view()),
    path("stk/query/",QueryMpesaStatement.as_view()),
    path("check/transaction/status/",CheckTransactionStatus.as_view()),
    path("callback/",MpesaCallbackApiView.as_view()),
    path("filter/",FilterTransaction.as_view()),
    path("verify/manual/",VerifyManualApiView.as_view()),
    path('validation_url/', C2BValidationApiView.as_view(), name='c2b_validation_url'),
    path('confirmation_url/', C2BConfirmationApiView.as_view(), name='c2b_confirmation_url'),
    path("c2b_simulate/",MakeC2BPaymentApiView.as_view()),
    path("b2c/timeout/", B2cTimeOut.as_view(), name="b2c_timeout"),
    path("b2c/result/", B2cResult.as_view(), name="b2c_result"),
    path("c2b/register/url/",RegisterURL.as_view()),
    path("c2b/simulate/",SimulateApiView.as_view()),
    path("merchant/post/",RecurringCardsView.as_view()),
    
     path(
        "c2b/confirmation/", C2bConfirmation.as_view(), name="c2b_confirmation"
    ),
    path("c2b/validate/", C2bValidation.as_view(), name="c2b_validation"),
    path(
        "c2b/online_checkout/callback/",
        OnlineCheckoutCallback.as_view(),
        name="c2b_checkout_callback",
    ),
]
