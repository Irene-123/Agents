import os
from dotenv import load_dotenv

from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from langchain.agents import initialize_agent, tool
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

load_dotenv()

todo_list = []

@tool
def add_task_to_todo_list(task: str) -> str:
    """Adds the task to the todo list."""
    todo_list.append(task)
    return f'Task {task} added to your todo list.'

@tool
def show_all_tasks_in_todo_list(input="") -> str:
    """Shows all the tasks that user have in his todo list"""
    return f"You have following tasks in your todo list: \n ".join(f"{task}\n" for task in todo_list)


model = AzureAIChatCompletionsModel(
    endpoint=os.getenv("AZURE_INFERENCE_ENDPOINT"),
    credential=os.getenv("AZURE_INFERENCE_CREDENTIAL"),
    model_name="gpt-4o-mini"
)

tools = [add_task_to_todo_list, show_all_tasks_in_todo_list]
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

conversational_agent("Add a task to buy the groceries")
conversational_agent("Add a task to pay the bills")
print(todo_list)
conversational_agent("Remind me to call the doctor tomorrow")
conversational_agent("Show me all my tasks")