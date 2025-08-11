import aiohttp
# Config
from config import API_KEY, API_URL

async def make_post_request(action: str, params: dict = {}) -> dict:
    payload = {
        "key": API_KEY,
        "action": action,
        **params
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, data=payload) as response:
            return await response.json()
            
# Rate olish
async def get_rate_by_service_id(service_id: int) -> int | None:
    services = await make_post_request("services")
    for service in services:
        if service.get("service") == service_id:
            return int(float(service["rate"]))
    return None  # Agar topilmasa


# Max va Min qiymatlarni olish
async def get_max_by_service_id(service_id: int) -> int | None:
    services = await make_post_request("services")
    for service in services:
        if service.get("service") == service_id:
            return int(service["max"])
    return None

async def get_min_by_service_id(service_id: int) -> int | None:
    services = await make_post_request("services")
    for service in services:
        if service.get("service") == service_id:
            return int(service["min"])
    return None

async def add_order(service_id: int, link: str, quantity: int):
    response = await make_post_request("add", {
        "service": service_id,
        "link": link,
        "quantity": quantity
    })
    return response

async def get_order_status(order_id: int):
    response = await make_post_request("status", {
    "order": order_id
    })
    return response