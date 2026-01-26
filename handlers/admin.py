from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from database.db import check_admin

admin_router = Router()

@admin_router.callback_query(F.data.in_(["accept_yes", "accpet_no"]))
async def accept_ariza(callback: CallbackQuery):
    new_text = callback.message.caption + "\n✅<i>Qabul qilingan</i>" 
    await callback.message.edit_caption(caption=new_text)
    

@admin_router.callback_query(F.data == "accpet_no")
async def accept_ariza(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer("Rad etildi", show_alert=True)
