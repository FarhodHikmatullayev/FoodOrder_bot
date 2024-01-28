from aiogram import types
from aiogram.types import CallbackQuery, Message

from handlers.users.menu_handlers import show_item
from keyboards.inline.cart_keyboard import edit_cart, cart_keyboard
from keyboards.inline.menu_keyboard import menu_callback_data, subcategories_keyboard, categories_keyboard, \
    items_keyboard, item_keyboard, buy_item, add_cart

from loader import dp, db


@dp.callback_query_handler(add_cart.filter())
async def exact_item_and_count(call: CallbackQuery, callback_data: dict):
    user_telegram_id = call.from_user.id
    user = await db.select_user(telegram_id=user_telegram_id)
    function = callback_data.get('function')
    count_item = int(callback_data.get('count_item'))
    item_id = int(callback_data.get('item_id'))
    item = await db.get_product(product_id=item_id)
    category_code = item['category_code']
    subcategory_code = item['subcategory_code']
    if function == 'plus':
        await show_item(call, category_code, subcategory_code, item_id, count_item=count_item + 1)
    elif function == 'minus':
        if count_item > 1:
            await show_item(call, category_code, subcategory_code, item_id, count_item=count_item - 1)

    elif function == "add":
        items = await db.get_user_orders(user_id=user['id'], item_id=item_id, is_ordered=False)
        if not items:
            cart_item = await db.add_to_cart(int(user['id']), int(item_id), count_item)


# @dp.callback_query_handler(edit_cart.filter())
# async def cart(call: CallbackQuery, callback_data: dict):
#     user = await db.select_user(telegram_id=call.from_user.id)
#     user_id = user['id']
#     markup = cart_keyboard(user_id)
#     print(markup)
#     await call.message.edit_reply_markup(reply_markup=markup)

@dp.callback_query_handler(text='open_cart')
async def open_cart(call: CallbackQuery):
    user = await db.select_user(telegram_id=call.from_user.id)
    user_id = user['id']
    items = await db.get_user_orders(user_id=user_id, is_ordered=False)
    if items:
        markup = await cart_keyboard(user_id)
        await call.message.edit_text(text="Sizning savatingizdagi mahsulotlar:", reply_markup=markup)
    else:
        markup = await categories_keyboard()
        await call.message.edit_text(
            text="Sizning savatchangizda mahsulot mavjud emas, "
                 "\n Savatga mahsulot qo'shish uchun quyidagi mahsulotlardan tanlang: ",
            reply_markup=markup)


@dp.callback_query_handler(edit_cart.filter())
async def edit_items_count(call: CallbackQuery, callback_data: dict):
    user = await db.select_user(telegram_id=call.from_user.id)
    user_id = user['id']
    item_id = int(callback_data.get('item_id'))
    count_item = int(callback_data.get('count_item'))
    function = callback_data.get('function')
    if function == 'plus':
        new_item = await db.update_items_count(user_id, item_id, count_item + 1)
    elif function == 'minus' and count_item > 1:
        new_item = await db.update_items_count(user_id, item_id, count_item - 1)
    elif count_item == 1:
        await db.delete_order(user_id=user['id'], item_id=item_id)
    items = await db.get_user_orders(user_id=user_id, is_ordered=False)
    if items:
        markup = await cart_keyboard(user_id)
        await call.message.edit_reply_markup(reply_markup=markup)
    else:
        markup = await categories_keyboard()
        await call.message.edit_text(
            text="Sizning savatchangizda mahsulot mavjud emas, "
                 "\n Savatga mahsulot qo'shish uchun quyidagi mahsulotlardan tanlang: ",
            reply_markup=markup)
