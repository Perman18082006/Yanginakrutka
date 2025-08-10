import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN

#DATABASE FUNKSIYALARNI YUKLAYMIZ
from database_funk.users_funk import create_users_db, create_users_order
from database_funk.orders_funk import create_services_table, add_service
#HANDLERLAR
from handlers.user_handlers import start, referal, my_balance, support, payment, buyurtma, buyurtma_davomi, buyurtmalar
#ADMIN HANDLERLAR
from handlers.admin_handlers import javob_yoz, panel, statistika, xizmat_qoshish, xizmat_tahrirla, api_qosh, foydalanuvchi_boshqarish, tolov_tasdiqla

# Create bot and dispatcher
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


#Routerga ulaymiz
dp.include_router(start.router)
dp.include_router(referal.router)
dp.include_router(my_balance.router)
dp.include_router(support.router)
dp.include_router(payment.router)
dp.include_router(buyurtma.router)
dp.include_router(buyurtma_davomi.router)
dp.include_router(buyurtmalar.router)

#Admin router
dp.include_router(javob_yoz.router)
dp.include_router(panel.router)
dp.include_router(statistika.router)
dp.include_router(xizmat_qoshish.router)
dp.include_router(xizmat_tahrirla.router)
dp.include_router(api_qosh.router)
dp.include_router(foydalanuvchi_boshqarish.router)
dp.include_router(tolov_tasdiqla.router)


async def main():
    # Create database tables
    await create_users_db()
    await create_users_order()
    await create_services_table()
    # Start bot
    logging.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')