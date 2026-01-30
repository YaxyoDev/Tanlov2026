from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from database.db import check_admin

admin_router = Router()

@admin_router.callback_query(F.data == "accept_yes")
async def accept_ariza_yes(callback: CallbackQuery):
    new_text = callback.message.caption + "\n✅<i>Qabul qilingan</i>" 
    await callback.message.edit_caption(caption=new_text)
    

@admin_router.callback_query(F.data == "accept_no")
async def accept_ariza_no(callback: CallbackQuery):
    next_text = callback.message.caption + "\n<i>❌Bekor qilingan</i>"
    await callback.message.edit_caption(caption=next_text)
