from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_inline_keyboard(res_data, data):
    inline_keyboards = []
    for ent in res_data:
        id = ent['_id']
        inline_keyboards.append([InlineKeyboardButton(text=ent['name'], callback_data=f'{data}:{id}')])
    keyboard = InlineKeyboardMarkup(
            inline_keyboard=inline_keyboards
        )
    return keyboard