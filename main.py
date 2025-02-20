from dotenv import load_dotenv
load_dotenv()

from langchain.agents import initialize_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

from src.tools.todo_list import add_task_to_todo_list, show_all_tasks_in_todo_list
from src.models.azure_model import model


tools = [add_task_to_todo_list, show_all_tasks_in_todo_list]
memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=10,
    return_messages=True
)

conversational_agent = initialize_agent(
    agent='chat-conversational-react-description',  # Changed agent type
    tools=tools,
    llm=model,
    memory=memory,
    max_iterations=3,
    verbose=True,
    early_stopping_method='generate'
)

conversational_agent("Add a task to buy the groceries")
conversational_agent("Make sure I dont forget to pay my electricity bill on 10th")
conversational_agent("Remind me to call the doctor tomorrow")
conversational_agent("Show me all my tasks")