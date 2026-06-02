from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_menu_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Tanlovda ishtirok etish")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

phone_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Telefon raqam yuborish", request_contact=True)
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

