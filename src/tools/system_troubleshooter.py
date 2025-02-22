import os
import json
import subprocess
from datetime import datetime
from src.models.azure_model import model

from langchain.agents import tool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

probable_issues = []

@tool
def run_diagnosis(input_text: str) -> str:
    """
    Run a system diagnosis to find out the probable issues that the system is facing.
    :return: A message that contains the probable issues that the system is facing.
    """
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """Given a message by the user. For example, find why my Wi-Fi is not working, or why my restart is stuck. I want you to write
        a bash script that can diagnose the issue, the script may contain set of commands or a single command. Please write script completing in a span of 15 seconds.
        The script need not be included with any filters for specific information, it's okay if there's some information than required. Give the output as a JSON object with the key 'command'
        Do not add json label at the beginning of the response. Don't add any comments in json files"""),
        ("user", "{input_text}")
    ])
    output_parser = StrOutputParser()
    model_chain = prompt_template | model | output_parser

    num_of_retries = 5
    commands_tried = ""

    for i in range(num_of_retries):
        response = model_chain.invoke({"input_text": input_text + "\n\n" + commands_tried})
        print(response)
        command = json.loads(response)['command']
        process = subprocess.Popen(["bash", "-c", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            commands_tried += f"I already tried running this command - \n{command}\nI got the following error: {stderr.decode('utf-8')}\n\n"
        else:
            break

    bash_response = stdout.decode('utf-8')
    print(bash_response)

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """You are a system troubleshooter who has been tasked to respond to user issues about their PC.
         Given the request made by the user, and the response received from the bash script to answer that query,
         Analyze the response and provide the user with the information requested.
         Give the output as a JSON object with the key 'response'. Do not add json label at the beginning of the response. 
        """),
        ("user", "User request: {request}\nBash script response: {script_response}")
    ])
    model_chain = prompt_template | model | output_parser
    user_response = model_chain.invoke({"request": input_text, "script_response": bash_response})
    print(user_response)
    return json.loads(user_response)['response']


@tool
def execute_troubleshooting(input_text: str) -> str:
    """
    Execute the troubleshooting script and return the output.
    :return: The output of the troubleshooting script.
    """
    pass
