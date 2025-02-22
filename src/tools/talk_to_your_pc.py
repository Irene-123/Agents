import json
import subprocess

from langchain.agents import tool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from src.models.azure_model import model

@tool
def get_pc_settings(input_text: str) -> str:
    """
    This tool can be used when the user wants to know something about the settings of his PC.
    This included everything related to softwares installed in the PC like volume, brightness, wifi networks, etc.
    :param input_text: The attribute that the user wants to know about his PC.
    :return: A message that informs the user about the setting of his PC.

    Some sample prompts that should work with this tool:
    - What is the current volume of my PC?
    - What are available wifi networks right now?
    - Which wifi am I connected to right now?
    - What is my battery percentage?
    """
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """You are a system analyst who has been tasked of writing powershell scripts that can extract
            the information requested by the user. These scripts will run on windows machines. Your script should be
            able to extract the information about the settings of the PC, as well as softwares installed in the PC.
            Given a message by the user, write the required script. Script should have the required details in the output,
            You dont need to apply filters just to extract the required information, its fine if the script gives more 
            information than required. Give the output as a JSON object with the key 'command'
            Do not add json label at the beginning of the response.
        """),
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
        
        # Execute the PowerShell script and capture the output
        process = subprocess.Popen(["powershell", "-Command", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            commands_tried += f"I already tried running this command - \n{command}\nI got the following error: {stderr.decode('utf-8')}\n\n"
        else:
            break

    powershell_response = stdout.decode('utf-8')
    print(powershell_response)

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """You are a system analyst who has been tasked to respond to user queries about their PC.
         Given the request made by the user, and the response received from the powershell script to answer that query,
         Analyze the response and provide the user with the information requested.
         Give the output as a JSON object with the key 'response'. Do not add json label at the beginning of the response. 
        """),
        ("user", "User request: {request}\nPowershell script response: {script_response}")
    ])
    model_chain = prompt_template | model | output_parser
    user_response = model_chain.invoke({"request": input_text, "script_response": powershell_response})
    print(user_response)
    return json.loads(user_response)['response']