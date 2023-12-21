# database.py
import sqlite3

class Database:
    def __init__(self, db_name='bets.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                expiration_date DATETIME,
                yes_user_id TEXT,
                no_user_id TEXT,
                value INTEGER,
                cancel_requested TEXT
            )
        ''')
        self.conn.commit()
