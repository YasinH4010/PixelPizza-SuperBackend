import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv

from config import CONFIG, WAITINGS
load_dotenv(dotenv_path='config.env')

from aiogram import Bot, Dispatcher, types, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
import command_handler.start as start
import command_handler.manage_items as item_manager
import command_handler.manage_users as user_manager
import command_handler.manage_orders as order_manager
import command_handler.login_handler as login_manager
import command_handler.stat as stat

from fastapi import FastAPI, Header, HTTPException
import uvicorn

# ------------------- CONFIG -------------------
TOKEN = getenv('TOKEN')
ADMIN_ID = getenv('ADMIN_ID')
if ADMIN_ID is None:
    raise ValueError("⚠️ ADMIN_ID در config.env ست نشده!")
ADMIN_ID = int(ADMIN_ID)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()
dp.include_router(router)


# ------------------- FASTAPI -------------------

app = FastAPI()

SECRET = getenv('NEW_ORDER_SECRET')

@app.get("/new-order/{order_id}")
async def send_notif(order_id: int, x_secret: str = Header(...)):
    if x_secret != SECRET:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid secret")

    txt = CONFIG['manage_orders']['new_order']
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=CONFIG['manage_orders']['new_order_btn'], callback_data=f'manage_new_orders:{order_id}')]
        ]
    )
    await bot.send_message(ADMIN_ID, f'{txt}', reply_markup=keyboard)
    return {"status": "ok"}


# ------------------- AIROGRAM HANDLERS -------------------
@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await start.handler(message)

@dp.message(Command("login"))
async def login_handler(message: Message, command: Command):
    await login_manager.handler(message, command)

@dp.message()
async def echo_handler(message: Message):
    try:
        for user_id, data in list(WAITINGS.items()):
            if user_id == message.from_user.id:
                action = data.split(':')[0]
                if action == 'add_item':
                    await item_manager.add_item_handler(message, data)
                    return
                if action == 'edit_item':
                    await item_manager.edit_item_handler(message, data)
                    return
                if action == 'manage_users':
                    await user_manager.edit_user_handler(message, data)
                    return

        if message.text == CONFIG['start_keyboards']['manage_items']:
            WAITINGS.pop(query.from_user.id, None)
            await item_manager.handler(message)
        elif message.text == CONFIG['start_keyboards']['manage_users']:
            WAITINGS.pop(query.from_user.id, None)
            await user_manager.handler(message)
        elif message.text == CONFIG['start_keyboards']['manage_orders']:
            WAITINGS.pop(query.from_user.id, None)
            await order_manager.handler(message)
        elif message.text == CONFIG['start_keyboards']['stat']:
            WAITINGS.pop(query.from_user.id, None)a
            await stat.handler(message)

    except Exception as e:
        print('error:', e)

@router.callback_query()
async def callback_handler(query: CallbackQuery):
    data = query.data
    if data.startswith('add_item'):
        await item_manager.add_item_handler(query, data)
    elif data.startswith('edit_item'):
        await item_manager.edit_item_handler(query, data)
    elif data.startswith('manage_users'):
        await user_manager.edit_user_handler(query, data)
    elif data.startswith('manage_all_orders') or data.startswith('manage_new_orders'):
        await order_manager.edit_order_handler(query, data)
    elif data == 'cancel_waiting':
        WAITINGS.pop(query.from_user.id, None)
        await query.message.delete()
        await query.answer(CONFIG['cancel_waiting_msg'])


# ------------------- START BOT -------------------
async def start_bot():
    await dp.start_polling(bot)

# ------------------- START API -------------------
async def start_api():
    config = uvicorn.Config(app, host="0.0.0.0", port=70, reload=False)
    server = uvicorn.Server(config)
    await server.serve()

# ------------------- MAIN -------------------
async def main():
    await asyncio.gather(
        start_bot(),
        start_api()
    )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
