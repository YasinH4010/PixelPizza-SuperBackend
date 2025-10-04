from config import CONFIG
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot, Dispatcher, html

if __name__ == "__main__":
    print('run bot.py')

async def handler(message):
    sk = CONFIG['start_keyboards']
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=sk['manage_orders'])],
            [KeyboardButton(text=sk['manage_items']), 
             KeyboardButton(text=sk['manage_users'])],
            [KeyboardButton(text=sk['manage_offers'])],
            [KeyboardButton(text=sk['stat'])]
        ],
        resize_keyboard=True
    )
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!", reply_markup=keyboard)
