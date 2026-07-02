from aiogram import Router
from aiogram.types import Message, ReplyMarkupUnion
from aiogram.filters import CommandStart, CommandObject
from keyboard import (share_phone_number, clear_markup_bar, admin_options, user_options)
from database import Database
from aiogram import F
from model import User
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from model import (UserStartState, RoleOptions)
from config import (code_text, ADMINS)

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
        if message.from_user.id in ADMINS:
            await message.answer('Xush kelibsiz admin 😇', reply_markup=admin_options)
            await state.set_state(RoleOptions.AdminOption)
        else:
            await message.answer(f'Xush kelibsiz {message.from_user.full_name} 😇.\nXizmatlardan birini tanlang !!!', reply_markup=user_options)
            await state.set_state(RoleOptions.UserOption)


@router.message(F.contact, UserStartState.ClickedRegister)
async def register_user(message: Message, state: FSMContext):
    database.add_user(User(full_name=message.contact.full_name, phone_number= message.contact.phone_number, chat_id=message.from_user.id, id=None))
    await message.answer('Ro\'yhatga olindingiz 🎉', reply_markup=clear_markup_bar)
    await state.clear()

@router.message(F.contact, UserStartState.CodeAfterRegistered)
async def register_user_deep_link(message: Message, state:FSMContext):
    chat_id = message.from_user.id
    database.add_user(User(full_name=message.contact.full_name, phone_number=message.contact.phone_number,
                           chat_id=chat_id, id=None))
    await message.answer('Ro\'yhatga olindingiz 🎉')
    user = database.get_user_by_chat_id(chat_id)
    token_data = database.get_token_data_by_phone_number(user.phone_number)
    await state.clear()
    if token_data:
        if chat_id in ADMINS:
            reply_markup = admin_options
            await state.set_state(RoleOptions.AdminOption)
        else:
            reply_markup = user_options
            await state.set_state(RoleOptions.UserOption)
        await send_code(message,user.phone_number, reply_markup=reply_markup)

@router.message(F.text, StateFilter(None))
async def verify_handlers(message: Message):
    await message.answer('⚠️ Tushunarsiz narsani kiritdingiz !')


async def send_code(message:Message, phone_number:str, reply_markup:ReplyMarkupUnion | None = None):
    token_data = database.get_token_data_by_phone_number(phone_number)
    if token_data:
        await message.answer(
            code_text(token_data.code),
            parse_mode='html',
        reply_markup=reply_markup)
        database.remove_token_data(token_data.phone_number)
    else:
        await message.answer('Tasdiqlash kodi topilmadi')