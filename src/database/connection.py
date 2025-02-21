import sqlite3

def db_connect():
    conn = sqlite3.connect('src/database/agents.db', autocommit=True)
    cursor = conn.cursor()
    return conn, cursor