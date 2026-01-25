from aiogram import Router, F
from aiogram.types import Message

from bot_buttons.reply import start_menu_button

error_router = Router()

@error_router.message(F.text)
async def error_cmd(message: Message):
    text = f"""
Iltimos botga to'g'ridan-to'g'ri xabar yubormang
"""
    await message.answer(text, reply_markup=start_menu_button)