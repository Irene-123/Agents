import json

from langchain.agents import tool
from langchain_core.output_parsers import StrOutputParser

from src.database.connection import db_connect
from src.models.azure_model import model
from src.database.db_prompt import DATABASE_QUERY_PROMPT, DATABASE_VERIFICATION_PROMPT

@tool
def get_results_from_database(request: str) -> str:
    """
    Gets the result from the database. Based on the user input,
    this tool can run query on the database to fetch the required results.
    :param request: The request that the user wants to make to the database.
    :return: The result that is fetched from the database.

    Some sample tasks that can be achieved with this tool -
    1. Fetch all todo list tasks from the database
    2. Get all the details of the user with the name 'John'
    """
    output_parser = StrOutputParser()
    query_model_chain = DATABASE_QUERY_PROMPT | model | output_parser
    verification_model_chain = DATABASE_VERIFICATION_PROMPT | model | output_parser
    
    query_response = query_model_chain.invoke({"input_text": request})
    query_json = json.loads(query_response)
    verification_response = verification_model_chain.invoke({"input_text": query_json["Query"]})
    verification_json = json.loads(verification_response)

    conn, cursor = db_connect()
    cursor.execute(query_json["Query"])
    result = cursor.fetchall()
    conn.close()

    response = f"""
        Query: {query_json['Query']}
        Verification status: {"Verified" if verification_json['Verification'] == 1 else "Failure"}
        Results :
        {result}
    """
    return response