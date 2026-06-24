from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, CommandObject
from keyboard import (share_phone_number, clear_markup_bar)
from database import Database
from aiogram import F
from model import User
from config import ADMINS
from aiogram.fsm.context import FSMContext
from model import UserStartState

router = Router()
database = Database()

@router.message(CommandStart(deep_link=True))
async def start_with_deep_link(message: Message, state: FSMContext, command: CommandObject):
    args = command.args
    if not database.get_user_by_chat_id(message.chat.id):
        markup = share_phone_number
    else:
        markup = None
        if args == 'code':
            token_data = database.get_token_data_by_phone_number(
                database.get_user_by_chat_id(message.from_user.id).phone_number)
            if token_data:
                await message.answer(f'Tasdiqlash kodi <code>{token_data.code}</code>\nUshbu kodni hech kimga bermang!',
                                     parse_mode='html')
                database.remove_token_data(token_data.phone_number)
    await state.set_state(UserStartState.StartClicked)
    await message.answer('Assalomu aleykum 👋. Ushbu bot <strong>Maintenance Service</strong>ni supporter boti', parse_mode='html', reply_markup=markup)

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    if not database.get_user_by_chat_id(message.chat.id):
        markup = share_phone_number
    else:
        markup = None
        await state.set_state(UserStartState.StartClicked)
    await message.answer('Assalomu aleykum 👋. Ushbu bot <strong>Maintenance Service</strong>ni supporter boti', parse_mode='html', reply_markup=markup)

@router.message(F.contact)
async def register_user(message: Message, state: FSMContext):
    database.add_user(User(full_name=message.contact.full_name, phone_number= message.contact.phone_number, chat_id=message.from_user.id, id=None))
    await state.set_state(UserStartState.StartClicked)
    await message.answer('Ro\'yhatga olindingiz 🎉', reply_markup=clear_markup_bar)