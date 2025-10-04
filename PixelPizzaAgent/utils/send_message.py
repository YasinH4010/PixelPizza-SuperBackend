from aiogram import types

async def send_message(msg, qom, keyboard=None):
    if isinstance(qom, types.Message):
        await qom.answer(msg, reply_markup=keyboard)
    else:
        await qom.message.answer(msg, reply_markup=keyboard)