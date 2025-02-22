from dotenv import load_dotenv
load_dotenv()

from langchain.agents import initialize_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

from src.tools.todo_list import add_task_to_todo_list, show_all_tasks_in_todo_list
from src.tools.query_db import get_results_from_database
from src.tools.talk_to_your_pc import get_pc_settings
from src.tools.system_troubleshooter import run_diagnosis
from src.models.azure_model import model
from src.speech_capability import speak_message, get_user_input


tools = [add_task_to_todo_list, show_all_tasks_in_todo_list, get_results_from_database, get_pc_settings, run_diagnosis]
memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=10,
    return_messages=True
)

conversational_agent = initialize_agent(
    agent='chat-conversational-react-description',
    tools=tools,
    llm=model,
    memory=memory,
    max_iterations=3,
    verbose=True,
    early_stopping_method='generate'
)

if __name__ == '__main__':
    # Use this code for text input
    while True:
        print("Enter your message: ")
        user_input = input()
        if user_input != "":
            response = conversational_agent.invoke(user_input, return_only_outputs=True)
            print("BOT: ", response['output'])

    # Use this code for microphone input
    while True:
        user_input = get_user_input().lstrip()
        if user_input != "":
            print("HUMAN: ", user_input)
            response = conversational_agent.invoke(user_input, return_only_outputs=True)
            print("BOT: ", response['output'])
            speak_message(response['output'])