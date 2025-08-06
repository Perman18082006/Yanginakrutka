from aiogram import Router, F
from aiogram.types import Message
# CONFIG
from config import referal_price
# TEXTLAR
from texts.user_texts import REFERAL_TEXT, REFERAL_TEXT2

router = Router()

@router.message(F.text == "👥Referral")
async def cmd_referral(message: Message):
    user_id = message.from_user.id
    bot_info = await message.bot.get_me()
    first_msg = await message.answer(REFERAL_TEXT.format(bot_username=bot_info.username, user_id=user_id))
    await message.answer(REFERAL_TEXT2.format(referal_price=referal_price), reply_to_message_id=first_msg.message_id)
