import aiohttp
import asyncio
import json
from config import SESSIONS
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path='config.env')

from os import getenv

async def login_request(username, password):
    url = getenv('API_URL') + '/login'
    payload = {"email": username, "password": password}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            data = await response.json() 
            return data

# تست مستقیم
async def main():
    result = await login_request("yasin", "12345")
    if(result['status'] == 'success'):
        print(result['token'])
    else:
        print(result['message'])

if __name__ == "__main__":
    asyncio.run(main())


async def handler(message, command):
    if not command.args:
        await message.reply("لطفاً نام کاربری و رمز عبور را وارد کنید. مثال:\n/login yasin 12345")
        return

    parts = command.args.split(maxsplit=1)  # فقط یک بار جدا کن
    if len(parts) < 2:
        await message.reply("فرمت درست نیست. باید نام کاربری و رمز رو بدی. مثال:\n/login yasin 12345")
        return

    username, password = parts[0], parts[1]
    result = await login_request(username, password)
    if(result['status'] == 'success'):
        print('token: ',result['token'])
        SESSIONS[message.from_user.id] = result['token']

    else:
        await message.answer(result['message'])   

