from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

# Keyboards
from keyboards.admin_keyboard.admin_inline import xizmat_tah_qosh, tahrir_ustun
from keyboards.admin_keyboard.admin_reply import boshqaruv
# States
from .admin_states import Xizmat_tahrir, Xizmat_id
# Database funk
from database_funk.orders_funk import edit_service, delete_service
# Filter
from filters import IsAdmin


router = Router()

@router.message(F.text == "🛠️ Xizmatlarni tah/qosh", IsAdmin())
async def xizmat_tahrirla_handler(message: Message, state: FSMContext):
    await message.answer("Quyidagilardan birini tanlang:", reply_markup=xizmat_tah_qosh)
    await state.clear()

@router.callback_query(F.data == "xizmat_tahrirlash")
async def xizmat_tahrirlash_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Xizmat service ID sini kiriting!", reply_markup=boshqaruv)
    await state.set_state(Xizmat_id.xizmat_id)
    await callback.answer()

@router.message(Xizmat_id.xizmat_id)
async def xizmat_id_handler(message: Message, state: FSMContext):
    xizmat_id = message.text
    if not xizmat_id.isdigit():
        await message.answer("Xizmat ID faqat raqamlardan iborat bo'lishi kerak")
        return
    if int(xizmat_id) < 0:
        await message.answer("Xizmat ID manfiy bo'lishi mumkin emas")
        return
    xizmat_id = int(xizmat_id)
    await state.update_data(xizmat_id=xizmat_id)
    await message.answer("Nimani tahrirlamoqchisiz?", reply_markup=tahrir_ustun)

@router.callback_query(F.data.startswith("tahrir_"))
async def tahrir_ustun_handler(callback: CallbackQuery, state: FSMContext):
    tahrir_data = callback.data.split("_")[1]
    if tahrir_data == "serviceid":
        await state.set_state(Xizmat_tahrir.service_id)
        await callback.message.answer("Yangi service ID ni kiriting")
    elif tahrir_data == "kategoriya":
        await state.set_state(Xizmat_tahrir.kategoriya)
        await callback.message.answer("Yangi kategoriya nomini kiriting")
    elif tahrir_data == "bolim":
        await state.set_state(Xizmat_tahrir.bolim)
        await callback.message.answer("Yangi bo'lim nomini kiriting")
    elif tahrir_data == "xizmat":
        await state.set_state(Xizmat_tahrir.xizmat)
        await callback.message.answer("Yangi xizmat nomini kiriting")
    elif tahrir_data == "narx":
        await state.set_state(Xizmat_tahrir.narx)
        await callback.message.answer("Yangi narxni kiriting")
    elif tahrir_data == "tavsif":
        await state.set_state(Xizmat_tahrir.tavsif)
        await callback.message.answer("Yangi tavsifni kiriting")
    elif tahrir_data == "delete":
        data = await state.get_data()
        service_id = data['xizmat_id']
        await delete_service(service_id)
        await callback.message.answer("Xizmat o'chirildi!")
    await callback.answer()

@router.message(Xizmat_tahrir.service_id)
async def tahrir_service_id_handler(message: Message, state: FSMContext):
    yangi_id = message.text
    if not yangi_id.isdigit():
        await message.answer("Service ID faqat raqamlardan iborat bo'lishi kerak")
        return
    data = await state.get_data()
    eski_id = int(data['xizmat_id'])
    await edit_service(eski_id, service_id=int(yangi_id))
    await message.answer("Yangi service ID qabul qilindi!")
    await state.clear()

@router.message(Xizmat_tahrir.kategoriya)
async def tahrir_kategoriya_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    service_id = data['xizmat_id']
    await edit_service(service_id, categoria_nomi=message.text)
    await message.answer("Yangi kategoriya nomi qabul qilindi!")
    await state.clear()

@router.message(Xizmat_tahrir.bolim)
async def tahrir_bolim_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    service_id = data['xizmat_id']
    await edit_service(service_id, bolim_nomi=message.text)
    await message.answer("Yangi bo'lim nomi qabul qilindi!")
    await state.clear()

@router.message(Xizmat_tahrir.xizmat)
async def tahrir_xizmat_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    service_id = data['xizmat_id']
    await edit_service(service_id, xizmat_nomi=message.text)
    await message.answer("Yangi xizmat nomi qabul qilindi!")
    await state.clear()

@router.message(Xizmat_tahrir.narx)
async def tahrir_narx_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    service_id = data['xizmat_id']
    narx = message.text
    if not narx.isdigit():
        await message.answer("Narxi faqat raqamlardan iborat bo'lishi kerak")
        return
    if int(narx) < 0:
        await message.answer("Narxi manfiy bo'lishi mumkin emas")
        return
    await edit_service(service_id, narxi=narx)
    await message.answer("Yangi narx qabul qilindi!")
    await state.clear()

@router.message(Xizmat_tahrir.tavsif)
async def tahrir_tavsif_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    service_id = data['xizmat_id']
    await edit_service(service_id, tavsif=message.text)
    await message.answer("Yangi tavsif qabul qilindi!")
    await state.clear()
