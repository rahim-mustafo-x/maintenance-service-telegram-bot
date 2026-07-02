from fastapi import (FastAPI, status)
from model import TokenRequest
from database import Database
from telegram_bot import bot
from config import code_text

app = FastAPI()
db = Database()

@app.get("/")
async def root():
    print(db.get_tokens())
    return {"message": "Hello World"}

@app.post("/send_code", status_code=status.HTTP_201_CREATED)
async def send_code(data:TokenRequest):
    try:
        user = db.get_user_by_chat_phone_number(data.phone_number.removeprefix('+'))
        print(user)
        print(data.phone_number)
        if user is None:
            db.add_token(data)
        else:
            await bot.send_message(chat_id=user.chat_id, text=code_text(data.code), parse_mode='html')
            db.remove_token_data(user.phone_number)
        return {"message": "Code sent successfully"}
    except Exception as e:
        return {"message": str(e)}