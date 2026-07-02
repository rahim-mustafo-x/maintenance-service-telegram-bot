from aiogram import Dispatcher
from handlers import (router_start, router_admin, router_user)
from asyncio import run, gather
from uvicorn import Server, Config
from routes import app
from telegram_bot import bot

dispatcher = Dispatcher()

async def main():
    config = Config(app=app, port=8000, log_level='info')
    server = Server(config=config)
    dispatcher.include_routers(router_start, router_admin, router_user)
    await gather(
        dispatcher.start_polling(bot),
        server.serve()
    )

if __name__ == '__main__':
    run(main())