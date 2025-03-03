import config
import asyncio
from os import system
from handlers import router
from datetime import datetime
from funcs import update_data
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.enums.parse_mode import ParseMode
from funcs import process_file, format_arbitrages
from callbacks.callback_handlers import callback_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from data.db import get_autoupdate_users, add_arbitrage_message, clear_arbitrage_message



system("cls")

bot = Bot(
    token=config.TOKEN
)

async def set_bot_commands():
    await bot.set_my_commands(
        commands=[
            BotCommand(
                command="/start",
                description="🏠  Главное сообщение"
            ),
            BotCommand(
                command="/autoupdate",
                description="🔄  Переключает автообновление связок"
            ),
            BotCommand(
                command="/links",
                description="🔎  Найти связки"
            ),
            BotCommand(
                command="/subnews",
                description="📢  подписаться на рассылку"
            ),
            BotCommand(
                command="/devlog",
                description="📄  Последние обновления"
            )
        ]
    )


async def chats_autoupdate():  # sourcery skip: for-index-underscore, use-named-expression    
    users = get_autoupdate_users()
    for user in users:
        if user[4] == '':
            continue
        try:
            for msg_id in user[4].split('|'):
                await bot.delete_message(chat_id=user[1], message_id=int(msg_id))
        except Exception:
            continue
        clear_arbitrage_message(tgid=user[1])

    file = process_file()
    arbitrages = format_arbitrages(file)
    for user in users:
        messages = []
        for arbitrage_link in arbitrages:
            msg = await bot.send_message(chat_id=user[1], text=arbitrage_link, disable_web_page_preview=True, parse_mode=ParseMode.HTML)
            messages.append(msg.message_id)
        add_arbitrage_message(user[1], messages)


dispatcher = Dispatcher()
dispatcher.include_router(router)
dispatcher.include_router(callback_router)
dispatcher.startup.register(set_bot_commands)
scheduler = AsyncIOScheduler()


async def main():
    start_time = datetime.now()
    # update_data()
    scheduler.add_job(
        func=update_data,
        trigger='interval',
        seconds=60*2
    )
    scheduler.add_job(
        func=chats_autoupdate,
        trigger='interval',
        seconds=60*5
    )
    scheduler.start()
    await bot.get_updates(offset=-1)
    await dispatcher.start_polling(bot)
    


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        exit()