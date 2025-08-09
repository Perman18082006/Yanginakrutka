import aiohttp
from config import API_KEY, API_URL

async def get_services():
    """
    Xizmatlar ro'yxatini olish
    """
    async with aiohttp.ClientSession() as session:
        payload = {
            "key": API_KEY,
            "action": "services"
        }
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
        payload = {
            "key": API_KEY,
            "action": "balance"
        }
        async with session.post(API_URL, data=payload) as resp:
            return await resp.json()


async def get_service_limits(service_id: int):
    """
    Berilgan service_id bo'yicha min va max qiymatlarni olish
    """
    async with aiohttp.ClientSession() as session:
        payload = {
            "key": API_KEY,
            "action": "services"
        }
        async with session.post(API_URL, data=payload) as resp:
            services = await resp.json()

    for service in services:
        if service.get("service") == service_id:
            return {
                "name": service.get("name"),
                "min": int(service.get("min")),
                "max": int(service.get("max"))
            }

    return None