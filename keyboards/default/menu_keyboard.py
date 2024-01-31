from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

back_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="◀ Bosh menyu", ),
        ],
    ]
)
