import requests
from typing import List, Union, Optional


class OMFClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def send_messages(self, messages: List[dict], endpoint: str = "/message") -> dict:
        """Send multiple messages to the server."""
        response = requests.post(f"{self.base_url}{endpoint}", json=messages)
        response.raise_for_status()
        return response.json()

    def create_text_content(self, text: str) -> dict:
        """Create a text content item."""
        return {"type": "text", "text": text}

    def create_image_content(
        self, base64_data: str, media_type: str = "image/jpeg"
    ) -> dict:
        """Create an image content item."""
        return {
            "type": "image",
            "source": {"type": "base64", "media_type": media_type, "data": base64_data},
        }

    def create_image_url_content(self, url: str) -> dict:
        """Create an image URL content item."""
        return {"type": "image_url", "image_url": {"url": url}}


def run_chatbot():
    client = OMFClient(base_url="http://localhost:8080")
    conversation = []

    while True:
        # Get user input
        user_input = input("You: ")

        # Exit the loop if the user types 'exit' or 'quit'
        if user_input.lower() in ["exit", "quit"]:
            break

        # Create the user message and add it to the conversation history
        user_message = {
            "role": "user",
            "content": [client.create_text_content(user_input)],
        }
        conversation.append(user_message)

        # Send the entire conversation history to the backend
        response = client.send_messages(conversation)

        # Assume the last message in the response is the bot's reply
        bot_response = {"role": response["role"], "content": response["content"]}
        conversation.append(
            bot_response
        )  # Add the bot's response to the conversation history

        # Print the bot's response
        print(f"Bot: {bot_response['content']}")


if __name__ == "__main__":
    run_chatbot()
