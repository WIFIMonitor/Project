from __future__ import print_function
import time
import swagger_client
import requests
from swagger_client.rest import ApiException
from pprint import pprint
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

try:
    #
    # **GET** /AccessPoint
    #
    #api_response = api_instance.access_point_get()
    #pprint(api_response)
    
    #
    # **GET** /AccessPoint/Count
    #
    #api_response = api_instance.access_point_count_get()
    #pprint(api_response)
    
    #
    # **GET** /AccessPoint/{id}
    #
    #api_response = api_instance.access_point_id_get(10055296)
    #pprint(api_response)
    
    #
    # **GET** /AccessPoint/{name}/DeviceTypeCount
    #
    api_response = api_instance.access_point_name_device_type_count_get("biblioteca-ap11")
    pprint(api_response)
    
    #
    # **GET** /AccessPoint/{name}/TotalUsernames
    #
    #api_response = api_instance.access_point_name_total_usernames_get("dbio-ap13")
    #pprint(api_response)
    
    #
    # **GET** /Building
    #
    #api_response = api_instance.building_get()
    #pprint(api_response)

    #
    # **GET** /NetworkMetric/{building}
    #
    #api_response = api_instance.network_metric_building_get("DBIO", "rx")
    #pprint(api_response)

    #
    # **GET** /RogueAccessPointAlarm/Count
    #
    #api_response = api_instance.rogue_access_point_alarm_count_get()
    #pprint(api_response)

    #
    # **GET** /RogueAccessPointAlarm
    #
    #api_response = api_instance.rogue_access_point_alarm_get()
    #pprint(api_response)

    #
    # **GET** /RogueAccessPointAlarm/{id}
    #
    #api_response = api_instance.rogue_access_point_alarm_id_get(2909414704)
    #pprint(api_response)

except ApiException as e:
    print("Exception when calling DefaultApi->access_point_count_get: %s\n" % e)
