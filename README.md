# Open Message Format (OMF)
## Overview
OMF is a compact, user-friendly specification that defines a lightweight API contract between client and server for building conversational agents, and defines a standard schema for the "messages" object, which contains user and assistant interactions. The "messages" object schema in OMF serves a dual purpose, to define a standard way to exchange user and assistant conversations from the client to your backend server, and from your backend server to an upstream LLM.

Developers building conversational agents and generative AI applications waste precious time on two things:
- Writing integration code that works only with specific client-side UI tools such as Gradio or Streamlit, which reduces their ability to experiment with new tools quickly. 
- Writing integration code what works with specific LLMs, reducing their ability to easily swap between LLMs for quick experimentation.

Writing boilerplate integration code results in a slowed pace of development and a system that is rigid and difficult to change. OMF eliminates this undifferentiated heavy lifting by defining a standard API contract and a schema to exchange messages for conversational apps, and providers built-in convertors that make it easy for developers to experiment with different LLMs.

The key advantages of using OMF are:
- **Interoperability:** OMF standardizes prompt interactions between clients, servers, and LLMs. OMF is also interoperable across multiple popular LLMs.
- **Extensibility:** OMF is designed to be extended in order to fit all developers' use cases.
## Benefits for Developers
OMF simplifies the process of sending messages, making it easier to deploy conversational agents and other LLM-based tools and applications. It removes the guesswork for developers on how to send and receive messages.

![image](https://github.com/user-attachments/assets/f34e812a-eacb-420a-89f1-c6b15ab8c446)
![image (1)](https://github.com/user-attachments/assets/2c58b2a3-5437-46ad-ae89-581eac7c77bb)



## How to Use OMF

### 1. Setting Up Your Endpoint

#### a. Choose Your Development Environment

You can use any programming language and web framework that supports OpenAPI specifications. Common choices include:

- **Python**: Flask, FastAPI, or Django.
- **JavaScript/Node.js**: Express.js.
- **Java**: Spring Boot.
- **Go**: Gin or Echo.
- **Rust**: Actix-web or Rocket.

#### b. Implement the API Endpoints

If tools like `openapi-generator-cli` are not be viable for creating server stubs, you can manually implement the endpoint described in the OMF spec:

1. **Manually Create the `/message` Endpoint**:
    - In your chosen framework, define a POST endpoint `/message`.
    - Ensure that this endpoint accepts and processes the JSON payload as defined in the OMF spec.
    - The endpoint should accept a an array of the [`Message`](https://github.com/open-llm-initiative/open-message-format/blob/e6d4d93e4652e0594c81f3b3b4d7192ad3dffab0/OMFspec.yml#L41) object. Each message will have a `role` and a `content` field, and the content could be text, base64-encoded images, or image URLs.

2. **Message Handling Logic**:
    - Parse the incoming JSON request into appropriate data models. The [`Message`](https://github.com/open-llm-initiative/open-message-format/blob/e6d4d93e4652e0594c81f3b3b4d7192ad3dffab0/OMFspec.yml#L41) object should be parsed with a `role` and an array of [`ContentItem`](https://github.com/open-llm-initiative/open-message-format/blob/e6d4d93e4652e0594c81f3b3b4d7192ad3dffab0/OMFspec.yml#L65) objects.
    - Implement logic to handle different types of content, such as text, images, and image URLs.
    - If you want to, you can directly send the array to an LLM by just passing it in the messages parameter for many LLM providers. You may need to create some tools to convert depending on the model you use.

3. **Construct Responses**:
    - Based on the request, generate a response that follows the [`ResponseMessage`](https://github.com/open-llm-initiative/open-message-format/blob/e6d4d93e4652e0594c81f3b3b4d7192ad3dffab0/OMFspec.yml#L106) schema outlined in the specification.

#### c. Example Setup

Here’s a simplified example of how to implement the `/message` endpoint in Python using Flask:

```python
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def handle_message():
    messages = request.json

    try:
        # Send the received messages directly to OpenAI API using the correct method
        response = openai.chat.completions.create(
            model="gpt-4o-mini", messages=messages
        )

        # Return the first choice's message directly
        return response.choices[0].message.content, 200
    except openai.error.OpenAIError as e:
        # Handle OpenAI API errors
        return {"error": str(e)}, 500
    
    return jsonify(response_message)

if __name__ == '__main__':
    app.run(port=8080)
```

#### d. Testing Locally

Once the endpoint is implemented, you can test it locally using `curl`, Postman, or any other HTTP client. For example, you can send the following request with curl:

```bash
curl -X POST http://localhost:8080/message \
     -H "Content-Type: application/json" \
     -d '[
             {
               "role": "user",
               "content": "Hello World"
             }
           ]'
```

### 3. Testing Your Implementation

After setting up the server, you can test the `/message` endpoint using tools like:

- **curl** (as shown above)
- **Postman**: Import the OpenAPI specification and generate requests directly to interact with your locally running server.

Ensure that your endpoint processes the incoming messages correctly and returns appropriate responses in line with the OMF specification.

### 4. Deploying Your API

Once your API is working locally, you can deploy it using your preferred method, such as:

- **Containerization**: Use Docker to containerize your application and deploy it to cloud services like AWS, Azure, or GCP.
- **Dedicated Server**: Run the application on a dedicated server using a production-ready web server and reverse proxy.

### Extending the Specification
OMF is designed to be flexible and generic, allowing users to extend and expand the specification to fit specific needs. For instance, users can add arguments specific to OpenAI roles or modify the specification for providers like Cohere, who require separate `message` and `chat_history` parameters. An example modification might include adding the `name` parameter for the OpenAI `user` role.

``` yaml
Message:
    type: object
    properties:
        role:
            type: string
            description: |
                Role of the message sender. Examples include:
                - `system`: For system messages
                - `user`: For messages from the user
                - `assistant`: For messages from the assistant
        content:
            oneOf:
                - type: array
                  items:
                      $ref: "#/components/schemas/ContentItem"
                  description: |
                      Content of the message. It can be a list of content items, such as text and images.
                - type: string
                  description: text content of the message,
        name:
            type: string
            description: the name of the user sending this message
    required:
        - role
        - content
```
*This is a modification to the base spec that adjusts for the name parameter in the OpenAI `user` message, allowing developers to have chats with multiple people*
```yaml
name:
    type: string
    description: |
                The name of the user sending the message.
```
*This is the section that was added to the spec in the above*
## Comparison
| LLM Provider   | Compatible with Stock OMF | Benefits from Additional Tooling | Requires Additional Tooling |
| -------------- | ------------------------- | -------------------------------- | --------------------------- |
| OpenAI         | Yes                       | Yes                              | No                          |
| Mistral AI     | Yes                       | Yes                              | No                          |
| Anthropic      | Yes                       | Yes                              | No                          |
| IBM            | No                        | No                               | Yes                         |
| Google         | Yes (Requires Conversion) | Yes                              | No                          |
| Amazon Bedrock | Yes (Requires Conversion) | Yes                              | No                          |
| Cohere         | Yes (Requires Conversion) | Yes                              | No                          |

*Note: Some models have unique parameters such as `message_id` or `name`. These parameters, while easy to add for specific models, are not universal and therefore not included in the base specification. Some models also have certain function calling capabilities but due to function calls being more relevant to a full `ChatCompletions` setup, this is more relevant to the Open Completions API*
## Roadmap
Future improvements include:

| Feature or Improvement                                | Description                                                                                                               |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Additional message metadata parameter                 | Allows servers to gain more insight into the origins or details of the messages object before it is sent to an LLM.       |
| Extended version of the spec for Open Completions API | Currently being worked on to provide more robust functionality.                                                           |
| `dependentRequired` keyword for OpenAPI 3.1.0         | Will be implemented once more tools support OpenAPI 3.1.0, ensuring content types align with the `type` in `ContentItem`. |
| Add more details to the `Metadata` object.            | Possible additions include a `timestamp` parameter, a `completion_tokens` parameter, and a `prompt_tokens` parameter      |

We encourage you to suggest and upvote new possible roadmap items via github issues.
