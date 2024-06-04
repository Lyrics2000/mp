import requests

url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

payload = {}
files={}


response = requests.request("GET", url, auth=('kRGH9T08n5D85iW2AVufj6TjZI9GgwEG','EpxSbYm2UK9jmAH2'))

print(response.json())