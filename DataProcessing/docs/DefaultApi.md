# swagger_client.DefaultApi

All URIs are relative to *https://localhost:8290/primecore*

Method | HTTP request | Description
------------- | ------------- | -------------
[**access_point_count_get**](DefaultApi.md#access_point_count_get) | **GET** /AccessPoint/Count | 
[**access_point_get**](DefaultApi.md#access_point_get) | **GET** /AccessPoint | 
[**access_point_id_get**](DefaultApi.md#access_point_id_get) | **GET** /AccessPoint/{id} | 
[**access_point_name_device_type_count_get**](DefaultApi.md#access_point_name_device_type_count_get) | **GET** /AccessPoint/{name}/DeviceTypeCount | 
[**access_point_name_total_usernames_get**](DefaultApi.md#access_point_name_total_usernames_get) | **GET** /AccessPoint/{name}/TotalUsernames | 
[**building_get**](DefaultApi.md#building_get) | **GET** /Building | 
[**network_metric_building_get**](DefaultApi.md#network_metric_building_get) | **GET** /NetworkMetric/{building} | 
[**rogue_access_point_alarm_count_get**](DefaultApi.md#rogue_access_point_alarm_count_get) | **GET** /RogueAccessPointAlarm/Count | 
[**rogue_access_point_alarm_get**](DefaultApi.md#rogue_access_point_alarm_get) | **GET** /RogueAccessPointAlarm | 
[**rogue_access_point_alarm_id_get**](DefaultApi.md#rogue_access_point_alarm_id_get) | **GET** /RogueAccessPointAlarm/{id} | 


# **access_point_count_get**
> InlineResponse2001 access_point_count_get()



### Example 
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: default
swagger_client.configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = swagger_client.DefaultApi()

try: 
    api_response = api_instance.access_point_count_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->access_point_count_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**InlineResponse2001**](InlineResponse2001.md)

### Authorization

[default](../README.md#default)

### HTTP request headers

 - **Content-Type**: application/json, application/xml
 - **Accept**: application/json, application/xml

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **access_point_get**
> InlineResponse200 access_point_get(max_result=max_result, first_result=first_result)



### Example 
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: default
swagger_client.configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
max_result = 3.4 # float | max number of results returned (limited to 1000 by the backend) (optional)
first_result = 3.4 # float | first result index to be returned (optional)

try: 
    api_response = api_instance.access_point_get(max_result=max_result, first_result=first_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->access_point_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **max_result** | **float**| max number of results returned (limited to 1000 by the backend) | [optional] 
 **first_result** | **float**| first result index to be returned | [optional] 

### Return type

[**InlineResponse200**](InlineResponse200.md)

### Authorization

[default](../README.md#default)

### HTTP request headers

 - **Content-Type**: application/json, application/xml
 - **Accept**: application/json, application/xml

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **access_point_id_get**
> AccessPointObject access_point_id_get(id)



### Example 
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: default
swagger_client.configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
id = 'id_example' # str | id

try: 
    api_response = api_instance.access_point_id_get(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->access_point_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id | 

### Return type

[**AccessPointObject**](AccessPointObject.md)

### Authorization

[default](../README.md#default)

### HTTP request headers

 - **Content-Type**: application/json, application/xml
 - **Accept**: application/json, application/xml

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **access_point_name_device_type_count_get**
> InlineResponse2002 access_point_name_device_type_count_get(name)



### Example 
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: default
swagger_client.configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
name = 'name_example' # str | name

try: 
    api_response = api_instance.access_point_name_device_type_count_get(name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->access_point_name_device_type_count_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| name | 

### Return type

[**InlineResponse2002**](InlineResponse2002.md)

### Authorization

[default](../README.md#default)

### HTTP request headers

 - **Content-Type**: application/json, application/xml
 - **Accept**: application/json, application/xml

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **access_point_name_total_usernames_get**
> InlineResponse2001 access_point_name_total_usernames_get(name)



### Example 
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: default
swagger_client.configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
name = 'name_example' # str | name

try: 
    api_response = api_instance.access_point_name_total_usernames_get(name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->access_point_name_total_usernames_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| name | 

### Return type

[**InlineResponse2001**](InlineResponse2001.md)

### Authorization

[default](../README.md#default)

### HTTP request headers

 - **Content-Type**: application/json, application/xml
 - **Accept**: application/json, application/xml

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **building_get**
> InlineResponse2004 building_get()



### Example 
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: default
swagger_client.configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = swagger_client.DefaultApi()

try: 
    api_response = api_instance.building_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->building_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**InlineResponse2004**](InlineResponse2004.md)

### Authorization

[default](../README.md#default)

### HTTP request headers

 - **Content-Type**: application/json, application/xml
 - **Accept**: application/json, application/xml

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **network_metric_building_get**
> MetricsObject network_metric_building_get(building, metric, time_interval=time_interval)



### Example 
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: default
swagger_client.configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
building = 'building_example' # str | building
metric = 'metric_example' # str | metric to fetch (tx or rx)
time_interval = 3.4 # float | time interval, integer (hours) (optional)

try: 
    api_response = api_instance.network_metric_building_get(building, metric, time_interval=time_interval)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->network_metric_building_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **building** | **str**| building | 
 **metric** | **str**| metric to fetch (tx or rx) | 
 **time_interval** | **float**| time interval, integer (hours) | [optional] 

### Return type

[**MetricsObject**](MetricsObject.md)

### Authorization

[default](../README.md#default)

### HTTP request headers

 - **Content-Type**: application/json, application/xml
 - **Accept**: application/json, application/xml

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **rogue_access_point_alarm_count_get**
> InlineResponse2001 rogue_access_point_alarm_count_get()



### Example 
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: default
swagger_client.configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = swagger_client.DefaultApi()

try: 
    api_response = api_instance.rogue_access_point_alarm_count_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->rogue_access_point_alarm_count_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**InlineResponse2001**](InlineResponse2001.md)

### Authorization

[default](../README.md#default)

### HTTP request headers

 - **Content-Type**: application/json, application/xml
 - **Accept**: application/json, application/xml

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **rogue_access_point_alarm_get**
> InlineResponse2003 rogue_access_point_alarm_get(max_result=max_result, first_result=first_result)



### Example 
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: default
swagger_client.configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
max_result = 3.4 # float | max number of results returned (limited to 1000 by the backend) (optional)
first_result = 3.4 # float | first result index to be returned (optional)

try: 
    api_response = api_instance.rogue_access_point_alarm_get(max_result=max_result, first_result=first_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->rogue_access_point_alarm_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **max_result** | **float**| max number of results returned (limited to 1000 by the backend) | [optional] 
 **first_result** | **float**| first result index to be returned | [optional] 

### Return type

[**InlineResponse2003**](InlineResponse2003.md)

### Authorization

[default](../README.md#default)

### HTTP request headers

 - **Content-Type**: application/json, application/xml
 - **Accept**: application/json, application/xml

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **rogue_access_point_alarm_id_get**
> RogueAccessPointAlarmObject rogue_access_point_alarm_id_get(id)



### Example 
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: default
swagger_client.configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
id = 'id_example' # str | id

try: 
    api_response = api_instance.rogue_access_point_alarm_id_get(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->rogue_access_point_alarm_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id | 

### Return type

[**RogueAccessPointAlarmObject**](RogueAccessPointAlarmObject.md)

### Authorization

[default](../README.md#default)

### HTTP request headers

 - **Content-Type**: application/json, application/xml
 - **Accept**: application/json, application/xml

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

