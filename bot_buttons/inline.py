from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

accept_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅Qabul qilish", callback_data="accept_yes"),
            InlineKeyboardButton(text="❌Rad etish", callback_data="accept_no")
        ]
    ]
)

preview = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅Ha", callback_data="say_yes"),
            InlineKeyboardButton(text="❌Yo'q", callback_data="say_no")
        ]
    ]
)

