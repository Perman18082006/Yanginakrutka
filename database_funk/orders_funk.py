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
            narxi INTEGER NOT NULL,
            tavsif TEXT,
            buyurtma_soni INTEGER DEFAULT 0,
            sarflangan_summa INTEGER DEFAULT 0
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
    fields = ["service_id",  "categoria_nomi", "bolim_nomi", "xizmat_nomi", "narxi", "tavsif"]

    # Bo'sh string => None
    values = [
        kwargs.get(f) if kwargs.get(f) not in ("", None) else None
        for f in fields
    ] + [service_id]

    async with aiosqlite.connect(ORDER_DB) as db:
        await db.execute(f"""
            UPDATE services SET
                service_id = COALESCE(?, service_id),
                categoria_nomi = COALESCE(?, categoria_nomi),
                bolim_nomi     = COALESCE(?, bolim_nomi),
                xizmat_nomi    = COALESCE(?, xizmat_nomi),
                narxi          = COALESCE(?, narxi),
                tavsif         = COALESCE(?, tavsif)
            WHERE service_id = ?
        """, values)
        await db.commit()

async def delete_service(service_id: int):
    """
    Berilgan service_id bo'yicha xizmatni o'chirish.
    """
    async with aiosqlite.connect(ORDER_DB) as db:
        await db.execute("DELETE FROM services WHERE service_id = ?", (service_id,))
        await db.commit()




async def get_service_by_id(service_id: int) -> dict | None:
    """
    Berilgan service_id bo'yicha barcha ustunlarni lug'at shaklida qaytaradi.
    """
    async with aiosqlite.connect(ORDER_DB) as db:
        async with db.execute(
            """
            SELECT service_id, categoria_nomi, bolim_nomi, xizmat_nomi, narxi, tavsif, buyurtma_soni, sarflangan_summa
            FROM services
            WHERE service_id = ?
            """,
            (service_id,)
        ) as cursor:
            row = await cursor.fetchone()

    if row:
        return {
            "service_id": row[0],
            "categoria_nomi": row[1],
            "bolim_nomi": row[2],
            "xizmat_nomi": row[3],
            "narxi": int(row[4]),
            "tavsif": row[5],
            "buyurtma_soni": row[6],
            "sarflangan_summa": int(row[7])
        }
    return None