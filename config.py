BOT_TOKEN = "7002570947:AAEPaTfgtnRwsX_VzDTJplBxerNPqi2HfCc"

import json

# JSON fayldan qiymatlarni yuklash
try:
    with open("database/data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    referal_price = data.get("referal_price", 100)
    API_KEY = data.get("API_KEY", "6fa37e02dade47d723f3c1b45a822b2f")
    API_URL = data.get("API_URL", "https://topsmm.uz/api/v2")
    FIO = data.get("FIO", "Shamuratov Perman")
    karta = data.get("karta", "8600 0000 0000 0000")
    min_pay = data.get("min_pay", 1000)
    max_pay = data.get("max_pay", 1000000)
    adminlar = data.get("adminlar", [])
    kanallar = data.get("kanallar", [])
except (FileNotFoundError, json.JSONDecodeError):
    referal_price = 100

DB_NAME = "database/users.db"

SUPER_ADMIN = 7547413961

FIO = "Shamuratov Perman"
karta = "8600 0000 0000 0000"
min_pay = 1000
max_pay = 1000000

API_KEY = "6fa37e02dade47d723f3c1b45a822b2f"  # <-- O'z API kalitingizni qo'ying
API_URL = "https://topsmm.uz/api/v2"

ORDER_DB = "database/orders.db"
JSON_FILE = "database/data.json"