import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN

#DATABASE FUNKSIYALARNI YUKLAYMIZ
from database_funk.funk import create_users_db, create_users_order
#HANDLERLAR
from handlers.user_handlers import start, referal, my_balance, support

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



async def main():
    # Create database tables
    await create_users_db()
    await create_users_order()
    # Start bot
    logging.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')