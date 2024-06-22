
from django.http import JsonResponse
from config.settings.settings import UAT_ENV
import requests

class MicrosoftValidation:
    def __init__(self,request):
        print(request.META)
        self.sub_key = request.META.get('HTTP_OCP_APIM_SUBSCRIPTION_KEY', None)
        self.token = request.META.get('HTTP_AUTHORIZATION', None)
        self.baseUrl = "https://brtgw.britam.com"   if UAT_ENV else "http://172.18.0.37:31011"


    
    
        
        
    def verify(self):
        
        if None in [self.sub_key, self.token]:
            return  JsonResponse(
                                {"message": "fill all required headeer"},
                                status=401
                            )
        url = f"{self.baseUrl}/api/auth/verify/"
        
        headers = {
            'Ocp-Apim-Subscription-Key': self.sub_key,
            'Authorization': f'{self.token}'
            }

        response = requests.get(url, headers=headers,verify=False)
        
        
        # print("the response is that ", response.json())

        if response.status_code ==  401:
            return JsonResponse(response.json(),status  =  response.status_code)
        
        return response
       