import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline.start_keyboard import menu
from loader import dp, db


@dp.message_handler(CommandStart())
async def bot_start(msg: types.Message):
    try:
        user = await db.add_user(
            telegram_id=msg.from_user.id,
            full_name=msg.from_user.full_name,
            username=msg.from_user.username
        )

    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=msg.from_user.id)
    await msg.answer(
        f"Xush kelibsiz {user[1]}! "
        f"\nXizmatlarimizdan foydalanishingiz uchun quyidagi bo'limlardan birini tanlang!",
        reply_markup=menu,
    )
