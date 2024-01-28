from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
            self,
            command,
            *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO Users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

    async def add_product(
            self,
            category_code,
            category_name,
            subcategory_code,
            subcategory_name,
            productname,
            photo=None,
            price=None,
            description="",
    ):
        sql = "INSERT INTO Products (category_code, category_name, subcategory_code, subcategory_name, productname, photo, price, description) VALUES($1, $2, $3, $4, $5, $6, $7, $8) returning *"
        return await self.execute(
            sql,
            category_code,
            category_name,
            subcategory_code,
            subcategory_name,
            productname,
            photo,
            price,
            description,
            fetchrow=True,
        )

    async def get_categories(self):
        sql = "SELECT DISTINCT category_name, category_code FROM Products"
        return await self.execute(sql, fetch=True)

    async def get_subcategories(self, category_code):
        sql = f"SELECT DISTINCT subcategory_name, subcategory_code FROM Products WHERE category_code='{category_code}'"
        return await self.execute(sql, fetch=True)

    async def get_product(self, product_id):
        sql = f"SELECT * FROM Products WHERE id='{product_id}'"
        return await self.execute(sql, fetchrow=True)

    async def count_products(self, category_code, subcategory_code=None):
        if subcategory_code:
            sql = f"SELECT COUNT(*) FROM Products WHERE category_code='{category_code}' AND subcategory_code='{subcategory_code}'"
        else:
            sql = f"SELECT COUNT(*) FROM Products WHERE category_code='{category_code}'"
        return await self.execute(sql, fetchval=True)

    async def get_products(self, category_code, subcategory_code):
        sql = f"SELECT * FROM Products WHERE category_code='{category_code}' AND subcategory_code='{subcategory_code}'"
        return await self.execute(sql, fetch=True)

    async def get_product(self, product_id):
        sql = f"SELECT * FROM Products WHERE id={product_id}"
        return await self.execute(sql, fetchrow=True)

    async def drop_products(self):
        await self.execute("DROP TABLE Products", execute=True)

    async def add_to_cart(self, user_id, item_id, quantity):
        sql = "INSERT INTO Cart (user_id, item_id, quantity, is_ordered) VALUES ($1, $2, $3, FALSE) returning *"
        return await self.execute(sql, user_id, item_id, quantity, fetchrow=True)

    async def update_items_count(self, user_id, item_id, quantity):
        sql = """
            UPDATE Cart
            SET quantity = $3
            WHERE user_id = $1 AND item_id = $2
            RETURNING *
        """
        return await self.execute(sql, user_id, item_id, quantity, fetchrow=True)

    async def cart_ordered(self, cart_id):
        sql = """
                UPDATE Cart
                SET is_ordered = TRUE
                WHERE id = $1 and is_ordered = FALSE
                RETURNING *
            """
        return await self.execute(sql, cart_id, fetchrow=True)

    async def delete_order(self, user_id, item_id):
        sql = "DELETE FROM Cart WHERE user_id = $1 and item_id = $2"
        return await self.execute(sql, user_id, item_id, execute=True)

    async def get_user_orders(self, **kwargs):
        sql = "SELECT * FROM Cart WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def get_user_order(self, **kwargs):
        sql = "SELECT * FROM Cart WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def get_product_orders(self, item_id):
        sql = "SELECT * FROM Cart WHERE item_id = $1"
        return await self.execute(sql, item_id, fetch=True)

    async def create_user_order(self, name, phone, user_id, total_price=0):
        sql = 'INSERT INTO "order" (name, phone, user_id, total_price) VALUES($1, $2, $3, $4) returning *'
        return await self.execute(sql, name, phone, user_id, total_price, fetchrow=True)

    async def add_cart_to_order(self, order_id, cart_id):
        sql = "INSERT INTO Order_carts (order_id, cart_id) VALUES($1, $2) returning *"
        return await self.execute(sql, order_id, cart_id, fetchrow=True)

    async def update_order_price(self, price, order_id):
        sql = """
                UPDATE "order"
                SET total_price = $1
                WHERE id = $2
                RETURNING *
               """
        return await self.execute(sql, price, order_id, fetchrow=True)
