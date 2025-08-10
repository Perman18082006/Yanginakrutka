import aiosqlite
import asyncio
# Vaqtni olish uchun
from datetime import datetime
from zoneinfo import ZoneInfo
# Config
from config import DB_NAME

# 🧱 Foydalanuvchilar uchun jadval yaratadi: user_id, balance, referal_id, referal_count
async def create_users_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                balance INTEGER DEFAULT 0,
                referal_id INTEGER,
                referal_count INTEGER DEFAULT 0
            )
        """)
        await db.commit()

# 📋 Buyurtmalar uchun jadval yaratadi: user_id, nomi, xizmat_turi, linkin, narxi, vaqti
async def create_users_order():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users_order (
                user_id INTEGER,
                order_id INTEGER PRIMARY KEY,
                xizmat_turi TEXT,
                link TEXT,
                amount INTEGER,
                narx INTEGER,
                vaqt TEXT
            )
        """)
        await db.commit()
        
# 🔍 Barcha foydalanuvchilarni user_id si bilan olib keladi
async def get_all_user_ids():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT user_id FROM users")
        rows = await cursor.fetchall()
        await db.commit()
        return [row[0] for row in rows] # user_id larni listga aylantirib qaytaradi

# 🔍 Foydalanuvchi bazada mavjudligini tekshiradi
async def user_exists(user_id: int) -> bool:
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT 1 FROM users WHERE user_id = ? LIMIT 1", (user_id,))
        return await cursor.fetchone() is not None        
        
# ➕ Yangi user qo‘shadi va agar referal bo‘lsa, hisoblaydi
async def add_user(user_id, referal_id=None):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT INTO users (user_id, referal_id) VALUES (?, ?)", (user_id, referal_id))
        if referal_id:
            await db.execute(
                "UPDATE users SET referal_count = referal_count + 1 WHERE user_id = ?",
                (referal_id,)
            )
        await db.commit()

# 💰 Foydalanuvchi balansiga qo‘shadi
async def add_balance(user_id, balance):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE users SET balance = balance + ? WHERE user_id = ?",
            (balance, user_id)
        )
        await db.commit()

# 💸 Foydalanuvchi balansidan ayiradi
async def subtract_balance(user_id, balance):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE users SET balance = balance - ? WHERE user_id = ?",
            (balance, user_id)
        )
        await db.commit()

# 🔍 User maʼlumotlarini bazadan olib keladi (user_id bo‘yicha)
async def get_user_data(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        if row:
            return {
                "user_id": row[0],
                "balance": row[1],
                "referal_id": row[2],
                "referal_count": row[3]
            }
        return None


async def add_order_db(user_id, order_id, xizmat_nomi, link, amount, narx):
    # Toshkent vaqti
    vaqt = datetime.now(ZoneInfo("Asia/Tashkent")).strftime("%Y-%m-%d %H:%M:%S")
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO users_order (
                user_id, order_id, xizmat_turi, link, amount, narx, vaqt
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, order_id, xizmat_nomi, link, amount, narx, vaqt))
        await db.commit()


async def get_orders_by_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            SELECT * FROM users_order WHERE user_id = ?
            ORDER BY vaqt DESC
        """, (user_id,))
        rows = await cursor.fetchall()
        return [
            {
                "user_id": row[0],
                "order_id": row[1],
                "xizmat_turi": row[2],
                "link": row[3],
                "amount": row[4],
                "narx": row[5],
                "vaqt": row[6]
            } for row in rows
        ]


