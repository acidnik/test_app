from app.db import users, books, shops, orders
from sqlalchemy.sql import select, and_

class Order:
    @classmethod
    def order_to_dict(cls, order):
        return {
            'book': {
                'id': order['books_id'],
                'author': order['books_author'],
                'title': order['books_title'],
            },
            'shop': {
                'id': order['shops_id'],
                'name': order['shops_name'],
            },
            'id': order['orders_id'],
            'amount': order['orders_amount'],
        }

    @classmethod
    async def get_user_orders(cls, user, conn):
        cursor = await conn.execute(
            select([users, orders, books, shops], use_labels=True)
            .select_from(users.join(orders).join(shops).join(books))
            .where(users.c.id == user.id)
        )
        rows = await cursor.fetchall()
        return rows

    @classmethod
    async def place_orders(cls, user_id, book_id, shop_id, amount, conn):
        cur = await conn.execute(orders.insert(returning=[orders.c.id]), [
            {'user_id': user_id, 'book_id': book_id, 'shop_id': shop_id, 'amount': amount}
        ])
        res = await curr.fetchone()
        return res['id']
