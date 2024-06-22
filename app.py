import requests

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer nLnjlcPjFErEsE4eZh7X4TcdYfAk'
}
payload = {
    "BusinessShortCode": 174379,
    "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjQwNjIyMTY0MzI4",
    "Timestamp": "20240622164328",
    "CheckoutRequestID": "ws_CO_22062024155446612757484575",
  }

response = requests.post('https:/sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query',  data = payload,headers = headers)
print(response.json())