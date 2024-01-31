from typing import Union
from aiogram.dispatcher import filters
from aiogram import types
from aiogram.types import CallbackQuery, Message

from keyboards.inline.menu_keyboard import menu_callback_data, subcategories_keyboard, categories_keyboard, \
    items_keyboard, item_keyboard

from loader import dp, db


@dp.message_handler(filters.Command('menu'))
@dp.message_handler(filters.Text(equals=("◀ Bosh menyu")))
@dp.callback_query_handler(text="menu")
async def menu(message: Union[CallbackQuery, Message]):
    if isinstance(message, CallbackQuery):
        callback = message
        await list_categories(callback)
    elif isinstance(message, Message):
        await list_categories(message)


async def list_categories(message: Union[CallbackQuery, Message], **kwargs):
    markup = await categories_keyboard()
    if isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_text(text="Categoriyalardan birini tanlang:", reply_markup=markup)
    elif isinstance(message, Message):
        await message.answer(text="Categoriyalardan birini tanlang:", reply_markup=markup)


async def list_subcategories(callback: CallbackQuery, category, **kwargs):
    markup = await subcategories_keyboard(category)
    await callback.message.edit_text(text="SubCategoriyalardan birini tanlang:", reply_markup=markup)


async def list_items(callback: CallbackQuery, category, subcategory, **kwargs):
    markup = await items_keyboard(category, subcategory)
    await callback.message.edit_text(text="Mahsulot tanlang:", reply_markup=markup)


async def show_item(callback: CallbackQuery, category, subcategory, item_id, **kwargs):
    markup = item_keyboard(category, subcategory, item_id, **kwargs)
    item = await db.get_product(item_id)
    if item["photo"]:
        text = f"<a href=\"{item['photo']}\">{item['productname']}</a>\n\n"
    else:
        text = f"{item['productname']}\n\n"
    text += f"Narxi: {item['price']}$\n{item['description']}"
    await callback.message.edit_text(text=text, reply_markup=markup)


@dp.callback_query_handler(menu_callback_data.filter())
async def navigate_all(call: CallbackQuery, callback_data: dict):
    current_level = callback_data.get('level')
    category = callback_data.get('category')
    subcategory = callback_data.get('subcategory')
    item_id = callback_data.get('item_id')

    levels = {
        "0": list_categories,
        "1": list_subcategories,
        "2": list_items,
        "3": show_item,
    }
    current_level_function = levels[current_level]
    await current_level_function(
        call, category=category, subcategory=subcategory, item_id=item_id
    )
