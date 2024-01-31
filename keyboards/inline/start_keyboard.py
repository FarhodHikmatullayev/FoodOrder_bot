from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db

menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📖 Bosh menyu", callback_data='menu'),
        ],
        [
            InlineKeyboardButton(text="🗒 Mening buyurtmalarim", callback_data='my_orders'),
        ],
        [
            InlineKeyboardButton(text="🛒 Savatcha", callback_data='open_cart'),
            InlineKeyboardButton(text="🤝 Support", callback_data='support')
        ],

    ],
)
