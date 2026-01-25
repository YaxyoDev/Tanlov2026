from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

accept_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅Qabul qilish", callback_data="accept_yes"),
            InlineKeyboardButton(text="❌Rad etish", callback_data="accept_no")
        ]
    ]
)

