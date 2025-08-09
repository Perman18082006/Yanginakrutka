import aiohttp
import json
from config import API_KEY, API_URL


async def update_services_cache():
    """
    API dan xizmatlar ro'yxatini olib,
    database/services.json fayliga saqlaydi
    """
    async with aiohttp.ClientSession() as session:
        payload = {"key": API_KEY, "action": "services"}
        async with session.post(API_URL, data=payload) as resp:
            services = await resp.json()

    # JSON faylga yozish
    with open("database/services.json", "w", encoding="utf-8") as f:
        json.dump(services, f, ensure_ascii=False, indent=2)

#Ishlatilmayabdi
async def get_services():
    """
    API dan xizmatlar ro'yxatini olish
    """
    async with aiohttp.ClientSession() as session:
        payload = {"key": API_KEY, "action": "services"}
        async with session.post(API_URL, data=payload) as resp:
            return await resp.json()


async def add_order(service_id: int, link: str, quantity: int, runs: int = None, interval: int = None):
    """
    Buyurtma berish
    """
    async with aiohttp.ClientSession() as session:
        payload = {
            "key": API_KEY,
            "action": "add",
            "service": service_id,
            "link": link,
            "quantity": quantity
        }
        if runs:
            payload["runs"] = runs
        if interval:
            payload["interval"] = interval

        async with session.post(API_URL, data=payload) as resp:
            return await resp.json()


async def get_order_status(order_id: int):
    """
    Buyurtma holatini tekshirish
    """
    async with aiohttp.ClientSession() as session:
        payload = {
            "key": API_KEY,
            "action": "status",
            "order": order_id
        }
        async with session.post(API_URL, data=payload) as resp:
            return await resp.json()


async def get_balance():
    """
    Balansni olish
    """
    async with aiohttp.ClientSession() as session:
        payload = {"key": API_KEY, "action": "balance"}
        async with session.post(API_URL, data=payload) as resp:
            return await resp.json()


async def get_service_limits(service_id: int):
    """
    Xizmatning min va max qiymatlarini olish
    API chaqirmasdan, JSON cache fayldan o'qiydi
    """
    try:
        with open("database/services.json", "r", encoding="utf-8") as f:
            services = json.load(f)
    except FileNotFoundError:
        # Agar fayl bo'lmasa API dan olib cache yangilash
        await update_services_cache()
        with open("database/services.json", "r", encoding="utf-8") as f:
            services = json.load(f)

    for service in services:
        if int(service.get("service")) == service_id:
            return {
                "min": int(service.get("min", 0)),
                "max": int(service.get("max", 0))
            }

    return {"min": None, "max": None}