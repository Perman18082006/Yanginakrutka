from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext


# Keyboards
from keyboards.users_keyboard.users_inline import payment_keyboard, tolov_qildim
from keyboards.users_keyboard.users_reply import cancel
from keyboards.admin_keyboard.admin_inline import admin_tasdiqla
# Texts
from texts.user_texts import PAY1
# Config
from config import karta, FIO, min_pay, max_pay, SUPER_ADMIN
# States
from .states import Payment
# Database
from database.payment_methods import payment_methods

router = Router()


@router.message(F.text == "💰Hisob toʻldirish")
async def cmd_payment(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("💵To'lov turini tanlang!", reply_markup=payment_keyboard()) 

@router.callback_query(F.data == "cancel")
async def process_payment_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("💵To'lov turini tanlang!", reply_markup=payment_keyboard())


@router.callback_query(F.data.startswith("pay:"))
async def process_payment(callback: CallbackQuery, state: FSMContext):
    payment_method = callback.data.split(":")[1]
    await state.update_data(payment_method=payment_method)
    await callback.message.edit_text(PAY1.format(karta=karta, FIO=FIO, min_pay=min_pay, max_pay=max_pay), reply_markup=tolov_qildim())
    await state.set_state(Payment.pay1)

@router.callback_query(Payment.pay1, F.data == "tolov_qildim")
async def process_payment_done(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("💰To'lov qilingan pul miqdorini kiriting!", reply_markup=cancel)
    await state.set_state(Payment.pay2)

@router.message(Payment.pay2)
async def process_payment_amount(message: Message, state: FSMContext):
    amount = message.text
    if not amount.isdigit():
        await message.answer("💰To'lov qilingan pul miqdorini kiriting!")
        return
    if int(amount) < min_pay or int(amount) > max_pay:
        await message.answer(f"💰To'lov miqdori {min_pay} so'mdan {max_pay} so'mgacha bo'lishi kerak!")
        return
    await state.update_data(amount=amount)
    await message.answer("✅Qabul qilindi. Endi to'lov chekini yuboring!\n\n‼️To'lov chekini faqat rasm ko'rinishida yuboring hamda 1 ta chekni qayta-qayta yubormang!")
    await state.set_state(Payment.pay3)

@router.message(Payment.pay3, F.photo)
async def process_payment_receipt(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    payment_method = payment_methods[data.get("payment_method")]
    amount = data.get("amount")
    receipt = message.photo[-1].file_id
    await message.answer("✅To'lov qabul qilindi. Tez orada hisobingizga pul o'tkaziladi!")
    await state.clear()
    # To'lovni adminlarga yuborish
    await message.bot.send_photo(SUPER_ADMIN, receipt, caption=f"To'lov turi: {payment_method}\nTo'lov miqdori: {amount} so'm\nTo'lovchi: {message.from_user.id}", reply_markup=admin_tasdiqla(user_id, amount))


