import json
import os
import aiofiles
import aiohttp
from config import JSON_FILE

async def read_json():
    """JSON dan ma'lumot o‘qish (async)"""
    if not os.path.exists(JSON_FILE):
        return {}
    async with aiofiles.open(JSON_FILE, "r", encoding="utf-8") as f:
        content = await f.read()
        return json.loads(content)

async def write_json(data):
    """JSON ga ma'lumot yozish (async)"""
    async with aiofiles.open(JSON_FILE, "w", encoding="utf-8") as f:
        await f.write(json.dumps(data, indent=4, ensure_ascii=False))

async def update_json(key, value):
    """JSON ichida qiymatni yangilash (async)"""
    data = await read_json()
    data[key] = value
    await write_json(data)
    return data



async def check_api_key(api_url: str, api_key: str) -> bool:
    """API key ishlashini tekshiradi"""
    try:
        async with aiohttp.ClientSession() as session:
            payload = {
                "key": api_key,
                "action": "balance"  # odatda balance tekshirish ishlaydi
            }
            async with session.post(api_url, data=payload) as resp:
                if resp.status != 200:
                    return False
                result = await resp.json()

                # API dan muvaffaqiyatli javob kelganini tekshirish
                return "balance" in result or "currency" in result

    except Exception as e:
        print(f"Xatolik: {e}")
        return False