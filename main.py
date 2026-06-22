from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from routes import app
from config import BOT_TOKEN
from asyncio import run, gather
from uvicorn import Server, Config

dispatcher = Dispatcher()
bot = Bot(token=BOT_TOKEN)

@dispatcher.message(CommandStart())
async def start(message: types.Message):
    await message.answer('Hi')

async def main():
    config = Config(app=app, port=8000, log_level='info')
    server = Server(config=config)
    await gather(
        dispatcher.start_polling(bot),
        server.serve()
    )

if __name__ == '__main__':
    run(main())