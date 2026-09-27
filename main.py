import sys
from aiogram import Dispatcher
from handlers import (
    router_start,
    router_admin,
    router_user
)
from asyncio import run, gather
from uvicorn import Server, Config
from apis import app
from telegram_bot import bot
from config import (PORT, APP_NAME, EUREKA_URL)
from py_eureka_client.eureka_client import init_async, stop_async

dispatcher = Dispatcher()


async def main():
    await init_async(
        eureka_server=EUREKA_URL,
        app_name=APP_NAME,
        instance_port=PORT
    )
    config = Config(
        app=app,
        host="0.0.0.0",
        port=PORT
    )

    server = Server(config=config)

    dispatcher.include_routers(
        router_start,
        router_admin,
        router_user,
    )

    try:
        await gather(
            dispatcher.start_polling(bot),
            server.serve(),
        )
    finally:
        await stop_async()


if __name__ == "__main__":
    try:
        run(main())
    except KeyboardInterrupt:
        sys.exit(0)