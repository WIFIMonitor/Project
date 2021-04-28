from django.shortcuts import render


import time
import swagger_client
import requests
from swagger_client.rest import ApiException
from pprint import pprint
import os
from requests.auth import HTTPBasicAuth

# Getting the access token
url = 'https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid'
header = {'Content-Type': 'application/x-www-form-urlencoded'}

x = requests.post(url,headers=header,auth=HTTPBasicAuth('cbi0930f2mdfjDgf9vaywDfnk1Ia','ime3TsBSGd2fDMeYsTnRMsZoH0Ya'))
resp = x.json()

# Configure OAuth2 access token for authorization
swagger_client.configuration.access_token = resp["access_token"]

# create an instance of the API class
api_instance = swagger_client.DefaultApi()

def index(request):
    #esta a dar erro
    #api_response = api_instance.access_point_name_device_type_count_get("biblioteca-ap11")
    #pprint(api_response)

    return render(request,'index.html')