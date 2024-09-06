# openapi_client.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**message_post**](DefaultApi.md#message_post) | **POST** /message | This method allows developers to receive chat messages from an upstream client in a standard format.


# **message_post**
> ResponseMessage message_post(message)

This method allows developers to receive chat messages from an upstream client in a standard format.

This endpoint receives a message or messages object from a client and returns a message containing the content of the response. 

### Example


```python
import openapi_client
from openapi_client.models.message import Message
from openapi_client.models.response_message import ResponseMessage
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    message = [openapi_client.Message()] # List[Message] | 

    try:
        # This method allows developers to receive chat messages from an upstream client in a standard format.
        api_response = api_instance.message_post(message)
        print("The response of DefaultApi->message_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->message_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **message** | [**List[Message]**](Message.md)|  | 

### Return type

[**ResponseMessage**](ResponseMessage.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Response containing the content string. |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

