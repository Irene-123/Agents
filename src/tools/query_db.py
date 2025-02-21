from langchain.agents import tool

from src.database.connection import db_connect
from src.models.azure_model import model

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
    conn, cursor = db_connect()
    if parameters:
        cursor.execute(query, parameters)
    else:
        cursor.execute(query)
    conn.commit()
    conn.close()