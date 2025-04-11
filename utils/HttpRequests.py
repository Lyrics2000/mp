import requests
import json


class HttpCalls:
    def __init__(self):
        pass

    def post(self,data,url):
        payload = json.dumps(data)
        headers = {
        'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response
