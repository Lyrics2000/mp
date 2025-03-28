import requests
import json
import logging

logger = logging.getLogger(__name__)
url = "http://172.28.1.36:8259/dashboard/add/api/"
def make_api_request_log_request(data,request):
    # try:
        sub_key = request.META.get('HTTP_OCP_APIM_SUBSCRIPTION_KEY', None)
        token = request.META.get('HTTP_AUTHORIZATION', None)
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip_address:
            ip_address = ip_address.split(',')[0].strip()  # Get first IP from the list
        else:
            ip_address = request.META.get('REMOTE_ADDR', '')
        try:
             data['request_ip']  =ip_address.split(":")[0]
        except:
             data['request_ip']  =ip_address
        headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": sub_key,
        "Authorization": token
        }
        data['role'] = data['role'][0]
        print("the data to send is ",data)
        logger.info(f"The data to send is : {data}")
        print("The ip address is ",ip_address)
        logger.info(f"The ip address is: {ip_address}")
        
       
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        print("the response from sending is ", response.json())
        logger.info(f"The response from sending is : {response.json()}")
        return response.json()
    # except requests.exceptions.RequestException as e:
    #     print(f"Error occurred: {e}")
    #     logger.info(f"The Error occured is  : {e}")
    #     return None

# Example usage


# data = {
#     "role": "DOCUMENT_CREATE_DOCUMENT",
#     "successfull": False,
#     "message": "successfull call",
#     "request_ip": "102.219.210.70",
#     "endpoint": "/api/v1/email/"
# }

