import config
import asyncio
from aiogram import Bot
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums.parse_mode import ParseMode
from callbacks.StartCallback import StartCallbackClass
from data.db import get_user, add_user, switch_autoupdate
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from funcs import userExist, addUser, process_file, format_arbitrages



router = Router()



@router.message(Command('start'))
async def start(message: Message, bot: Bot):
    try:
        add_user(message.from_user.id)
        print(f"new user: {message.from_user.id}")
    except ValueError:
        pass
    
    await bot.delete_message(
        chat_id=message.chat.id, 
        message_id=message.message_id
    )

    if not userExist(message.from_user.id):
        addUser(
            message.from_user.username, 
            message.from_user.id, 
            message.from_user.full_name
        )
    
    start_keyboaard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Найти связки! 🚀",
                    callback_data=StartCallbackClass(option="search", answer_id=message.from_user.id).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text="Подписаться на новости 💬",
                    callback_data=StartCallbackClass(option="subscribe", answer_id=message.from_user.id).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text="Поддержка 🚨", 
                    callback_data=StartCallbackClass(option="contacts", answer_id=message.from_user.id).pack()
                )
            ]
        ]
    )
    await message.answer(
        text=f"Добро пожаловать в наш бот 🔥\n{config.INFO}", 
        reply_markup=start_keyboaard,
        parse_mode=ParseMode.HTML
    )



@router.message(Command('contacts'))
async def contacts(message: Message, bot: Bot):
    await bot.delete_message(
        chat_id=message.chat.id, 
        message_id=message.message_id
    )
    await message.answer(text=config.CONTACTS_INFO, parse_mode=ParseMode.HTML)



@router.message(Command("links"))
async def links(message: Message, bot: Bot):
    await bot.delete_message(
        chat_id=message.chat.id, 
        message_id=message.message_id
    )
    
    arb_list = format_arbitrages(process_file())
    for text in arb_list:
        await bot.send_message(
            chat_id=message.from_user.id, 
            text=text, 
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML
        )



@router.message(Command("devlog"))
async def devlog(message: Message):
    await message.answer(
        text=config.DEVLOG,
        parse_mode=ParseMode.HTML
    )



@router.message(Command("autoupdate"))
async def autoupdate(message: Message):
    user = get_user(message.from_user.id)
    switch_autoupdate(user["tgid"])
    if user["autoupdate"] == 0:
        await message.answer(text="✅  Вы включили автообновление связок!\n🔄  Сообщения будут обновляться автоматически каждые 10 минут!")
    else:
        await message.answer(text="🔴  Вы выключили автообновление связок!\nАвтообновление остановлено!")




@router.message(Command("ogre"))
async def ogre(message: Message):
    await message.answer("🧌")
    


@router.message()
async def message(message: Message, bot: Bot):
    await bot.delete_message(
        chat_id=message.chat.id, 
        message_id=message.message_id
    )
    msg = await message.answer(text=config.COMMAND_ERROR_MESSAGE, parse_mode=ParseMode.HTML)
    await asyncio.sleep(2)
    await bot.delete_message(message.chat.id, msg.message_id)