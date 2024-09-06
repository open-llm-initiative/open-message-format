# ResponseMessage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **str** | The content of the response message. | 
**refusal** | **str** | The refusal message if applicable, or null if not. | [optional] 
**role** | **str** | The role of the author of the message (e.g., &#39;assistant&#39;). | 
**metadata** | [**Metadata**](Metadata.md) |  | [optional] 

## Example

```python
from openapi_client.models.response_message import ResponseMessage

# TODO update the JSON string below
json = "{}"
# create an instance of ResponseMessage from a JSON string
response_message_instance = ResponseMessage.from_json(json)
# print the JSON string representation of the object
print(ResponseMessage.to_json())

# convert the object into a dict
response_message_dict = response_message_instance.to_dict()
# create an instance of ResponseMessage from a dict
response_message_from_dict = ResponseMessage.from_dict(response_message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


