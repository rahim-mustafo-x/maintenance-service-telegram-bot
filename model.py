from dataclasses import dataclass
from typing import Optional
from aiogram.fsm.state import (State, StatesGroup)

@dataclass
class User:
    id: Optional[int]
    full_name: str
    phone_number: str
    chat_id: int

@dataclass
class TokenData:
    id: Optional[int]  # Optional because new tokens don't have an ID yet
    code: str
    phone_number: str #to recognize with

@dataclass
class TokenRequest:
    code: str
    phone_number: str #to recognize with

class UserStartState(StatesGroup):
    ClickedRegister = State()
    CodeAfterRegistered = State()
class RoleOptions(StatesGroup):
    #user
    UserOption = State()
    #admin
    AdminOption = State()
    BroadcastUsers = State()