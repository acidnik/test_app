from app.db import users, books, shops, orders
from sqlalchemy.sql import select, and_, text
from sqlalchemy.dialects.postgresql import insert

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
    async def place_orders(cls, user_id, orders_list, conn):
        res = []
        for o in orders_list:
            # aiopg does not support multiple inserts https://github.com/aio-libs/aiopg/issues/112
            cur = await conn.execute(
                # sqlalchemy sucks, raw sql rules, and here's why:
                text("""
                    with new_orders as (
                        insert into orders (user_id, book_id, shop_id, amount) 
                        values (:user_id, :book_id, :shop_id, :amount)
                        on conflict (user_id, book_id, shop_id) do update
                            set amount = orders.amount + excluded.amount
                        returning id, amount, book_id, shop_id
                    )
                    select b.id as books_id, b.author as books_author, b.title as books_title,
                    s.id as shops_id, s.name as shops_name,
                    o.id as orders_id,
                    o.amount as orders_amount
                    from new_orders o
                    join books b on b.id = o.book_id
                    join shops s on s.id = o.shop_id
                """),
                { 'user_id': user_id, 'book_id': o['book_id'], 'shop_id': o['shop_id'], 'amount': o['amount'] } 
            )
            res.append(await cur.fetchone())
        return res
