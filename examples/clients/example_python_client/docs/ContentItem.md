# ContentItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The type of content, such as text or image URL. | 
**text** | **str** | The text content. Required if type is &#39;text&#39;. | [optional] 
**image_url** | **object** | The image URL object. Required if type is &#39;image_url&#39;. | [optional] 
**source** | **object** | The source object. Required if type is &#39;image&#39;. | [optional] 

## Example

```python
from openapi_client.models.content_item import ContentItem

# TODO update the JSON string below
json = "{}"
# create an instance of ContentItem from a JSON string
content_item_instance = ContentItem.from_json(json)
# print the JSON string representation of the object
print(ContentItem.to_json())

# convert the object into a dict
content_item_dict = content_item_instance.to_dict()
# create an instance of ContentItem from a dict
content_item_from_dict = ContentItem.from_dict(content_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


