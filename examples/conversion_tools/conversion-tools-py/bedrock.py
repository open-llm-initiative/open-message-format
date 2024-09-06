"""
This Python script demonstrates the conversion of messages from the Open Message Format (OMF)
to the AWS Bedrock message format. The script includes a conversion function that processes 
OMF messages, which may contain text and/or images (in Base64 format), and converts them into
a format compatible with AWS Bedrock.

The script also includes test cases to validate the conversion function. These tests check
the conversion of:
- Text-only messages
- Image-only messages (PNG)
- Mixed content messages (both text and image)
- Messages with non-PNG images (JPEG, GIF, WebP)
"""

from typing import List, Dict
import logging
import boto3

from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_conversation(bedrock_client, model_id, messages):
    """
    Sends messages to a model.
    Args:
        bedrock_client: The Boto3 Bedrock runtime client.
        model_id (str): The model ID to use.
        system_prompts (JSON) : The system prompts for the model to use.
        messages (JSON) : The messages to send to the model.

    Returns:
        response (JSON): The conversation that the model generated.

    """

    logger.info("Generating message with model %s", model_id)

    # Send the message.
    response = bedrock_client.converse(
        modelId=model_id,
        messages=messages,
    )

    # Log token usage.
    token_usage = response["usage"]
    logger.info("Input tokens: %s", token_usage["inputTokens"])
    logger.info("Output tokens: %s", token_usage["outputTokens"])
    logger.info("Total tokens: %s", token_usage["totalTokens"])
    logger.info("Stop reason: %s", response["stopReason"])

    return response


# Function to convert a list of OMF messages to Bedrock messages
def convert_omf_to_bedrock(messages: List[Dict]) -> List[Dict]:
    """
    Converts a list of OMF messages to Bedrock messages.

    Args:
        messages (List[Dict]): A list of OMF message dictionaries.

    Returns:
        List[Dict]: A list of Bedrock message dictionaries.
    """
    bedrock_messages = []

    for message in messages:
        role = message["role"]
        bedrock_content = []

        # Check if the content is a list (complex content)
        if isinstance(message["content"], list):
            for item in message["content"]:
                # Handle text content
                if item["type"] == "text":
                    bedrock_content.append({"text": item["text"]})
                # Handle image content
                elif item["type"] == "image":
                    # Map the media type to a simpler format string
                    format_map = {
                        "image/png": "png",
                        "image/jpeg": "jpeg",
                        "image/gif": "gif",
                        "image/webp": "webp",
                    }
                    format = format_map.get(item["source"]["media_type"], "unknown")
                    bedrock_content.append(
                        {
                            "image": {
                                "format": format,
                                "source": {"bytes": item["source"]["data"]},
                            }
                        }
                    )

        # Add the converted message to the list
        bedrock_messages.append({"role": role, "content": bedrock_content})

    return bedrock_messages


# Test case for converting a text-only message
def test_convert_text_only():
    """
    Tests the conversion of a text-only OMF message to Bedrock format.
    """
    omf_messages = [
        {"role": "user", "content": [{"type": "text", "text": "Hello, World!"}]}
    ]

    expected_bedrock_messages = [
        {"role": "user", "content": [{"text": "Hello, World!"}]}
    ]

    assert convert_omf_to_bedrock(omf_messages) == expected_bedrock_messages


# Test case for converting an image-only (PNG) message
def test_convert_image_only():
    """
    Tests the conversion of an image-only OMF message (PNG) to Bedrock format.
    """
    omf_messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": "base64_image_data",
                    },
                }
            ],
        }
    ]

    expected_bedrock_messages = [
        {
            "role": "user",
            "content": [
                {"image": {"format": "png", "source": {"bytes": "base64_image_data"}}}
            ],
        }
    ]

    assert convert_omf_to_bedrock(omf_messages) == expected_bedrock_messages


# Test case for converting a message with both text and image content
def test_convert_text_and_image():
    """
    Tests the conversion of a mixed content OMF message (text and image) to Bedrock format.
    """
    omf_messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": "base64_image_data",
                    },
                },
                {"type": "text", "text": "What is in this image?"},
            ],
        }
    ]

    expected_bedrock_messages = [
        {
            "role": "user",
            "content": [
                {"image": {"format": "png", "source": {"bytes": "base64_image_data"}}},
                {"text": "What is in this image?"},
            ],
        }
    ]

    assert convert_omf_to_bedrock(omf_messages) == expected_bedrock_messages


# Test case for converting messages with non-PNG images (JPEG, GIF, WebP)
def test_convert_non_png_images():
    """
    Tests the conversion of OMF messages containing non-PNG images (JPEG, GIF, WebP) to Bedrock format.
    """
    omf_messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": "base64_jpeg_data",
                    },
                },
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/gif",
                        "data": "base64_gif_data",
                    },
                },
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/webp",
                        "data": "base64_webp_data",
                    },
                },
            ],
        }
    ]

    expected_bedrock_messages = [
        {
            "role": "user",
            "content": [
                {"image": {"format": "jpeg", "source": {"bytes": "base64_jpeg_data"}}},
                {"image": {"format": "gif", "source": {"bytes": "base64_gif_data"}}},
                {"image": {"format": "webp", "source": {"bytes": "base64_webp_data"}}},
            ],
        }
    ]

    assert convert_omf_to_bedrock(omf_messages) == expected_bedrock_messages


def test_multiple_messages():
    """
    Tests the conversion of multiple messages to Bedrock format.
    """
    omf_messages = [
        {"role": "user", "content": [{"type": "text", "text": "Hello, World!"}]},
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {"media_type": "image/png", "data": "base64_image_data"},
                }
            ],
        },
    ]

    expected_bedrock_messages = [
        {"role": "user", "content": [{"text": "Hello, World!"}]},
        {
            "role": "user",
            "content": [
                {"image": {"format": "png", "source": {"bytes": "base64_image_data"}}}
            ],
        },
    ]

    assert convert_omf_to_bedrock(omf_messages) == expected_bedrock_messages


def test_sending_messages_to_aws_bedrock():
    """
    Entrypoint for Anthropic Claude 3 Sonnet example.
    """

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    model_id = "meta.llama3-8b-instruct-v1:0"

    omf_messages = [
        {"role": "user", "content": [{"type": "text", "text": "Hello, World!"}]}
    ]

    messages = convert_omf_to_bedrock(omf_messages)
    try:

        bedrock_client = boto3.client(service_name="bedrock-runtime")
        response = generate_conversation(bedrock_client, model_id, messages)

        # Add the response message to the conversation.
        output_message = response["output"]["message"]
        messages.append(output_message)

        # Show the complete conversation.
        for message in messages:
            print(f"Role: {message['role']}")
            for content in message["content"]:
                print(f"Text: {content['text']}")
            print()

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        raise Exception(f"A client error occured: {message}")

    else:
        print(f"Finished generating text with model {model_id}.")


# Run all tests
test_convert_text_only()
test_convert_image_only()
test_convert_text_and_image()
test_convert_non_png_images()
test_multiple_messages()
test_sending_messages_to_aws_bedrock()

print("All tests passed!")
