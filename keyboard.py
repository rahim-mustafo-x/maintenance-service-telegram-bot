from aiogram.utils.keyboard import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton, ReplyKeyboardRemove

share_phone_number = ReplyKeyboardMarkup(
    keyboard=[
     [KeyboardButton(text='Telefon raqamini berish 📱', request_contact=True)]
    ],
    resize_keyboard=True, one_time_keyboard=True
)

user_options = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Admin bilan xabarlashish 💻️'), KeyboardButton(text='Xato haqida habar berish ⚠️')]
    ],
    resize_keyboard=True, one_time_keyboard=True
)
admin_options = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Yangilik haqida e\'lon berish 📢')]
    ],
    resize_keyboard=True, one_time_keyboard=True
)

clear_markup_bar = ReplyKeyboardRemove()