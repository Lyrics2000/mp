from rest_framework_simplejwt.tokens import UntypedToken, RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
import time 
import requests
from rest_framework_simplejwt.tokens import AccessToken
import jwt

from .important.validateToken import ValidateToken
from datetime import datetime, timezone

from django.urls import resolve



from rest_framework.response import Response

from config.settings.settings import (
    AUDIENCE,
    ISSUER_ID
)


import logging

logger = logging.getLogger(__name__)



    

class AzureADAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logger.info("YourMiddleware initialized.")
        
        
    def __call__(self, request):
        logger.debug("Processing request in YourMiddleware.")
        # Code to be executed for each request before
        # the view (and later middleware) are called.

       
        # Code to be executed for each request/response after
        # the view is called.
        
        print(request.path)
        print(request.headers['Host'])
        # print(request.headers['Accept-Language'])
        print(request.META['REQUEST_METHOD'])
        print(request.META['HTTP_USER_AGENT'])
        
        
        
        # allowed_endpoints = [
        #     'client_onboarding:RegisterClient',
        #     # Add more allowed views as needed
        # ]

        # # Get the view name for the current request
        # current_endpoint = resolve(request.path_info).url_name

        # # Check if the current endpoint is in the allowed list
        # if current_endpoint in allowed_endpoints:
        authorization_header = request.headers.get('Authorization')

        if authorization_header and authorization_header.startswith('Bearer '):
                access_token = authorization_header.split(' ')[1]

                # Replace with your actual values for audience and role
                audience =  AUDIENCE
                role = ISSUER_ID

                try:
                    app = ValidateToken(access_token, audience, role)
                    decoded_token = app.decode_and_verify_token()
                    
                    # print("decoded token ", decoded_token)
                    request.decoded_token = decoded_token
           
                except Exception as e:
                    logger.error(f"Internal issue occures  {str(e)}")
                    return JsonResponse(
                        {"code": "Unauthorized", "description": f"Error with Authentication"},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
        else:
                return JsonResponse(
                    {"code": "authorization_header_missing", "description": "Authorization header is expected"},
                    status=status.HTTP_401_UNAUTHORIZED
                )


        response = self.get_response(request)

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # List of endpoints where the middleware should be applied
 
       
        # # Continue with the default processing for other endpoints
        # response = self.get_response(request)
    
        return None

    
