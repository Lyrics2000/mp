import base64
import hmac
import hashlib

import requests
import json

key = "9c3dc428-1dd6-45c6-9abd-dd5ee2e73075"
shared_secret =  "ZuebHsMjjZrXU+006G+6QP4EHN9kwqUfKFJDG3wggSM="
def generate_signature_from_params(signature_params: str, secret_key: str) -> str:
    sig_bytes = signature_params.encode('utf-8')
    decoded_secret = base64.b64decode(secret_key)
    hmac_sha256 = hmac.new(decoded_secret, sig_bytes, hashlib.sha256)
    message_hash = hmac_sha256.digest()
    return base64.b64encode(message_hash).decode('utf-8')



import requests
import json

url = "https://apitest.cybersource.com/rbs/v1/subscriptions"

payload = json.dumps({
  "clientReferenceInformation": {
    "code": "TC501713",
    "partner": {
      "developerId": "ABCD1234",
      "solutionId": "GEF1234"
    },
    "applicationName": "CYBS-SDK",
    "applicationVersion": "v1"
  },
  "processingInformation": {
    "commerceIndicator": "recurring",
    "authorizationOptions": {
      "initiator": {
        "type": "merchant"
      }
    }
  },
  "subscriptionInformation": {
    "planId": "6868912495476705603955",
    "name": "Subscription with PlanId",
    "startDate": "2024-06-11"
  },
  "paymentInformation": {
    "customer": {
      "id": "C24F5921EB870D99E053AF598E0A4105"
    }
  }
})
headers = {
  'Content-Type': 'application/json',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-site',
  'host':'apitest.cybersource.com',
  'digest': 'SHA-256=l+x/evDuJUleLgcgPf5W7TceIjKOg3s1wu47BRsDq3Y=',
  'sec-ch-ua': '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
  'signature': 'keyid="b9e5fab9-2d75-4ddb-92f1-ac8639347648", algorithm="HmacSHA256", headers="host v-c-date request-target digest v-c-merchant-id", signature="yKOe3YAuVZcdkTSB7d21DApucR+TFmm7Mp5MwbB+mGE="',
  'v-c-date': 'Wed, 16 Apr 2025 12:35:05 GMT',
  'v-c-merchant-id': 'britamke'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
