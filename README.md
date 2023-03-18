# OpenAI_QT5_GUI
A QT5 GUI for accessing the various models available at OpenAI. This program is a quick and effective way to get into using the APIs to query the models


Program Specifications:
1. The program will create a GUI application for chatting with OpenAI models using the OpenAI API.
2. The program will initialize an OpenAIAPIWrapper class to handle loading the OpenAI API key and fetching the available models.
3. The program will load the fetched models into a QComboBox widget in the GUI.
4. Users can input their message into a QTextEdit widget and select the model they want to use for the AI response from the QComboBox.
5. On selecting the model and input of message, the program will call the send_message method of the OpenAIAPIWrapper class to send the user message to the selected AI model and receive the AI's response.
6. The program will update the GUI to display both the user message and the AI response in the AI Response QTextEdit widget.
7. The program will have an option for chat mode or completion mode.
8. The program will have a clear button to clear the AI Response QTextEdit widget.
