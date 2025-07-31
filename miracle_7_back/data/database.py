import sqlite3

def get_connection():
    return sqlite3.connect("data/miracle_7.db")  # 또는 ':memory:' if in-memory 용도

def init_db(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()
