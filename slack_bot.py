import os
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from flask import Flask, request, jsonify, Response
import time

# Load bot token from environment variables or set it directly
SLACK_BOT_TOKEN = "xoxb-7715112267175-7768517775362-2v9cAdMljH71gyCs7Mn0rGGL"  # Replace with your Slack bot token
client = WebClient(token=SLACK_BOT_TOKEN)

app = Flask(__name__)

# Private API endpoint (replace with your actual API endpoint)
PRIVATE_API_URL = "https://genai.pt-df.inday.io/api/v2alpha/prompt/generate/YzFmNmQxYTAtMjc5MC00MDJjLTkzY2EtMGEzZTcxNGE4NDMwOjpnYWdhbi5zaW5naA"

# Track processed message IDs and their timestamps
processed_messages = {}

# Event handler for messages and challenge verification
@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json

    # Respond to Slack URL verification challenge
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    # Check if the event type is a message
    if "event" in data and data["event"]["type"] == "message":
        event = data["event"]

        # Ignore bot messages (including the bot's own messages)
        if "subtype" in event and event.get("bot_id") is not None:
            return Response(status=200)

        # Ignore messages without text or messages from Slack bots
        if "text" not in event or "bot_profile" in event:
            return Response(status=200)

        # Get the message text, message ID, and channel ID
        text = event["text"].strip().lower()  # Convert to lowercase for case-insensitive matching
        message_id = event["ts"]  # Unique timestamp-based message ID
        channel_id = event["channel"]
        user_id = event["user"]  # Get the user ID to track individual conversations


        # Check if this message ID has already been processed and if enough time has passed
        current_time = time.time()
        if message_id in processed_messages:
            return Response(status=200)  # Ignore if already processed
        
        # Mark the message as processed immediately to prevent multiple responses
        processed_messages[message_id] = time.time()  

        # Send introduction message
        intro_message = (
            f"Hi there, <@{user_id}>! Please hold on while I find the answer for you 😊.\n"
            "_Please note: If you don't receive an answer, feel free to try again in a few minutes._"
        )
        try:
            client.chat_postMessage(channel=channel_id, text=intro_message)
        except SlackApiError as e:
            print(f"Error posting introduction message: {e.response['error']}")

        # Prepare headers for the API request
        headers = {
            'accept': 'application/json',
            'wd-origin': 'gagan.singh',  # Replace with your origin
            'wd-pca-feature-key': 'gagan.singh',  # Replace with actual feature key
            'api_key': 'eyJ1c2VySWQiOiJnYWdhbi5zaW5naCIsImFwaUtleSI6Ijg3ZjRiMzQ1LWExZGUtNGVmYi04MmFiLTQxZjA5YTIzMzE4MSJ9',  # Replace with your actual API key
            'Content-Type': 'application/json'
        }

        # Read document file to variable
        f = open("document.txt", "r")
        document = f.read()

        # Prepare the JSON payload for the API request
        payload = {
            "inputArgs": {
                "question": text,  # Use the Slack message as the question
                "document": document  # Replace with actual document content if necessary
            },
            "promptItems": [
                {
                    "type": "user",
                    "content": "add a newline at the end"
                }
            ]
        }

        # Call the private API to get a response
        try:
            api_response = requests.post(PRIVATE_API_URL, 
                                         headers=headers, 
                                         json=payload)

            # Debugging: Print raw API response
            print(f"Raw API response: {api_response.text}")
            print(f"API Status Code: {api_response.status_code}")
            print(f"API Headers: {api_response.headers}")
            print(f"Response Content-Type: {api_response.headers.get('Content-Type')}")

            # Ensure the response is successful (200 OK)
            if api_response.status_code == 200:
                # Check if the response is JSON
                content_type = api_response.headers.get('Content-Type', '')
                if 'application/json' in content_type:
                    response_data = api_response.json()
                    
                    # Print the full response to identify the correct field
                    print(f"Full JSON Response: {response_data}")
                    
                    # Try extracting fields based on what you see in the API response
                    # Adjust the key accordingly
                    response_message = response_data.get("generatedText")
                else:
                    # Handle non-JSON response (e.g., HTML or plain text)
                    response_message = f"API returned non-JSON content: {api_response.text}"
            else:
                response_message = f"API returned status code {api_response.status_code}: {api_response.text}"

        except requests.exceptions.RequestException as e:
            response_message = f"Error fetching data from the API: {e}"

        # Send response message to the channel
        try:
            # Add the message ID to processed before posting
            processed_messages[message_id] = current_time
            client.chat_postMessage(channel=channel_id, text=response_message)

        except SlackApiError as e:
            print(f"Error posting message: {e.response['error']}")

    return Response(status=200)

if __name__ == "__main__":
    app.run(port=3000)  # Run the Flask app on port 3000
