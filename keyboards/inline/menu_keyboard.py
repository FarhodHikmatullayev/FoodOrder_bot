from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db

menu_callback_data = CallbackData("show_menu", "level", "category", "subcategory", "item_id")
buy_item = CallbackData("buy", "item_id")
add_cart = CallbackData('add_cart', 'item_id', 'count_item', 'function')


# count_items = CallbackData('item', 'count', 'plus_or_minus')


# Bizning menu 3 qavat (LEVEL) dan iborat
# 0 - Kategoriyalar
# 1 - Ost-kategoriyalar
# 2 - Mahsulotlar
# 3 - Yagona mahsulot


def make_callback_data(level, category="0", subcategory="0", item_id="0"):
    return menu_callback_data.new(
        level=level,
        category=category,
        subcategory=subcategory,
        item_id=item_id
    )


async def categories_keyboard():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=1)
    categories = await db.get_categories()
    for category in categories:
        count_of_item = await db.count_products(category_code=category['category_code'])

        text_button = f"{category['category_name']} ({count_of_item} dona)"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category['category_code'])

        markup.insert(
            InlineKeyboardButton(
                text=text_button,
                callback_data=callback_data
            )
        )
    return markup


async def subcategories_keyboard(category):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=1)

    subcategories = await db.get_subcategories(category)
    for subcategory in subcategories:
        number_of_items = await db.count_products(
            category_code=category, subcategory_code=subcategory["subcategory_code"]
        )

        text_button = f"{subcategory['subcategory_name']} ({number_of_items} dona)"

        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            category=category,
            subcategory=subcategory["subcategory_code"],
        )
        markup.insert(
            InlineKeyboardButton(
                text=text_button,
                callback_data=callback_data
            )
        )

    markup.row(
        InlineKeyboardButton(
            text="⬅️Ortga",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1)
        )
    )
    return markup


async def items_keyboard(category, subcategory):
    CURRENT_LEVEL = 2

    markup = InlineKeyboardMarkup(row_width=1)

    items = await db.get_products(category, subcategory)
    for item in items:
        button_text = f"{item['productname']} - ${item['price']}"

        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            category=category,
            subcategory=subcategory,
            item_id=item["id"],
        )
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    markup.row(
        InlineKeyboardButton(
            text="⬅️Ortga",
            callback_data=make_callback_data(
                level=CURRENT_LEVEL - 1, category=category
            ),
        )
    )
    return markup


def item_keyboard(category, subcategory, item_id, count_item=1):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➖",
                                     callback_data=add_cart.new(item_id=item_id, count_item=count_item,
                                                                function='minus')),
                InlineKeyboardButton(text=f"{count_item}", switch_inline_query_current_chat=""),
                InlineKeyboardButton(text="➕",
                                     callback_data=add_cart.new(item_id=item_id, count_item=count_item,
                                                                function='plus'))
            ],
            [
                InlineKeyboardButton(text=f"🛒 Savatga Qo'shish",
                                     callback_data=add_cart.new(item_id=item_id, count_item=count_item,
                                                                function='add')),
            ],
            [
                InlineKeyboardButton(
                    text="⬅️Ortga",
                    callback_data=make_callback_data(
                        level=CURRENT_LEVEL - 1, category=category, subcategory=subcategory
                    ),
                ),
                InlineKeyboardButton(
                    text="🛒 Savatcha",
                    callback_data="open_cart"
                )
            ]
        ]
    )

    return markup
