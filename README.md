# Slack Chatbot: Hackathon Project

This Slack chatbot was developed as part of a **hackathon project** to leverage an AI model for reading documents and answering questions. It is particularly designed to assist with **customer support queries** by skimming a provided document and rephrasing answers to user questions.

While this was built during a time-limited hackathon, the chatbot provides a functional prototype for customer support automation. Due to the nature of API responses, there might be occasional errors or incorrect answers, which can be improved in future iterations.

---

## **Features**
- Reads a given document (e.g., `document.text`) to extract and rephrase answers.
- Integrates with Slack, allowing users to interact with the bot directly.
- Designed for customer support scenarios where quick responses are required.

---

## **Steps to Test the Chatbot**

### 1. **Prerequisites**
- Ensure **Python 3** is installed on your system.
- Create a Slack Chatbot using the Slack API and obtain the required bot credentials (e.g., Bot Token, Signing Secret).
- Add the bot to a Slack workspace where it can interact with users.

### 2. **Run the Script**
In a terminal (e.g., Visual Studio Code), execute the following command to start the bot:

```bash
python3 slack_bot.py
```

### 3. **Set Up ngrok**
Use ngrok to expose the bot locally for Slack's event subscription. In a separate terminal, run:

```bash
ngrok http --url=polite-donkey-truly.ngrok-free.app 3000
```

- Replace `polite-donkey-truly.ngrok-free.app` with your own ngrok URL.
- Ensure port `3000` matches the one specified in the `slack_bot.py` script.

### 4. **Test the Chatbot**
- Once both the bot and ngrok are running, you can interact with the Slack chatbot using natural language queries.
- The bot will skim the `document.text` file, process the query using the AI model, and respond within Slack.

---

## **Limitations**
- The bot's accuracy depends on the AI model and the quality of the document provided.
- As this was a hackathon project, error handling and advanced features may need refinement.
