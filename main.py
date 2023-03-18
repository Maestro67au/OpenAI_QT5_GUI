# OpenAI QT5 GUI
# You will need an openai api key to make it work
#
import sys
import openai
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLabel, QComboBox, QLineEdit, QWidget, QInputDialog, QCheckBox
)

class OpenAIAPIWrapper:
    def __init__(self):
        self.api_key = None
        self.load_api_key()

    def load_api_key(self):
        try:
            with open("api_key.txt", "r") as file:
                self.api_key = file.read().strip()
                openai.api_key = self.api_key
        except FileNotFoundError:
            self.prompt_api_key()

    def prompt_api_key(self):
        api_key, ok = QInputDialog.getText(None, "API Key", "Enter your OpenAI API Key:")
        if ok:
            self.api_key = api_key.strip()
            openai.api_key = self.api_key
            with open("api_key.txt", "w") as file:
                file.write(self.api_key)

    def get_models(self):
        # Get the chat models from OpenAI
        response = openai.Model.list()

        self.models = openai.Model.list()
        self.chat_models = [model.id for model in self.models['data'] if 'chat' in model.id]

        return [model.id for model in response['data']]

    def send_message(self, model, message):
        # Send a user message to the selected model and receive the AI's response
        openai.api_key = self.api_key

        message = self.user_input.toPlainText().strip()
        if not message:
            return

        selected_model = self.model_selector.currentText()
        chat_mode = self.chat_mode_toggle.isChecked()

        if chat_mode:
            response = self.api_wrapper.send_chat_message(selected_model, message)
        else:
            response = self.api_wrapper.send_completion_message(selected_model, message)

        self.ai_response.append(f'User: {message}')
        self.ai_response.append(f'AI ({selected_model}): {response}')

        self.user_input.clear()
        ai_response = response.choices[0].message.content
        return ai_response.strip()

    def send_chat_message(self, model, message):
        openai.api_key = self.api_key

        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message},
            ],
        )

        ai_response = response.choices[0].message.content
        return ai_response.strip()

    def send_completion_message(self, model, message):
        openai.api_key = self.api_key

        response = openai.Completion.create(
            engine=model,
            prompt=message,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        ai_response = response.choices[0].text
        return ai_response.strip()


class ChatAppGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Chat with OpenAI')

        # Create widgets and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)

        self.ai_response_label = QLabel('AI Response:')
        top_layout.addWidget(self.ai_response_label)

        self.model_label = QLabel('Model:')
        top_layout.addWidget(self.model_label)

        self.model_selector = QComboBox()
        top_layout.addWidget(self.model_selector)

        # Add a "Clear" button in the top area
        self.clear_button = QPushButton('Clear')
        top_layout.addWidget(self.clear_button)

        self.ai_response = QTextEdit()
        self.ai_response.setReadOnly(True)
        main_layout.addWidget(self.ai_response)

        self.prompt_label = QLabel('Your Message:')
        main_layout.addWidget(self.prompt_label)

        self.user_input = QTextEdit()
        main_layout.addWidget(self.user_input)

        bottom_layout = QHBoxLayout()
        main_layout.addLayout(bottom_layout)

        self.send_button = QPushButton('Send')
        bottom_layout.addWidget(self.send_button)

        self.chat_mode_toggle = QCheckBox("Chat Mode")
        bottom_layout.addWidget(self.chat_mode_toggle)

        self.character_count_label = QLabel('Character Count: 0')
        bottom_layout.addWidget(self.character_count_label)

        # Connect signals to slots
        self.send_button.clicked.connect(self.send_message)
        self.clear_button.clicked.connect(self.clear_ai_response)  # Connect the "Clear" button to a new slot
        self.user_input.textChanged.connect(self.update_character_count)

        # Initialize API Wrapper and load models
        self.api_wrapper = OpenAIAPIWrapper()
        self.load_models()

    def load_models(self):
        # Load models into the model_selector QComboBox
        models = self.api_wrapper.get_models()
        self.chat_models = [model for model in models if 'chat' in model]
        for model in models:
            self.model_selector.addItem(model)

    def send_message(self):
        # Get user input and send it to the AI
        message = self.user_input.toPlainText().strip()
        if not message:
            return

        selected_model = self.model_selector.currentText()
        chat_mode = self.chat_mode_toggle.isChecked()

        if chat_mode:
            response = self.api_wrapper.send_chat_message(selected_model, message)
        else:
            response = self.api_wrapper.send_completion_message(selected_model, message)

        self.ai_response.append(f'User: {message}')
        self.ai_response.append(f'AI ({selected_model}): {response}')
        self.user_input.clear()

    # Add a new slot for the "Clear" button
    def clear_ai_response(self):
        self.ai_response.clear()


    def update_character_count(self):
        char_count = len(self.user_input.toPlainText())
        self.character_count_label.setText(f'Character Count: {char_count}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_app = ChatAppGUI()
    chat_app.show()
    sys.exit(app.exec_())
