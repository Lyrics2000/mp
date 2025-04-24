
from .models import (
    Callbackhanldlers,
    C2BCallbackResponses
)


import re
from utils.HttpRequests import (
    HttpCalls
)

import re

class C2BSendMessages:
    def __init__(self):
        pass

    def sendCallbacks(self, confirmation_obj):
        check_url = Callbackhanldlers.objects.filter(
            paybill=confirmation_obj.BusinessShortCode
        ).first()

        if check_url:
            if re.match(rf"{check_url.regex}", confirmation_obj.BillRefNumber):
                data = {
                    "Body": {
                        "stkCallback": {
                            "MerchantRequestID": "84115-769684-1",
                            "CheckoutRequestID": confirmation_obj.BillRefNumber,
                            "ResultCode": 0,
                            "ResultDesc": "The service request is processed successfully.",
                            "CallbackMetadata": {
                                "Item": [
                                    {"Name": "Amount", "Value": float(confirmation_obj.TransAmount)},
                                    {"Name": "MpesaReceiptNumber", "Value": confirmation_obj.TransID},
                                    {"Name": "Balance"},
                                    {"Name": "TransactionDate", "Value": confirmation_obj.TransTime},
                                    {"Name": "PhoneNumber", "Value": confirmation_obj.MSISDN}
                                ]
                            }
                        }
                    }
                }
                try:
                    ap = HttpCalls()
                    response = ap.post(data, check_url.url)
                    C2BCallbackResponses.objects.create(
                        callbackhandler=check_url,
                        sent=True,
                        response=response.text
                    )
                    confirmation_obj.confirmation_status = True
                    confirmation_obj.save()

                except Exception as e:
                    print(f"There is an error sending data: {e}")
            else:
                print("BillRefNumber does not match the required pattern.")
        else:
            print("No matching callback handler found for the provided paybill.")
