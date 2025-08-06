from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.filters.command import CommandObject
from aiogram.types import Message
from aiogram import Bot

# CONFIG
from config import BOT_TOKEN, referal_price

# TEXTLAR
from texts.user_texts import START_TEXT

# DATABASE FUNKSIYALAR
from database_funk.funk import add_user, user_exists, add_balance

# KEYBOARD
from keyboards.users_keyboard.users_reply import menu


bot = Bot(token=BOT_TOKEN)
router = Router()

@router.message(CommandStart(deep_link=True))  # faqat bitta handler kifoya
async def start_deeplink_handler(message: Message, command: CommandObject):
    user_id = message.from_user.id
    args = command.args
    referal_id = None

    # Referalni tekshirish
    if args and args.isdigit():
        temp_id = int(args)
        if temp_id != user_id:
            referal_id = temp_id

    # Foydalanuvchi mavjud emas bo‘lsa qo‘shish
    if not await user_exists(user_id):
        await add_user(user_id, referal_id)

        # Referalga xabar yuborish
        if referal_id:
            try:
                await bot.send_message(
                    referal_id,
                    f"🎉 Sizning referalingiz orqali yangi foydalanuvchi qo‘shildi: {user_id}!"
                )
                await add_balance(referal_id, referal_price)
            except Exception as e:
                print(f"Referalga xabar yuborilmadi: {e}")

    await message.answer(START_TEXT, reply_markup=menu)


@router.message(CommandStart())
async def start_handler(message: Message):
    user_id = message.from_user.id
    # Foydalanuvchi mavjud emas bo‘lsa qo‘shish
    if not await user_exists(user_id):
        await add_user(user_id)
    await message.answer(START_TEXT, reply_markup=menu)

