from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.filters.command import CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
# CONFIG
from config import referal_price, SUPER_ADMIN

# TEXTLAR
from texts.user_texts import START_TEXT

# DATABASE FUNKSIYALAR
from database_funk.users_funk import add_user, user_exists, add_balance

# KEYBOARD
from keyboards.users_keyboard.users_reply import menu
from keyboards.admin_keyboard.admin_reply import admin_menu


router = Router()

@router.message(CommandStart(deep_link=True))  # faqat bitta handler kifoya
async def start_deeplink_handler(message: Message, command: CommandObject, state: FSMContext):
    user_id = message.from_user.id
    await state.clear()
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
                referal_user = await message.bot.get_chat(user_id)
                if referal_user.username:
                    link = f"https://t.me/{referal_user.username}"
                    text = f"📳 Sizda yangi [taklif]({link}) mavjud!"
                else:
                    text = f"📳 Sizda yangi taklif mavjud!"
                # referal price qo'shish
                await message.bot.send_message(
                    referal_id,
                    text,
                    parse_mode="Markdown", disable_web_page_preview=True)
                await add_balance(referal_id, referal_price)
                await message.bot.send_message(
                    referal_id,
                    f"💰 Sizning hisobingizga {referal_price} so'm qo'shildi!")
            except Exception as e:
                print(f"Referalga xabar yuborilmadi: {e}")

    # Asosiy xabarni yuborish
    await message.answer(START_TEXT, reply_markup=menu)


@router.message(CommandStart() | F.text == "⏪ Orqaga", F.from_user.id == SUPER_ADMIN)
async def start_handler(message: Message):
    user_id = message.from_user.id
    # Foydalanuvchi mavjud emas bo‘lsa qo‘shish
    if not await user_exists(user_id):
        await add_user(user_id)
    if user_id == SUPER_ADMIN:
        await message.answer(START_TEXT, reply_markup=admin_menu)
    else:
        await message.answer(START_TEXT, reply_markup=menu)
@router.message(F.text == "🚫 Bekor qilish")
async def cancel_handler(message: Message, state: FSMContext):
    await message.answer("🏠Asosiy menyudasiz", reply_markup=menu)
    await state.clear()

@router.callback_query(F.data == "back")
async def back_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🏠Asosiy menyudasiz", reply_markup=menu)
    await callback.delete()
    await state.clear()
    await callback.answer()
