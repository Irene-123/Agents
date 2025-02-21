# Conversational Agent Project

This project implements a conversational agent using LangChain, Azure AI, and speech recognition capabilities. The agent can add tasks to a to-do list, show all tasks, and respond to user inputs.

## Project Structure

```
/d:/PersonalProjects/Agents
│
├── main.py
├── requirements.txt
├── .gitignore
├── src
│   ├── tools
│   │   └── todo_list.py
│   ├── models
│   │   └── azure_model.py
│   └── speech_capability.py
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
    ```sh
    git clone <repository_url>
    cd Agents
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv agents_env
    source agents_env/bin/activate  # On Windows use `agents_env\Scripts\activate`
    ```

3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    Create a `.env` file in the root directory and add the following variables:
    ```
    AZURE_INFERENCE_ENDPOINT=<your_azure_inference_endpoint>
    AZURE_INFERENCE_CREDENTIAL=<your_azure_inference_credential>
    ```

## Usage

1. **Run the main script:**
    ```sh
    python main.py
    ```

2. **Interact with the agent:**
    - The agent listens for user input through the microphone.
    - You can add tasks to the to-do list or ask the agent to show all tasks.

## Tools and Libraries Used

- **LangChain:** For building the conversational agent.
- **Azure AI:** For language model integration.
- **SpeechRecognition:** For capturing user input through the microphone.
- **pyttsx3:** For text-to-speech capabilities.