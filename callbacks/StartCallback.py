from aiogram.filters.callback_data import CallbackData


class StartCallbackClass(CallbackData, prefix="start"):
    option: str
    answer_id: int