from aiogram import Bot, Dispatcher
from handlers import (router_start, router_user)
from config import BOT_TOKEN
from asyncio import run, gather
from uvicorn import Server, Config
from routes import app

dispatcher = Dispatcher()
bot = Bot(token=BOT_TOKEN)

async def main():
    config = Config(app=app, port=8000, log_level='info')
    server = Server(config=config)
    dispatcher.include_routers(router_start, router_user)
    await gather(
        dispatcher.start_polling(bot),
        server.serve()
    )

if __name__ == '__main__':
    run(main())