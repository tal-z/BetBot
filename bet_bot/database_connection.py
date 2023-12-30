# database.py
import sqlite3


class DatabaseConnection:
    def __init__(self, db_name='bets.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                predicate TEXT,
                expiration_date DATETIME,
                challenging_user_id TEXT,
                challenged_user_id TEXT,
                value TEXT,
                challenge_accepted BOOLEAN,
                cancel_requested TEXT
            )
        ''')
        self.conn.commit()
