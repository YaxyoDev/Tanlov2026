from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot_buttons.reply import start_menu_button

start_router = Router()

@start_router.message(Command('start'))
async def start_cmd(message: Message):
    text = f"""
Assalom aleykum, botga xush kelibsiz! 
Siz ushbu bot orqali “Yoshlar giyohvandlikka qarshi” nomli videoroliklar tanlovida ishtirok etishingiz mumkin.
"""
    await message.answer(text, reply_markup=start_menu_button)

