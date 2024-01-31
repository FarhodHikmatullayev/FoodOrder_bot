from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

confirmation_callback_data = CallbackData('confirm', "confirm_or_cancel", "user_id", "order_id")


async def confirmation_keyboard(user_id, order_id):
    markup = InlineKeyboardMarkup()
    markup.insert(
        InlineKeyboardButton(
            text="Confirm", callback_data=confirmation_callback_data.new(
                confirm_or_cancel="confirm",
                user_id=f"{user_id}",
                order_id=f"{order_id}"
            ),
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text="Cancel", callback_data=confirmation_callback_data.new(
                confirm_or_cancel="cancel",
                user_id=f"{user_id}",
                order_id=f"{order_id}"
            ),
        )
    )
    return markup
