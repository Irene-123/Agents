from langchain_core.prompts import ChatPromptTemplate

DATABASE_CONTEXT = """
    The database schema is as follows:
    Table: todo_list
    Columns:
    - id: INTEGER PRIMARY KEY
    - task: TEXT NOT NULL
    - deadline: DATE
    - status: TEXT  -- Can be 'Pending', 'Completed', 'Delayed'
    - added_on: DATE DEFAULT CURRENT_TIMESTAMP
"""

DATABASE_QUERY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", f"""You are a data engineer. You have been tasked to write sqlite queries for the
        tasks user asks you to do. 

        {DATABASE_CONTEXT}
     
        You have to give back the response in JSON format with 'Query' as the key.
        Do not add json label at the beginning of the response.
        """),
    ("user", "Write a sqlite query for - {input_text}")
])

DATABASE_VERIFICATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", f"""You are a senior data engineer. You have been tasked to
        verify the sqlite queries written by the junior data engineer.
        You have to verify if the queries are written correctly to be executed on
        the sqlite3 database.
     
        {DATABASE_CONTEXT}

        Give the response in JSON format with 'Verification' as the key, and 0 or 1 for correct or wrong as the value.
        Do not add json label at the beginning of the response.
     """),
     ("user", "Verify the sqlite query - {input_text}")
])