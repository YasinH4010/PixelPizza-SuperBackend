from config import CONFIG, WAITINGS, SESSIONS
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pathlib import Path
from os import getenv
from aiogram import types
import aiohttp
from utils.req import req
from utils.check_message import check_message
from utils.send_message import send_message
from utils.create_inline_keyboard import create_inline_keyboard

if __name__ == "__main__":
    print('run bot.py')

async def handler(message):
    k = CONFIG['manage_users']['keyboard']
    keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=k['manage_users'], callback_data='manage_users')],
                         ]
            )
    await message.answer(CONFIG['manage_users']['main'], reply_markup=keyboard)




async def edit_user_handler(qom, data):
    pl = data.split(':')
    def create_keyboard_e(data):
        k = CONFIG['manage_users']['edit_type_keyboard']
        keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=k['name'], callback_data=f'{data}:edit_name'),
                        InlineKeyboardButton(text=k['email'], callback_data=f'{data}:edit_email'),
                        InlineKeyboardButton(text=k['address'], callback_data=f'{data}:edit_address')],
                    [InlineKeyboardButton(text=k['balance'], callback_data=f'{data}:edit_balance')],
                    [InlineKeyboardButton(text=k['delete'], callback_data=f'{data}:delete')],
                    [InlineKeyboardButton(text=CONFIG['cancel_waiting'], callback_data=f'cancel_waiting')]
                    ]
            )
        return keyboard
    if(len(pl) < 2):
        WAITINGS[qom.from_user.id] = data
        res, _ = await req('/users', qom)
        if(res == None):
            return
        if hasattr(qom, 'text') and qom.text:
            status = await check_message(res['data'], data, qom, CONFIG['manage_users']['change_type'], create_keyboard_e)
            if(status == 'OK'):
                return
                    
        keyboard = create_inline_keyboard(res['data'], data)
        await send_message(CONFIG['manage_users']['help_edit'], qom, keyboard)
        return
    if(len(pl) < 3):
        WAITINGS.pop(qom.from_user.id, None)
        keyboard = create_keyboard_e(data)
        await send_message(CONFIG['manage_users']['change_type'], qom , keyboard)
        return
    target_id = pl[1]
    
    if(pl[2] == 'delete'):
        WAITINGS.pop(qom.from_user.id, None)
        if(len(pl) > 3 and pl[3] == 'confirm'):
            res, _ = await req(f'/users/deleteUser/{target_id}', qom, 'DELETE')
            if(res == None):
                return

        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text= CONFIG['manage_users']['edit']['delete_confirm_btn'], callback_data=f'{data}:confirm')]
            ])
            await send_message(CONFIG['manage_users']['edit']['delete_confirm'], qom, keyboard)
            return
    
    if(pl[2] == 'edit_name' or pl[2] == 'edit_email' or pl[2] == 'edit_address' or pl[2] == 'edit_balance'):
        WAITINGS.pop(qom.from_user.id, None)
        p = pl[2].split('_')[1]
        if not hasattr(qom, "text") or not qom.text:
            WAITINGS[qom.from_user.id] = data
            txt = ''
            txt = CONFIG['manage_users'][f'send_{p}']
            return await qom.answer(txt)
        payload = {p: qom.text}
        url = f'/users/editUser/{target_id}'
        res, res_status = await req(url, qom, 'PATCH',payload)
        if(res_status in (200,201)):
            await qom.answer('edited')
        else:
            await qom.answer(res['message'])