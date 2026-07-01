from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, CommandObject
from keyboard import (share_phone_number, clear_markup_bar)
from database import Database
from aiogram import F
from model import User
from aiogram.fsm.context import FSMContext
from model import UserStartState

router = Router()
database = Database()

@router.message(CommandStart(deep_link=True))
async def start_with_deep_link(message: Message, state: FSMContext, command: CommandObject):
    args = command.args
    if args == 'code':
        if not database.get_user_by_chat_id(message.chat.id):
            await message.answer('Assalomu aleykum 👋. Ushbu bot <strong>Maintenance Service</strong>ni supporter boti',
                                 parse_mode='html', reply_markup=share_phone_number)
            await state.set_state(UserStartState.CodeAfterRegistered)
        else:
            user = database.get_user_by_chat_id(message.chat.id)
            await send_code(message, user.phone_number)


@router.message(CommandStart())
async def start_handler(message: Message, state:FSMContext):
    if not database.get_user_by_chat_id(message.chat.id):
        await message.answer('Assalomu aleykum 👋. Ushbu bot <strong>Maintenance Service</strong>ni supporter boti',
                             parse_mode='html', reply_markup=share_phone_number)
        await state.set_state(UserStartState.ClickedRegister)
    else:
        await state.set_state(UserStartState.StartClicked)

@router.message(F.contact, UserStartState.ClickedRegister)
async def register_user(message: Message, state: FSMContext):
    database.add_user(User(full_name=message.contact.full_name, phone_number= message.contact.phone_number, chat_id=message.from_user.id, id=None))
    await message.answer('Ro\'yhatga olindingiz 🎉', reply_markup=clear_markup_bar)
    await state.set_state(UserStartState.StartClicked)
    print(await state.get_state())

@router.message(F.contact, UserStartState.CodeAfterRegistered)
async def code_after(message: Message, state: FSMContext):
    database.add_user(User(full_name=message.contact.full_name, phone_number=message.contact.phone_number,
                           chat_id=message.from_user.id, id=None))
    await message.answer('Ro\'yhatga olindingiz 🎉', reply_markup=clear_markup_bar)
    user = database.get_user_by_chat_id(message.chat.id)
    token_data = database.get_token_data_by_phone_number(user.phone_number)
    if token_data:
        await send_code(message,user.phone_number)
        await state.set_state(UserStartState.StartClicked)



async def send_code(message:Message, phone_number:str):
    token_data = database.get_token_data_by_phone_number(phone_number)
    if token_data:
        await message.answer(
            f'Tasdiqlash kodi <code>{token_data.code}</code>\nUshbu kodni hech kimga bermang!',
            parse_mode='html')
        database.remove_token_data(token_data.phone_number)
    else:
        await message.answer('Tasdiqlash kodi topilmadi')