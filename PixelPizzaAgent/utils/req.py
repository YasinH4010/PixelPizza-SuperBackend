import aiohttp
from config import SESSIONS
from os import getenv

async def req(url: str, data, method: str = 'GET', payload: dict = None):
    url = getenv('API_URL') + url
    token = SESSIONS.get(data.from_user.id, 'notfound')
    headers = {"Authorization": f"Bearer {token}"}
    method = method.upper()

    async with aiohttp.ClientSession() as session:
        try:
            async with session.request(method, url, json=payload, headers=headers) as response:
                if response.status == 204:
                    return None, response.status
                if response.status not in (200, 201):
                    print(f"Request failed: {response.status} - {await response.text()}")
                    await data.answer('Something is wrong..')
                    return None, response.status
                res = await response.json()
                return res, response.status
        except aiohttp.ClientError as e:
            print(f"HTTP Error: {e}")
            await data.answer('Connection error..')
            return None, None
