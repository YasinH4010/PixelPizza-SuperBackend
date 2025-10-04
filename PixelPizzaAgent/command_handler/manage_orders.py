from config import CONFIG, WAITINGS, SESSIONS
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pathlib import Path
from os import getenv
from aiogram import types
import aiohttp
from utils.req import req
from utils.send_message import send_message


if __name__ == "__main__":
    print('run bot.py')

async def handler(message):
    k = CONFIG['manage_orders']['keyboard']
    keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=k['manage_new_orders'], callback_data='manage_new_orders')],
                    [InlineKeyboardButton(text=k['manage_all_orders'], callback_data='manage_all_orders')]
                         ]
            )
    await message.answer(CONFIG['manage_orders']['main'], reply_markup=keyboard)




async def edit_order_handler(qom, data):
    pl = data.split(':')
    def create_keyboard_e(data):
        k = CONFIG['manage_orders']['edit_type_keyboard']
        keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=k['preparing'], callback_data=f'{data}:preparing'),
                        InlineKeyboardButton(text=k['baking'], callback_data=f'{data}:baking'),
                        InlineKeyboardButton(text=k['out_for_delivery'], callback_data=f'{data}:out_for_delivery')],
                    [InlineKeyboardButton(text=k['delivered'], callback_data=f'{data}:delivered')],
                    [InlineKeyboardButton(text=k['cancelled'], callback_data=f'{data}:cancelled')],
                    ]
            )
        return keyboard
    if(len(pl) < 2):
        print('data:',data)
        WAITINGS[qom.from_user.id] = data
        res, res_status = await req('/orders', qom)
        print('RES', res)
        if hasattr(qom, 'text') and qom.text:
            for order in res['data']:
                if order['orderID'] == qom.text:
                    id = order['_id']
                    new_data = f'{data}:{id}'
                    keyboard = create_keyboard_e(new_data)
                    WAITINGS.pop(qom.from_user.id, None)
                    await send_message(CONFIG['manage_orders']['change_type'], qom, keyboard)
                    return
                    
        inline_keyboards = []
        for order in res['data']:
            status = order['status']
            if(pl[0] == 'manage_new_orders' and (status == 'cancelled' or status == 'delivered')):
                continue
            id = order['_id']
            order_id = order['orderID']
            paid = order['paid']
            inline_keyboards.append([InlineKeyboardButton(text=f'{order_id} | {paid}T | {status}', callback_data=f'{data}:{order_id}')])
        keyboard = InlineKeyboardMarkup(
                inline_keyboard=inline_keyboards
            )
        if(len(inline_keyboards) < 1):
            await send_message(CONFIG['manage_orders']['no_orders'], qom)
        else:
            await send_message(CONFIG['manage_orders']['help_edit'], qom, keyboard)
        return
    target_id = pl[1]
    if(len(pl) < 3):
        order_res, order_res_status = await req(f'/orders/manage/{target_id}', qom)
        order_data = order_res['data']
        orderer_id = order_data['orderer']
        user_res, user_res_status = await req(f'/users/{orderer_id}', qom)
        user_data = user_res['data']
        items = ''
        for item in order_data['items']:
            item_name = item['item']['name']
            items = f'{items}\n{item_name}'
        txt = (
            CONFIG['manage_orders']['order_information']
        .replace('{{name}}', user_data['name'])
        .replace('{{email}}', user_data['email'])
        .replace('{{address}}', order_data['address'])
        .replace('{{order_id}}', str(order_data['orderID']))
        .replace('{{paid}}', str(order_data['paid']))
        .replace('{{items}}', items)
        )
        WAITINGS.pop(qom.from_user.id, None)
        keyboard = create_keyboard_e(data)
        await send_message(txt, qom, keyboard)
        return
    print('pl: ',pl)
    
    if(pl[2]):
        WAITINGS.pop(qom.from_user.id, None)
        payload = {'status': pl[2]}
        url = f'/orders/manage/{target_id}'
        res, res_status = await req(url, qom, 'PATCH',payload)
        if(res_status in (200,201)):
            await qom.answer('edited')
        else:
            await qom.answer(res['message'])
                    
                    