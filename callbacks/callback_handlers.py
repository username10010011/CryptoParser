import config
from aiogram import Bot
from aiogram import Router
from callbacks.StartCallback import StartCallbackClass
from aiogram.enums.parse_mode import ParseMode
from funcs import format_arbitrages, process_file
from aiogram.types.callback_query import CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.db import switch_autoupdate, get_user


callback_router = Router()


@callback_router.callback_query(StartCallbackClass.filter())
async def callback_handler(callback: CallbackQuery, bot: Bot):
    option = callback.data.split(':')[1]
    user_id = callback.data.split(':')[2]
    
    await callback.answer(show_alert=True)

    if option == "contacts":
        await bot.send_message(chat_id=user_id, text=config.CONTACTS_INFO, parse_mode=ParseMode.HTML)
        return
    
    if option == "info":
        await bot.send_message(chat_id=user_id, text=config.INFO, parse_mode=ParseMode.HTML)
        return
    
    if option == "autoupdate":
        user = get_user(user_id)
        switch_autoupdate(user["tgid"])
        if user["autoupdate"] == 0:
            await bot.send_message(user_id, "✅  Вы включили автообновление связок!\n🔄  Сообщения будут обновляться автоматически каждые 2 минуты!")
        else:
            await bot.send_message(user_id, "🔴  Вы выключили автообновление связок!\nАвтообновление остановлено!")
    
    if option == "search":
        arb_list = format_arbitrages(process_file())
        for text in arb_list:
            await bot.send_message(
                chat_id=user_id, 
                text=text, 
                disable_web_page_preview=True,
                parse_mode=ParseMode.HTML
            )
        
        update_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Обновить ⚙️", 
                        callback_data=StartCallbackClass(option="search", answer_id=user_id).pack()
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Автообновление 🔄",
                        callback_data=StartCallbackClass(option="autoupdate", answer_id=user_id).pack()
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Поддержка 🚨", 
                        callback_data=StartCallbackClass(option="contacts", answer_id=user_id).pack()
                    )
                ]
            ]
        )
        await bot.send_message(
            chat_id=user_id, 
            text="Нажмите кнопку чтобы обновить сделки ⚙️",
            reply_markup=update_keyboard
        )
        
        return
    
    if option == "subscribe":
        await bot.send_message(
            chat_id=user_id,
            text="text",
            reply_markup=None
        )
