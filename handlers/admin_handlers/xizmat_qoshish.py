from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
# Database funk
from database_funk.orders_funk import add_service
# States
from .admin_states import Xizmat_qosh
# Keyboards
from keyboards.admin_keyboard.admin_inline import xizmat_qoshish_tasdiqla
from keyboards.admin_keyboard.admin_reply import boshqaruv
router = Router()

@router.callback_query(F.data == "xizmat_qoshish")
async def xizmat_qoshish_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except Exception:
        pass
    await callback.message.answer("Service ID kiriting", reply_markup=boshqaruv)
    await state.set_state(Xizmat_qosh.service_id)
    try:
        await callback.answer()
    except Exception:
        pass

@router.message(Xizmat_qosh.service_id)
async def xizmat_qoshish_service_id(message: Message, state: FSMContext):
    service_id = message.text
    if not service_id.isdigit():
        await message.answer("Service ID faqat raqamlardan iborat bo'lishi kerak")
        return
    if int(service_id) < 0:
        await message.answer("Service ID manfiy bo'lishi mumkin emas")
        return
    service_id = int(service_id)
    await state.update_data(service_id=service_id)
    await message.answer("Kategoriya nomini kiriting")
    await state.set_state(Xizmat_qosh.categoria_nomi)

@router.message(Xizmat_qosh.categoria_nomi)
async def xizmat_qoshish_category(message: Message, state: FSMContext):
    categoria_nomi = message.text
    await state.update_data(categoria_nomi=categoria_nomi)
    await message.answer("Bo'lim nomini kiriting")
    await state.set_state(Xizmat_qosh.bolim_nomi)

@router.message(Xizmat_qosh.bolim_nomi)
async def xizmat_qoshish_bolim(message: Message, state: FSMContext):
    bolim_nomi = message.text
    await state.update_data(bolim_nomi=bolim_nomi)
    await message.answer("Xizmat nomini kiriting")
    await state.set_state(Xizmat_qosh.xizmat_nomi)

@router.message(Xizmat_qosh.xizmat_nomi)
async def xizmat_qoshish_xizmat(message: Message, state: FSMContext):
    xizmat_nomi = message.text
    await state.update_data(xizmat_nomi=xizmat_nomi)
    await message.answer("Narxini kiriting")
    await state.set_state(Xizmat_qosh.narxi)

@router.message(Xizmat_qosh.narxi)
async def xizmat_qoshish_narxi(message: Message, state: FSMContext):
    narxi = message.text
    if not narxi.isdigit():
        await message.answer("Narxi faqat raqamlardan iborat bo'lishi kerak")
        return
    if int(narxi) < 0:
        await message.answer("Narxi manfiy bo'lishi mumkin emas")
        return
    narxi = int(narxi)
    await state.update_data(narxi=narxi)
    await message.answer("Tavsifini kiriting")
    await state.set_state(Xizmat_qosh.tavsif)

@router.message(Xizmat_qosh.tavsif)
async def xizmat_qoshish_tavsif(message: Message, state: FSMContext):
    tavsif = message.text
    await state.update_data(tavsif=tavsif)
    data = await state.get_data()
    await message.answer(
        f"Xizmat qo'shishni tasdiqlaysizmi?\n\n"
        f"Service ID: {data['service_id']}\n"
        f"Kategoriya: {data['categoria_nomi']}\n"
        f"Bo'lim: {data['bolim_nomi']}\n"
        f"Xizmat: {data['xizmat_nomi']}\n"
        f"Narxi: {data['narxi']}\n"
        f"Tavsif: {data['tavsif']}\n", reply_markup=xizmat_qoshish_tasdiqla
    )

@router.callback_query(F.data == "xizmat_qoshish_tasdiqla")
async def xizmat_qoshish_tasdiqla_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await add_service(
        data['service_id'], data['categoria_nomi'], data['bolim_nomi'], data['xizmat_nomi'], data['narxi'], data['tavsif']
    )
    await callback.message.answer("Xizmat muvaffaqiyatli qo'shildi!")
    await state.clear()
    try:
        await callback.answer()
    except Exception:
        pass