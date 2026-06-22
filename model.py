from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: Optional[int]
    full_name: str
    phone_number: str
    chat_id: int

    def __init__(self, full_name: str, phone_number: str, chat_id: int):
        self.full_name = full_name
        self.phone_number = phone_number
        self.chat_id = chat_id

@dataclass
class TokenData:
    id: Optional[int]  # Optional because new tokens don't have an ID yet
    pending_token: str
    otp_code: str
    token: str
    def __init__(self, pending_token: str, otp_code: str, token: str):
        self.pending_token = pending_token
        self.otp_code = otp_code
        self.token = token
