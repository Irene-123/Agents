import json
from datetime import datetime

from langchain.agents import tool

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from src.models.azure_model import model

user_todo_list = []

@tool
def add_task_to_todo_list(task_with_deadline: str) -> str:
    """
    Adds the task to the todo list.
    :param task: The task that user wants to add to his todo list, it may or may not come with deadline. 
    If the deadline is not given by the user, then it should be set to today by default.
    :return: A message that confirms that the task has been added to the todo list

    Some sample prompts that should work with this tool:
    - Add a task to buy the groceries
    - Remind me to go to the doctor tomorrow
    - Make sure I dont forget to pay the SIP on 16th
    - I need to review the documents, can you remind me?
    """
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """Given a message by the user, extract a task and its deadline that should be 
         added to the todo list. If the deadline cannot be found, then extract it as 'Not Present'.
         Today's date is {date}. 
         If the deadline is present, convert it to date string in the format '%Y-%m-%d'.
         If deadline only has date, then set it to the nearest date in the future that matches it.
         If deadline only has a month, set it to the last day of that month.
         Give output as a JSON object with keys 'Task' and 'Deadline'."""),
        ("user", "{input_text}")
    ])

    output_parser = StrOutputParser()
    model_chain = prompt_template | model | output_parser

    response = model_chain.invoke({"input_text": task_with_deadline, "date": datetime.today().date()})
    print(response)
    task, deadline = json.loads(response)['Task'], json.loads(response)['Deadline']
    if deadline == 'Not Present':
        deadline = datetime.today().date()
    else:
        deadline = datetime.strptime(deadline, '%Y-%m-%d').date()

    user_todo_list.append({"task": task, "deadline": deadline, "added_on": datetime.today().date()})
    print(user_todo_list)
    return f'I will make sure to remind you about {task}'

@tool
def show_all_tasks_in_todo_list(input="") -> str:
    """
    Show all the tasks that are currently in the todo list of the user.
    :param input: Any input that the user wants to provide. This is just a placeholder.
    :return: A message that contains all the tasks that are in the todo list.

    Some sample prompts that should work with this tool:
    - Show me all my tasks
    - What are the tasks that I have in my todo list?
    - Can you show me my todo list?
    """
    response = "You have the following tasks in your todo list: \n"
    for task in user_todo_list:
        response += f"{task['task']}, {task['deadline']}, was added on {task['added_on']}\n"
    return response