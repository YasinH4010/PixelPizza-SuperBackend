from config import WAITINGS
from aiogram import types
from utils.send_message import send_message

async def check_message(res_data, data, qom, msg, create_keyboard_e):
    for ent in res_data:
        if ent['name'] == qom.text:
            id = ent['_id']
            new_data = f'{data}:{id}'
            keyboard = create_keyboard_e(new_data)
            WAITINGS.pop(qom.from_user.id, None)
            await send_message(msg, qom, keyboard)
            return 'OK'