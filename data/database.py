import sqlite3

def get_connection():
    return sqlite3.connect("data/miracle_7.db")  # ¶Ç´Â ':memory:' if in-memory ¿ëµµ

def init_db(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()

# 사용자 정보를 저장할 users 테이블을 생성 === 새로 추가한 코드 by Yj
def create_table():
    table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
        );
    """
    return table_query