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
    Berilgan service_id bo'yicha kerakli maydonlarni yangilash.
    Bo'sh string kiritilsa yoki maydon berilmasa, o'zgarishsiz qoladi.
    """
    fields = ["categoria_nomi", "bolim_nomi", "xizmat_nomi", "narxi", "tavsif"]

    # Bo'sh string => None
    values = [
        kwargs.get(f) if kwargs.get(f) not in ("", None) else None
        for f in fields
    ] + [service_id]

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


async def get_service_name(service_id: int) -> str | None:
    """
    Berilgan service_id bo'yicha xizmat_nomi ni olish
    """
    async with aiosqlite.connect(ORDER_DB) as db:
        async with db.execute(
            "SELECT xizmat_nomi FROM services WHERE service_id = ?",
            (service_id,)
        ) as cursor:
            row = await cursor.fetchone()

    return row[0] if row else None


async def get_service_narxi(service_id: int) -> float | None:
    """
    Berilgan service_id bo'yicha narxini olish
    """
    async with aiosqlite.connect(ORDER_DB) as db:
        async with db.execute(
            "SELECT narxi FROM services WHERE service_id = ?",
            (service_id,)
        ) as cursor:
            row = await cursor.fetchone()

    if row:
        return float(row[0])
    return None

