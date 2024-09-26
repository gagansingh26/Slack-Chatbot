**GitHub README Update: Testing the Slack Chatbot GenAssist**

To test the Slack Chatbot GenAssist, ensure Python 3 is installed on your system.

### Steps to Run:

1. **Run the script**: 
   In a terminal (e.g., Visual Studio Code), execute the following command to start the bot:
   ```bash
   python3 slack_bot.py
   ```

2. **Set up ngrok**:  
   In a separate terminal, use ngrok to expose the application locally by running:
   ```bash
   ngrok http --url=polite-donkey-truly.ngrok-free.app 3000
   ```
   (ngrok allows local testing, and port 3000 is specified in the script.)

3. **Test the chatbot**:  
   Once both the bot and ngrok are running, you can interact with the Slack chatbot using GenAI prompts.

