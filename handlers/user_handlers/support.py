from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
# Config
from config import SUPER_ADMIN
# States
from .states import Support
# Texts
from texts.admin_texts import ADMINGA_XABAR
# Keyboards
from keyboards.users_keyboard.users_reply import cancel
from keyboards.admin_keyboard.admin_inline import javob_yoz

router = Router()

@router.message(F.text == "☎️ Qo'llab-quvvatlash")
async def cmd_support(message: Message, state: FSMContext):
    await message.answer("Murojaat matnini yuboring", reply_markup=cancel)
    await state.set_state(Support.message)


@router.message(Support.message, F.text.not_in(["🚫 Bekor qilish", "💰Hisob toʻldirish", "👤Mening hisobim", "👥Referral", "🗂 Xizmatlar"]))
async def process_support_message(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_message = message.text
    await message.answer("⏳ Murojaatingiz qabul qilindi! \n\nTez orada murojaatingizni ko'rib chiqamiz.")
    await state.clear()
    await message.bot.send_message(
        SUPER_ADMIN,
        ADMINGA_XABAR.format(user_id=user_id, user_message=user_message), reply_markup=javob_yoz(user_id))