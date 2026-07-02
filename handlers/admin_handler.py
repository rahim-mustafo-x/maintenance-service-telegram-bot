from aiogram import Router
from database import Database
from model import RoleOptions
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from telegram_bot import bot
from aiogram import F

router = Router()
db = Database()

@router.message(RoleOptions.AdminOption, F.text=='Yangilik haqida e\'lon berish 📢')
async def admin_handler(message: Message, state: FSMContext):
    await message.answer('Yozmoqchi bo\'lgan ma\'lumotingizni bu yerga tashlang 🗣️')
    await state.set_state(RoleOptions.BroadcastUsers)

@router.message(F.text, RoleOptions.BroadcastUsers)
async def broadcast_users(message: Message, state: FSMContext):
    for user in db.get_all_users():
        await bot.send_message(chat_id=user.chat_id, text=message.text)
    await message.answer('Xabar yuborildi ✉️')
    await state.clear()
    await state.set_state(RoleOptions.AdminOption)