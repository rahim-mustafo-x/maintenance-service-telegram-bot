from sqlite3 import connect
from os import makedirs
# Import your dataclasses
from model import (User, TokenData)


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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                phone_number TEXT UNIQUE NOT NULL,
                chat_id INTEGER NOT NULL
            )
        """)

        # 2. Tokens Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pending_token TEXT NOT NULL,
                otp_code TEXT NOT NULL,
                token TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    # --- TOKENS OPERATIONS ---

    # DO: Pass the dataclass directly to save it
    def add_token(self, token_obj: TokenData):
        conn = connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tokens (pending_token, otp_code, token) VALUES (?, ?, ?)",
            (token_obj.pending_token, token_obj.otp_code, token_obj.token)
        )
        conn.commit()
        conn.close()

    # GET: Returns a clean TokenData object instead of a tuple
    def get_token_by_pending(self, pending_str: str) -> TokenData | None:
        conn = connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, pending_token, otp_code, token FROM tokens WHERE pending_token = ?",
            (pending_str,)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            # Unpack the row directly into the dataclass layout
            return TokenData(id=row[0], pending_token=row[1], otp_code=row[2], token=row[3])
        return None

    # --- USERS OPERATIONS ---

    def add_user(self, user_obj: User):
        conn = connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (full_name, phone_number, chat_id) VALUES (?, ?, ?)",
            (user_obj.full_name, user_obj.phone_number, user_obj.chat_id)
        )
        conn.commit()
        conn.close()

    def get_user(self, chat_id: int) -> User | None:
        conn = connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name, phone_number, chat_id FROM users WHERE chat_id = ?", (chat_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return User(id=row[0], full_name=row[1], phone_number=row[2], chat_id=row[3])
        return None

    def get_all_users(self) -> list[int]:
        conn = connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT chat_id FROM users")
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]
