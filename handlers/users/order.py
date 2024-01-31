import asyncio
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
import logging
from data.config import ADMINS
from keyboards.default.contact_keyboard import contact_keyboard
from keyboards.default.location_keyboard import location_keyboard
from keyboards.default.menu_keyboard import back_menu
from keyboards.inline.confirm_order import confirmation_callback_data, confirmation_keyboard
from loader import dp, db, bot
from states.get_order import Order_state
from aiogram.dispatcher import filters


@dp.callback_query_handler(text='make_order', state=None)
async def enter_test(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await call.message.answer("To'liq ismingizni kiriting")
    await Order_state.full_name.set()


@dp.message_handler(state=Order_state.full_name)
async def answer_fullname(message: types.Message, state: FSMContext):
    full_name = message.text

    await state.update_data(
        {"full_name": full_name}
    )

    await message.answer(text="Telefon raqamingizni kiriting", reply_markup=contact_keyboard)
    await Order_state.next()


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=Order_state.phone_number)
async def answer_phone_number(message: types.Message, state: FSMContext):
    contact = message.contact
    await state.update_data(
        {
            'contact': contact
        }
    )
    await message.answer(text="Manzilingizni yuboring", reply_markup=location_keyboard)
    await Order_state.next()


@dp.message_handler(content_types=types.ContentTypes.LOCATION, state=Order_state.location)
async def answer_location(message: types.Message, state: FSMContext):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    await state.update_data(
        {
            'location':
                {
                    "latitude": latitude,
                    "longitude": longitude,
                }
        }
    )
    user_telegram_id = message.from_user.id
    user = await db.select_user(telegram_id=user_telegram_id)
    user_id = user['id']
    user_carts = await db.get_user_orders(user_id=user_id, is_ordered=False)
    data = await state.get_data()
    name = data.get("full_name")
    contact = data.get('contact')
    phone_number = contact['phone_number']
    location = data.get('location')
    lat = location.get('latitude')
    long = location.get('longitude')
    order = await db.create_user_order(name=name, phone=phone_number, user_id=user_id)
    total_price = 0
    for cart in user_carts:
        quantity = cart['quantity']
        item_id = cart['item_id']
        item = await db.get_product(product_id=item_id)
        price_item = item['price'] * quantity
        total_price += price_item
        cart_id = cart['id']
        order_cart = await db.add_cart_to_order(order_id=order['id'], cart_id=cart_id)
        await db.cart_ordered(cart_id)
    order = await db.update_order_price(total_price, order['id'])
    await message.answer("Sizning ma'lumotlaringiz adminlarga yuborildi,\n"
                         "tez orada sizga aloqaga chiqishadi", reply_markup=back_menu)
    await state.finish()
    text = f"Mijoz ismi: {order['name']}\n"
    text += f"Tel: {order['phone']}\n"
    text += f"Umumiy narx: {order['total_price']}$\n"
    text += "Ushbu yuyurtmani tasdiqlaysizmi (confirm/cancel)?"
    markup = await confirmation_keyboard(user_id=user_id, order_id=order['id'])
    for admin in ADMINS:
        try:
            await dp.bot.send_message(chat_id=admin, text=text, reply_markup=markup)
        except Exception as err:
            logging.exception(err)


@dp.callback_query_handler(confirmation_callback_data.filter())
async def admin_confirm_order(call: types.CallbackQuery, callback_data: dict):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    cancel_or_confirm = callback_data.get('confirm_or_cancel')
    user_id = int(callback_data.get("user_id"))
    user = await db.select_user(id=user_id)
    chat_id = user['telegram_id']
    if cancel_or_confirm == "confirm":
        try:
            await dp.bot.send_message(
                chat_id=chat_id,
                text="✅ Buyurtmangiz tasdiqlandi, tez orada yetkaziladi,\n"
                     "Xizmatlarimizdan foydalanganingiz uchun tashakkur!",
            )
        except Exception as err:
            logging.exception(err)
    else:
        try:
            await dp.bot.send_message(
                chat_id=chat_id,
                text="❌ Buyurtmangiz tasdiqdan o'tmadi\n"
                     "Qaytadan urunib ko'ring",
            )

        except Exception as err:
            logging.exception(err)


@dp.message_handler(filters.Command('my_orders'))
@dp.callback_query_handler(text='my_orders')
async def open_my_orders(message: Union[types.CallbackQuery, types.Message]):
    if isinstance(message, types.CallbackQuery):
        call = message
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        user_telegram_id = call.from_user.id
        user = await db.select_user(telegram_id=user_telegram_id)
        user_id = user['id']
        orders = await db.get_order(user_id=user_id)
        print("orders", orders)
        text = "📋 Sizning buyurtmalaringiz:\n"
        count_items = 0
        for order in orders:
            count_items += 1
            order_carts = await db.get_order_carts(order_id=order['id'])
            text += f"{count_items}. Umumiy summasi {order['total_price']}$\n"
            for order_cart in order_carts:
                cart = await db.get_user_order(id=order_cart['cart_id'])
                cart = cart[0]
                product_id = cart['item_id']
                product = await db.get_product(product_id=product_id)
                text += f"  {cart['quantity']} ta {product['productname']} -> {cart['quantity'] * product['price']}$\n"
        if orders:
            await call.message.answer(text=text, reply_markup=back_menu)
        else:
            await call.message.answer(
                text="Sizda hali buyurtma mavjud emas", reply_markup=back_menu
            )
    elif isinstance(message, types.Message):
        user_telegram_id = message.from_user.id
        user = await db.select_user(telegram_id=user_telegram_id)
        user_id = user['id']
        orders = await db.get_order(user_id=user_id)
        text = "📋 Sizning buyurtmalaringiz:\n"
        count_items = 0
        for order in orders:
            count_items += 1
            order_carts = await db.get_order_carts(order_id=order['id'])
            text += f"{count_items}. Umumiy summasi {order['total_price']}$\n"
            for order_cart in order_carts:
                cart = await db.get_user_order(id=order_cart['cart_id'])
                cart = cart[0]
                product_id = cart['item_id']
                product = await db.get_product(product_id=product_id)
                text += f"  {cart['quantity']} ta {product['productname']} -> {cart['quantity'] * product['price']}$\n"
        if orders:
            await message.answer(text=text, reply_markup=back_menu)
        else:
            await message.answer(
                text="Sizda hali buyurtma mavjud emas", reply_markup=back_menu
            )
