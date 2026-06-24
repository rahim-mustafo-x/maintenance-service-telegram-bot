from aiogram.types import Message
from aiogram import Router
from database import Database
from model import UserStartState
from config import ADMINS

router = Router()
database = Database()

@router.message(UserStartState.StartClicked)
async def user_started(message: Message):
    if message.from_user.id in ADMINS:
        await message.answer('Xush kelibsiz admin 😇')
    else:
        await message.answer(f'Xush kelibsiz {message.from_user.full_name} 😇.\nXizmatlardan birini tanlang !!!')