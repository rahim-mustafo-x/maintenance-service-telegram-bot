from sqlite3 import connect
from os import makedirs
from typing import Generator

from model import (User, TokenData, TokenRequest)


class Database:
    def __init__(self):
        makedirs('db', exist_ok=True)
        self.db_path = 'db/database.db'
        self.create_tables()

    def create_tables(self):
        conn = connect(self.db_path)
        cursor = conn.cursor()

        # 1. Users Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id integer primary key autoincrement,
                full_name TEXT NOT NULL,
                phone_number TEXT UNIQUE NOT NULL,
                chat_id integer not null
            )
        """)

        # 2. Tokens Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS token_data (
                id integer primary key autoincrement,
                code TEXT NOT NULL,
                phone_number text NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    # --- TOKENS OPERATIONS ---

    # DO: Pass the dataclass directly to save it
    def add_token(self, request: TokenRequest):
        conn = connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO token_data (code, phone_number) VALUES (?, ?)',
            (request.code, request.phone_number)
        )
        conn.commit()
        conn.close()

    def get_token_data_by_phone_number(self, phone_number: str) -> TokenData | None:
        conn = connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM token_data WHERE phone_number LIKE ?',
            ('%'+phone_number+'%',)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            # Unpack the row directly into the dataclass layout
            return TokenData(*row)
        return None

    # --- USERS OPERATIONS ---

    def add_user(self, user_obj: User):
        conn = connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (full_name, phone_number, chat_id) VALUES (?, ?, ?)',
            (user_obj.full_name, user_obj.phone_number, user_obj.chat_id)
        )
        conn.commit()
        conn.close()

    def get_all_users(self) -> Generator[User, None, None]:
        conn = connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        for row in cursor:
            yield User(*row)
        conn.close()

    def get_user_by_chat_id(self, chat_id: int) -> User | None:
        conn = connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, full_name, phone_number, chat_id FROM users WHERE chat_id = ?',
        (chat_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return User(*row)
        return None
    def get_user_by_chat_phone_number(self, phone_number) -> User | None:
        conn = connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, full_name, phone_number, chat_id FROM users WHERE phone_number LIKE ?',
        ('%'+phone_number+'%',))
        row = cursor.fetchone()
        conn.close()
        if row:
            return User(*row)
        return None

    def remove_token_data(self, phone_number: str):
        conn = connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM token_data WHERE phone_number = ?', (phone_number,))
        conn.commit()
        conn.close()
    def get_tokens(self) -> list[TokenData]:
        conn = connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, code, phone_number FROM token_data')
        rows = cursor.fetchall()
        conn.close()
        return [TokenData(*row) for row in rows]