import aiosqlite
from config import ORDER_DB

async def create_services_table():
    async with aiosqlite.connect(ORDER_DB) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS services (
            service_id INTEGER PRIMARY KEY,
            categoria_nomi TEXT NOT NULL,
            bolim_nomi TEXT NOT NULL,
            xizmat_nomi TEXT NOT NULL,
            narxi REAL NOT NULL,
            tavsif TEXT,
            buyurtma_soni INTEGER DEFAULT 0,
            sarflangan_summa REAL DEFAULT 0.0
        )
        """)
        await db.commit()

async def add_service(service_id, categoria_nomi, bolim_nomi, xizmat_nomi, narxi, tavsif):
    async with aiosqlite.connect(ORDER_DB) as db:
        await db.execute("""
        INSERT OR IGNORE INTO services (
            service_id, categoria_nomi, bolim_nomi, xizmat_nomi, narxi, tavsif
        ) VALUES (?, ?, ?, ?, ?, ?)
        """, (service_id, categoria_nomi, bolim_nomi, xizmat_nomi, narxi, tavsif))
        await db.commit()

# Unikal kategoriyalarni olish
async def get_categories():
    try:
        async with aiosqlite.connect(ORDER_DB) as db:
            cursor = await db.execute("SELECT DISTINCT categoria_nomi FROM services")
            rows = await cursor.fetchall()
            return [row[0] for row in rows]
    except aiosqlite.OperationalError:
        return []
        # await create_services_table()
# Tanlangan kategoriya bo‘yicha bo‘limlar
async def get_bolimlar(category):
    try:
        async with aiosqlite.connect(ORDER_DB) as db:
            cursor = await db.execute(
            "SELECT DISTINCT bolim_nomi FROM services WHERE categoria_nomi = ?", (category,)
            )
            rows = await cursor.fetchall()
            return [row[0] for row in rows]
    except aiosqlite.OperationalError:
        return []
# Tanlangan bo‘lim bo‘yicha xizmatlar
async def get_xizmatlar(category, bolim):
    try:
        async with aiosqlite.connect(ORDER_DB) as db:
            cursor = await db.execute(
            "SELECT service_id, xizmat_nomi FROM services WHERE categoria_nomi = ? AND bolim_nomi = ?", (category, bolim)
            )
            rows = await cursor.fetchall()
            return rows  # [(service_id, xizmat_nomi), ...]
    except aiosqlite.OperationalError:
        return []

# Xizmatlarni tahrirlash
async def edit_service(service_id: int, **kwargs):
    """
    Kerakli joyini yangilash.
    Faqat berilgan maydonlar o'zgaradi, qolganlari o'z holida qoladi.
    """
    fields = ["categoria_nomi", "bolim_nomi", "xizmat_nomi", "narxi", "tavsif"]

    # SQL da COALESCE ishlatish uchun tartib bo‘yicha qiymatlar
    values = [kwargs.get(f) for f in fields] + [service_id]

    async with aiosqlite.connect(ORDER_DB) as db:
        await db.execute(f"""
            UPDATE services SET
                categoria_nomi = COALESCE(?, categoria_nomi),
                bolim_nomi     = COALESCE(?, bolim_nomi),
                xizmat_nomi    = COALESCE(?, xizmat_nomi),
                narxi          = COALESCE(?, narxi),
                tavsif         = COALESCE(?, tavsif)
            WHERE service_id = ?
        """, values)
        await db.commit()
