import sqlite3

def get_connection():
    return sqlite3.connect("data/miracle_7.db", timeout=10)  # ¶Ç´Â ':memory:' if in-memory ¿ëµµ

def init_db(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()

# 사용자 정보를 저장할 users 테이블을 생성 === 새로 추가한 코드 by Yj
def create_user_table():
    table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        state BOOLEAN
        );
    """
    return table_query

def create_liked_table():
    return """ 
    CREATE TABLE IF NOT EXISTS bookmarks (
        username TEXT NOT NULL,
        article TEXT NOT NULL,
        direction TEXT NOT NULL,
        floor TEXT NOT NULL,
        area1 TEXT NOT NULL,
        distance TEXT NOT NULL,
        duration TEXT NOT NULL,
        confirmymd TEXT NOT NULL,
        torname TEXT NOT NULL,
        url TEXT,
        id INTEGER,
        PRIMARY KEY (username, article, direction, floor, area1, confirmymd, torname)
        );
    """