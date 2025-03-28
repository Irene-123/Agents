import os
import sys
import json
import time
import subprocess
from datetime import datetime
sys.path.append(os.getcwd())
from src.models.azure_model import model
from static.risky_keywords import RISKY_KEYWORDS
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

def execute(command):
    process = subprocess.Popen(["bash", "-c", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    commands_tried = ""
    if process.returncode != 0:
        commands_tried += f"I already tried running this command - \n{command}\nI got the following error: {stderr.decode('utf-8')}\n\n"
        return commands_tried

    bash_response = stdout.decode('utf-8')
    return bash_response

@tool
def execute_troubleshooting(input_text: str) -> str:
    """
    Execute the troubleshooting script and return the output.
    If a command contains risky keywords, prompt the user for confirmation before executing.
    :return: The output of the troubleshooting script.
    ASK TO EXECUTE AT YOUR OWN RISK
    Execute the troubleshooting script and return the output.
    :return: The output of the troubleshooting script.

    Examples:
    1. Delete temp files, clear cache
    2. Reset adapter, flush DNS, renew IP
    3. Run system repair commands
    4. Check for updates & install
    5. Identify & restart problematic process
    6. Reconfigure Firewall Settings
    7. update drivers
    8. Optimize system performance
    9. Enable/disable process or services
    10. Run Disk cleanup
    11. Change Power configuration
    12. Renew IP
    13. Restore deleted files
    """
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """Given a troubleshooting task described by the user, write a bash script to execute the task. 
        The script may include a series of commands or a single command to perform the action. 
        Ensure the script completes within 15 seconds. Provide the output as a JSON object with the key 'command'.
        Do not add json label at the beginning of the response. Don't include comments in the JSON."""),
        ("user", "{input_text}")
    ])
    output_parser = StrOutputParser()
    model_chain = prompt_template | model | output_parser
    stdout = b""
    stderr = b""
    bash_response = ""


    response = model_chain.invoke({"input_text": input_text})
    print(response)
    command = json.loads(response)['command']

    # Check for risky keywords in the command
    risky_found = [keyword for keyword in RISKY_KEYWORDS if keyword in command]
    if risky_found:
        print(f"Warning: The following command contains risky keywords: {', '.join(risky_found)}")
        for keyword in risky_found:
            print(f"- {keyword}: {RISKY_KEYWORDS[keyword]}")
        user_input = input("Do you want to proceed with this command? (yes/no): ").strip().lower()
        if user_input != "yes":
            print("Skipping this command.")
            bash_response = "User chose not to execute/abort the command due to risky keywords/unkown reason"
        else:
            print("Executing the command in 5 secs...\n{command}\nINTERRUPT TO STOP")
            for i in range(5, 0, -1):
                print(i, end=" ", flush=True)
                time.sleep(1)
                bash_response = execute(command)
            print(bash_response)
    else:
        print("Here, Executing the command in 5 secs...\n{command}\nINTERRUPT TO STOP")
        for i in range(5, 0, -1):
            print(i, end=" ", flush=True)
            time.sleep(1)
        bash_response = execute(command)
        print(bash_response)

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """You are a system troubleshooter tasked with executing user-requested troubleshooting tasks. 
        Based on the user's request and the bash script's response, provide a summary of the action taken and its result. 
        Give the output as a JSON object with the key 'response'. Do not add json label at the beginning of the response."""),
        ("user", "User request: {request}\nBash script response: {script_response}")
    ])
    model_chain = prompt_template | model | output_parser
    user_response = model_chain.invoke({"request": input_text, "script_response": bash_response})
    print(user_response)
    return json.loads(user_response)['response']


 