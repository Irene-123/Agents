# Conversational Agent Project

This project implements a conversational agent using LangChain, Azure AI, and speech recognition capabilities. The agent can add tasks to a to-do list, show all tasks, query a database, and respond to user inputs about PC settings.

## Project Structure

```
/d:/PersonalProjects/Agents
│
├── main.py
├── requirements.txt
├── .gitignore
├── src
│   ├── tools
│   │   ├── todo_list.py
│   │   ├── query_db.py
│   │   └── talk_to_your_pc.py
│   ├── models
│   │   └── azure_model.py
│   ├── database
│   │   ├── db_prompt.py
│   │   └── connection.py
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
    - The agent listens for user input through the microphone or text input.
    - You can add tasks to the to-do list, ask the agent to show all tasks, query the database, or get information about PC settings.

## Functionalities

1. **Add Task to To-Do List:**
    - Adds a task to the user's to-do list with an optional deadline.
    - Example prompts: 
        - "Add a task to buy the groceries"
        - "Remind me to go to the doctor tomorrow"

2. **Show All Tasks in To-Do List:**
    - Displays all tasks currently in the user's to-do list.
    - Example prompts:
        - "Show me all my tasks"
        - "What are the tasks that I have in my to-do list?"

3. **Query Database:**
    - Executes SQL queries on the database based on user input.
    - Example prompts:
        - "Get all tasks with a deadline of today"
        - "Show all completed tasks"

4. **Get PC Settings:**
    - Provides information about the PC settings and installed software.
    - Example prompts:
        - "What is the current volume of my PC?"
        - "What are available wifi networks right now?"

## Tools and Libraries Used

- **LangChain:** For building the conversational agent.
- **Azure AI:** For language model integration.
- **SpeechRecognition:** For capturing user input through the microphone.
- **pyttsx3:** For text-to-speech capabilities.