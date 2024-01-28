from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.contact_keyboard import contact_keyboard
from keyboards.default.location_keyboard import location_keyboard
from loader import dp, db
from states.get_order import Order_state


# @dp.callback_query_handler(text='make_order')
# async def make_user_orders(call: types.CallbackQuery):
#     user_telegram_id = call.from_user.id
#     user = await db.select_user(telegram_id=user_telegram_id)
#     user_id = user['id']
#     user_carts = await db.get_user_orders(user_id=user_id, is_ordered=False)
#     print('user_carts', user_carts)
#     order = await db.create_user_order()
#     for cart in user_carts:
#         pass


@dp.callback_query_handler(text='make_order', state=None)
async def enter_test(call: types.CallbackQuery):
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
    await message.answer("Sizning ma'lumotlaringiz adminlarga yuborildi, tez orada sizga aloqaga chiqishadi")
    await state.finish()
