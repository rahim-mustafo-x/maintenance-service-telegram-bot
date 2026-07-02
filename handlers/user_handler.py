from aiogram import Router, F
from aiogram.types import Message
from model import RoleOptions
from config import (ADMIN_USER_NAME, here_is_admin_user_name)

router = Router()

@router.message(F.text.in_(['Admin bilan xabarlashish 💻️', F.text == 'Xato haqida habar berish ⚠️']), RoleOptions.UserOption)
async def user_option_handler(message: Message):
    text = message.text
    if text == 'Admin bilan xabarlashish 💻️':
        await message.answer(here_is_admin_user_name(ADMIN_USER_NAME))
    elif text == 'Xato haqida habar berish ⚠️':
        await message.answer(here_is_admin_user_name(ADMIN_USER_NAME))