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
def run_diagnosis(user_issue: str) -> str:
    """
    Run a system diagnosis to find out the probable issues that the system is facing.
    :return: A message that contains the probable issues that the system is facing.
    """
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """Given a message by the user, run a system diagnosis to find out the probable issues that the system is facing.
         If the system is facing any issues, then provide a message that contains the probable issues.
         If the system is not facing any issues, then provide a message that says 'No issues found'."""),
        ("user", "Run a system diagnosis")
    ])

    output_parser = StrOutputParser()
    model_chain = prompt_template | model | output_parser

    response = model_chain.invoke({})
    probable_issues.append(json.loads(response)['Probable Issues'])
    return json.loads(response)['Probable Issues']


@tool
def show_probable_issues(input="") -> str:
    """
    Show the probable issues that the system is facing.
    :param input: Any input that the user wants to provide. This is just a placeholder.
    :return: A message that contains the probable issues that the system is facing.
    """
    if not probable_issues:
        return 'No issues found'
    return probable_issues