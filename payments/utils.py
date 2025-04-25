
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
        )

        if len(check_url) > 0:
            for i in check_url:
                if re.match(rf"{i.regex}", confirmation_obj.BillRefNumber):
                    data = {
                        "Body": {
                            "stkCallback": {
                                "MerchantRequestID": "84115-769684-1",
                                "CheckoutRequestID": i.BillRefNumber,
                                "ResultCode": 0,
                                "ResultDesc": "The service request is processed successfully.",
                                "CallbackMetadata": {
                                    "Item": [
                                        {"Name": "Amount", "Value": float(i.TransAmount)},
                                        {"Name": "MpesaReceiptNumber", "Value": i.TransID},
                                        {"Name": "Balance"},
                                        {"Name": "TransactionDate", "Value": i.TransTime},
                                        {"Name": "PhoneNumber", "Value": i.MSISDN}
                                    ]
                                }
                            }
                        }
                    }
                    try:
                        ap = HttpCalls()
                        response = ap.post(data, check_url.url)
                        
                        try:
                            if response.status_code ==  200:
                                json = response.json()
                                if json['ResponseCode'] == 0:

                                    C2BCallbackResponses.objects.create(
                                        callbackhandler=check_url,
                                        sent=True,
                                        response=response.text
                                    )
                                    confirmation_obj.confirmation_status = True
                                    confirmation_obj.save()
                        except Exception as e:
                            print(f"There is an error saving data: {e}")


                    except Exception as e:
                        print(f"There is an error sending data: {e}")
                else:
                    print("BillRefNumber does not match the required pattern.")
        
        else:
            print("No matching callback handler found for the provided paybill.")
