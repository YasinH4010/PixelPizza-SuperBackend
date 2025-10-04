# from config import CONFIG, WAITINGS, SESSIONS
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from pathlib import Path
# from os import getenv
# from aiogram import types
# import aiohttp
# from utils.req import req

# if __name__ == "__main__":
#     print('run bot.py')

# async def handler(message):
#     k = CONFIG['manage_items']['keyboard']
#     keyboard = InlineKeyboardMarkup(
#                 inline_keyboard=[
#                     [InlineKeyboardButton(text=k['add_item'], callback_data='add_item')],
#                     [InlineKeyboardButton(text=k['edit_item'], callback_data='edit_item')]
#                     ]
#             )
#     await message.answer(CONFIG['manage_items']['main'], reply_markup=keyboard)



# async def add_item_handler(qom, data):
#     UPLOAD_DIR = Path(getenv("UPLOAD_DIR"))
#     UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
#     if hasattr(qom, "text") and qom.text:
#         d = ':'.join(qom.text.split('\n'))
#         data = f'{data}:{d}'
#     elif hasattr(qom, "caption") and qom.caption:
#         d = ':'.join(qom.caption.split('\n'))
#         data = f'{data}:{d}'
#     pl = data.split(':')
#     if(len(pl) < 5):
#         WAITINGS[qom.from_user.id] = data
#         await qom.answer(CONFIG['manage_items']['help'])
#     else:
#         if not qom.photo:
#             WAITINGS[qom.from_user.id] = data
#             await qom.answer(CONFIG['manage_items']['send_photo'])
#             return
#     print('xxx')
#     photo = qom.photo[-1]
#     file_path = UPLOAD_DIR / f"{qom.from_user.id}_{photo.file_id}.jpg"
#     file = await qom.bot.get_file(photo.file_id)
#     await qom.bot.download_file(file.file_path, destination=file_path)

#     payload = {"name": pl[1], "price": pl[2], "weight": pl[3], "category": pl[4], "image": f"{getenv('UPLOAD_URL')}/{qom.from_user.id}_{photo.file_id}.jpg"}
#     req, _ = await req('/items/addItem', qom, 'POST', payload)
#     if(req == None):
#         return
#     await qom.answer('added')
                


# async def edit_item_handler(qom, data):
#     UPLOAD_DIR = Path(getenv("UPLOAD_DIR"))
#     UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
#     pl = data.split(':')
#     def create_keyboard_e(data):
#         k = CONFIG['manage_items']['edit_type_keyboard']
#         keyboard = InlineKeyboardMarkup(
#                 inline_keyboard=[
#                     [InlineKeyboardButton(text=k['name'], callback_data=f'{data}:edit_name'),
#                         InlineKeyboardButton(text=k['price'], callback_data=f'{data}:edit_price'),
#                         InlineKeyboardButton(text=k['photo'], callback_data=f'{data}:edit_photo')],
#                     [InlineKeyboardButton(text=k['all'], callback_data=f'{data}:edit_all')],
#                     [InlineKeyboardButton(text=k['all'], callback_data=f'{data}:delete')],
#                     [InlineKeyboardButton(text=CONFIG['cancel_waiting'], callback_data=f'cancel_waiting')]
#                     ]
#             )
#         return keyboard
#     if(len(pl) < 2):
#         print('data:',data)
#         WAITINGS[qom.from_user.id] = data
#         res, res_status = await req('/items', qom)
#         if hasattr(qom, 'text') and qom.text:
#             for item in res['data']:
#                 if item['name'] == qom.text:
#                     id = item['_id']
#                     new_data = f'{data}:{id}'
#                     keyboard = create_keyboard_e(new_data)
#                     WAITINGS.pop(qom.from_user.id, None)
#                     if isinstance(qom, types.Message):
#                         await qom.answer(CONFIG['manage_items']['change_type'], reply_markup=keyboard)
#                     else:
#                         await qom.message.answer(CONFIG['manage_items']['change_type'], reply_markup=keyboard)
#                     return
                    
#         inline_keyboards = []
#         for item in res['data']:
#             id = item['_id']
#             inline_keyboards.append([InlineKeyboardButton(text=item['name'], callback_data=f'{data}:{id}')])
#         keyboard = InlineKeyboardMarkup(
#                 inline_keyboard=inline_keyboards
#             )
#         if isinstance(qom, types.Message):
#             await qom.answer(CONFIG['manage_items']['help_edit'], reply_markup=keyboard)
#         else:
#             await qom.message.answer(CONFIG['manage_items']['help_edit'], reply_markup=keyboard)
#         return
#     if(len(pl) < 3):
#         WAITINGS.pop(qom.from_user.id, None)
#         keyboard = create_keyboard_e(data)
#         if isinstance(qom, types.Message):
#             await qom.answer(CONFIG['manage_items']['change_type'], reply_markup=keyboard)
#         else:
#             await qom.message.answer(CONFIG['manage_items']['change_type'], reply_markup=keyboard)
#         return
#     target_id = pl[1]
#     print('pl: ',pl)
    
#     if(pl[2] == 'delete'):
#         WAITINGS.pop(qom.from_user.id, None)
#         if(len(pl) > 3 and pl[3] == 'confirm'):
#             res, res_status = await req(f'/items/deleteItem/{target_id}', qom, 'DELETE')
#             print(res)
#             if(res_status == 204):
#                 await qom.answer('deleted')
#             else:
#                 await qom.answer(res['message'])

#         else:
#             keyboard = InlineKeyboardMarkup(
#                 inline_keyboard=[
#                     [InlineKeyboardButton(text= CONFIG['manage_items']['edit']['delete_confirm_btn'], callback_data=f'{data}:confirm')]
#             ])
#             if isinstance(qom, types.Message):
#                 await qom.answer(CONFIG['manage_items']['edit']['delete_confirm'], reply_markup=keyboard)
#             else:
#                 await qom.message.answer(CONFIG['manage_items']['edit']['delete_confirm'], reply_markup=keyboard)
#         return
#     if(pl[2] == 'edit_photo'):
#         WAITINGS.pop(qom.from_user.id, None)
#         if not hasattr(qom, 'photo') or not qom.photo:
#             print('XXN')
#             WAITINGS[qom.from_user.id] = data
#             await qom.answer(CONFIG['manage_items']['send_photo'])
#             return
#         print('xxx')
#         photo = qom.photo[-1]
#         file_path = UPLOAD_DIR / f"{qom.from_user.id}_{photo.file_id}.jpg"
#         file = await qom.bot.get_file(photo.file_id)
#         await qom.bot.download_file(file.file_path, destination=file_path)

#         url = f'/items/editItem/{target_id}'
#         payload = {"image": f"{getenv('UPLOAD_URL')}/{qom.from_user.id}_{photo.file_id}.jpg"}
#         res, res_status = await req(url, qom, 'PATCH',payload)
#         if(res_status in (200,201)):
#             await qom.answer('image edited')
#         else:
#             await qom.answer(res['message'])

#     if(pl[2] == 'edit_name' or pl[2] == 'edit_price'):
#         WAITINGS.pop(qom.from_user.id, None)
#         if not hasattr(qom, "text") or not qom.text:
#             WAITINGS[qom.from_user.id] = data
#             txt = ''
#             if(pl[2] == 'edit_name'):
#                 txt = 'send_name'
#             else:
#                 txt = 'send_price'
#             return await qom.answer(txt)
#         if(pl[2] == 'edit_name'):
#             payload = {"name": qom.text}
#         else:
#             payload = {"price": qom.text}
#         url = f'/items/editItem/{target_id}'
#         res, res_status = await req(url, qom, 'PATCH',payload)
#         if(res_status in (200,201)):
#             await qom.answer('edited')
#         else:
#             await qom.answer(res['message'])
                    
#     if(pl[2] == 'edit_all'):
#         if hasattr(qom, "text") and qom.text:
#             d = ':'.join(qom.text.split('\n'))
#             data = f'{data}:{d}'
#         elif hasattr(qom, "caption") and qom.caption:
#             d = ':'.join(qom.caption.split('\n'))
#             data = f'{data}:{d}'
#         print('pl:    ', pl)
#         if(len(pl) < 7):
#             WAITINGS[qom.from_user.id] = data
#             await qom.answer(CONFIG['manage_items']['edit']['test'])  
#             return
#         else:
#             if not hasattr(qom, 'photo') or not qom.photo:
#                 WAITINGS.pop(qom.from_user.id, None)
#                 WAITINGS[qom.from_user.id] = data
#                 await qom.answer(CONFIG['manage_items']['send_photo'])
#                 return
#         print('xxx')
#         photo = qom.photo[-1]
#         file_path = UPLOAD_DIR / f"{qom.from_user.id}_{photo.file_id}.jpg"
#         file = await qom.bot.get_file(photo.file_id)
#         await qom.bot.download_file(file.file_path, destination=file_path)

#         url = f'/items/editItem/{target_id}'
#         payload = {"name": pl[1+2], "price": pl[2+2], "weight": pl[3+2], "category": pl[4+2], "image": f"{getenv('UPLOAD_URL')}/{qom.from_user.id}_{photo.file_id}.jpg"}
#         res, res_status = await req(url, qom, 'PATCH',payload)
#         if(res_status in (200,201)):
#             await qom.answer('edited')
#         else:
#             await qom.answer(res['message'])
                    

from config import CONFIG, WAITINGS
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pathlib import Path
from os import getenv
from utils.req import req
from utils.check_message import check_message
from utils.send_message import send_message
from utils.create_inline_keyboard import create_inline_keyboard
from aiogram import types

if __name__ == "__main__":
    print('run bot.py')


async def handler(message):
    k = CONFIG['manage_items']['keyboard']
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=k['add_item'], callback_data='add_item')],
            [InlineKeyboardButton(text=k['edit_item'], callback_data='edit_item')],
        ]
    )
    await message.answer(CONFIG['manage_items']['main'], reply_markup=keyboard)


async def add_item_handler(qom, data):
    UPLOAD_DIR = Path(getenv("UPLOAD_DIR"))
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    pl = data.split(':')
    if hasattr(qom, "text") and qom.text:
        d = ':'.join(qom.text.split('\n'))
        ndata = f'{data}:{d}'
        pl = ndata.split(':')
    elif hasattr(qom, "caption") and qom.caption:
        d = ':'.join(qom.caption.split('\n'))
        ndata = f'{data}:{d}'
        pl = ndata.split(':')
    if(len(pl) < 5):
        WAITINGS[qom.from_user.id] = data
        if isinstance(qom, types.Message):
            await qom.answer(CONFIG['manage_items']['format_help'])
        else:
            await qom.message.answer(CONFIG['manage_items']['help'])
        return
    else:
        if not qom.photo:
            WAITINGS[qom.from_user.id] = ndata
            await qom.answer(CONFIG['manage_items']['send_photo'])
            return
    WAITINGS.pop(qom.from_user.id, None)
    photo = qom.photo[-1]
    file_path = UPLOAD_DIR / f"{qom.from_user.id}_{photo.file_id}.jpg"
    file = await qom.bot.get_file(photo.file_id)
    await qom.bot.download_file(file.file_path, destination=file_path)

    payload = {"name": pl[1], "price": pl[2], "weight": pl[3], "category": pl[4], "image": f"{getenv('UPLOAD_URL')}/{qom.from_user.id}_{photo.file_id}.jpg"}
    res, _ = await req('/items/addItem', qom, 'POST', payload)
    if(res == None):
        return
    await qom.answer('added')
                

async def edit_item_handler(qom, data):
    upload_dir = Path(getenv("UPLOAD_DIR"))
    upload_dir.mkdir(parents=True, exist_ok=True)

    pl = data.split(':')

    def create_keyboard_e(data):
        k = CONFIG['manage_items']['edit_type_keyboard']
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=k['name'], callback_data=f'{data}:edit_name'),
                    InlineKeyboardButton(text=k['price'], callback_data=f'{data}:edit_price'),
                    InlineKeyboardButton(text=k['photo'], callback_data=f'{data}:edit_photo'),
                ],
                [InlineKeyboardButton(text=k['all'], callback_data=f'{data}:edit_all')],
                [InlineKeyboardButton(text=k['delete'], callback_data=f'{data}:delete')],
                [InlineKeyboardButton(text=CONFIG['cancel_waiting'], callback_data='cancel_waiting')],
            ]
        )
        return keyboard

    if len(pl) < 2:
        WAITINGS[qom.from_user.id] = data
        res, _ = await req('/items', qom)
        if res is None:
            return
        if hasattr(qom, 'text') and qom.text:
            status = await check_message(res['data'], data, qom, CONFIG['manage_items']['change_type'], create_keyboard_e)
            if status == 'OK':
                return
        keyboard = create_inline_keyboard(res['data'], data)
        return await send_message(CONFIG['manage_items']['help_edit'], qom, keyboard)

    if len(pl) < 3:
        WAITINGS.pop(qom.from_user.id, None)
        keyboard = create_keyboard_e(data)
        return await send_message(CONFIG['manage_items']['change_type'], qom, keyboard)

    target_id = pl[1]

    if pl[2] == 'delete':
        WAITINGS.pop(qom.from_user.id, None)
        if len(pl) > 3 and pl[3] == 'confirm':
            res, _ = await req(f'/items/deleteItem/{target_id}', qom, 'DELETE')
            if res is None:
                return
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=CONFIG['manage_items']['edit']['delete_confirm_btn'],
                        callback_data=f'{data}:confirm'
                    )]
                ]
            )
            return await send_message(CONFIG['manage_items']['edit']['delete_confirm'], qom, keyboard)

    if pl[2] == 'edit_photo':
        WAITINGS.pop(qom.from_user.id, None)
        if not hasattr(qom, 'photo') or not qom.photo:
            WAITINGS[qom.from_user.id] = data
            return await qom.answer(CONFIG['manage_items']['send_photo'])

        photo = qom.photo[-1]
        file_path = upload_dir / f"{qom.from_user.id}_{photo.file_id}.jpg"
        file = await qom.bot.get_file(photo.file_id)
        await qom.bot.download_file(file.file_path, destination=file_path)

        url = f'/items/editItem/{target_id}'
        payload = {"image": f"{getenv('UPLOAD_URL')}/{qom.from_user.id}_{photo.file_id}.jpg"}
        res, res_status = await req(url, qom, 'PATCH', payload)
        if res_status in (200, 201):
            await qom.answer('image edited')
        else:
            await qom.answer(res['message'])

    if pl[2] in ('edit_name', 'edit_price'):
        WAITINGS.pop(qom.from_user.id, None)
        field = pl[2].split('_')[1]
        if not hasattr(qom, "text") or not qom.text:
            WAITINGS[qom.from_user.id] = data
            return await qom.answer(CONFIG['manage_items'][f'send_{field}'])
        payload = {field: qom.text}
        url = f'/items/editItem/{target_id}'
        res, res_status = await req(url, qom, 'PATCH', payload)
        if res_status in (200, 201):
            await qom.answer('edited')
        else:
            await qom.answer(res['message'])

    if pl[2] == 'edit_all':
        text_data = None
        pl = data.split(':')
        if hasattr(qom, "text") and qom.text:
            text_data = qom.text
        elif hasattr(qom, "caption") and qom.caption:
            text_data = qom.caption

        if text_data:
            d = ':'.join(text_data.split('\n'))
            ndata = f'{data}:{d}'
        
            pl = ndata.split(':')

        if len(pl) < 7:
            WAITINGS[qom.from_user.id] = data
            if isinstance(qom, types.Message):
                await qom.answer(CONFIG['manage_items']['format_help'])
            else:
                await qom.message.answer(CONFIG['manage_items']['help'])
            return

        if not hasattr(qom, 'photo') or not qom.photo:
            WAITINGS[qom.from_user.id] = ndata
            return await qom.answer(CONFIG['manage_items']['send_photo'])
        
        WAITINGS.pop(qom.from_user.id, None)
        photo = qom.photo[-1]
        file_path = upload_dir / f"{qom.from_user.id}_{photo.file_id}.jpg"
        file = await qom.bot.get_file(photo.file_id)
        await qom.bot.download_file(file.file_path, destination=file_path)

        url = f'/items/editItem/{target_id}'
        payload = {
            "name": pl[3],
            "price": pl[4],
            "weight": pl[5],
            "category": pl[6],
            "image": f"{getenv('UPLOAD_URL')}/{qom.from_user.id}_{photo.file_id}.jpg",
        }
        res, res_status = await req(url, qom, 'PATCH', payload)
        if res_status in (200, 201):
            await qom.answer('edited')
        else:
            await qom.answer(res['message'])
