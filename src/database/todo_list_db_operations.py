from .connection import db_connect

def create_todo_list_table():
    conn, cursor = db_connect()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS todo_list (
            id INTEGER PRIMARY KEY,
            task TEXT NOT NULL,
            deadline DATE,
            status TEXT,
            added_on DATE DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.close()