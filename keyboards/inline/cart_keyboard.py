from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from keyboards.inline.menu_keyboard import make_callback_data
from loader import db

edit_cart = CallbackData('edit_cart', 'item_id', 'count_item', 'function')


async def cart_keyboard(user_id):
    markap = InlineKeyboardMarkup()

    cart_items = await db.get_user_orders(user_id=user_id, is_ordered=False)
    for order in cart_items:
        quantity = order['quantity']
        item = await db.get_product(order['item_id'])
        item_id = item['id']
        item_name = item['productname']

        markap.insert(
            InlineKeyboardButton(
                text=f"{item_name}", callback_data="ni"
            )
        )
        markap.row(
            InlineKeyboardButton(
                text="➖", callback_data=edit_cart.new(item_id=item_id, count_item=quantity, function='minus')
            )
        )
        markap.insert(
            InlineKeyboardButton(
                text=f"{quantity}", callback_data='nimadirgadir'
            )
        )
        markap.insert(
            InlineKeyboardButton(
                text="➕", callback_data=edit_cart.new(item_id=item_id, count_item=quantity, function='plus')
            )
        )
    markap.row(
        InlineKeyboardButton(
            text="⬅️Ortga",
            callback_data='menu',
        ),
    )
    markap.insert(
        InlineKeyboardButton(
            text="🚚 Buyurtma berish", callback_data='make_order'
        )
    )
    return markap
